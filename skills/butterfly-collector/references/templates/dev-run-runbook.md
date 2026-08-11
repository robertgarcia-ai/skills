# Contract — dev-run runbook (`dev-run-runbook.md`)

Exemplar: `references/examples/dev-run-runbook.md`. The runbook operationalizes the dev-run plan
into checkboxes a person walks; it is the single source of truth for commands and expected values
(the cowork plan never restates them).

## Reconciliation slot (top, filled post-run)
After the run, a blockquote records box-level disposition: ✅/⚠️/❌/UNTESTED per stage, whether
boxes were ticked live or the run was recorded in the report/log instead, and any mandatory-first
leftovers. "Do not tick retroactively."

## Verification stamp + corrections
The runbook is written by **re-verifying every premise of the plan read-only** (checker `pre`,
typecheck/build, artifact freshness) and records the date. Then a numbered **"Corrections to the
plan, found while verifying it"** section — this section is mandatory even when empty, because the
exemplar's rehearsal would have overwritten synced files on every device as planned, and
verification is what caught it. Corrections also live inline at the step they touch.

## Standing premises
Anything that changes what the run optimizes for (e.g. "the data is disposable" flips hedged
checks to destructive ones and re-weights the one-shot migration observation). State each premise
and its consequences explicitly.

## Scheduling
Time gates (local-evening date tests, with the concrete expected dates for the written run day);
ordering constraints (destructive checks late, after the stages that want a populated state;
findings written up before any scrap; the scrap last of all); rough per-stage timings.

## Division of labor + ground rules
Who drives the app vs who runs commands; repo-root discipline with the exact `cd`;
no-two-instances rule; app-quit-before-checker/restore; measurement-protection rules (nothing
into watched folders until the post-launch gate); no commits during the run.

## Stages as checkbox lists
`- [ ]` per check with the expected value inline (exact numbers, not "about"), the command where
one exists, and the plan section it traces to. Every box must be tickable on evidence.

## Findings protocol
Four parts per finding: what you did · what you saw · what the plan/code says should happen · the
repro line a fixer lane can run. Plus: **fresh-state phrasing** ("park any file 11 months out",
never a named personal row); the `needs-migration-history: yes/no` flag — yes means capture
exhaustively **before** any destructive stage, because afterward nobody has such state.

## If something is wrong — restore, in this order
Copy of the plan's procedure with concrete paths/commands, ending in the checker `pre` pass.
