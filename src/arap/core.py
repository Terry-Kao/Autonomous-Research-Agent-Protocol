from __future__ import annotations

import hashlib
import json
import os
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

REQUIRED_FILES = (
    "control/PROJECT_STATE.json",
    "control/PROTOCOL.json",
    "control/GATES.json",
    "control/ARTIFACT_INDEX.json",
)
DECISIONS = {"PASS", "REVISE", "BLOCKED"}
MAX_JSON_BYTES = 10 * 1024 * 1024


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_json(path: Path) -> Any:
    if path.stat().st_size > MAX_JSON_BYTES:
        raise ValueError(f"JSON file exceeds {MAX_JSON_BYTES} bytes: {path}")

    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle, object_pairs_hook=reject_duplicates)
    except RecursionError as error:
        raise ValueError(f"JSON nesting is too deep: {path}") from error


@contextmanager
def pinned_project_root(root: Path) -> Iterator[tuple[Path, int | None]]:
    try:
        resolved_root = root.resolve()
    except RuntimeError as error:
        raise ValueError(f"path could not be resolved safely: {root}") from error
    if os.name != "posix":
        yield resolved_root, None
        return
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
    root_fd = os.open(resolved_root, flags)
    try:
        yield resolved_root, root_fd
    finally:
        os.close(root_fd)


def write_json(
    path: Path,
    value: Any,
    *,
    contained_root: Path | None = None,
    contained_root_fd: int | None = None,
    relative_path: Path | None = None,
) -> None:
    try:
        rendered = json.dumps(value, indent=2, sort_keys=True) + "\n"
    except RecursionError as error:
        raise ValueError(f"JSON nesting is too deep to write: {path}") from error
    if contained_root_fd is not None:
        if relative_path is None or relative_path.is_absolute() or ".." in relative_path.parts:
            raise ValueError(f"path must be inside project: {path}")
        flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
        directory_fd = os.dup(contained_root_fd)
        destination_name = relative_path.name
        temporary_name = f".{destination_name}.{uuid.uuid4().hex}.tmp"
        try:
            for component in relative_path.parts[:-1]:
                try:
                    next_fd = os.open(component, flags, dir_fd=directory_fd)
                except FileNotFoundError:
                    os.mkdir(component, dir_fd=directory_fd)
                    os.fsync(directory_fd)
                    next_fd = os.open(component, flags, dir_fd=directory_fd)
                os.close(directory_fd)
                directory_fd = next_fd
            file_flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
            file_fd = os.open(temporary_name, file_flags, 0o666, dir_fd=directory_fd)
            with os.fdopen(file_fd, "w", encoding="utf-8", newline="\n") as handle:
                handle.write(rendered)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary_name, destination_name, src_dir_fd=directory_fd, dst_dir_fd=directory_fd)
            os.fsync(directory_fd)
        finally:
            try:
                os.unlink(temporary_name, dir_fd=directory_fd)
            except OSError:
                pass
            finally:
                os.close(directory_fd)
        return
    if contained_root is not None:
        resolved_root = contained_root.resolve()
        destination = resolved_root / relative_path if relative_path is not None else path
        resolved_parent = destination.parent.resolve()
        try:
            resolved_parent.relative_to(resolved_root)
        except ValueError as error:
            raise ValueError(f"path must be inside project: {path}") from error
        if destination.is_symlink():
            destination.unlink()
    else:
        destination = path
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(rendered)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def project_path(root: Path, path: str | Path, *, must_exist: bool = False) -> Path:
    candidate = Path(path)
    absolute = candidate if candidate.is_absolute() else root / candidate
    try:
        resolved = absolute.resolve()
        resolved_root = root.resolve()
    except RuntimeError as error:
        raise ValueError(f"path could not be resolved safely: {path}") from error
    try:
        resolved.relative_to(resolved_root)
    except ValueError as error:
        raise ValueError(f"path must be inside project: {path}") from error
    if must_exist and not resolved.is_file():
        raise FileNotFoundError(path)
    return resolved


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
    except (OSError, ValueError, json.JSONDecodeError) as error:
        return [f"invalid JSON: {error}"]

    if not all(isinstance(item, dict) for item in (state, protocol, gates, artifact_index)):
        return ["all control files must contain a JSON object"]

    for field in ("project", "phase", "status", "next_action"):
        if not isinstance(state.get(field), str) or not state[field].strip():
            errors.append(f"PROJECT_STATE.{field} must be a non-empty string")
    if isinstance(state.get("status"), str) and state["status"] not in DECISIONS | {"PLANNED", "RUNNING"}:
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
            if not isinstance(gate, dict):
                errors.append("each gate must be an object")
                continue
            gate_id = gate.get("id")
            if not isinstance(gate_id, str) or not gate_id:
                errors.append("each gate requires an id")
            elif gate_id in ids:
                errors.append(f"duplicate gate id: {gate_id}")
            else:
                ids.add(gate_id)
            status = gate.get("status")
            if not isinstance(status, str) or status not in {"PASS", "FAIL", "UNSUPPORTED", "PENDING"}:
                errors.append(f"gate {gate_id!r} has invalid status")
            if not isinstance(gate.get("mandatory"), bool):
                errors.append(f"gate {gate_id!r} mandatory must be boolean")
            evidence = gate.get("evidence")
            if not isinstance(evidence, list) or not all(isinstance(item, str) and item for item in evidence):
                errors.append(f"gate {gate_id!r} evidence must be a list of non-empty strings")
    artifacts = artifact_index.get("artifacts")
    if not isinstance(artifacts, list):
        errors.append("ARTIFACT_INDEX.artifacts must be a list")
        artifacts = []
    indexed: dict[str, dict[str, Any]] = {}
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            errors.append("each artifact must be an object")
            continue
        relative = artifact.get("path")
        if not isinstance(relative, str) or not relative:
            errors.append("each artifact requires a non-empty path")
            continue
        if relative in indexed:
            errors.append(f"duplicate artifact path: {relative}")
            continue
        indexed[relative] = artifact
        try:
            target = project_path(root, relative, must_exist=True)
        except (OSError, RuntimeError, ValueError) as error:
            errors.append(f"artifact {relative!r} is invalid: {error}")
            continue
        expected_hash = artifact.get("sha256")
        expected_size = artifact.get("size_bytes")
        if not isinstance(expected_hash, str) or len(expected_hash) != 64:
            errors.append(f"artifact {relative!r} has invalid sha256")
        elif sha256_file(target) != expected_hash:
            errors.append(f"artifact {relative!r} sha256 mismatch")
        if not isinstance(expected_size, int) or isinstance(expected_size, bool) or expected_size < 0:
            errors.append(f"artifact {relative!r} has invalid size_bytes")
        elif target.stat().st_size != expected_size:
            errors.append(f"artifact {relative!r} size mismatch")
    if isinstance(gates.get("gates"), list):
        for gate in gates["gates"]:
            if not isinstance(gate, dict):
                continue
            for evidence in gate.get("evidence", []) if isinstance(gate.get("evidence"), list) else []:
                if not isinstance(evidence, str):
                    continue
                if evidence.startswith("https://"):
                    continue
                if evidence.startswith("http://"):
                    errors.append(f"gate {gate.get('id')!r} external evidence must use https: {evidence}")
                    continue
                if evidence not in indexed:
                    errors.append(f"gate {gate.get('id')!r} evidence is not indexed: {evidence}")
    return errors


