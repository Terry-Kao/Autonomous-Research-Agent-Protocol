import json
from pathlib import Path

import pytest

from arap.cli import init_project
from arap.core import evaluate_gates, index_artifacts, sha256_file, validate_project


def test_init_is_valid(tmp_path: Path) -> None:
    root = tmp_path / "demo"
    init_project(root)
    assert validate_project(root) == []


def test_mandatory_pending_blocks(tmp_path: Path) -> None:
    root = tmp_path / "demo"
    init_project(root)
    result = evaluate_gates(root, "reviewer")
    assert result["decision"] == "BLOCKED"
    assert "integrity" in result["failed_or_pending_gates"]


def test_failed_gate_requires_revision(tmp_path: Path) -> None:
    root = tmp_path / "demo"
    init_project(root)
    path = root / "control/GATES.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    for gate in data["gates"]:
        gate["status"] = "FAIL" if gate["id"] == "integrity" else "PASS"
    path.write_text(json.dumps(data), encoding="utf-8")
    assert evaluate_gates(root, "reviewer")["decision"] == "REVISE"


def test_all_mandatory_pass(tmp_path: Path) -> None:
    root = tmp_path / "demo"
    init_project(root)
    path = root / "control/GATES.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    for gate in data["gates"]:
        gate["status"] = "PASS"
    path.write_text(json.dumps(data), encoding="utf-8")
    assert evaluate_gates(root, "reviewer")["decision"] == "PASS"


def test_index_records_hash(tmp_path: Path) -> None:
    root = tmp_path / "demo"
    init_project(root)
    artifact = root / "evidence/result.json"
    artifact.write_text('{"score": 1}\n', encoding="utf-8")
    result = index_artifacts(root, [Path("evidence/result.json")])
    assert result["artifacts"][0]["sha256"] == sha256_file(artifact)


def test_index_rejects_external_file(tmp_path: Path) -> None:
    root = tmp_path / "demo"
    init_project(root)
    external = tmp_path / "external.txt"
    external.write_text("no", encoding="utf-8")
    with pytest.raises(ValueError):
        index_artifacts(root, [external])


def test_duplicate_gate_ids_are_invalid(tmp_path: Path) -> None:
    root = tmp_path / "demo"
    init_project(root)
    path = root / "control/GATES.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["gates"].append(dict(data["gates"][0]))
    path.write_text(json.dumps(data), encoding="utf-8")
    assert any("duplicate gate id" in error for error in validate_project(root))

