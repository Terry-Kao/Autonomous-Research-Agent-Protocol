"""Windows directory handles that prevent rename and reparse mutation."""
from __future__ import annotations

import ctypes
from contextlib import contextmanager
from ctypes import wintypes
from pathlib import Path
from typing import Iterator


@contextmanager
def locked_directory(path: Path) -> Iterator[int]:
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    create = kernel.CreateFileW
    create.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, ctypes.c_void_p,
                       wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE]
    create.restype = wintypes.HANDLE
    close = kernel.CloseHandle
    close.argtypes = [wintypes.HANDLE]
    close.restype = wintypes.BOOL
    info = kernel.GetFileInformationByHandleEx
    info.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD]
    info.restype = wintypes.BOOL

    class AttributeTag(ctypes.Structure):
        _fields_ = [("attributes", wintypes.DWORD), ("tag", wintypes.DWORD)]

    # Withhold delete sharing so the directory cannot be renamed or replaced.
    # Write sharing is required for child-file replacement on Windows.
    handle = create(str(path), 0x80000000, 3, None, 3, 0x02000000 | 0x00200000, None)
    if handle == ctypes.c_void_p(-1).value:
        raise ctypes.WinError(ctypes.get_last_error())
    try:
        attributes = AttributeTag()
        if not info(handle, 9, ctypes.byref(attributes), ctypes.sizeof(attributes)):
            raise ctypes.WinError(ctypes.get_last_error())
        if attributes.attributes & 0x400 or not attributes.attributes & 0x10:
            raise ValueError(f"contained output directory must not be a reparse point: {path}")
        yield handle
    finally:
        close(handle)


def replace_in_directory(source: Path, name: str, directory_handle: int) -> None:
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    create = kernel.CreateFileW
    create.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, ctypes.c_void_p,
                       wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE]
    create.restype = wintypes.HANDLE
    close = kernel.CloseHandle
    close.argtypes = [wintypes.HANDLE]
    native = ctypes.WinDLL("ntdll")
    rename = native.NtSetInformationFile
    rename.argtypes = [wintypes.HANDLE, ctypes.c_void_p, ctypes.c_void_p, wintypes.DWORD, ctypes.c_int]
    rename.restype = wintypes.LONG
    status_to_error = native.RtlNtStatusToDosError
    status_to_error.argtypes = [wintypes.LONG]
    status_to_error.restype = wintypes.DWORD

    class RenameInfo(ctypes.Structure):
        _fields_ = [("replace", wintypes.BOOL), ("root", wintypes.HANDLE),
                    ("length", wintypes.DWORD), ("name", wintypes.WCHAR * (len(name) + 1))]

    handle = create(str(source), 0x00010000, 7, None, 3, 0x00200000, None)
    if handle == ctypes.c_void_p(-1).value:
        raise ctypes.WinError(ctypes.get_last_error())
    try:
        data = RenameInfo()
        data.replace = True
        data.root = directory_handle
        data.length = len(name.encode("utf-16-le"))
        data.name = name
        status_block = (ctypes.c_void_p * 2)()
        status = rename(handle, ctypes.byref(status_block), ctypes.byref(data), ctypes.sizeof(data), 10)
        if status < 0:
            raise ctypes.WinError(status_to_error(status))
    finally:
        close(handle)
