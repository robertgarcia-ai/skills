# Phase — SYNTHESIZE

*Surface:* Claude Code (handoff if elsewhere). *Inputs:* Cowork report + user findings + the log.
*Outputs:* log section appended · `synthesis.md` · a **new** /orchestrator'd `bug-fix-plan.md`.
*Routes to:* Gate C (loop) or the hard gate (termination).

Kickoff: log `synthesize_started`.

## Merge

- Provenance-tag every finding `[cowork]` / `[user]` / `[both]`; dedupe against each other and
  against known-open (a re-observation annotates the pin, it does not duplicate).
- Target-tag every finding: `[target]` — a defect in the product under campaign, code or
  behaviour — or `[apparatus]` — the campaign's instruments, documents, process, or
  environment. A finding whose target is not yet separated by measurement is `[target]` until
  it is: the gate card may not run ahead of the evidence (the exemplar campaign committed
  "zero app-code defects" 42 minutes before the measurement that made it true). One count per
  underlying defect: a re-surfaced or rediagnosed defect annotates its original entry, never
  re-counts.
- Tag **regressions**: any finding traceable to a fix from this campaign (any iteration) carries
  `[regression-of <F#/commit>]` — the loop reports its own self-inflicted rate, and regressions
  outrank same-severity fresh bugs in the next plan.
- Re-triage severity across the merged set with the hunt convention (user impact).
- Disposition every claim exactly once; carry `UNTESTED(reason)` forward into the next plan
  rather than letting it evaporate.
- **Record retractions and withdrawals** in `synthesis.md` — a withdrawn finding with its
  refuting evidence is data; quiet deletion is the failure mode.
- Product calls surfaced by the run go to the user as NEEDS-DECISION with options; answers land
  in the new plan's §7.

## Harness growth (mandatory)

For every finding and every dispositioned claim, answer: **is this checkable by a harness now
that it is known?** (The exemplar report's F1 — a missing `stop_reason` guard — became
harness-checkable the moment it had a name.) Yes → a first-class harness-addition item handed to /orchestrator alongside the fix.
No → record *why it is structurally unreachable*, verbatim, for the next bundle's category
entry. Compute the **surface delta**: dev-run checks by category this iteration vs last; the
count goes in the trend row (`devrun_surface`) and on the Gate C card, naming which surviving
boxes remain **by choice** (a deliberately kept detector) vs structurally unreachable. A
surface that doesn't shrink is a standing cost, and the card says so.

## Bookkeeping (campaign conventions)

- Append `## The dev run — <date>` to `docs/bug-fix-log.md` in house style
  (`templates/bug-fix-log.md`); full four-part entries; the report's findings index links each
  F# to its log anchor. **The log is canonical.**
- Rewrite the outgoing plan's **Remaining** line as the honest successor list and append the
  compressed verdict block (counts by severity, claim dispositions, known-open state, pointer to
  the report).

- **Habitat report** (in `synthesis.md`): cluster the iteration's findings by breeding ground
  (file, pattern, missing layer); nominate at most a handful of structural prevention changes as
  NEEDS-DECISION items, each with the bug classes it would extinguish; approved nominations
  become their own lanes in the next plan.
- **Rubric consolidation**: fold every answered decision from the outgoing plan's §7 into the
  project's living rubric/spec document (create one if absent) and keep the fixer prompts
  pointed at it — decisions scattered across superseded plans are spec nobody reads.

## /orchestrator — the next plan

Feed the merged actionable set (new findings + confirmed claims + carried BLOCKED items +
carried UNTESTED + answered decisions + approved prevention nominations — the same list as
`templates/synthesis.md` §7) to `/orchestrator` with the plan contract; verify against the
contract as in HUNT. Create `iter-<N+1>/` and write the new plan there — each iteration's
directory holds the plan it executes (iteration 1's came from HUNT). An empty actionable set
skips the call and creates neither — that absence is what the termination test is about to
measure. If the termination test then **fails anyway** — criteria 3 and 4 can fail on residue
that is not plannable work: an unanswered NEEDS-DECISION, an unpinned known-open — Gate C is
demoted to `ask` regardless of setting (log `gate_C_demoted_empty_set`). The card then lists
the failing criteria and their blocking items instead of a plan shape, and EXECUTE is **not**
re-entered until the actionable set is non-empty: typically the user's answers become the set,
the skipped /orchestrator call runs then (creating `iter-<N+1>/` and its plan), and only that
re-arms the normal Gate C path. If the residue is not worth another pass, the user may close
or abandon instead (`references/state.md`). Write `synthesis.md` per `templates/synthesis.md` (the merge record + the actionable
set handed over), append the log section, update `artifacts`, set
`phase_status: artifacts_done`, stamp (log `synthesis_done`) — then evaluate the termination
test and route.

## Termination test — "nothing new to hand /orchestrator"

All four required, **each evaluated and recorded every time** — no criterion is ever marked
moot: a criterion's evidence is written down even when another has already failed. (The
exemplar campaign moot-skipped criteria 3–4 for two iterations while unanswered NEEDS-DECISION
items existed, which broke the comparability of its own failing-count series and hid the true
blocker from the card.)

