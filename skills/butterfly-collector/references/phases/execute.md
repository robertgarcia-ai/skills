# Phase — EXECUTE

*Surface:* Claude Code (handoff if elsewhere). *Inputs:* current `bug-fix-plan.md`.
*Outputs:* fixes merged + log entries + the dev-run bundle. *Gate after:* B.

## Preconditions

Plan exists and satisfies the contract; git baseline + tag exist (Phase 0 creates them if not);
unanswered NEEDS-DECISION items are surfaced immediately — lanes that don't depend on them run
meanwhile (authority gate: decisions come from the user, whatever the loop gates say).

## Run the plan — "fullest extent possible", operationally

Kickoff: log `execute_started`. Every plan item terminates in exactly one of:

| terminal state | requirement |
|---|---|
| `FIXED` | repro demonstrated → minimal fix → repro re-run green → typecheck/build green → adversarial verifier `SOUND` |
| `NEEDS-DECISION → implemented` | user's answer recorded in the plan §7; implementation matches the answer, not the lane's judgment |
| `BLOCKED(reason)` | reason logged in `docs/bug-fix-log.md`; carried into the next plan |
| `PINNED-OPEN` | a live pin in the harness/smoke suite so it can never go green over the bug; pin location recorded |

No silent drops. Approved prevention nominations from the previous synthesis run as their own
lanes under the same discipline — a habitat change ships with the bug classes it extinguishes as
its proof obligation. Execution mechanics come from the plan itself (worktrees, one owner per file,
merge one lane at a time smallest-diff-first, gates between merges, standing footguns). Verifier
verdicts route per the plan's escalation table (/orchestrator's law): a FLAWED verdict returns
the fix to its originating lane with the refutation attached; after **two FLAWED verdicts on the
same item, no further refutation round runs without the user's explicit say-so** — present the
refutations, spend so far, and a recommendation; the default lean is scope-out-and-pin, landing
as `PINNED-OPEN` (or `BLOCKED(reason)` where no pin can hold it), never a rebuilt mechanism. The
gated item waits without stalling other lanes (the NEEDS-DECISION pattern). Keep the
log current as lanes land: finding → lane → commit → proof → verifier verdict (house style:
`templates/bug-fix-log.md`).

**Before declaring the phase done, run the coverage check** (plan §5.4): for every file any lane
owns, list every finding in that file and diff against the lane lists; sweep by file, not by
severity — findings hide in the gap. Re-read the disputed list after related files changed. Log
`execute_done` when the sweep comes back clean.

## Generate the dev-run bundle (in this order)

1. **Enumerate mutations.** List every effect the upcoming run will cause — harness-reachable
   or not — into the plan's Mutation-enumeration section (`templates/dev-run-plan.md`); the
   snapshot manifest and the checker are derived from this list, not from guesswork.
2. **`dev-run-plan.md`** per `templates/dev-run-plan.md` — scope strictly to the five
   harness-unreachable categories, each present or explicitly empty; every entry records *why it
   is structurally unreachable* (the harness-growth audit reads these); state the **surface
   delta** vs the previous iteration's plan up front; tag `once-only` checks.
3. **Checker** per `templates/checker-spec.md`, generated from the plan's pins and expectation
   table; runnable from the repo root; command recorded in the runbook.
4. **`dev-run-runbook.md`** per its template — written by *re-verifying every plan premise
   read-only*, with the mandatory "corrections found while verifying" section (this step has
   caught a device-wide overwrite before; it is not optional) and the neutralization steps for
   outbound-propagating effects.
5. **`dev-run-cowork-plan.md`** per its template — actor map splitting every box into Cowork's
   autonomous column vs the user's reserved column; probe kit; risk register; report skeleton.
6. **Take and verify the snapshot** (last, because it needs the checker). With the app quit and
   at a location the user confirms, capture everything the mutation enumeration names — bytes
   **outside** the repo and the app's own dirs; write `snapshot-manifest.json` (paths + sha256 +
   sizes) into the iteration dir, flagging that it will contain absolute personal paths before
   it is ever committed to a shared repo, and noting any covered path on a sync share. Checker
   `pre` green is the verification. Log `snapshot_taken`, then `snapshot_verified`; fill state
   `snapshot` `{manifest, location, taken_at, keep_until}`; log `bundle_done`.

**Bundle-lite (proportionality).** When the surface is small — categories mostly empty, no new
irreversible effects, few checks — collapse ceremony, not protocol: merge plan+runbook into one
`dev-run-lite.md`, reduce the cowork plan to its actor map + stop rules + probe kit, and record
the choice in state `notes`. Never collapsed: the mutation enumeration, the checker, the
snapshot, and the gates. If **all five categories are empty**, the dev run itself may be
skipped. The skip is confirmed by the user at Gate B **regardless of the gate's `auto` setting**
— the fourth ask-forcing rule beside the three demotions — and logged `devrun_vacuous`. Then walk
the devrun phase's states instead of jumping over them, so a cold resume never lands between
phases: enter `devrun` / `in_progress`; write the declarations the termination test consumes —
`dev-run-report-<date>.md` reduced to an explicit no-run statement, and
`dev-run-findings-user.md` with its skip line (`templates/dev-run-findings-user.md`);
`artifacts_done`, stamp, advance to SYNTHESIZE (carried items can still fail termination).

## Gate B card

Fix-pass summary (terminal-state counts) · bundle summary (categories present/empty, once-only
checks, irreversible-effect count) · **surface delta vs previous iteration** · snapshot
(location, manifest size) · **snapshot verification status** — taken at bundle step 6; on a
resume, re-verify before the gate. Gate B on `auto` proceeds only if the snapshot verifies
(checker `pre` green + manifest hashes match); a failed verification demotes this pass to `ask`
and logs `gate_B_demoted_snapshot_unverified`. Update `artifacts`, stamp.
