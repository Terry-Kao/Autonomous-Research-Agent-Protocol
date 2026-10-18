import json
from pathlib import Path

import pytest

import arap
from arap.cli import init_project
from arap.cli import main
from arap.core import evaluate_gates, index_artifacts, load_json, sha256_file, validate_project


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


def test_index_rejects_symlinked_index_outside_project(tmp_path: Path) -> None:
    root = tmp_path / "demo"
    init_project(root)
    artifact = root / "evidence/result.json"
    artifact.write_text("{}\n", encoding="utf-8")
    outside = tmp_path / "outside-index.json"
    outside.write_text('{"sentinel": true}\n', encoding="utf-8")
    index_path = root / "control/ARTIFACT_INDEX.json"
    index_path.unlink()
    try:
        index_path.symlink_to(outside)
    except OSError as error:
        pytest.skip(f"symlinks unavailable: {error}")
    with pytest.raises(ValueError, match="path must be inside project"):
        index_artifacts(root, [Path("evidence/result.json")])
    assert outside.read_text(encoding="utf-8") == '{"sentinel": true}\n'


def test_index_rejects_symlinked_control_directory_outside_project(tmp_path: Path) -> None:
    root = tmp_path / "demo"
    init_project(root)
    artifact = root / "evidence/result.json"
    artifact.write_text("{}\n", encoding="utf-8")
    outside_control = tmp_path / "outside-control"
    try:
        (root / "control").rename(outside_control)
    except OSError as error:
        pytest.skip(f"directory symlink setup unavailable: {error}")
    try:
        (root / "control").symlink_to(outside_control, target_is_directory=True)
    except OSError as error:
        pytest.skip(f"directory symlinks unavailable: {error}")
    before = (outside_control / "ARTIFACT_INDEX.json").read_text(encoding="utf-8")
    with pytest.raises(ValueError, match="path must be inside project"):
        index_artifacts(root, [Path("evidence/result.json")])
    assert (outside_control / "ARTIFACT_INDEX.json").read_text(encoding="utf-8") == before


def test_duplicate_gate_ids_are_invalid(tmp_path: Path) -> None:
    root = tmp_path / "demo"
    init_project(root)
    path = root / "control/GATES.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["gates"].append(dict(data["gates"][0]))
    path.write_text(json.dumps(data), encoding="utf-8")
    assert any("duplicate gate id" in error for error in validate_project(root))


def test_untrusted_json_shape_is_reported_not_raised(tmp_path: Path) -> None:
    root = tmp_path / "demo"
    init_project(root)
    (root / "control/GATES.json").write_text('["not-an-object"]', encoding="utf-8")
    assert validate_project(root) == ["all control files must contain a JSON object"]


@pytest.mark.parametrize("value", [[], {}])
def test_project_state_status_shape_is_reported_not_raised(tmp_path: Path, value: object) -> None:
    root = tmp_path / "demo"
    init_project(root)
    path = root / "control/PROJECT_STATE.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["status"] = value
    path.write_text(json.dumps(data), encoding="utf-8")
    errors = validate_project(root)
    assert "PROJECT_STATE.status must be a non-empty string" in errors


def test_deeply_nested_json_is_reported_not_raised(tmp_path: Path) -> None:
    root = tmp_path / "demo"
    init_project(root)
    (root / "control/GATES.json").write_text("[" * 100_000 + "0" + "]" * 100_000, encoding="utf-8")
    errors = validate_project(root)
    assert len(errors) == 1
    assert "JSON nesting is too deep" in errors[0]


def test_duplicate_json_keys_are_rejected(tmp_path: Path) -> None:
    path = tmp_path / "duplicate.json"
    path.write_text('{"status":"PASS","status":"FAIL"}', encoding="utf-8")
    with pytest.raises(ValueError, match="duplicate JSON key"):
        load_json(path)


def test_tampered_indexed_artifact_is_invalid(tmp_path: Path) -> None:
    root = tmp_path / "demo"
    init_project(root)
    artifact = root / "evidence/result.json"
    artifact.write_text('{"score":1}\n', encoding="utf-8")
    index_artifacts(root, [Path("evidence/result.json")])
    artifact.write_text('{"score":2}\n', encoding="utf-8")
    assert any("sha256 mismatch" in error for error in validate_project(root))


def test_local_gate_evidence_must_be_indexed(tmp_path: Path) -> None:
    root = tmp_path / "demo"
    init_project(root)
    evidence = root / "evidence/result.json"
    evidence.write_text('{}\n', encoding="utf-8")
    gates = json.loads((root / "control/GATES.json").read_text(encoding="utf-8"))
    gates["gates"][0]["evidence"] = ["evidence/result.json"]
    (root / "control/GATES.json").write_text(json.dumps(gates), encoding="utf-8")
    assert any("evidence is not indexed" in error for error in validate_project(root))


def test_gate_output_cannot_escape_project(tmp_path: Path) -> None:
    root = tmp_path / "demo"
    init_project(root)
    assert main(["gate", str(root), "--reviewer", "reviewer", "--output", str(tmp_path / "outside.json")]) == 2
    assert not (tmp_path / "outside.json").exists()


@pytest.mark.parametrize("field,value", [("id", []), ("status", {})])
def test_nested_gate_types_return_validation_errors(tmp_path: Path, field: str, value: object) -> None:
    root = tmp_path / "demo"
    init_project(root)
    path = root / "control/GATES.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["gates"][0][field] = value
    path.write_text(json.dumps(data), encoding="utf-8")
    errors = validate_project(root)
    assert errors
    assert any(field in error for error in errors)


def test_plain_http_external_evidence_is_rejected(tmp_path: Path) -> None:
    root = tmp_path / "demo"
    init_project(root)
    path = root / "control/GATES.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["gates"][0]["evidence"] = ["http://example.test/result.json"]
    path.write_text(json.dumps(data), encoding="utf-8")
    assert any("must use https" in error for error in validate_project(root))


def test_resolution_loop_becomes_validation_error(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root = tmp_path / "demo"
    init_project(root)
    artifact = root / "evidence/loop"
    artifact.write_text("loop", encoding="utf-8")
    index_artifacts(root, [Path("evidence/loop")])
    original_resolve = Path.resolve

    def fail_loop(path: Path, *args: object, **kwargs: object) -> Path:
        if path.name == "loop":
            raise RuntimeError("symlink loop")
        return original_resolve(path, *args, **kwargs)

    monkeypatch.setattr(Path, "resolve", fail_loop)
    assert any("could not be resolved safely" in error for error in validate_project(root))


def test_runtime_version_matches_alpha_metadata() -> None:
    assert arap.__version__ == "0.1.0a1"

