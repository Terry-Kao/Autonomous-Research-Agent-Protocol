# Gate history

## 2026-10-18 — Public bootstrap

**Decision: BLOCKED**

- Public repository created without importing private research content.
- Initial commit `ae6ca2f398b0eafc3768840520e9867c86aa1ee7` is visible on `main`.
- GitHub Actions run `39050618056` passed on Python 3.10, 3.11, and 3.12.
- Local test suite passed 7/7 tests.
- Release remains blocked pending independent review and explicit maintainer release authorization.

This decision does not authorize a package publication, GitHub Release, public announcement, or sponsorship application.

## 2026-10-18 — Independent release review and remediation

**Decision: BLOCKED pending committed-byte CI and maintainer authorization**

- Independent review identified nine mandatory findings, IR-01 through IR-09.
- Path containment, hostile JSON handling, artifact-integrity validation, example provenance, documentation, packaging metadata, and clean-build CI were remediated.
- Local verification passed 12/12 tests and validated the example's indexed evidence.
- The independent review report and candidate release notes were added as reviewable evidence.
- Python matrix and clean-package gates remain pending until GitHub Actions evaluates the committed remediation.

No release, publication, announcement, private-repository access, or sponsorship application is authorized by this entry.

