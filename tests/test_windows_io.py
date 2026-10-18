import os
import subprocess
import ctypes
import struct
from pathlib import Path

import pytest

import arap.cli as cli
import arap.core as core

pytestmark = pytest.mark.skipif(os.name != "nt", reason="Windows native handle tests")


def junction(link: Path, target: Path) -> None:
    subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(target)], check=True, capture_output=True)


def test_windows_root_cannot_be_renamed_while_indexing(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root = tmp_path / "demo"
    cli.init_project(root)
    artifact = root / "evidence/result.json"
    artifact.write_text("{}\n", encoding="utf-8")
    original_hash = core.sha256_file
    attempted = []

    def attempt_swap(path: Path) -> str:
        with pytest.raises(PermissionError):
            root.rename(tmp_path / "renamed")
        attempted.append(True)
        return original_hash(path)

    monkeypatch.setattr(core, "sha256_file", attempt_swap)
    assert core.index_artifacts(root, [Path("evidence/result.json")])["artifacts"]
    assert attempted


@pytest.mark.parametrize("output", ["control/GATE_DECISION.json", "a/b/result.json"])
def test_windows_gate_rejects_exchanged_junction(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, output: str
) -> None:
    root = tmp_path / "demo"
    cli.init_project(root)
    relative = Path(output)
    ancestor = relative.parts[0]
    (root / relative.parent).mkdir(parents=True, exist_ok=True)
    outside = tmp_path / "outside"
    target = outside.joinpath(*relative.parts[1:])
    target.parent.mkdir(parents=True)
    target.write_text("sentinel", encoding="utf-8")
    original_write = core.write_json

    def exchange(path: Path, value: object, **kwargs: object) -> None:
        (root / ancestor).rename(root / f"{ancestor}-original")
        junction(root / ancestor, outside)
        original_write(path, value, **kwargs)

    monkeypatch.setattr(cli, "write_json", exchange)
    assert cli.main(["gate", str(root), "--reviewer", "test", "--output", output]) == 2
    assert target.read_text(encoding="utf-8") == "sentinel"


def test_windows_held_parent_blocks_rename(tmp_path: Path) -> None:
    from arap.windows_io import locked_directory
    parent = tmp_path / "parent"
    parent.mkdir()
    with locked_directory(parent):
        with pytest.raises(PermissionError):
            parent.rename(tmp_path / "other")
    parent.rename(tmp_path / "other")


@pytest.mark.parametrize("empty", [False, True])
def test_windows_in_place_reparse_does_not_redirect_write(tmp_path: Path, empty: bool) -> None:
    from arap.windows_io import atomic_write, locked_directory
    from ctypes import wintypes
    parent = tmp_path / "parent"
    parent.mkdir()
    if not empty:
        (parent / "sentinel").write_text("original", encoding="utf-8")
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "result.json").write_text("sentinel", encoding="utf-8")
    substitute = ("\\??\\" + str(outside)).encode("utf-16-le")
    printable = str(outside).encode("utf-16-le")
    names = substitute + b"\0\0" + printable + b"\0\0"
    payload = struct.pack("<IHHHHHH", 0xA0000003, 8 + len(names), 0,
                          0, len(substitute), len(substitute) + 2, len(printable)) + names
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    create = kernel.CreateFileW
    create.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, ctypes.c_void_p,
                       wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE]
    create.restype = wintypes.HANDLE
    ioctl = kernel.DeviceIoControl
    ioctl.argtypes = [wintypes.HANDLE, wintypes.DWORD, ctypes.c_void_p, wintypes.DWORD,
                      ctypes.c_void_p, wintypes.DWORD, ctypes.c_void_p, ctypes.c_void_p]
    ioctl.restype = wintypes.BOOL
    close = kernel.CloseHandle
    close.argtypes = [wintypes.HANDLE]
    with locked_directory(parent) as parent_handle:
        handle = create(str(parent), 0x40000000, 7, None, 3, 0x02200000, None)
        if handle == ctypes.c_void_p(-1).value:
            assert ctypes.get_last_error() in (5, 32)
        else:
            try:
                count = wintypes.DWORD()
                buffer = ctypes.create_string_buffer(payload)
                changed = ioctl(handle, 0x000900A4, buffer, len(payload), None, 0, ctypes.byref(count), None)
                if not empty:
                    assert not changed
            finally:
                close(handle)
        try:
            atomic_write(parent_handle, "result.json", "new")
        except OSError:
            pass
    assert (outside / "result.json").read_text(encoding="utf-8") == "sentinel"


def test_windows_replace_failure_preserves_index_and_cleans_temp(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    import arap.windows_io as windows_io
    root = tmp_path / "demo"
    cli.init_project(root)
    path = root / "control/ARTIFACT_INDEX.json"
    before = path.read_bytes()
    (root / "evidence/result.json").write_text("{}", encoding="utf-8")

    def fail(*args: object) -> None:
        raise OSError("injected rename failure")

    monkeypatch.setattr(windows_io, "replace_in_directory", fail)
    with pytest.raises(OSError, match="injected"):
        core.index_artifacts(root, [Path("evidence/result.json")])
    assert path.read_bytes() == before
    assert not list(path.parent.glob("*.tmp"))
