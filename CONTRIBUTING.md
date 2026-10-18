# Contributing

Thank you for improving ARAP.

1. Open or claim a bounded issue before substantial work.
2. Create a focused branch and include tests for behavior changes.
3. Run `python -m pytest` and `python -m arap.cli validate examples/minimal-project`.
4. Keep examples domain-neutral and free of private data, credentials, unpublished research, and model weights.
5. In the pull request, list changed contracts, evidence produced, and known limitations.

Maintainers evaluate contributions on correctness, scope, auditability, backward compatibility, and security. A passing test suite does not override a failed mandatory review gate.

By participating, you agree to follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Public feedback

For non-security feedback, open an issue with the commit/tag, operating system,
Python version, commands you tried, expected result, and actual result. A small
domain-neutral reproduction helps us verify onboarding and integration problems.
Do not include private data or credentials. Follow SECURITY.md for vulnerabilities.
Tell us whether feedback comes from a human, an AI tool, or an automated test;
automated review does not count as external human adoption.

Issue #4 is reserved as a first contribution opportunity. Maintainer-operated
examples and tests are documented as such. Public outreach and application
submission remain separate maintainer decisions.

### Choose the right entry point

- **Clean install or README usability:** open a public issue with exact commands
  and enough environment information to reproduce the result.
- **Integration result:** state what workflow you integrated, the target ARAP
  tag/commit, which gates and evidence were used, and the observed result. A
  sanitized minimal example is preferred.
- **Code or documentation contribution:** comment on or claim a bounded issue,
  then open a focused pull request. Issue #4 is the current first-contribution
  task and is intentionally reserved for an external contributor.
- **Security concern:** follow SECURITY.md and do not disclose sensitive details
  in a public issue, pull request, or discussion.

Please identify whether a report was authored by a human, AI-assisted, generated
by an automated test, or produced entirely by an AI/bot. AI assistance is
welcome, but it is recorded separately and is not treated as independent human
review. Maintainers verify external evidence in
[EXTERNAL_FEEDBACK_LOG.md](EXTERNAL_FEEDBACK_LOG.md).

