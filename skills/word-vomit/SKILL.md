---
name: word-vomit
description: Take raw, excited, disorganized thought and convert it into a structured, verifiable representation of the user's intent — whether that intent already exists or is still forming — then route it to execution, handoff, or a park. Use only when the user invokes /word-vomit, or pastes disorganized text WITH an explicit signal to act on or organize it ("sort this out," "make this actionable," "what do I do with all this"). A pasted wall of text alone is not a trigger — logs, quotes, drafts, and material to summarize all arrive as walls of text. Without the signal, do not launch: offer the skill in one line and proceed only if accepted.
argument-hint: "Paste your word vomit. Mess is fine."
---

Handle this yourself — do not spin up a sub-agent for it.

**Reference files** — consult at pointer sites, not preemptively:
- `references/choreography.md` — every gate and multi-topic rule: topic
  lifecycle, gate hold/release, topic gate, queue check, reconciliation,
  dispatch ordering. **No gate rule exists outside it.**
  Annex: **Cycle accounting** — later-firing scope, option-map exit
  accounting, path-unreconstructable rule, fork path state test.
- `references/definitions.md` — marker system, tests, thresholds, artifact
  formats, phase detail annexes.
  Annexes: Format table · Headers · Tier and mismatch tables · Switching
  criteria · Signal table · Felt-sense ladder · Fork selection · Gate
  check · Clearing scripts + acknowledgment threshold · Critique
  dimensions · Handoff argument. Annex title = spine pointer name, verbatim.
- `references/worked-example.md` — three-topic extractive transcript (gate
  hold/release, dispatch ordering, both park paths, reconciliation); read
  when multi-topic sequencing is unclear.
- `references/worked-example-2.md` — two-cycle single-topic transcript
  (generative mode, option map, fork-as-deliverable path, later-firing
  Phase 6, do-it-now gate check); read when generative mode or multi-cycle
  sequencing is unclear.

Definitions are owned by their reference file; this spine points and never
restates. Edits land in the owning file only.

---

## Purpose

An intent clarifier that tolerates chaos as input. One artifact — the
**verifiable output** (called the *verified* output after Phase 4 confirms
it; one artifact, one state change, two names) — then a route. If the route
is handoff, the verified output is the primary input to `/handoff`, which
owns the handoff document; this skill never produces that second artifact.

---

## Priority hierarchy — degradation order

When pressure (context limits, user urgency, an override) forces trade-offs,
shed from the bottom, never the top:

1. **Never fabricate intent.** No invented desired state; inventions are
   marked, never asserted.
2. **Confirm before commit.** Nothing executes or dispatches on an
   unconfirmed output.
3. **Flags surface before gates.** Every qualifying ⚑ lands before the gate
   it bears on fires.
4. **Assumptions are marked inline** — ◈ at identification, ⚑ for
   structural risk, in the turn where they're spotted.
5. **State is printed, not carried** — ledgers, dependency records, queue
   checks. An explicit empty print proves a check ran.
6. **Ceremony degrades first** — headers, scripts, offers, beat order.

**User override:** "skip it, just do it" is honored, not fought — comply,
preserving rungs 1–5 in a single line: name what was skipped and any open
markers, then act.

**Message boundaries:** a message ends at the first beat requiring a user
answer; statement beats (reflections, tier/mode reads, ledgers, route
statements, flag surfaces) ride at the top of that message, never alone.
Collapse adjacent beats freely under this rule
(→ definitions: Message boundaries).

---

## Pipeline

1 Absorb → 2 Mode + clarify (loop) → 3 Verifiable output → 4 Diff + confirm
(loop) → 5 Route → 6 Critique offer → gates. Re-entry is named, never
silent (→ definitions: Re-entry conditions). Phases 5–6 attach to confirmed
outputs, once each (→ choreography: Cycle accounting).

---

## Phase 1 — Absorb

Reflect subject matter only — name the topics present; no organizing, no
evaluating, no solutions. Bare invocation: ask for the dump. Thin input:
say it's thin, ask if there's more. **Multiple topics:** ask the
ordering-dependency question, then priority; on a declared dependency ask
the object question — needs the plan, or the executed result? ("unclear"
is a legitimate answer) — then print the dependency record:
*[T2] depends on [T1] — needs: {verified output | executed result |
unclear}.* The record keys the topic gate (→ choreography). Run the
pipeline on Topic 1 only.

---

## Phase 2 — Mode + clarify

**2a.** State the tier read (user's tier / problem's tier — 1 symptom,
2 task, 3 mechanism, 4 structure, 5 frame) and the mode read
(extractive / generative) in one sentence each at the top of the round-1
message. Mismatch: ask in the problem's tier's direction; user above the
problem: ground downward. Severe mismatch: say so plainly and mark ⚑
(pre-output basis rules → definitions: Interrupt threshold).

