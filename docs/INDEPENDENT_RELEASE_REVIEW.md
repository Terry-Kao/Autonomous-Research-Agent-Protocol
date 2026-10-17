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
| IR-07 | Packaging metadata used a legacy license table and omitted canonical project URLs. | Added SPDX license metadata, license file declaration, and canonical URLs. | Clean build and metadata check in CI. |
| IR-08 | Text line-ending conversion made some artifact hashes differ between Linux and Windows checkouts. | Fixed repository text files to LF through `.gitattributes`, then rebuilt indexes from normalized bytes. | Repository validation on normalized checkout and CI. |
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
