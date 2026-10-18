import json
import os
from pathlib import Path

import pytest

import arap
import arap.cli as cli
import arap.core as core
from arap.cli import init_project
from arap.cli import main
from arap.core import evaluate_gates, index_artifacts, load_json, sha256_file, validate_project, write_json


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


def test_index_replaces_internal_index_symlink_not_its_target(tmp_path: Path) -> None:
    root = tmp_path / "demo"
    init_project(root)
    artifact = root / "evidence/result.json"
    artifact.write_text("{}\n", encoding="utf-8")
    index_path = root / "control/ARTIFACT_INDEX.json"
    alternate = root / "control/alternate.json"
    alternate.write_text(index_path.read_text(encoding="utf-8"), encoding="utf-8")
    index_path.unlink()
    try:
        index_path.symlink_to(alternate)
    except OSError as error:
        pytest.skip(f"symlinks unavailable: {error}")
    before = alternate.read_text(encoding="utf-8")
    index_artifacts(root, [Path("evidence/result.json")])
    assert not index_path.is_symlink()
    assert alternate.read_text(encoding="utf-8") == before
    assert load_json(index_path)["artifacts"]


@pytest.mark.skipif(os.name != "posix", reason="secure directory-descriptor semantics are POSIX-specific")
def test_gate_swap_does_not_create_outside_directories(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root = tmp_path / "demo"
    init_project(root)
    outside = tmp_path / "outside"
    outside.mkdir()
    original_write_json = core.write_json

    def swap_before_write(path: Path, value: object, **kwargs: object) -> None:
        root.rename(tmp_path / "demo-original")
        root.symlink_to(outside, target_is_directory=True)
        original_write_json(path, value, **kwargs)

    monkeypatch.setattr(cli, "write_json", swap_before_write)
    assert main(["gate", str(root), "--reviewer", "reviewer", "--output", "new/nested/result.json"]) == 2
    assert not (outside / "new").exists()


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


def test_deeply_nested_json_write_does_not_truncate_existing_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path / "index.json"
    original = '{"sentinel": true}\n'
    path.write_text(original, encoding="utf-8")
    def fail_serialization(*args: object, **kwargs: object) -> str:
        raise RecursionError("injected nesting failure")

    monkeypatch.setattr(core.json, "dumps", fail_serialization)
    with pytest.raises(ValueError, match="JSON nesting is too deep to write"):
        write_json(path, {"nested": []})
    assert path.read_text(encoding="utf-8") == original


@pytest.mark.skipif(os.name != "posix", reason="secure directory-descriptor semantics are POSIX-specific")
def test_index_rejects_parent_symlink_swap_during_hashing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = tmp_path / "demo"
    init_project(root)
    artifact = root / "evidence/result.json"
    artifact.write_text("{}\n", encoding="utf-8")
    outside_control = tmp_path / "outside-control"
    outside_control.mkdir()
    outside_index = outside_control / "ARTIFACT_INDEX.json"
    sentinel = '{"sentinel": true}\n'
    outside_index.write_text(sentinel, encoding="utf-8")
    original_sha256_file = core.sha256_file
    swapped = False

    def swap_parent_then_hash(path: Path) -> str:
        nonlocal swapped
        if path == artifact.resolve() and not swapped:
            swapped = True
            (root / "control").rename(root / "control-original")
            (root / "control").symlink_to(outside_control, target_is_directory=True)
        return original_sha256_file(path)

    monkeypatch.setattr(core, "sha256_file", swap_parent_then_hash)
    try:
        index_artifacts(root, [Path("evidence/result.json")])
    except OSError:
        pass
    assert outside_index.read_text(encoding="utf-8") == sentinel
    assert (root / "control-original/ARTIFACT_INDEX.json").is_file()


@pytest.mark.skipif(os.name != "posix", reason="secure directory-descriptor semantics are POSIX-specific")
def test_index_pins_project_root_before_hashing(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root = tmp_path / "demo"
    init_project(root)
    artifact = root / "evidence/result.json"
    artifact.write_text("{}\n", encoding="utf-8")
    outside_root = tmp_path / "outside-root"
    (outside_root / "control").mkdir(parents=True)
    outside_index = outside_root / "control/ARTIFACT_INDEX.json"
    sentinel = '{"sentinel": true}\n'
    outside_index.write_text(sentinel, encoding="utf-8")
    original_sha256_file = core.sha256_file
    swapped = False

    def hash_then_swap_root(path: Path) -> str:
        nonlocal swapped
        result = original_sha256_file(path)
        if path == artifact.resolve() and not swapped:
            swapped = True
            root.rename(tmp_path / "demo-original")
            root.symlink_to(outside_root, target_is_directory=True)
        return result

    monkeypatch.setattr(core, "sha256_file", hash_then_swap_root)
    try:
        index_artifacts(root, [Path("evidence/result.json")])
    except OSError:
        pass
    assert outside_index.read_text(encoding="utf-8") == sentinel
    assert (tmp_path / "demo-original/control/ARTIFACT_INDEX.json").is_file()


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


@pytest.mark.skipif(os.name != "posix", reason="secure directory-descriptor semantics are POSIX-specific")
def test_gate_rejects_parent_symlink_swap_before_write(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = tmp_path / "demo"
    init_project(root)
    outside_control = tmp_path / "outside-control"
    outside_control.mkdir()
    outside_decision = outside_control / "GATE_DECISION.json"
    sentinel = '{"sentinel": true}\n'
    outside_decision.write_text(sentinel, encoding="utf-8")
    original_write_json = core.write_json

    def swap_parent_then_write(path: Path, value: object, **kwargs: object) -> None:
        (root / "control").rename(root / "control-original")
        (root / "control").symlink_to(outside_control, target_is_directory=True)
        original_write_json(path, value, **kwargs)

    monkeypatch.setattr(cli, "write_json", swap_parent_then_write)
    assert main(["gate", str(root), "--reviewer", "reviewer"]) == 2
    assert outside_decision.read_text(encoding="utf-8") == sentinel


@pytest.mark.skipif(os.name != "posix", reason="secure directory-descriptor semantics are POSIX-specific")
def test_gate_rejects_intermediate_parent_symlink_swap(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = tmp_path / "demo"
    init_project(root)
    (root / "a/b").mkdir(parents=True)
    outside = tmp_path / "outside"
    (outside / "b").mkdir(parents=True)
    outside_result = outside / "b/result.json"
    sentinel = '{"sentinel": true}\n'
    outside_result.write_text(sentinel, encoding="utf-8")
    original_write_json = core.write_json

    def swap_ancestor_then_write(path: Path, value: object, **kwargs: object) -> None:
        (root / "a").rename(root / "a-original")
        (root / "a").symlink_to(outside, target_is_directory=True)
        original_write_json(path, value, **kwargs)

    monkeypatch.setattr(cli, "write_json", swap_ancestor_then_write)
    assert main(["gate", str(root), "--reviewer", "reviewer", "--output", "a/b/result.json"]) == 2
    assert outside_result.read_text(encoding="utf-8") == sentinel


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


def test_root_resolution_loop_is_a_controlled_cli_error(tmp_path: Path) -> None:
    root = tmp_path / "loop"
    try:
        root.symlink_to(root, target_is_directory=True)
    except OSError as error:
        pytest.skip(f"symlinks unavailable: {error}")
    assert main(["index", str(root), "artifact.json"]) == 2
    assert main(["gate", str(root), "--reviewer", "reviewer"]) == 2


def test_runtime_version_matches_alpha_metadata() -> None:
    assert arap.__version__ == "0.1.0a1"

