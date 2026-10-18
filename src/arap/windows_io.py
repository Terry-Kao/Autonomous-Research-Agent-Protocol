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


def relative_handle(parent: int, name: str, *, directory: bool) -> int:
    """Open exactly one child relative to a held handle, refusing reparses."""
    native = ctypes.WinDLL("ntdll")

    class UnicodeString(ctypes.Structure):
        _fields_ = [("length", wintypes.USHORT), ("maximum", wintypes.USHORT), ("buffer", ctypes.c_void_p)]

    class ObjectAttributes(ctypes.Structure):
        _fields_ = [("length", wintypes.ULONG), ("root", wintypes.HANDLE),
                    ("name", ctypes.POINTER(UnicodeString)), ("attributes", wintypes.ULONG),
                    ("security", ctypes.c_void_p), ("quality", ctypes.c_void_p)]

    text = ctypes.create_unicode_buffer(name)
    encoded = name.encode("utf-16-le")
    string = UnicodeString(len(encoded), len(encoded) + 2, ctypes.cast(text, ctypes.c_void_p))
    attributes = ObjectAttributes(ctypes.sizeof(ObjectAttributes), parent, ctypes.pointer(string), 0x1040, None, None)
    create = native.NtCreateFile
    create.argtypes = [ctypes.c_void_p, wintypes.ULONG, ctypes.c_void_p, ctypes.c_void_p,
                       ctypes.c_void_p, wintypes.ULONG, wintypes.ULONG, wintypes.ULONG,
                       wintypes.ULONG, ctypes.c_void_p, wintypes.ULONG]
    create.restype = wintypes.LONG
    handle = wintypes.HANDLE()
    status_block = (ctypes.c_void_p * 2)()
    status = create(ctypes.byref(handle), 0x80100000 if directory else 0x40110000,
                    ctypes.byref(attributes), ctypes.byref(status_block), None,
                    0x10 if directory else 0x80, 3 if directory else 0,
                    3 if directory else 2, 0x200020 | (1 if directory else 0x40), None, 0)
    if status < 0:
        convert = native.RtlNtStatusToDosError
        convert.argtypes = [wintypes.LONG]
        convert.restype = wintypes.DWORD
        raise ctypes.WinError(convert(status))
    return handle.value


@contextmanager
def locked_child(parent: int, name: str) -> Iterator[int]:
    handle = relative_handle(parent, name, directory=True)
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    close = kernel.CloseHandle
    close.argtypes = [wintypes.HANDLE]
    try:
        yield handle
    finally:
        close(handle)


def replace_in_directory(handle: int, name: str, directory_handle: int) -> None:
    native = ctypes.WinDLL("ntdll")
    rename = native.NtSetInformationFile
    rename.argtypes = [wintypes.HANDLE, ctypes.c_void_p, ctypes.c_void_p, wintypes.DWORD, ctypes.c_int]
    rename.restype = wintypes.LONG
    status_to_error = native.RtlNtStatusToDosError
    status_to_error.argtypes = [wintypes.LONG]
    status_to_error.restype = wintypes.DWORD

    class RenameInfo(ctypes.Structure):
        _fields_ = [("replace", wintypes.BOOL), ("root", wintypes.HANDLE),
                    ("length", wintypes.DWORD), ("name", wintypes.WCHAR * (len(name.encode("utf-16-le")) // 2 + 1))]

    data = RenameInfo()
    data.replace = True
    data.root = directory_handle
    data.length = len(name.encode("utf-16-le"))
    data.name = name
    status_block = (ctypes.c_void_p * 2)()
    status = rename(handle, ctypes.byref(status_block), ctypes.byref(data), ctypes.sizeof(data), 10)
    if status < 0:
        raise ctypes.WinError(status_to_error(status))


def atomic_write(parent: int, name: str, rendered: str) -> None:
    import uuid
    temporary_name = f".{name}.{uuid.uuid4().hex}.tmp"
    handle = relative_handle(parent, temporary_name, directory=False)
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    close = kernel.CloseHandle
    close.argtypes = [wintypes.HANDLE]
    write = kernel.WriteFile
    write.argtypes = [wintypes.HANDLE, ctypes.c_void_p, wintypes.DWORD, ctypes.c_void_p, ctypes.c_void_p]
    write.restype = wintypes.BOOL
    flush = kernel.FlushFileBuffers
    flush.argtypes = [wintypes.HANDLE]
    flush.restype = wintypes.BOOL
    dispose = kernel.SetFileInformationByHandle
    dispose.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD]
    dispose.restype = wintypes.BOOL
    replaced = False
    try:
        payload = rendered.encode("utf-8")
        offset = 0
        while offset < len(payload):
            buffer = ctypes.create_string_buffer(payload[offset:])
            count = wintypes.DWORD()
            if not write(handle, buffer, len(payload) - offset, ctypes.byref(count), None):
                raise ctypes.WinError(ctypes.get_last_error())
            if not count.value:
                raise OSError("Windows write made no progress")
            offset += count.value
        if not flush(handle):
            raise ctypes.WinError(ctypes.get_last_error())
        replace_in_directory(handle, name, parent)
        replaced = True
    finally:
        if not replaced:
            delete = wintypes.BOOL(True)
            dispose(handle, 4, ctypes.byref(delete), ctypes.sizeof(delete))
        close(handle)
