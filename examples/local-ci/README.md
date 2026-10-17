# Local CI handoff

From the repository root after installation:

```bash
python examples/local-ci/run.py /path/to/new-demo-directory
```

This domain-neutral integration creates a fresh project, writes explicitly synthetic evidence, indexes it and validates the contract. It checks that missing mandatory reviews keep the decision BLOCKED. It never marks its own synthetic result as independent review. Use an absent or empty output directory. This is a maintainer-authored example, not a downstream integration or adoption claim.
