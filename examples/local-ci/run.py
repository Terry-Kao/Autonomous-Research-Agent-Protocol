"""Run a synthetic, domain-neutral local CI handoff in a fresh directory."""
import json
import subprocess
import sys
from pathlib import Path


def run(*args: str) -> None:
    subprocess.run([sys.executable, "-m", "arap.cli", *args], check=True)


root = Path(sys.argv[1]).resolve()
run("init", str(root))
evidence = root / "evidence/result.json"
evidence.write_text('{"synthetic": true, "check": "example-only", "passed": true}\n', encoding="utf-8")
run("index", str(root), "evidence/result.json")
run("validate", str(root))
# init deliberately leaves mandatory review gates pending. Preserve that state.
result = subprocess.run([sys.executable, "-m", "arap.cli", "gate", str(root), "--reviewer", "synthetic-ci-demo"])
assert result.returncode == 2
decision = json.loads((root / "control/GATE_DECISION.json").read_text(encoding="utf-8"))
assert decision["decision"] == "BLOCKED"
print("PASS: synthetic evidence indexed; missing reviews correctly BLOCKED")
