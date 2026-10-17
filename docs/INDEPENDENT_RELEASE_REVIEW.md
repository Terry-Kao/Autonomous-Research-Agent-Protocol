# Independent release review: v0.1.0-alpha

Review target: PR #2, `issue-1/release-readiness`

Reviewer: OpenAI Codex, acting independently from the bootstrap implementation

Review date: 2026-10-18

Scope authority: GitHub `main`, Issue #1, PR #2, and the committed public repository bytes only

## Verdict

**PASS for technical release readiness after remediation, subject only to explicit maintainer release authorization.**

This verdict does not authorize a GitHub Release, package publication, announcement, or Codex for OSS application. It makes no claim of external adoption or scientific validity.

## Mandatory findings and disposition

| ID | Finding | Resolution | Verification |
|---|---|---|---|
| IR-01 | Untrusted, valid JSON with unexpected top-level or nested types could raise exceptions instead of producing validation errors. Duplicate keys were accepted. | Added bounded JSON loading, duplicate-key rejection, and explicit shape/type validation. | Adversarial unit tests in `tests/test_core.py`. |
| IR-02 | Gate evaluation trusted local evidence paths and artifact metadata without verifying committed file existence, size, or SHA-256. | Validation now checks path containment, file existence, size, SHA-256, unique artifact paths, and requires every local gate-evidence path to be indexed. | Tamper and unindexed-evidence tests plus repository/example validation. |
| IR-03 | Gate output could be directed outside the governed project. | Gate output is resolved through the same project-boundary check as artifacts. | Output-escape unit test. |
| IR-04 | The example declared evidence-backed PASS while its artifact index was empty. | Indexed both example evidence files and validated their current bytes. | `arap validate examples/minimal-project`. |
| IR-05 | README claimed the gate example did not modify the project, although it refreshes the derived decision. | Corrected the user-visible contract. | Documentation review. |
| IR-06 | CI did not build or install distribution artifacts on a clean runner. | Added a packaging job that builds sdist/wheel, runs `twine check`, installs each artifact in a fresh virtual environment, and exercises the installed CLI. | GitHub Actions packaging job for the reviewed commit. |
| IR-07 | Packaging metadata used a legacy license table/classifier combination and omitted canonical project URLs. | Added SPDX license metadata and license-file declaration, removed the superseded license classifier, and added canonical URLs. | Clean build and metadata check in CI. |
| IR-08 | Text line-ending conversion made some artifact hashes differ between Linux and Windows checkouts. | Disabled Git text conversion through `.gitattributes` so each checkout preserves the exact committed blob bytes, then rebuilt the indexes. | Repository validation on Windows and Linux CI checkouts. |
| IR-09 | Distribution version `0.1.0` represented a stable PEP 440 release although the public target is an alpha. | Changed package metadata to the PEP 440 prerelease version `0.1.0a1`; candidate docs retain the human-facing `v0.1.0-alpha` label. | Wheel/sdist metadata check in CI. |

## Boundary review

- Repository content is domain-neutral and contains no private datasets, unpublished research findings, model weights, credentials, or private-repository references.
- The CLI reads JSON and hashes files; it does not execute evidence, research code, network requests, merges, or releases.
- External HTTPS evidence references are identifiers, not content-addressed local artifacts. Their availability and truth require separate review.
- A gate status is still a reviewed declaration; ARAP verifies the local evidence binding and decision mechanics, not the underlying domain truth.

## Reproducibility statement

CI verifies source checkout -> sdist/wheel build -> metadata check -> isolated installation -> installed CLI execution on a clean GitHub-hosted runner. This establishes clean functional reproducibility, not byte-for-byte reproducible archives across arbitrary build hosts.

## Evidence required for closure

- Python 3.10, 3.11, and 3.12 test/example jobs PASS.
- Clean packaging job PASS.
- The reviewed commit and successful workflow run are recorded in the control plane.
- All indexed local evidence hashes validate from committed bytes.

The maintainer-release-authorization gate intentionally remains `PENDING` until Terry explicitly authorizes release creation or publication.

## Closure evidence

- Remediation commit: `c0d4deb60e68d8ff3afde583d467efa9253c145f`
- Successful GitHub Actions run: `39053395906`
- Result: Python 3.10–3.12 test/example matrix PASS; clean sdist/wheel build, metadata check, isolated installs, and installed CLI checks PASS.
- Unresolved mandatory technical findings: none.

## Post-authorization GitHub Codex review

After maintainer authorization, the GitHub Codex review completed and reported seven additional findings. Merge was held while they were evaluated.

| ID | Finding | Disposition |
|---|---|---|
| GCR-01 | The repository artifact index used CRLF working-tree bytes instead of committed LF blobs. | Fixed: rebuilt every entry from a byte-preserving checkout and added repository-level validation to CI. |
| GCR-02 | PEP 639 metadata allowed setuptools versions older than 77. | Fixed: raised the build backend floor to `setuptools>=77`. |
| GCR-03 | README used the removed `arap index --output` compatibility option. | Fixed: corrected the quick-start command. |
| GCR-04 | Plain HTTP external evidence bypassed local artifact indexing. | Fixed: only HTTPS is exempt; HTTP now produces a validation error. |
| GCR-05 | Collection-valued nested gate identifiers or statuses could raise `TypeError`. | Fixed: validate string types before set membership, with adversarial tests. |
| GCR-06 | A cyclic symlink could raise `RuntimeError` during path resolution. | Fixed: convert resolution failures into fail-closed validation errors, with a regression test. |
| GCR-07 | Runtime `arap.__version__` disagreed with alpha distribution metadata. | Fixed: both now report `0.1.0a1`, with a regression test. |

These remediations require successful exact-head CI before `post-authorization-review-remediation` can pass. This section records technical review evidence, not external adoption or a third-party GitHub approval.
