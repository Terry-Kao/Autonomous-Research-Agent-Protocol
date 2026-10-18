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

## 2026-10-18 — Round-two remediation verification

**Decision: PASS for the bounded mandatory remediation**

- Remediation head `c69b59610e5f4acd14a4dd77831b0239a5f3207d` passed GitHub Actions run `39089728657`: Python 3.10, 3.11, 3.12 and package jobs.
- Claude Code exact-head re-review independently ran 23 tests on Python 3.11, 3.12 and 3.13, exercised both Linux symlink tests without skips, rebuilt and checked wheel/sdist artifacts, and completed six isolated installs.
- ARAP-01, ARAP-02, ARAP-03 and follow-up ARAP-13 are RESOLVED; unresolved mandatory findings: 0; Claude verdict: PASS.
- The earlier GitHub Codex Python 3.12 portability finding was corrected, verified by two successful CI heads, documented in the review thread, and resolved.
- Non-blocking hardening remains visible in issue #10. Gemini remains `UNSUPPORTED`, not PASS.

This gate does not claim human review, external adoption, program eligibility, or permission to publish to PyPI, promote broadly, or submit a Codex for OSS application.

## 2026-10-18 — GitHub Codex exact-head follow-up

**Decision: REVISE pending final exact-head CI and review**

- GitHub Codex reviewed `c69b59610e5f4acd14a4dd77831b0239a5f3207d` and opened two P2 findings: a Python 3.14-dependent deep-write test and a reproduced parent-symlink swap during artifact hashing.
- The test now injects the serialization failure deterministically.
- POSIX contained writes now create, fsync and replace the index relative to a securely held no-follow directory descriptor; a hostile regression exchanges `control/` during hashing and verifies that the outside sentinel is unchanged.
- Windows retains serialize-before-open protection. Windows junction/reparse race hardening remains a stated limitation and is not represented as tested.

The round-two gate is PENDING until the changed head passes the complete CI matrix and exact-head automated re-review.

- First remediation CI run `39090194783` preserved a useful failed attempt: packaging passed, while all Python jobs exposed an overly narrow regression assertion that expected only `OSError`; the implementation safely rejected the exchanged parent with `ValueError` before opening it. The test now accepts either fail-closed error and still requires the outside sentinel to remain unchanged.
- Corrected exact head `f3cc6c5eef665bb722ffdac43d2217b635afe0f6` passed CI run `39090252768` across Python 3.10–3.12 and packaging.
- Claude Code (Opus 5.5, medium reasoning) re-reviewed that exact head from a clean public clone, ran 24 tests without skips on each Python 3.10–3.14, targeted race and injected-failure probes, clean build/check, and ten isolated installs. Verdict: PASS; mandatory findings: 0.
- Claude's analogous non-blocking ARAP-14 gate-output race was corrected by applying the same contained write. The atomic file mode now follows the process umask, and the review documents were reconciled. Final exact-head CI and automated review remain required before PASS.
- GitHub Codex subsequently reproduced root replacement and intermediate-ancestor replacement windows, plus cleanup and crash-durability gaps. POSIX writes now pin the original project root before hashing/evaluation, traverse each ancestor relative to held no-follow descriptors, sync the destination directory after replace, and close descriptors even if cleanup fails. New adversarial tests cover both index and gate output paths.
- Windows does not use descriptor-relative traversal in this version. Concurrent junction/reparse mutation remains explicitly unsupported and must not be inferred from the ordinary Windows test result; it is retained as non-blocking platform hardening in issue #10.
- CI run `39091099924` retained another useful failed attempt: packaging passed, while two Linux race tests accepted only successful writes to the pinned original directory. The implementation instead rejected the mutations safely with `ENOTDIR` and `ENOENT`; both outside sentinels remained unchanged. The assertions now allow either safe rejection or a write through the held original descriptor.
- Claude's final mutation probes found two non-blocking regressions in the root-pinning refactor: a path-based pre-write `mkdir` could create empty directories after a root swap, and an internal symlink at `ARTIFACT_INDEX.json` could redirect the destination filename. The secure path now creates directories only through held descriptors and uses the validated relative destination name; dedicated regressions cover both cases.
- GitHub Codex exact-head review of `93af14a5adc24c93dfc161e898ff7876c52ea999` found three more P2 edge cases: newly created ancestor entries were not individually synced, a root symlink loop raised an uncontrolled `RuntimeError`, and the non-POSIX fallback still followed an internal index symlink. Parent descriptors are now synced after each `mkdir`, root resolution loops become controlled CLI errors, and the fallback replaces the validated relative index destination without modifying its target.
- The review request for `0f7ed588114807e84a202d265206911015121802` failed due account review quota; CI `39091884944` passed. The review failure is preserved, not treated as PASS.
- Terry chose native Windows protection while preserving functionality. Windows writes now use directory handles that deny deletion/rename, reject reparse directories, hold the ancestor chain, and rename the synced temporary file relative to the held parent handle. Local Windows verification: 25 passed, 9 skipped (POSIX or unavailable symlink privileges); the four native handle/junction tests passed. Initial implementation attempts with zero desired access and incompatible rename sharing failed and were corrected before push.
- The test workflow now covers Windows and Linux with Python 3.10–3.12. Round-two gate remains PENDING until CI and independent review verify this new code.
- Windows/Linux CI `39107487909` passed all seven jobs at `2bbc6189055c3d2aa4540face29c5d9ccb066565`. Further review of narrow Windows windows replaced path-based child opens with `NtCreateFile` relative to held directory handles, using no-reparse semantics. A single exclusive temporary-file handle is retained through write, flush and rename, eliminating the close/reopen window. Empty-directory in-place reparse and injected rename-failure tests were added. Local result: 28 passed, 9 skipped, including seven native Windows tests.
- Claude's review of `0f7ed58` returned REVISE for ARAP-17, an overbroad security claim. SECURITY.md now describes protected output writes and explicitly discloses path-based read/snapshot limitations. Native Windows implementation review remains pending; the browser reported a model switch from Opus 5.5 to Opus 4.8, which must be recorded in subsequent review identity.