def index_artifacts(root: Path, paths: list[Path], purpose: str = "run evidence") -> dict[str, Any]:
    with pinned_project_root(root) as (resolved_root, root_fd):
        index_relative = Path("control/ARTIFACT_INDEX.json")
        index_path = project_path(resolved_root, index_relative)
        current = load_json(index_path) if index_path.exists() else {"artifacts": []}
        if not isinstance(current, dict) or not isinstance(current.get("artifacts"), list):
            raise ValueError("ARTIFACT_INDEX.artifacts must be a list")
        by_path: dict[str, dict[str, Any]] = {}
        for item in current["artifacts"]:
            if not isinstance(item, dict) or not isinstance(item.get("path"), str):
                raise ValueError("each existing artifact requires a string path")
            by_path[item["path"]] = item
        for path in paths:
            resolved = project_path(resolved_root, path, must_exist=True)
            relative = resolved.relative_to(resolved_root).as_posix()
            by_path[relative] = {
                "path": relative,
                "purpose": purpose,
                "sha256": sha256_file(resolved),
                "size_bytes": resolved.stat().st_size,
                "status": "CURRENT",
            }
        result = {"updated_at": utc_now(), "artifacts": sorted(by_path.values(), key=lambda item: item["path"])}
        write_json(
            index_path,
            result,
            contained_root=resolved_root,
            contained_root_fd=root_fd,
            relative_path=index_relative,
        )
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

