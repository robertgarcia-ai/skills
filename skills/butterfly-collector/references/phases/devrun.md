# Phase — DEV RUN

*Surface:* Cowork (+ the user). *Inputs:* the bundle + a verified snapshot.
*Outputs:* `dev-run-report-<date>.md`, `dev-run-findings-user.md`. *Gate after:* none (flows into
SYNTHESIZE); the loop gate was B, before this phase.

Bundle-lite iterations walk the same sequence with the merged documents. A `devrun_vacuous`
iteration (all five categories empty, user-confirmed at Gate B) skips the run, not the phase:
its states are still walked, with the skip declarations as its artifacts — exact sequence in
`phases/execute.md` — because the termination test consumes declarations, not absences.

Sequenced for comparability — both passes start from the identical snapshot:

## 1. Snapshot re-verification (on this surface)

Log `devrun_started` on entering the phase.
The snapshot was taken and verified at the end of EXECUTE (`phases/execute.md`, bundle step 6);
this phase re-establishes it where the run will actually happen — surfaces change between
phases, and time may have passed. App quit confirmed, checker `pre` green again, manifest hashes
spot-checked against the stored bytes; append a fresh `snapshot_verified`. A `pre` failure here
is a class-A stop, not a shrug. If any covered path lives on a sync share, the manifest notes it
and the restore step warns that restoring there propagates (sometimes intended — say which).

## 2. Cowork's autonomous run

Cowork preflights per the cowork plan (log `cowork_run_started`; repo state, runbook virginity,
checker `pre` with info lines transcribed, **capability probe** with the adopted mechanism
recorded in Run conditions),
then executes every box in its column of the actor map to completion, queuing the user-reserved
boxes as it goes. Stop rules A/B/C and the host-read evidence rule apply verbatim from the cowork
plan. The report grows live from the skeleton; ticks only on evidence. Cowork proposes gated
commits; it never commits or pushes unauthorized.

## 3. The user's independent pass (optional — the reason the snapshot exists)

If the user wants a comparison run: restore per the runbook's restore-in-order (app quit first;
all independent state; checker `pre` re-verifies — record `restore_verified`), then the user
walks `dev-run-runbook.md` themselves, recording findings in `dev-run-findings-user.md` with the
same four-part protocol. **Once-only caveat:** effects that run once per data-state cannot fire
twice on the same profile; the second pass observes them via reconstruct-on-scratch — rebuild a
scratch profile from the byte-identical pre-state backup, re-run the observation there,
checker-gated (the campaign validated exactly this recovery when its one-way launch turned out
to be already consumed). The runbook's `once-only` tags say which checks this applies to.

If the user skips the pass, they say so; the skill writes `dev-run-findings-user.md` containing
its explicit skip line (contract: `templates/dev-run-findings-user.md` — the termination test
needs the declaration, not an absence). Whatever the user ran, the findings doc's header
detector table records it — reserved boxes and independent pass separately — because the
termination test and the hard-gate summary read participation from there. Log
`user_run_recorded` when the user executed *any* detector this run (reserved boxes count — the
exemplar campaign logged six bare skips for a user who ran boxes every iteration and sourced
three of its six highs); `user_run_skipped` only when the user ran none.

## 4. Finalize

Report finalization checklist (verdict last; every ⚠️/❌ cross-linked to a finding or
disposition; claims table complete — every claim exactly once; handoff table filled; commit plan
prepared). Runbook reconciliation note written; never tick what didn't happen. The **log write
is the gate** before any destructive stage in the run itself. Backups keep until the next fix
pass completes and its verifiers report (then the two-iteration pruning rule). Log
`cowork_run_summary` when the report's verdict is finalized. Update `artifacts`, stamp, proceed
to SYNTHESIZE.
