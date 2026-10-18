# ARAP public alpha introduction

Publication date: 2026-10-18  
Version: `v0.1.0-alpha`  
Baseline target: `5d6541bcecf58d0576785db388af5fad81b726a9`

Autonomous Research Agent Protocol (ARAP) is a small, dependency-free Python
governance toolkit for making agent-run research state, gates, evidence hashes,
review provenance, and authorized next actions inspectable.

This is an alpha evaluation release, not a claim that ARAP is production-ready.
The CLI validates declared protocol evidence; it does not run research code,
establish scientific truth, merge changes, or upload data.

## What to try

Use Python 3.10 or newer in a clean environment and follow the README quick
start. Useful reports include:

1. clean editable installation on Windows or Linux;
2. README onboarding and expected CLI exit codes;
3. validation and gating of the included minimal project;
4. a small, domain-neutral integration with an existing agent or research
   workflow; and
5. a bounded issue or pull request, including the first-contribution task in
   Issue #4.

Include the tag or commit, operating system, Python version, commands, expected
result, actual result, and a sanitized reproduction. Do not include private data,
credentials, model weights, unpublished findings, or proprietary prompts.

## Where to respond

- General feedback and reproducible reports: Issue #5.
- First contribution: Issue #4, reserved for an external contributor.
- Security reports: follow SECURITY.md, not a public issue or discussion.
- Pull requests: follow CONTRIBUTING.md and keep changes bounded.

Verified external evidence is recorded in EXTERNAL_FEEDBACK_LOG.md. Stars and
forks may be observed but are never counted as adoption without a verifiable
issue, pull request, comment, discussion, or integration report.

## Known limitations

- The schemas and CLI contract may change before a stable release.
- Windows path-based input reads and snapshots do not provide the same
  descriptor-relative race resistance as protected output writes; see
  SECURITY.md for the precise boundary.
- Gemini review was unsupported in the qualification round, and the final GitHub
  Codex re-review was unavailable because of quota. Neither is reported as PASS.
- Claude Code returned a bounded automated PASS with zero mandatory findings.
  That is AI review, not human review or external adoption.
- No PyPI package has been published, no Codex for OSS application has been
  submitted, and no OpenAI endorsement is claimed.

At publication time, an external account had opened PR #7 for Issue #4 and
identified the work as AI-assisted. It is recorded as a verifiable external
contributor interaction, not as independent human review, and remains subject to
normal CI and maintainer review.
