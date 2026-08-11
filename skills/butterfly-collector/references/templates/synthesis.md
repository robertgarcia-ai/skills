# Contract — synthesis record (`synthesis.md`, one per iteration)

The merge record for the iteration: what came in from every detector, what it became, and what
was handed to /orchestrator. It is **not** canonical — the log is; synthesis.md shows the work
between the run's outputs and the next plan's inputs, so a later reader (or a fresh-eyes hunt)
can audit every promotion, demotion, and disappearance. Every claim and finding from the inputs
appears here exactly once. Sections below are mandatory unless marked optional; "empty" is
written, never implied.

## 1. Inputs
Pointers with counts: the Cowork report, `dev-run-findings-user.md` (or its explicit
skipped/none declaration), the current log state, the outgoing plan.

## 2. Merge table
One row per merged finding: `F# | provenance [cowork]/[user]/[both] | target
[target]/[apparatus] | severity (re-triaged, user-impact convention) | disposition |
regression? [regression-of <F#/commit>] | log anchor`. Target: `[target]` = the product under
campaign, code or behaviour; `[apparatus]` = the campaign's instruments, documents, process, or
environment; unseparated = `[target]` until measured. One count per underlying defect — a
rediagnosis annotates its original, never re-counts.
Dedupe notes under the table: what merged with what, and re-observations annotated onto their
pins rather than duplicated.

## 3. Claims — dispositions carried
Every claim from the dev-run plan, exactly once, with its verdict (`CONFIRMED-BUG (→F#)` /
`REFUTED` / `CLOSED-BY-<box>` / `UNTESTED (reason)` / `DEAD-CODE`). `UNTESTED` rows name the
reason and are carried into §7's actionable set — they never evaporate. Flag any `UNTESTED`
claim now riding its second-or-later consecutive plan; the hard gate enumerates these.

## 4. Retractions and withdrawals
Each withdrawn finding with its refuting evidence; each scribe error with the rule it produced.
Quiet deletion is the failure mode this section exists to prevent.

## 5. Harness-growth audit
Per finding and per dispositioned claim: **harnessable now that it is known?** Yes → the
harness-addition item handed to /orchestrator. No → the verbatim structurally-unreachable reason
for the next bundle's category entry. Close with the **surface delta**: dev-run checks by
category, this iteration vs last, and the `devrun_surface` number that goes in the trend row.

## 6. Habitat report
Findings clustered by breeding ground (file, pattern, missing layer); at most a handful of
structural prevention nominations as NEEDS-DECISION items, each with the bug classes it would
extinguish. Note where answered §7 decisions were consolidated into the living rubric.

## 7. Actionable set handed to /orchestrator
The exact list: new findings + confirmed claims + carried BLOCKED + carried UNTESTED +
answered decisions + approved prevention nominations. If the set is empty, say so — that
absence is the termination test's subject.

## 8. Termination test
The four conditions, each with its evidence and verdict — **all four evaluated every time,
none marked moot** — then the overall pass/fail and the trend row as appended
(`{iter, new_findings, regressions, devrun_surface, target_findings, apparatus_findings,
cost}`).
