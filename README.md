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

```bash
python -m pip install -e .
arap init my-research-project
cd my-research-project
arap validate .
arap index . --output control/ARTIFACT_INDEX.json evidence/result.json
arap gate . --reviewer independent-review-bot
```

Try the included example without modifying it:

```bash
arap validate examples/minimal-project
arap gate examples/minimal-project --reviewer local-review
```

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
docs/                      architecture, workflow, security, roadmap
.github/                   issue/PR templates and CI
```

## Status

`v0.1.0-alpha` is intended for evaluation and contributor feedback. The first release will stabilize the schemas and CLI contract after public review. See [ROADMAP.md](ROADMAP.md) and [docs/RELEASE_PLAN.md](docs/RELEASE_PLAN.md).

## Contributing and security

Contributions are welcome. Start with [CONTRIBUTING.md](CONTRIBUTING.md). Please report vulnerabilities according to [SECURITY.md](SECURITY.md), not in a public issue.

Licensed under the [MIT License](LICENSE).

