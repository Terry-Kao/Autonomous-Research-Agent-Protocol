# ARAP v0.1.0-alpha release notes

ARAP is a dependency-free Python 3.10+ toolkit for representing frozen protocols, evidence indexes, mandatory gates, and explicit `PASS` / `REVISE` / `BLOCKED` decisions in autonomous research workflows.

## Included

- `arap init`, `validate`, `index`, and `gate` commands;
- project state, protocol, gate, decision, and SHA-256 artifact-index contracts;
- JSON Schemas for project state and gate decisions;
- a domain-neutral, evidence-backed example;
- Python 3.10–3.12 tests and clean sdist/wheel installation checks;
- contributor, security, architecture, workflow, and governance guidance.

## Alpha limitations

- Gate statuses remain reviewed declarations; ARAP does not establish domain truth.
- HTTPS evidence references are not locally content-addressed.
- Schemas and CLI contracts may change before v1.0 with documented migration notes.
- No external adoption is claimed.

## Release boundary

The maintainer authorized this GitHub pre-release after the committed independent review, remediation, clean packaging checks, and unchanged-head CI verification. This release does not publish to PyPI, claim external adoption, begin broad promotion, or submit a Codex for OSS application.
