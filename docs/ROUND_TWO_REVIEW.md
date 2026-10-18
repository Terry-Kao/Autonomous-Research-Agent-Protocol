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

## Remediation gate

The round-two remediation gate stays `PENDING` until the fixes and regression tests pass exact-head CI and an exact-head re-review finds no unresolved mandatory issue.