## 2026-10-18 — Final round-two decision

**Decision: PASS for bounded remediation; pending final evidence-commit CI and merge**

- Reviewed code SHA `4d294aca886c8428793335a5c1465c2af1fadd6c` passed CI `39107670200`, all seven Windows/Linux matrix and packaging jobs.
- Claude Code, serving `claude-opus-4-8` (medium), independently returned bounded PASS, mandatory 0, from a new clean public checkout. Linux runtime probes/tests/build/install passed; Windows assessment was static, with Windows runtime evidence supplied by local and hosted tests.
- All GitHub inline threads contain remediation evidence and are resolved. Final GitHub Codex re-review failed due quota; it is preserved as unavailable, not a pass. Gemini remains UNSUPPORTED.
- Non-blocking work remains in #10. CONTRIBUTING provides public feedback instructions. Genuine external adoption remains unestablished; issue #4 remains reserved for an external contributor.
- The next Human Gate is formal public introduction/outreach. No PyPI publication, OSS application or broad promotion is authorized by this PASS.

## 2026-10-18 — Post-merge verification completed

**Decision: PASS; await public-introduction Human Gate**

- PR #9 merged as `74b7bd0ace6d55046a362ffd7388b63ff6baeddb` under expected-head lease `a843c6db060dd74b533c3801dc175fbb007dfa5c` after its CI `39108054249` and Claude evidence verification passed; unresolved review threads: 0.
- Main push CI `39108181654` passed every step in all seven jobs. Additional local Windows execution at the merge passed tests, root/example validation, local-CI, clean build/twine, and two new isolated wheel/sdist installs. Tracked working files remained unchanged.
- Issue #8 is closed; #5 retains detailed public evidence and feedback instructions, #4 remains open, and #10 records remaining hardening.
- Public counters were 0 stars / 1 fork / 0 subscribers. Confirmed human usage/adoption remains unestablished. No private/PFM data accessed; no PyPI, application submission or broad promotion performed.

## 2026-10-18 — Formal public introduction authorized

**Decision: PASS for bounded public introduction and feedback collection**

- Terry explicitly authorized a limited, non-spam public introduction for
  `v0.1.0-alpha` at baseline `5d6541bcecf58d0576785db388af5fad81b726a9`.
- README and CONTRIBUTING provide clear try, feedback, integration-report, and
  first-contribution entry points. PUBLIC_INTRODUCTION.md states the alpha scope,
  limitations, review provenance, and prohibited claims.
- EXTERNAL_FEEDBACK_LOG.md separates verifiable external contributor evidence
  from AI/bot review and public counters.
- External account `yuefdev` opened PR #7 for reserved Issue #4 and disclosed the
  contribution as AI-assisted. This is a verifiable external contributor PR,
  not independent human review; merge and integration remain pending CI and
  normal maintainer review.

This gate does not authorize PyPI publication, a Codex for OSS submission,
claims of OpenAI endorsement, broad promotion, or access to private/PFM content.

