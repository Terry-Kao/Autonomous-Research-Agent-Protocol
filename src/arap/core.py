from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REQUIRED_FILES = (
    "control/PROJECT_STATE.json",
    "control/PROTOCOL.json",
    "control/GATES.json",
    "control/ARTIFACT_INDEX.json",
)
DECISIONS = {"PASS", "REVISE", "BLOCKED"}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_project(root: Path) -> list[str]:
    errors: list[str] = []
    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            errors.append(f"missing required file: {relative}")
    if errors:
        return errors

    try:
        state = load_json(root / "control/PROJECT_STATE.json")
        protocol = load_json(root / "control/PROTOCOL.json")
        gates = load_json(root / "control/GATES.json")
        artifact_index = load_json(root / "control/ARTIFACT_INDEX.json")
    except (OSError, json.JSONDecodeError) as error:
        return [f"invalid JSON: {error}"]

    for field in ("project", "phase", "status", "next_action"):
        if not isinstance(state.get(field), str) or not state[field].strip():
            errors.append(f"PROJECT_STATE.{field} must be a non-empty string")
    if state.get("status") not in DECISIONS | {"PLANNED", "RUNNING"}:
        errors.append("PROJECT_STATE.status is not an allowed value")
    if not isinstance(protocol.get("frozen"), bool):
        errors.append("PROTOCOL.frozen must be boolean")
    if protocol.get("frozen") and not protocol.get("frozen_at"):
        errors.append("a frozen protocol requires frozen_at")
    if not isinstance(gates.get("gates"), list) or not gates["gates"]:
        errors.append("GATES.gates must contain at least one gate")
    else:
        ids: set[str] = set()
        for gate in gates["gates"]:
            gate_id = gate.get("id")
            if not isinstance(gate_id, str) or not gate_id:
                errors.append("each gate requires an id")
            elif gate_id in ids:
                errors.append(f"duplicate gate id: {gate_id}")
            ids.add(gate_id)
            if gate.get("status") not in {"PASS", "FAIL", "UNSUPPORTED", "PENDING"}:
                errors.append(f"gate {gate_id!r} has invalid status")
            if not isinstance(gate.get("mandatory"), bool):
                errors.append(f"gate {gate_id!r} mandatory must be boolean")
    if not isinstance(artifact_index.get("artifacts"), list):
        errors.append("ARTIFACT_INDEX.artifacts must be a list")
    return errors


def index_artifacts(root: Path, paths: list[Path], purpose: str = "run evidence") -> dict[str, Any]:
    index_path = root / "control/ARTIFACT_INDEX.json"
    current = load_json(index_path) if index_path.exists() else {"artifacts": []}
    by_path = {item["path"]: item for item in current.get("artifacts", [])}
    for path in paths:
        absolute = path if path.is_absolute() else root / path
        resolved = absolute.resolve()
        try:
            relative = resolved.relative_to(root.resolve()).as_posix()
        except ValueError as error:
            raise ValueError(f"artifact must be inside project: {path}") from error
        if not resolved.is_file():
            raise FileNotFoundError(path)
        by_path[relative] = {
            "path": relative,
            "purpose": purpose,
            "sha256": sha256_file(resolved),
            "size_bytes": resolved.stat().st_size,
            "status": "CURRENT",
        }
    result = {"updated_at": utc_now(), "artifacts": sorted(by_path.values(), key=lambda item: item["path"])}
    write_json(index_path, result)
    return result


def evaluate_gates(root: Path, reviewer: str) -> dict[str, Any]:
    errors = validate_project(root)
    if errors:
        decision = "BLOCKED"
        failed = ["project-contract"]
    else:
        gates = load_json(root / "control/GATES.json")["gates"]
        failed = [gate["id"] for gate in gates if gate["mandatory"] and gate["status"] == "FAIL"]
        pending = [gate["id"] for gate in gates if gate["mandatory"] and gate["status"] in {"PENDING", "UNSUPPORTED"}]
        decision = "REVISE" if failed else "BLOCKED" if pending else "PASS"
        failed += pending
    return {
        "decision": decision,
        "reviewer": reviewer,
        "reviewed_at": utc_now(),
        "failed_or_pending_gates": failed,
        "validation_errors": errors,
        "policy": "All mandatory gates must PASS. Performance cannot override integrity, safety, provenance, or independence failures.",
    }

