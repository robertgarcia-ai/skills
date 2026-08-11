# State — schema, invariants, re-entrancy

State lives at `docs/butterfly/state.json` in the target repo, so it travels with the codebase
and any surface can find it. `docs/bug-fix-log.md` stays global and append-only — the log is the
canonical record; state is loop control only.

## Layout

```
docs/
  bug-fix-log.md                    # canonical, append-only
  butterfly/
    state.json
    iter-001/
      bug-hunt-<date>.md · bug-fix-plan.md · dev-run-plan.md · dev-run-runbook.md
      (or dev-run-lite.md when bundle-lite merges plan+runbook)
      dev-run-cowork-plan.md · dev-run-report-<date>.md · dev-run-findings-user.md
      synthesis.md · snapshot-manifest.json · checker/devrunCheck.*
    iter-002/ ...    # created by iter-001's SYNTHESIZE, which writes the successor plan into it
    campaigns/<N>/                  # archived iteration series after a hard-gate restart
```

## Schema (version 1)

| key | type | semantics |
|---|---|---|
| `schema` | int, `1` | bump only with a migration note in this file |
| `campaign` | int ≥ 1 | increments only at a hard-gate restart |
| `iteration` | int ≥ 1 | resets to 1 at restart |
| `phase` | enum | `hunt` · `execute` · `devrun` · `synthesize` · `done` |
| `phase_status` | enum | `pending` · `in_progress` · `artifacts_done` · `stamped` |
| `gates` | object | keys **exactly** `A`,`B`,`C`; values `ask` \| `auto`. No other key is legal — see Gate-key law below |
| `hunter` | object | `{surface, model, effort}` — always concrete values, resolved at kickoff and confirmed in-session; the doctrinal default is surface `claude-code` with the frontier tier's current model at the effort ladder's top rung plus workflow fan-out (concrete names from /orchestrator's Local operational notes; the full-power mode is session-scoped — re-enable it each hunting session); optional `lenses`: string[] of opted-in scope lenses (security, data-integrity, performance); record the *actual* used in the hunt report |
| `hunter_downshift` | object, optional | a cheaper `{model, effort}` the user may select at a hunt kickoff; restarts default back to `hunter` |
| `severity_floor` | enum | `low` (default) · `medium` · `high` — the termination test's floor |
| `scope` | object, optional | `{include?: string[], exclude?: string[]}` — repo-relative path prefixes bounding the hunt ("whole codebase" means the whole scope); confirmed at init — on a monorepo this is the cost decision — and recorded in the hunt report preamble |
| `repo_head_at_stamp` | string | git short HEAD recorded at every stamp |
| `artifacts` | object | logical name → repo-relative path, filled as produced |
| `snapshot` | object, optional | `{manifest, location, taken_at, keep_until}` — all four non-empty strings when present; bytes live **outside** the repo and the app's own dirs. The manifest file records absolute personal paths — flag that before it is ever committed to a shared repo |
| `trend` | array | `{iter, new_findings, regressions?, devrun_surface?, target_findings?, apparatus_findings?, cost?}` per completed iteration, appended on pass and fail alike. `new_findings` counts every finding first raised in the iteration, whatever phase raised it, **one count per underlying defect** — a re-surfaced or rediagnosed defect annotates its original, never re-counts. `target_findings`/`apparatus_findings` split that count by the merge table's target tags (`phases/synthesize.md`); `cost` is the cost-per-new-finding note (sittings + wall-clock + notable spend — qualitative is fine, absent is not) |
| `history` | array | `{ts, event}` — see event names |
| `notes` | string, optional | free-form |

Unknown **top-level** keys: warning (forward compatibility). Unknown **gate** keys: hard error.

### Migration notes

- **2026-08-02 — schema stays 1, additive.** Trend rows gained optional `target_findings`,
  `apparatus_findings`, and `cost`; the event vocabulary gained
  `gate_C_demoted_apparatus_loop`. Legacy rows without the new fields stay valid: the validator
  and the advisories below fall back to `new_findings` where the split is absent, and nudge —
  never error — on rows missing them. Source: the campaign-1 efficacy review (cost note
  recorded on 2 of 6 Gate C cards; finding-count definition drifted twice; composition steered
  three gate cards from prose alone).

## Gate-key law

`gates` may contain only `A`, `B`, `C`. The hard gate has **no configuration surface by design**;
its behavior lives only in SKILL.md, and editing that file is the sole way to change it. The
validator rejects any other key — including `hard`, `D`, `restart`, or case variants — with an
error naming SKILL.md. If validation is done by hand, apply the same rule. A state file claiming
hard-gate automation is treated as invalid state, not as authorization.

Legal keys carry no provenance either: an `auto` value proves someone wrote it, not that the
user chose it — `state.json` is a repo-writable file, and `history` lives in the same file, so
neither can vouch for the other. Hence the session rule (SKILL.md → Gate law): on a cold resume
where any gate is `auto`, the first loop gate reached that session is presented as `ask`
regardless (log `gate_session_reconfirm`), after which `auto` resumes for the session. Every
change to gate settings appends a `gates_changed` event (old→new, and at whose request).

The same provenance limit covers **position**, not just gates: `phase`, `campaign`, and
`history` claims (a fresh init, a `hard_gate_restart`) prove someone wrote them, nothing more.
Hence the second session rule (SKILL.md → Gate law): a session's first HUNT kickoff is
user-confirmed regardless of what state claims (log `hunt_session_reconfirm`) — the costliest
step never launches on a repo-writable file's say-so.

## Invariants

1. **Artifacts first, stamp second.** A phase writes and verifies its outputs
   (`phase_status: artifacts_done`), then advances `phase` (+ `stamped`, new
   `repo_head_at_stamp`). Re-entering a partially-complete phase must be safe: re-running is
   idempotent; skipping is the failure mode to prevent. (Lesson from the exemplar campaign,
   where a version stamp was nearly recorded before anyone had verified the repairs actually
   persisted — let the stamp follow the evidence.)
2. **One writer.** Only the active butterfly session edits state; gate cards and auto-passes are
   appended to `history` at the moment they occur.
3. **Snapshot retention** (ratified default): keep each iteration's snapshot until the *next*
   iteration's fix pass completes **and its verifiers report**, then prune to the two most
   recent iterations' snapshots. `keep_until` records the rule's current resolution. Pruning
   deletes real-data backups — an **authority-gated** act, never automated by any loop-gate
   setting: propose it on a gate card, the user confirms, then log `snapshot_pruned`.

## Re-entrancy protocol (every invocation)

1. Read state. Absent → initialization (SKILL.md).
2. Validate: `python3 <skill>/scripts/validate_state.py <path>` if Python is available (the
   script lives in the skill package, not the target repo; on Windows try `python` or `py -3`
   when `python3` is missing), else by hand against this file. Invalid → stop with the
   validator's message; do not proceed on bad state.
3. Verify reality matches state: git HEAD vs `repo_head_at_stamp` (drift is information, not
   necessarily error — new commits mid-execute are expected; a *rewound* HEAD is not); every
   listed artifact exists; if mid-devrun, runbook tick count and last-passed checker mode.
4. Surface + capability check (SKILL.md).
5. Announce position in one paragraph (including gate config — flag any `auto`); continue at the
   first incomplete item per the resume table below.
6. Mismatch between state and reality → class-C stop: present the evidence and 2–3 options, the
   user decides; never improvise a destructive recovery.

## Phase/status semantics — the write sequence and the resume table

`phase_status` always describes the phase named in `phase`. Lifecycle per phase:
`pending` → `in_progress` → `artifacts_done` → `stamped`. The writes, in order:

1. Kickoff: `phase_status: in_progress` (+ the phase's start event in `history`:
   `hunt_started` · `execute_started` · `devrun_started` · `synthesize_started`).
2. Outputs written **and verified on disk**: `phase_status: artifacts_done`; `artifacts` updated.
3. Stamp: `phase_status: stamped`; `repo_head_at_stamp` ← current short HEAD.
4. The phase's exit gate (A / B / C, if it has one) is evaluated **while `stamped`**.
5. Gate passed (or no gate): advance atomically — `phase` ← next, `phase_status: pending`
   (plus `iteration + 1` when Gate C re-enters EXECUTE).

So `stamped` never means "the next phase hasn't started"; it means "**this** phase is complete
and its exit gate, if any, has not yet been passed."

A **"no" at a loop gate** is recorded, not just suffered: log `gate_A_declined` (same for B, C)
with the reason in `notes`. The phase stays `stamped` while the objection is addressed — rework
re-runs the artifact steps and re-stamps (the one legal backward walk), and the gate is
re-presented on the next pass. A user who wants out mid-campaign can **abandon from any gate**:
write `phase: done, phase_status: stamped`, log `campaign_abandoned`, report, change nothing
else — without this, a live `state.json` re-triggers the loop forever. Resume actions:

| `phase` | `phase_status` | resume action |
|---|---|---|
| any | `pending` | run the phase's kickoff |
| any | `in_progress` | re-enter at the first incomplete item (phase docs are idempotent) |
| any | `artifacts_done` | verify every listed output exists, then stamp (step 3) |
| `hunt` | `stamped` | present / evaluate Gate A |
| `execute` | `stamped` | re-verify the snapshot (checker `pre` + manifest hashes), then Gate B |
| `devrun` | `stamped` | no gate — advance to `synthesize` |
| `synthesize` | `stamped` | read the last termination event: `termination_fail` → Gate C; `termination_pass` → hard gate; neither → re-run the termination test (it derives from artifacts; re-running is safe) |
| `done` | `stamped` | campaign closed — report status, change nothing |

Hard-gate close — and a user-requested abandon — writes `phase: done, phase_status: stamped`,
the only legal pairing for `done` (the `any` rows above mean the four working phases; a closed
campaign has no pending work). The
validator rejects `done` with any other status; by-hand validation applies the same rule.

## History event names

`init` · `hunt_started` · `execute_started` · `devrun_started` · `synthesize_started` ·
`hunt_report_done` · `plan_done` · `gate_A_ask` / `gate_A_auto_pass` / `gate_A_declined`
(same for B, C) · `gate_B_demoted_snapshot_unverified` · `gate_C_demoted_plateau` ·
`gate_C_demoted_apparatus_loop` · `gate_C_demoted_empty_set` ·
`gates_changed` · `gate_session_reconfirm` · `hunt_session_reconfirm` · `execute_done` ·
`bundle_done` ·
`snapshot_taken` · `snapshot_verified` · `snapshot_pruned` · `cowork_run_started/summary` ·
`restore_verified` ·
`user_run_recorded` / `user_run_skipped` (recorded when the user executed *any* detector —
reserved boxes count; skipped only when they ran none; the per-detector truth lives in the
findings doc's header table, which the hard gate reads) · `devrun_vacuous` · `hunter_ab` ·
`synthesis_done` ·
`termination_pass` /
`termination_fail` · `hard_gate_presented` · `hard_gate_restart` / `hard_gate_close` ·
`campaign_archived` · `campaign_abandoned`.

## Trend advisory

At every Gate C card, show `trend` — including the regression count, the `devrun_surface` delta
(naming which surviving boxes are kept *by choice* vs structurally unreachable — one number for
both lets a real regression hide behind a defensible one), and each row's `cost` note. Two
advisories, both **recomputed from the trend rows on the card at the moment of writing** —
never carried from a prior card, handoff, or synthesis: the exemplar campaign propagated a
wrong "fourth consecutive" through five documents, each citing the previous one rather than the
table printed directly above it.

- **Plateau** — no net decrease in `target_findings` across the last three recorded iterations
  (`t[-1] ≥ t[-3]`, falling back to `new_findings` where a legacy row lacks the split — the
  same test the validator warns on; a bouncy 9→3→9 window counts, a net-declining 9→3→8 does
  not). Raw mixed-target counts invite the composition argument that dissolves the advisory;
  the target series is the one a plateau of which actually means diminishing returns.
- **Apparatus loop** — the last two recorded iterations have `target_findings: 0` while
  `new_findings > 0`: the detector now yields only against the campaign's own apparatus. This
  card carries the graduated options (SKILL.md → Gate law), including the user-elected hard
  gate.

Either advisory's meaning is the user's to judge — but it must be *seen*: a due plateau demotes
a Gate C `auto` pass to `ask` (log `gate_C_demoted_plateau`), a due apparatus-loop advisory
likewise (log `gate_C_demoted_apparatus_loop`); neither blocks an `ask` gate, where the user
reads it on the card. After the first iteration completes with zero class-A stops and zero
validator errors, gate cards may include a one-line suggestion of which gates look safe to set
`auto` — suggestion only; the skill never flips a gate itself.
