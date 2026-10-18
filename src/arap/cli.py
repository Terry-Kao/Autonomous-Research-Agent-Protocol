from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .core import evaluate_gates, index_artifacts, pinned_project_root, project_path, utc_now, validate_project, write_json


def init_project(root: Path) -> None:
    if root.exists() and any(root.iterdir()):
        raise FileExistsError(f"target directory is not empty: {root}")
    (root / "control").mkdir(parents=True, exist_ok=True)
    (root / "evidence").mkdir(exist_ok=True)
    write_json(root / "control/PROJECT_STATE.json", {
        "project": root.name,
        "phase": "bootstrap",
        "status": "PLANNED",
        "next_action": "Freeze the protocol before inspecting final results.",
        "updated_at": utc_now(),
    })
    write_json(root / "control/PROTOCOL.json", {
        "version": 1,
        "frozen": False,
        "frozen_at": None,
        "scope": "Define the bounded research question and acceptance criteria.",
        "exclusions": [],
    })
    write_json(root / "control/GATES.json", {"gates": [
        {"id": "integrity", "mandatory": True, "status": "PENDING", "evidence": []},
        {"id": "provenance", "mandatory": True, "status": "PENDING", "evidence": []},
        {"id": "independent-review", "mandatory": True, "status": "PENDING", "evidence": []},
    ]})
    write_json(root / "control/ARTIFACT_INDEX.json", {"updated_at": utc_now(), "artifacts": []})
    (root / "README.md").write_text(f"# {root.name}\n\nGoverned with ARAP.\n", encoding="utf-8")


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(prog="arap")
    sub = result.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init", help="create a governed project")
    init.add_argument("directory", type=Path)
    validate = sub.add_parser("validate", help="validate a project contract")
    validate.add_argument("directory", type=Path)
    index = sub.add_parser("index", help="hash and index evidence files")
    index.add_argument("directory", type=Path)
    index.add_argument("files", nargs="+", type=Path)
    index.add_argument("--purpose", default="run evidence")
    gate = sub.add_parser("gate", help="evaluate declared gates")
    gate.add_argument("directory", type=Path)
    gate.add_argument("--reviewer", required=True)
    gate.add_argument("--output", type=Path)
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "init":
            init_project(args.directory)
            print(f"initialized {args.directory}")
        elif args.command == "validate":
            errors = validate_project(args.directory)
            if errors:
                print("INVALID")
                for error in errors:
                    print(f"- {error}")
                return 1
            print("VALID")
        elif args.command == "index":
            result = index_artifacts(args.directory, args.files, args.purpose)
            print(f"indexed {len(result['artifacts'])} artifact(s)")
        elif args.command == "gate":
            with pinned_project_root(args.directory) as (resolved_root, root_fd):
                result = evaluate_gates(resolved_root, args.reviewer)
                output = project_path(resolved_root, args.output or Path("control/GATE_DECISION.json"))
                relative_output = output.relative_to(resolved_root)
                write_json(
                    output,
                    result,
                    contained_root=resolved_root,
                    contained_root_fd=root_fd,
                    relative_path=relative_output,
                )
            print(result["decision"])
            return 0 if result["decision"] == "PASS" else 2
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

