# Architecture

ARAP separates orchestration from truth claims. Agents and CI may collect evidence and evaluate declared gates, but they do not discover or certify domain truth on their own.

## Control plane

- `PROJECT_STATE.json` is the current, bounded handoff state.
- `PROTOCOL.json` records scope, exclusions, and whether acceptance criteria are frozen.
- `GATES.json` declares mandatory and advisory gates with explicit evidence links.
- `ARTIFACT_INDEX.json` binds evidence paths to SHA-256 digests.
- `GATE_DECISION.json` is a derived review result, not an authority to merge by itself.

Validation treats control JSON as untrusted input: top-level and nested shapes are checked, duplicate keys and oversized JSON are rejected, project-local paths may not escape the project root, and every local gate-evidence path must be bound to its current bytes in `ARTIFACT_INDEX.json`. HTTPS references identify external evidence but are not treated as content-addressed local artifacts.

## Trust boundaries

The authoring agent may propose implementation and evidence. Independent review must run from committed bytes and must not treat the author's conclusion as evidence. Repository protections and human maintainer policy remain authoritative for merge and release.

## Decision semantics

- `PASS`: every mandatory gate passes.
- `REVISE`: at least one mandatory gate explicitly fails.
- `BLOCKED`: required evidence or a mandatory gate remains pending or unsupported.

Advisory performance results never override mandatory integrity, provenance, safety, or independence gates.

## Extension model

Projects can add domain-specific gates and schemas while preserving the core decision semantics. Integrations should write evidence files first, index their hashes, then update gate status through a reviewable pull request.

