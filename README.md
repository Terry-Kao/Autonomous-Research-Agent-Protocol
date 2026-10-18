# Autonomous Research Agent Protocol (ARAP)

ARAP is a small, dependency-free governance toolkit for research teams that use autonomous or multi-agent workflows. It turns claims such as “the run passed” into reviewable state, explicit gates, and content-addressed evidence.

The project is domain-neutral. It contains no private research datasets, unpublished findings, model weights, credentials, or project-specific scientific claims.

## Why ARAP

Autonomous agents are good at producing files and conclusions. Maintainers still need to know:

- what was frozen before results were inspected;
- which evidence was actually produced;
- whether mandatory gates passed;
- who or what performed the independent review;
- what exact action is authorized next.

ARAP makes those questions machine-checkable while keeping the final decision visible to humans.

## Core loop

```text
plan -> freeze -> execute on branch -> index evidence -> independent review
     -> PASS / REVISE / BLOCKED -> merge or open the next bounded task
```

Three invariants guide the protocol:

1. A performance result cannot override a failed mandatory integrity, safety, provenance, or independence gate.
2. Failed and superseded evidence remains visible; it is never rewritten into success.
3. A run is incomplete until its state, gate decision, evidence hashes, and authorized next action are committed.

## Quick start

Requires Python 3.10+ and no runtime dependencies.

Clone this repository and enter it first. A fresh virtual environment is recommended.

```bash
python -m pip install -e .
arap init my-research-project
cd my-research-project
arap validate .
arap gate . --reviewer independent-review-bot
```

The last command prints `BLOCKED` and exits with code 2: new projects have pending mandatory gates. This is expected. Add real evidence before indexing it with `arap index . evidence/result.json`; `init` does not create that file. Review the protocol and gates before recording any PASS.

Return to the repository root before running the included example below.

Try the included example (the gate command refreshes its derived decision timestamp):

```bash
arap validate examples/minimal-project
arap gate examples/minimal-project --reviewer local-review
```

For a fresh synthetic CI handoff that preserves missing-review blockers, see [examples/local-ci](examples/local-ci/README.md).

## Try it and report back

ARAP is an alpha. The most useful feedback is a reproducible report from a clean
Python 3.10+ environment:

- **Try it:** follow the quick start above and record the tag or commit, operating
  system, Python version, commands, and exit codes.
- **Give feedback:** reply to [the public introduction discussion](https://github.com/Terry-Kao/Autonomous-Research-Agent-Protocol/discussions/13)
  or use [the public feedback issue](https://github.com/Terry-Kao/Autonomous-Research-Agent-Protocol/issues/5)
  for README usability, clean-install, or behavior reports. Use
  [SECURITY.md](SECURITY.md) instead for vulnerabilities.
- **Report integration results:** describe the workflow you tried, what ARAP
  governed, expected and actual results, and a small domain-neutral reproduction.
- **Make a first contribution:** [Issue #4](https://github.com/Terry-Kao/Autonomous-Research-Agent-Protocol/issues/4)
  is reserved for an external contributor. Please coordinate on the issue before
  starting overlapping work.

See [PUBLIC_INTRODUCTION.md](PUBLIC_INTRODUCTION.md) for the public alpha scope and
[EXTERNAL_FEEDBACK_LOG.md](EXTERNAL_FEEDBACK_LOG.md) for the evidence policy and
verified feedback log. Stars and forks are observations, not proof of use.

## What the CLI does

- `arap init DIR` creates a governed project with state, protocol, gates, and evidence folders.
- `arap validate DIR` validates the cross-file contract and reports actionable errors.
- `arap index DIR FILE...` records SHA-256, size, purpose, and status for evidence files.
- `arap gate DIR --reviewer NAME` evaluates mandatory gates and emits a machine-readable decision.

The CLI never runs research code, merges a pull request, uploads data, or claims scientific truth. It evaluates declared evidence against a declared protocol.

## Repository map

```text
src/arap/                  dependency-free CLI and validation library
schemas/                   JSON Schemas for interoperable state files
examples/minimal-project/  runnable domain-neutral example
control/                   this repository's own state, gates, and evidence index
docs/                      architecture, workflow, security, roadmap
.github/                   issue/PR templates and CI
```

ARAP governs its own release preparation. The current decision and blockers are recorded in [`control/PROJECT_STATE.json`](control/PROJECT_STATE.json) and [`control/GATE_HISTORY.md`](control/GATE_HISTORY.md).

## Status

`v0.1.0-alpha` is intended for evaluation and contributor feedback. The first release will stabilize the schemas and CLI contract after public review. See [ROADMAP.md](ROADMAP.md) and [docs/RELEASE_PLAN.md](docs/RELEASE_PLAN.md).

External human adoption is not claimed merely from automated review, stars, or
forks. Verifiable external issues, pull requests, discussion comments, or
integration reports are recorded separately from AI/bot review.

## Contributing and security

Contributions are welcome. Start with [CONTRIBUTING.md](CONTRIBUTING.md). Please report vulnerabilities according to [SECURITY.md](SECURITY.md), not in a public issue.

Licensed under the [MIT License](LICENSE).

