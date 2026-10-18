# Security policy

## Supported versions

Security fixes are provided for the latest tagged release and the default branch.

## Reporting a vulnerability

Do not open a public issue for suspected vulnerabilities. Use GitHub's private vulnerability reporting feature when enabled. If it is unavailable, contact the maintainer privately through the verified contact method on the maintainer's GitHub profile.

Include affected version, impact, minimal reproduction, and any suggested mitigation. Do not include real credentials, private datasets, or third-party personal data.

## Threat model

ARAP reads project-local JSON and hashes project-local files. Important risks include path traversal, untrusted evidence, forged gate status, secret inclusion, dependency confusion in downstream integrations, and treating agent-produced conclusions as independent review. ARAP rejects duplicate keys and oversized control JSON, rejects artifact and output paths outside the resolved project root, verifies indexed hashes and sizes, requires local gate evidence to be indexed, and never executes evidence files.

The `index` and `gate` write paths pin the project directory before evaluation.
POSIX writes walk directories through no-follow descriptors. Windows writes use
native directory handles, no-reparse relative opens, and replacement through a
held file handle; junctions in the output ancestor chain are rejected. A failed
protected operation returns an error rather than using an unprotected fallback.
CI tests Windows and Linux on Python 3.10–3.12, including junction/rename cases.

ARAP is not a sandbox for a hostile local process. Control-file reads and artifact
hashing still use paths and do not produce an immutable snapshot against concurrent
modification. Work from a checkout that other processes cannot modify when relying
on a gate decision. Declared gate statuses also require independent review of the
evidence; a PASS is not authentication of the person or tool that supplied them.

