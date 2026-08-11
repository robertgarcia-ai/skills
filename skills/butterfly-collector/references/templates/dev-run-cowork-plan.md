# Contract — Cowork execution plan (`dev-run-cowork-plan.md`)

Exemplar: `references/examples/dev-run-cowork-plan.md`. This document directs the Cowork session
running the runbook. It never restates commands or expected values (the runbook owns those); it
says **who does each step, what is measured automatically, what is recorded where, and what
happens when something goes wrong**. Deliverables named up front: all runbook boxes dispositioned
with evidence, the report, the log section, the handoff.

## §0 Mission and ground truth
The one open item this run closes; expected repo tree + HEAD; "anything else modified → stop and
ask"; which effects are one-shot and why this run is their only observation.

## §1 Read first, in order
Numbered list with the load-bearing line ranges. Include any tool footguns (files that break
grep/rg, etc.).

## §2 Cast and hard rules
**The user acts only where the act is irreversible or their eyes are the instrument**: the
enumerated irreversible acts; every in-app gesture; perception judgments; product decisions.
**Cowork does everything else.** Hard rules, no exceptions — adapt but always include:
- The real profile's app is never launched, killed, or driven by Cowork; only self-spawned pids;
  every process lookup/termination scoped by a command-line match on the scratch dir.
- Real-profile quits are the user closing the app, **verified** by a read-only process check —
  never assumed, never induced.
- Never write live config files while the app runs (contaminates the measurement).
- No commits except the gated ones; the only runbook edits are `- [ ]` → `- [x]`.
- Any test fixtures designed to trip safety systems are quoted from the runbook, typed by the
  user, never authored/varied/sent elsewhere by Cowork; Cowork records what renders.
- **Access grants pre-arranged before Stage 0** so no permission prompt lands mid-one-way-launch.

## §3 Preflight — all green before Stage 0; results open the report
Repo state vs expected; runbook virginity (0 boxes ticked; a tick = partial prior attempt →
reconcile first); checker `pre` ends `ALL CHECKS PASSED` with its info lines **transcribed into
the report as pinned premises** (config under test, deviation → stop and ask); **capability
probe**: verify what Cowork can actually drive on this machine, adopt a mechanism for the gaps
(the exemplar invented a file-bridge job runner when the terminal turned out to be click-only),
and record the adopted mechanism in the report's Run conditions.

## §4 The pair-run loop + stop rules
Loop: run → condense observed vs expected → tick **only on evidence** → advance, honoring the
ordering constraints. Three stop classes, verbatim-adaptable:
- **A — measurement gates**: a checker FAIL stops the run; restore rescues *the run*, not the
  data; the `pre` gate is mandatory before resuming.
- **B — app misbehavior is never a stop**: it is the point. File a finding, restore any setting
  the test changed, continue. Exception: damage to the measurement environment — file it **and**
  re-verify before continuing.
- **C — a state neither document predicted**: pause, present evidence and 2–3 options, the user
  decides. Never improvise a destructive recovery.
**Session-death recovery**: a fresh session reads this plan, reads the report, counts ticked
boxes, re-runs the last passed checker mode, resumes at the first unticked box.

## §5 The per-box actor map
One table row per runbook box: `Box | Actor (C/U) | Notes` — who gestures, who proves, which
probe, what counts as evidence. This is where "to the fullest extent possible" is made concrete:
Cowork's column is its autonomous run; the user's column is the queue.

## §6 Findings and evidence
The runbook's four-part protocol plus report-side extensions: severity · `file:line` where known ·
fresh-state phrasing · needs-migration-history · suggested lane → tier · new vs confirms-claim-N.
**Host-read rule**: no claim about file content becomes a finding until read on the host machine
(staged copies are for orientation only — a stale-bytes read produced a retracted finding once).
"An app misbehavior is a finding, not a stop. A checker failure is a stop, not a finding."

## §7 The log write — the gate before anything destructive
Transpose finding stubs into `docs/bug-fix-log.md` (house style), verify nothing still needs the
old state, and only then allow the destructive stage. The log is canonical; the report indexes it.

## §8 Tier assignments
Table in tier terms (frontier / heavy / workhorse / mechanical) per /orchestrator's Assignment
law, concretized by the bug-fix plan's pinned, dated tier→model mapping; "recorded, not chosen"
for the app's own config under test; fallback instruction if the pinned model is unavailable
(use the strongest available at that tier and record the actual). (The exemplar's §8 predates
the tier form and quotes a retired model-name rhyme — the contract wins; do not imitate it.)

## §9 Post-run sequence
Log write → destructive stages per actor map → report finalization (verdict last; every ⚠️/❌
cross-linked) → runbook reconciled ("never tick what didn't happen") → plan bookkeeping (rewrite
the Remaining line as the honest successor list + compressed verdict block) → **gated commits**
(Cowork proposes, the user authorizes each individually; no push unless asked) → backups outlive
the run until the fix pass completes **and its verifiers report**.

## §10 Risk register
Table: risk | mitigation — one-way effects consumed silently, shared-folder blast radius,
zombie re-ingest landmines, no single-instance guard, scratch mismanagement, measurement
contamination, date staleness, exit-code semantics, session mortality.

## Appendix A — report skeleton
The full report template (see `templates/dev-run-report.md`), copied out at preflight and filled
live.

## Appendix B — probe kit (read-only)
Named probes with exact commands: process check (quiescence/quit verification), scoped scratch
quit, DB/state probe template ("discover schema first, then query — don't guess column names"),
artifact reads, blast-radius before/after snapshot diff ("the blast radius gets measured, not
recalled"). Probes are informational; they never replace a checker gate.