**2b.** Extractive — intent exists, buried: converge on it. Generative —
intent forming: diverge then eliminate, surface forks and decision
criteria; a decided fork is a legitimate exit. Switch to extractive when a
statement is quotable-and-holdable; switch back per the discard test — two
consecutive discards, same lineage (→ definitions: Discard test).

**2c.** One to three questions per round, prioritized by what most changes
the output. Cover: current state, desired state, type of work, constraints,
scope, execution context. Context: fill session-side facts yourself
(tools, connectors — already in view); spend questions on user-side facts
only (→ definitions: Execution context). **Terminate** when the output is
complete with no invented answers. Not converging — or provably unable to
converge — diagnose the cause before acting (→ definitions: Non-convergence
taxonomy, including its trigger and the decidability probe). **Park here is
a pipeline exit:** in a multi-topic session run the queue check first
(→ choreography: Queue check), produce the park artifact, stop.

---

## Phase 3 — Verifiable output

Select format by type of work (→ definitions: Format table; option map when
intent is still forming). Every format makes explicit: current state,
desired state, the gap, and the execution-context block appended after a
horizontal rule — skipped only for true greenfield, and then marked ◈.
Open with the intent-verification header for the mode (→ definitions:
Headers). The output must be specific enough that the user can be *wrong*
about it.

---

## Phase 4 — Diff + confirm

Iterate until explicit confirmation. Silence never counts; a cold thread
closes as unconfirmed. "Feels wrong but can't say why" is valid input —
run the felt-sense ladder: gate (legitimize "can't name it";
confabulation-check any named reason) → section triangulation → one
contrast probe → premise test (→ definitions: Felt-sense ladder). Classify
corrections: **ordinary** — edit in place; **format break** — rebuild per
the Format table; **premise break** — ⚑ in that turn, re-enter Phase 2
from the top with a fresh 2a, reconcile open markers
(→ definitions: Re-entry conditions). A newly surfaced system reference:
gather its actual state now, update the block in place, discard-test the
plan's assumption. **Option map:** exits are park / corrections / fork
selected → fork protocol: confirm commitments, then ask deliverable-or-input
(→ definitions: Fork selection; firing accounting →
choreography: Cycle accounting). Non-convergence: same taxonomy. **Park
here is a pre-confirmation exit** — same queue-check rule as Phase 2. After
confirmation, ask what the pass surfaced that's still unresolved.

---

## Phase 5 — Route

Print `[Marker ledger — Phase 5]` (chain rules → definitions: Marker
ledger); check each projected-basis flag against the confirmed plan; any
flag meeting the interrupt threshold surfaces now, one or two sentences,
before the route. Routes:

- **Do it now** — small, self-contained, fully specified, session has the
  context and tools. Ties between *eligible* routes break toward it; it
  cannot seat a route whose own conditions are unmet.
- **Hand it off** — large, multi-session, or polluted context. Supply a
  1–3 sentence argument naming type of work and desired state; the verified
  output, context block, and current ledger ride along uncompressed
  (→ definitions: Handoff argument).
- **Decided fork** — produce the decision record; offer plan-or-park at
  its gate.
- **Park** — name the blocker (→ definitions: Park artifact format).

State the route. **The execution gate fires only after Phase 6 clears** —
and in multi-topic sessions it may be held, with the topic gate interleaved
(→ choreography: Ordering spine, Gate hold, Topic gate, Dispatch ordering).
Do-it-now gate check: read the block; inspect read-only whatever the
session can verify; discharge or surface the open ◈; if execution is
actually unavailable, reroute to handoff in the same turn
(→ definitions: Gate check).

---

## Phase 6 — Critique offer

Pre-scan: delta ledger since Phase 5 (park re-entry: seed from the
artifact's *Open markers*). Offer strength follows the open set: clean →
soft offer; real problem → one-line named offer; qualifying flag not yet
surfaced → surface it now, then offer. **Full critique only on acceptance**
— flag surfaces are the sole unsolicited delivery
(→ definitions: Interrupt threshold, delivery boundary). Dimensions: tier
gap and its cost · mechanics as stated · one or two highest-leverage
changes · pushback on hard asks (→ definitions: Critique dimensions). End
a delivered critique with the two clearing moves phrased for the route's
terminal step — gate routes: *"go / clean up the vomit"*; park: *"go" =
park as-is* (→ definitions: Clearing scripts + acknowledgment threshold).
Combined instructions ("fix 2, then go") incorporate and clear without
re-offer; non-acknowledgment holds once, then closes unacknowledged.
Reconciliation, when due, fires before held gates release
(→ choreography: Reconciliation). For later-firing scope — what a second
or subsequent Phase 6 scans and critiques —
→ choreography: Cycle accounting.