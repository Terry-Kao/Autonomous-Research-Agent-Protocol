# ARAP OSS Qualification Sprint

Date: 2026-10-18. Maintainer-operated evidence; no external adoption is inferred.

## Release baseline

- PR #2 merge: cd080c754051f70532553586baaa145654a4cc2c
- GitHub pre-release: https://github.com/Terry-Kao/Autonomous-Research-Agent-Protocol/releases/tag/v0.1.0-alpha
- Post-merge CI: https://github.com/Terry-Kao/Autonomous-Research-Agent-Protocol/actions/runs/39054593527
- Python 3.10–3.12 tests, root/example hashes, clean sdist/wheel and isolated installations: PASS.

## Maintenance work

- v0.2 roadmap: issue #3
- Good first issue: #4 (documentation, good first issue)
- Future independent review entry: #5; no completed Claude/Gemini/human review claimed
- Description now identifies Python governance toolkit and alpha status; homepage links README; topics: agent-governance, python, reproducibility, research-automation.
- Maintainer-authored domain-neutral integration: examples/local-ci/run.py
- Application preparation checklist: docs/CODEX_FOR_OSS_EVIDENCE_CHECKLIST.md

## PR #6 and round-two review

- PR #6 merged as `5d27607746d5f4d9e40b064ee89e836675cef3fe`.
- Main post-merge CI run `39071122579` passed Python 3.10, 3.11 and 3.12 plus the clean packaging job.
- A fresh Claude Code review of that merge commit returned `REVISE` with three mandatory hostile-input/path-containment findings, recorded in issue #8 and `docs/ROUND_TWO_REVIEW.md`.
- Gemini's initial response was rejected as ungrounded; its corrected result is `UNSUPPORTED` because it could not retrieve the commit-pinned files. It is not counted as PASS evidence.
- The remediation gate is `PENDING` until exact-head CI and re-review complete.

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

Genuine external use and feedback remain unestablished. Automated round-two review is underway and is not external adoption. The repository page showed 0 stars and 0 forks on this date; these are a dated observation, not a permanent count. No PyPI download claim exists. Application materials may be drafted from current evidence, but acceptance and ecosystem importance are not established by engineering checks. Final submission needs Terry's separate authorization.
