# Round-two automated independent review

Date: 2026-10-18. Target: `5d27607746d5f4d9e40b064ee89e836675cef3fe`.

This is AI/automated review evidence. It is not a human approval, external usage, or adoption evidence.

## Claude Code

- Tool/model shown: Claude Code, Opus 5.5, medium reasoning.
- Environment: fresh cloud container and clean checkout of the public repository only.
- Actions: code inspection, hostile-input probes, Python 3.11/3.12 tests, clean wheel/sdist builds, metadata checks, and isolated installs.
- Verdict: **REVISE**.

Mandatory findings recorded in issue #8:

1. `ARAP-01`: an unhashable `PROJECT_STATE.status` could raise an uncaught `TypeError`.
2. `ARAP-02`: deeply nested control JSON could raise an uncaught `RecursionError`.
3. `ARAP-03`: `arap index` did not resolve its artifact-index output before writing, allowing an outside-root write through a symlinked index file or control directory.

Exact-head re-review confirmed those three reproductions fail closed after remediation, then found one remaining ARAP-02 write-path case: deeply nested JSON could raise during serialization after the destination was opened, truncating the existing index. The remediation now serializes successfully before opening the destination and returns a controlled error without altering the prior file.

The same review listed lower-severity hardening ideas. They are non-blocking backlog candidates and do not replace the three mandatory remediations.

## Gemini

- Tool/model shown: Gemini web app, Flash-Lite.
- Environment: fresh chat with only the public repository URL and exact target SHA.
- First response was rejected as ungrounded because it cited a nonexistent `requirements.txt` and missed README text that was already present.
- On correction, Gemini reported that it could not open any commit-pinned repository files and returned **UNSUPPORTED**.
- A clean public-only ZIP was prepared for a bounded retry, but the browser integration could not upload local files without changing Chrome extension permissions. No permission change was made.

Gemini produced no valid finding or approval. Its failed first response and explicit `UNSUPPORTED` correction are retained as limitations, not converted into PASS evidence.

## Remediation verification

- Remediation head: `c69b59610e5f4acd14a4dd77831b0239a5f3207d`.
- GitHub Actions run `39089728657`: Python 3.10/3.11/3.12 and package jobs all PASS.
- Claude Code exact-head re-review: ARAP-01, ARAP-02, ARAP-03 and the follow-up write-path case ARAP-13 all RESOLVED; unresolved mandatory findings: 0; verdict PASS.
- Claude independently ran 23 tests on each of Python 3.11, 3.12 and 3.13. Linux symlink tests ran without skips. Wheel/sdist builds, metadata checks and six isolated installs passed.
- Limitations: Claude did not test Python 3.10 or Windows junction/reparse behavior; GitHub CI provides the Python 3.10 run, while Windows junction coverage remains future hardening.

The bounded findings at `c69b59610e5f4acd14a4dd77831b0239a5f3207d` passed, but a later exact-head GitHub Codex review returned the overall round-two gate to `PENDING` for the follow-up below. Non-blocking hardening remains in issue #10.

## GitHub Codex exact-head follow-up

GitHub Codex reviewed `c69b59610e5f4acd14a4dd77831b0239a5f3207d` and opened two P2 findings before merge. The gate returned to `PENDING` while they were addressed:

1. the deep-write regression depended on an interpreter-specific recursion threshold and failed on Python 3.14.4;
2. the artifact-index output path could be exchanged for an outside-root parent symlink after its initial resolution and before the write.

The regression now injects `RecursionError` deterministically. On POSIX, contained JSON writes use a no-follow directory descriptor, create and fsync a temporary file relative to that held descriptor, and replace the destination relative to the same descriptor. A hostile test exchanges `control/` during artifact hashing and verifies that the outside index remains unchanged. Windows retains the serialize-before-open behavior; Windows junction/reparse race hardening remains an explicit platform limitation.

Final PASS requires exact-head CI and a fresh exact-head automated review with no unresolved mandatory finding.

Claude Code (Opus 5.5, medium reasoning) then re-reviewed `f3cc6c5eef665bb722ffdac43d2217b635afe0f6` from a new clean public clone. It ran all 24 tests without skips on Python 3.10–3.14, performed targeted race/failure probes, built and checked both distributions, and completed ten isolated installs. Its final verdict was PASS with no mandatory findings. It identified one analogous non-blocking gate-output parent race (ARAP-14), a file-mode change, and documentation drift; all three were corrected before the final gate decision.

GitHub Codex exact-head reviews then exercised narrower concurrent swaps. The POSIX implementation now pins the original project root before hashing or gate evaluation, traverses every output ancestor relative to that descriptor without following symlinks, syncs both the file and directory, and closes the held descriptor even when cleanup fails. Regression tests cover root replacement, final-parent replacement, intermediate-ancestor replacement, and both index and gate output paths. Equivalent Windows descriptor-relative semantics are not available in this implementation; Windows concurrent junction/reparse races remain explicitly unsupported and tracked as non-blocking hardening rather than being represented as tested.

## Windows remediation and review availability

The preceding Windows exception was not accepted as a completed security fix.
Terry explicitly chose preserving Windows functionality with native protection.
The new implementation pins directories with native handles that deny delete
sharing, rejects junction/reparse directories, and holds every ancestor through
the write. It serializes and fsyncs a temporary file, then renames it relative to
the held destination-directory handle. Local Windows tests verify blocked root
renames, blocked held-parent renames, and rejection of exchanged junctions at
both a direct and an intermediate output ancestor. CI now includes Windows and
Linux on Python 3.10–3.12. This implementation remains pending independent review.

The GitHub Codex review request for `0f7ed588114807e84a202d265206911015121802`
failed because the account code-review quota was exhausted (PR comment
6244954486). It is not a passing review. Claude's initial review began in fresh
model context; subsequent re-reviews used new clean public checkouts within the
same conversation, a limitation retained explicitly.
