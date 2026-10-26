# External feedback log

This log records only public, verifiable evidence. Maintainer actions and AI/bot
reviews are separated from external contributor activity. A star, fork, view, or
download count alone does not establish human use or adoption.

## Evidence rules

An entry must link to a public issue, pull request, discussion/comment, or
integration report and identify the actor, date, target version/commit when
known, evidence type, AI-assistance disclosure when known, and disposition.
External means the actor is not the maintainer account `Terry-Kao` and is not an
automation account controlled for this project. Account identity alone does not
prove offline identity; claims are limited to the observable GitHub evidence.

## Verified external evidence

| Date | Actor | Evidence | AI/bot classification | Status | Adoption interpretation |
| --- | --- | --- | --- | --- | --- |
| 2026-10-27 | `yuefdev` | [PR #7](https://github.com/Terry-Kao/Autonomous-Research-Agent-Protocol/pull/7), completing [Issue #4](https://github.com/Terry-Kao/Autonomous-Research-Agent-Protocol/issues/4) | Contributor disclosed AI-assisted follow-up using OpenCode (`gpt-6.1-sol`) | Merged as `e91049cd24108551fbcc1ce1cedeb6b09384f65b` after exact-head CI `39951080937`, maintainer review `5660329017`, and main CI `40418261921` passed; Issue #4 closed | Verifiable external contributor lifecycle completed; not independent human review and not proof of real-world adoption |

## Public introduction locations

| Date | Location | Actor | Purpose |
| --- | --- | --- | --- |
| 2026-10-18 | [GitHub Discussion #13](https://github.com/Terry-Kao/Autonomous-Research-Agent-Protocol/discussions/13) | `Terry-Kao` | Bounded public alpha introduction and reproducible feedback request |

No off-GitHub post was made in this round. Hacker News required a login and the
available Reddit account could not post. No login, account creation, policy
bypass, or substitute account was attempted.

## Automated review evidence (excluded from human adoption)

| System | Result | Interpretation |
| --- | --- | --- |
| Claude Code | Bounded PASS; mandatory findings 0 | Automated review only |
| Gemini | UNSUPPORTED | No PASS inferred |
| GitHub Codex final re-review | Unavailable because of quota | No PASS inferred |

## Public counters

The latest maintainer observation before this introduction was 0 stars, 1 fork,
and 0 subscribers. These counters are context only, are not targets, and are not
counted as adoption without linked evidence.

## Current conclusion

PR #7 completed a public, verifiable external contributor lifecycle: reserved
Issue #4, external fork and PR, maintainer feedback, contributor revision,
exact-head CI, bounded maintainer review, merge, post-merge CI, and issue closure.
The contribution was AI-assisted and is not independent human review. A verified
real-world integration remains unestablished. Codex for OSS application
preparation may use this log as evidence, but submission remains a separate
maintainer decision.
