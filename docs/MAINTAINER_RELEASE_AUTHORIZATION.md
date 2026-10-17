# Maintainer release authorization: v0.1.0-alpha

Authorizer: Terry Kao, repository owner and maintainer

Authorization date: 2026-10-18 (Asia/Taipei)

Authorized release: GitHub pre-release `v0.1.0-alpha`

## Authorized actions

- Set the mandatory `maintainer-release-authorization` gate to `PASS`.
- Merge PR #2 only after confirming its head has not drifted, its CI remains successful, and no new unresolved mandatory finding exists.
- Perform post-merge tests, domain-neutral example validation, artifact/hash validation, and clean sdist/wheel build and isolated-install checks on `main`.
- Create tag and GitHub pre-release `v0.1.0-alpha` with accurate limitations and governance evidence.
- Begin the public ARAP OSS Qualification Sprint through honest repository maintenance, documentation, examples, issues, metadata, and a future independent-review entry point.

## Explicit exclusions

This authorization does not permit:

- publishing to PyPI or another package index;
- broad public promotion;
- submitting a Codex for OSS application;
- inventing stars, forks, users, issues, reviews, pull requests, integrations, or adoption evidence;
- reading, modifying, importing, or publishing content from any private research repository;
- changing the public API, license, or project positioning beyond the reviewed alpha scope without a new maintainer decision.

## Evidence at authorization time

- PR #2 head: `050d67eacbb38e9307da02b69d2627d79a945202`
- Head CI: GitHub Actions run `39053508899`, conclusion `success`
- PR state: open, non-draft, mergeable
- Independent review: technical `PASS`; IR-01 through IR-09 resolved
- GitHub review threads: none unresolved
- External adoption claim: none

This file is the repository-visible maintainer attestation for the bounded release action. It is not evidence of external review or adoption.
