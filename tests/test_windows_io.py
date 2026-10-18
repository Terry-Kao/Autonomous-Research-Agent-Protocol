import os
import subprocess
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