1. Zero new `[target]` findings at or above `severity_floor` surviving disposition — a finding
   closed working-as-intended by the user's answer lands in the rubric and does not block —
   and zero claims dispositioned `CONFIRMED-BUG` against the target, from either the Cowork
   report or the user's findings doc. An unseparated finding counts as `[target]`.
2. The user's findings doc, read as a whole, is an unretracted no-findings declaration — never
   a mere absence, and never the skip line alone: the header's detector table
   (`templates/dev-run-findings-user.md`) states per detector (user-reserved boxes ·
   independent pass) what ran, and every detector the user ran reported nothing. User-sourced
   findings filed through the Cowork report count under criterion 1, not here.
3. Every remaining open item is an answered product decision or `PINNED-OPEN` with a live
   harness pin — nothing is merely unmentioned, and `[apparatus]` findings are open items like
   any other. An open **integrity defect in a measuring instrument** — a checker that can pass
   without looking, a sweep that drops a failing suite, an unregistered check — fails this
   criterion outright: criterion 1's evidence flows through those instruments.
4. The previous plan is fully dispositioned: no unanswered NEEDS-DECISION, no unexecuted lane,
   no unverified fix.

Either way, append the trend row first: `{iter, new_findings, regressions, devrun_surface,
target_findings, apparatus_findings, cost}` (zeros where earned; `cost` is the
cost-per-new-finding note — sittings + wall-clock + notable model spend over new findings;
qualitative is fine, absent is not — it lives in the row because a note that rides only the
card was written twice in six iterations).

**Fail →** log `termination_fail`, present the Gate C card: synthesis summary · the new plan's
shape · the trend with regression count, surface delta (chosen vs unreachable boxes named), and
each row's cost note · the advisories if due — **plateau** (`t[-1] ≥ t[-3]` over
`target_findings`, falling back to `new_findings` on legacy rows) and **apparatus loop** (the
last two rows have `target_findings: 0` while `new_findings > 0`), each recomputed from the
rows on this card, never carried from a prior document · (after the first clean iteration) the
auto-candidate suggestion line. A due apparatus-loop advisory's card offers the graduated
responses (SKILL.md → Gate law): continue as-is · raise `severity_floor` · narrow `scope` or
set `hunter.lenses` · aim the next iteration at instrument hygiene targeting a vacuous dev run
· elect the hard gate now.
`ask` → stop for the user; `auto` → only if no advisory is due: a due plateau demotes this
pass to `ask` (log `gate_C_demoted_plateau`), a due apparatus-loop advisory likewise (log
`gate_C_demoted_apparatus_loop`) — the advisories exist to be seen, and an auto-pass would
bury them in `history`; otherwise log `gate_C_auto_pass` and re-enter EXECUTE with
`iteration+1`.

**Pass →** log `termination_pass` and go to the hard gate — its exact conduct lives in SKILL.md
(Gate law), which is deliberately the only place it lives. The summary makes the **saturation
claim, not an absence claim**: this apparatus found nothing new above the floor — not that no
bugs remain. Present: the trend across all iterations (including regressions and
cost-per-new-finding) · totals fixed/pinned/decided · **every known-open still alive, with its
pin** · every open `[apparatus]` finding · unresolved product calls · every claim still
`UNTESTED` after riding two or more consecutive plans · the user's participation **per
detector** — iterations with reserved boxes run, with an independent pass run, with neither
(read from each findings doc's header table; the bare `user_run_recorded`/`user_run_skipped`
counts under-report a user who ran boxes every iteration and found the campaign's highs) —
saturation is claimed only for the detectors that ran · **every human-reserved act deferred to
campaign close**, each re-presented for fresh confirmation (SKILL.md → hard gate) · what the
last clean run proved. Then the two options — the
restart option carries the hunter A/B offer (`phases/hunt.md`) — and stop. On an explicit restart: archive `iter-*/` into
`docs/butterfly/campaigns/<N>/`, `campaign+1`, `iteration=1`, recreate `iter-001/`, log
`campaign_archived` + `hard_gate_restart`, and enter HUNT under the fresh-eyes rule. On close: `phase: done`, log
`hard_gate_close`, final summary.
