# ARAP OSS Qualification Sprint

Date: 2026-10-18. Maintainer-operated evidence; no external adoption is inferred.

## Current completion state

- PR #6 merged as `5d27607746d5f4d9e40b064ee89e836675cef3fe`; main CI `39071122579` passed.
- Security remediation PR #9 merged as `74b7bd0ace6d55046a362ffd7388b63ff6baeddb`; [main push CI 39108181654](https://github.com/Terry-Kao/Autonomous-Research-Agent-Protocol/actions/runs/39108181654) passed all seven jobs (Windows/Linux Python 3.10–3.12 and packaging).
- Main verification: tests, root/example hashes, local-CI integration, clean wheel/sdist build, metadata checks and isolated installs PASS. Additional Windows local verification at that merge: 28 passed, 9 platform/privilege skips; all seven native Windows regressions passed.
- Round-two mandatory remediation and Claude review complete. Gemini remains UNSUPPORTED; GitHub Codex final review was unavailable due quota. No passing result is fabricated for either.
- Issue #8 closed by PR #9. #5 remains the public feedback entry; #3/#10 retain non-blocking roadmap items. #4 remains open for an external contributor.
- Public GitHub API observation on 2026-10-18: 0 stars, 1 fork, 0 subscribers. A fork alone does not establish real usage; confirmed external human feedback/adoption remains 0 / unestablished.
- Next Human Gate: Terry's formal public introduction/outreach. PyPI publication and Codex for OSS submission remain separately unauthorized.

The dated sections below preserve the sprint history; this section states the current completion state.

## Release baseline

- PR #2 merge: cd080c754051f70532553586baaa145654a4cc2c
- GitHub pre-release: https://github.com/Terry-Kao/Autonomous-Research-Agent-Protocol/releases/tag/v0.1.0-alpha
- Post-merge CI: https://github.com/Terry-Kao/Autonomous-Research-Agent-Protocol/actions/runs/39054593527
- Python 3.10–3.12 tests, root/example hashes, clean sdist/wheel and isolated installations: PASS.

## Maintenance work

- v0.2 roadmap: issue #3
- Good first issue: #4 (documentation, good first issue)
- Independent review entry: #5; completed Claude automated reviews, Gemini UNSUPPORTED, no external human review claimed
- Description now identifies Python governance toolkit and alpha status; homepage links README; topics: agent-governance, python, reproducibility, research-automation.
- Maintainer-authored domain-neutral integration: examples/local-ci/run.py
- Application preparation checklist: docs/CODEX_FOR_OSS_EVIDENCE_CHECKLIST.md

## PR #6 and round-two review

- PR #6 merged as `5d27607746d5f4d9e40b064ee89e836675cef3fe`.
- Main post-merge CI run `39071122579` passed Python 3.10, 3.11 and 3.12 plus the clean packaging job.
- A fresh Claude Code review of that merge commit returned `REVISE` with three mandatory hostile-input/path-containment findings, recorded in issue #8 and `docs/ROUND_TWO_REVIEW.md`.
- Gemini's initial response was rejected as ungrounded; its corrected result is `UNSUPPORTED` because it could not retrieve the commit-pinned files. It is not counted as PASS evidence.
- Mandatory remediation passed exact-head CI run `39089728657`; Claude's exact-head re-review found zero unresolved mandatory findings and returned PASS. Non-blocking hardening is tracked in issue #10.
- GitHub Codex then found two P2 follow-ups at `c69b59610e5f4acd14a4dd77831b0239a5f3207d`: a Python 3.14-sensitive test and a parent-symlink swap during index writing. The deterministic test and no-follow directory-descriptor remediation passed CI run `39090252768` at `f3cc6c5eef665bb722ffdac43d2217b635afe0f6`.
- Claude Code independently re-reviewed that head from a clean public clone: 24 tests on each Python 3.10–3.14, targeted race probes, clean build/check, ten isolated installs, zero mandatory findings, final verdict PASS. Its analogous non-blocking gate-output race, file-mode note and documentation drift were corrected before the final gate decision.
- Later GitHub Codex exact-head probes required stronger POSIX race containment: the original root is now pinned before long-running work, every output ancestor is traversed descriptor-relatively without following symlinks, directory metadata is synced, and cleanup cannot leak the held descriptor. Windows concurrent junction/reparse protection remains an explicit unsupported limitation and backlog item; ordinary Windows behavior remains covered by the hosted Python matrix only where CI provides it.

## Fresh-environment README usability validation

Windows, Python 3.11, new virtual environment without system site-packages. Installed with `python -m pip install -e .`; distribution version 0.1.0a1.

Initial sandbox network resolution failed while downloading setuptools. Retried with authorized network access; installation succeeded. This environmental failure is retained here and was not counted as a package defect.

Usability findings: README assumed an evidence/result.json file that init does not produce, did not explain expected BLOCKED exit status, and left users in the newly initialized directory before referring to repository examples. Documentation now explains the file prerequisite, expected exit code 2 and return to repository root.

Observed after correction:

| Check | Result |
|---|---|
| Fresh editable install | PASS |
| init in new directory | PASS |
| validate new project | VALID |
| gate new project | BLOCKED, exit 2 (expected) |
| synthetic local CI integration | PASS; one artifact indexed; missing reviews BLOCKED |
| included minimal project validation | VALID |
| regression suite | 17 passed |

This is automated maintainer usability validation, not a real external user's testimonial. CI repeats installation and the synthetic integration on clean hosted runners.

## Remaining evidence

Windows native remediation supersedes the earlier unsupported/non-blocking
classification: Terry requested preserved Windows functionality with native
handle protection. New junction/handle regressions and Windows CI were added;
the overall remediation remains pending review. GitHub Codex review for
`0f7ed588114807e84a202d265206911015121802` failed due quota and is not PASS.

Final reviewed code `4d294aca886c8428793335a5c1465c2af1fadd6c` passed seven CI jobs in run `39107670200` and Claude Code (serving Opus 4.8) returned bounded PASS, mandatory findings 0. Windows native runtime tests passed on real Windows CI; Claude independently ran Linux and performed static Windows FFI review. See `docs/ROUND_TWO_REVIEW.md` for commands and limitations. The GitHub Codex final re-review failed due account quota; Gemini remains UNSUPPORTED.

Genuine external use and feedback remain unestablished. Completed automated review is not external adoption. The earlier repository observation was 0 stars and 0 forks; it is a dated observation, not a permanent count. No PyPI download claim exists. CONTRIBUTING.md now provides a public feedback format and keeps issue #4 available for an external contributor. Formal public introduction/outreach is the next Human Gate. Application materials may be drafted from current evidence, but acceptance and ecosystem importance are not established by engineering checks. Final submission needs Terry's separate authorization.
