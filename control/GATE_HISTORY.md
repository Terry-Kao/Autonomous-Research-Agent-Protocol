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

## 2026-10-18 — Post-authorization remediation verification

**Decision: PASS for merge and the bounded GitHub pre-release**

- Verified remediation commit: `8f0b9e0489e5fcc3811370968f2322362b8f4124`.
- GitHub Actions run `39054314202` completed successfully.
- Python 3.10, 3.11, and 3.12 passed 17 tests plus repository-level and example validation.
- The packaging job built and checked sdist/wheel artifacts, installed both in isolated environments, and exercised the installed CLI.
- All seven GitHub Codex findings are remediated; the repository has no unresolved mandatory technical finding.

The remaining authorized sequence is final-head CI confirmation, merge, post-merge verification on `main`, and creation of the `v0.1.0-alpha` GitHub pre-release. PyPI publication, broad promotion, private-repository access, fabricated adoption evidence, and Codex for OSS submission remain excluded.

## 2026-10-18 — Alpha release and qualification sprint

- PR #2 merged as cd080c754051f70532553586baaa145654a4cc2c after CI 39054427964 passed and seven review threads were resolved with remediation evidence.
- Post-merge CI 39054593527 passed all four jobs, including clean build/install and root/example hashes.
- Tag v0.1.0-alpha points to that merge commit; GitHub pre-release was published with alpha limitations and no adoption claim.
- Qualification roadmap, contributor task and review entry issues #3–#5 were opened. Fresh-environment validation and a domain-neutral integration are documented in docs/QUALIFICATION_SPRINT.md.

Release gates PASS applies to the alpha release. It does not assert OSS program eligibility or authorize application submission.

## 2026-10-18 — Qualification merge and round-two automated review

**Decision: REVISE pending mandatory remediation and exact-head re-review**

- PR #6 merged as `5d27607746d5f4d9e40b064ee89e836675cef3fe` after an expected-head check; main CI run `39071122579` passed all four jobs.
- Fresh local verification independently passed 17 tests, repository/example hash validation, the synthetic local-CI handoff, clean wheel/sdist builds, metadata checks, and isolated installs.
- Claude Code (Opus 5.5, medium reasoning) reviewed a clean public checkout in a fresh cloud container and found three mandatory defects: hostile state shape crash, deeply nested JSON crash, and artifact-index write escape through an outside-root symlink.
- Gemini Flash-Lite could not access the commit-pinned files. Its initial ungrounded response was rejected and its corrected result is `UNSUPPORTED`, not PASS.
- Issue #8 records the mandatory findings. Remediation is bounded to code, regression tests, exact-head CI and re-review.
- Exact-head re-review confirmed the initial three reproductions fail closed, then exposed a remaining deep-JSON serialization path that could truncate an existing index before raising. The same bounded remediation now serializes before opening the destination and preserves the previous file on failure.

No private repository was accessed. This entry does not authorize PyPI, broad promotion, fabricated adoption, or a Codex for OSS submission.

