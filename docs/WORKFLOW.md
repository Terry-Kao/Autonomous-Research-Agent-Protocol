# PR-driven workflow

1. Open one bounded issue with scope, exclusions, inputs, acceptance gates, failure conditions, and required evidence.
2. Freeze the protocol before inspecting final results.
3. Implement on a task branch. Keep failed attempts as evidence instead of rewriting history.
4. Add tests, adversarial controls, evidence, hashes, and a concise report.
5. Open a pull request linked to the issue. State what was frozen, what changed, and whether work was executed or only prepared.
6. Run independent review from committed bytes. Verify hashes before interpreting metrics.
7. Emit `PASS`, `REVISE`, or `BLOCKED` with failed gate identifiers.
8. Merge only under repository policy. Update state and open the next bounded issue after merge.

Every handoff should name the commit or PR, evidence paths, gate decision, blockers, and sole authorized next action.

