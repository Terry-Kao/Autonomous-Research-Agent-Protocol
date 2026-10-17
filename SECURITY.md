# Security policy

## Supported versions

Security fixes are provided for the latest tagged release and the default branch.

## Reporting a vulnerability

Do not open a public issue for suspected vulnerabilities. Use GitHub's private vulnerability reporting feature when enabled. If it is unavailable, contact the maintainer privately through the verified contact method on the maintainer's GitHub profile.

Include affected version, impact, minimal reproduction, and any suggested mitigation. Do not include real credentials, private datasets, or third-party personal data.

## Threat model

ARAP reads project-local JSON and hashes project-local files. Important risks include path traversal, untrusted evidence, forged gate status, secret inclusion, dependency confusion in downstream integrations, and treating agent-produced conclusions as independent review. ARAP rejects duplicate keys and oversized control JSON, rejects artifact and output paths outside the resolved project root, verifies indexed hashes and sizes, requires local gate evidence to be indexed, and never executes evidence files.

