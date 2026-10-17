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

## 2026-10-18 — Remediation verification

**Decision: BLOCKED only on maintainer release authorization**

- Reviewed remediation commit: `c0d4deb60e68d8ff3afde583d467efa9253c145f`.
- GitHub Actions run `39053395906` passed the Python 3.10–3.12 matrix and the clean packaging job.
- The packaging job built sdist and wheel, passed metadata checks, installed each artifact in an isolated environment, and exercised the installed CLI.
- All independent-review findings IR-01 through IR-09 are resolved with no open mandatory technical finding.
- `maintainer-release-authorization` remains `PENDING` by design.

The sole authorized next action is to request Terry's explicit release authorization. This entry does not itself authorize release or publication.

## 2026-10-18 — Maintainer release authorization

**Decision: PASS for the bounded GitHub alpha release**

- Terry explicitly authorized updating `maintainer-release-authorization` to `PASS`, merging PR #2, verifying the resulting `main`, and creating the `v0.1.0-alpha` GitHub pre-release.
- Before this entry, PR #2 remained at head `050d67eacbb38e9307da02b69d2627d79a945202`, was non-draft and mergeable, and Actions run `39053508899` completed successfully for that exact head.
- No GitHub review submission or unresolved inline review thread existed. The optional GitHub Codex summary still displayed its earlier `running` state and is not represented as an approval or as a frozen mandatory gate.
- Independent review findings IR-01 through IR-09 remain resolved; no new mandatory finding was present at authorization time.
- Authorization evidence and exact exclusions are recorded in `docs/MAINTAINER_RELEASE_AUTHORIZATION.md`.
- Pre-merge Windows verification then exposed two evidence defects: repository-level artifact hashes had been generated from CRLF working-tree bytes rather than committed LF bytes, and the README still showed the removed `arap index --output` option. Both were corrected before merge; CI now validates the repository-level contract so committed-byte drift fails closed.

This authorization is limited to a GitHub pre-release and the public qualification sprint. It does not authorize PyPI publication, broad promotion, fabricated adoption evidence, private-repository access, or submission of a Codex for OSS application.

## 2026-10-18 — Post-authorization GitHub Codex review

**Decision: BLOCKED pending exact-head remediation CI**

- The previously running GitHub Codex review completed and opened seven findings, GCR-01 through GCR-07.
- GCR-01 and GCR-03 were already corrected by authorization commit `525bce58589437d99ad0e4fef08b1e88a7c4dcb7`.
- The remaining findings were remediated with targeted tests for hostile nested types, non-HTTPS evidence, path-resolution loops, and runtime version consistency; the packaging backend floor was raised to setuptools 77.
- The `post-authorization-review-remediation` gate remains `PENDING` until GitHub Actions succeeds for the exact remediation head.

No merge or release is authorized while this gate is pending.

