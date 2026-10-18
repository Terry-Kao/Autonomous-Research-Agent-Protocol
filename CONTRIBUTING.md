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

