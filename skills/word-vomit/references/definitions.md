## `references/definitions.md` — Part 1: core definitions

# Definitions — single-topic semantics

Definitions are owned here; the spine points and never restates. Edits land
here only. Gates, multi-topic coordination, and cycle accounting are owned
by `choreography.md` — no gate rule lives in this file.

> **Relocation pass: complete.** Renames applied: *Severe critique interrupt
> threshold* → **Interrupt threshold**; *Non-convergence cause taxonomy* →
> **Non-convergence taxonomy**; all *Cycle invariant* references →
> **Cycle accounting** (choreography.md). All "above / below / next
> definition" relatives resolved to named anchors. The per-phase
> non-convergence handling tables are consolidated into the taxonomy —
> their former in-phase homes were compressed out of the spine, which
> would have left "handling is defined in-phase" dangling. Annex titles
> match spine pointer names verbatim.

---

## Core definitions

### Message boundaries

A message ends at the first beat that requires a user answer — a question, a
confirmation request, a gate. Statement beats (the Phase 1 reflection, the
Phase 2a tier and mode readings, ledger prints, route statements, flag
surfaces) never get a message of their own: each rides at the top of the
message that ends at the next answer-requiring beat. No statement beat is a
silent stop, and none adds a latency turn.

Correction of a statement beat is therefore positional, not sequential: it
sits directly above the question the user is about to answer, so a disputed
reading comes back in that same reply — before the pipeline proceeds on it —
not before the statement shapes the message it opens.

Adjacent beats collapse freely under this rule. The standard Phase 5→6
collapse: ledger print, interrupt surface (if any), route statement, and
critique offer ride one message ending at the offer — one answer-requiring
beat, four statement beats aboard.

### Marker convention

When a structural flag or load-bearing assumption is identified during any
phase, mark it immediately in that response. Do not batch or defer — the
marker goes in the turn where it's identified, at the point in the response
where the issue arises.

Two types:

- **`⚑ Flag:`** — a structural issue that may affect whether the plan works
  or is worth executing: severe tier mismatch, circular dependency, a
  violated constraint, a risk that changes the route. When placed before a
  confirmed output exists, include the basis for the cost estimate in the
  marker itself (basis rules, the route-relative executor, and the legal
  *unknown* value → **Interrupt threshold**).
- **`◈ Assumption:`** — a load-bearing assumption the plan depends on that
  hasn't been validated: something that must be true for the mechanics to
  hold, and that no one has checked.

Each marker is one sentence (plus the projected-cost basis where required).
It is not a separate section — it lives in context, inline with the response
where the issue was spotted. Phase 6 scans for these markers to determine
offer strength. Scans collect and print their result per the **Marker
ledger** (→ **Marker ledger**).

**Trigger conditions** — consult this list at each phase, not only when
something feels notable:

**`⚑ Flag:` fires when:**
- A tier mismatch is identified **and is severe** *(→ **Tier and mismatch
  tables**; the severity gate is canonical at both sites — a mild mismatch
  is stated plainly in the Phase 2a reading and mints nothing)*
- A constraint, dependency, or execution context check would require
  discarding the current direction if it failed — unvalidated, circular, or
  already contradicted *(→ **Discard test**, Phase 4 constraint-check row)*
- Acting on the current direction would waste substantial effort or involve
  irreversible side effects *(→ **Interrupt threshold**)*
- A new fork or premise break has emerged that conflicts with the existing
  output *(→ **Non-convergence taxonomy**, mode-mismatch and
  unresolved-fork rows)*
- A structural risk or conflict materially changes whether the planned
  route is viable

**`◈ Assumption:` fires when:**
- The plan's mechanics require something to be true that hasn't been
  checked or validated
- A forced version invents an answer to fill an unresolved point
  *(→ **Forced version format**)*
- A conditional-proceed at the topic gate is accepted *(→ choreography.md:
  Topic gate)*
- A "do it now" route is selected but execution tooling or environment
  wasn't confirmed during Phase 2 *(→ **Gate check**)*
- Execution context is skipped on a greenfield judgment — the environment
  is assumed to have no relevant prior surface *(→ **Execution context**,
  skip condition)*

**Critique minting:** a Phase 6 critique finding that meets one of the
trigger conditions above mints its marker inline in the critique turn — at
the point where the issue is named, per this convention. Analytical content
that meets no trigger condition stays prose. The trigger list is the
boundary; "this feels important" is not a substitute trigger, and
"analytical content" is not a protected category — a critique finding can
mint if it qualifies. The critique turn is subject to the same "do not
batch or defer" rule as any other turn: markers land at identification, not
in a ledger appended to the critique.

### Marker ledger

The printed product of a marker scan — a materialized view of the current
open marker set. Phase 5's interrupt scan and Phase 6's pre-scan already
compute this set internally; the ledger writes the result down so the next
scan starts from it instead of re-deriving the join from the whole
transcript.

**Format** — fixed anchor header, one line per entry:

```
[Marker ledger — {site}]
⚑ {one-line restatement} — {status}
◈ {one-line restatement} — {status}
```

**Statuses:** **open** (live, unresolved) · **discharged** (validated or
resolved — state how) · **accepted** (user knowingly accepted the risk —
retained as the no-re-trigger record) · **moot** (its premise no longer
exists — state why).

**Empty case prints:** `[Marker ledger — {site}] No open markers.` An
explicit empty result proves the scan ran; absence is ambiguous between
"scanned, clean" and "forgot." (Same principle as `[not gathered]` in the
execution context block.)

**Chain rule:** a scan = **most recent ledger + markers placed or
state-changed since it.** With no prior ledger, lookback runs to session
start — or to the topic's opening ledger (topic transitions →
choreography.md: Topic gate, continue-here rule), or the park artifact's
*Open markers* field (park re-entry).

**Placement is untouched:** "do not batch or defer" stands. Markers are
placed inline at identification; the ledger collects, it cannot create.
Never defer a marker "to the ledger."

**Materialized view, not source of truth:** the transcript is ground truth.
On conflict, the transcript wins and the ledger rebuilds. An older marker
that resurfaces folds into the next ledger with its transcript-derived
status — the chain is self-healing; a missed entry is not propagated
forever.

**Entry lifecycle:** *open* and *accepted* entries persist ledger to
ledger — acceptance is load-bearing state (the no-re-trigger rule and
Later-firing scope, both in choreography.md: Cycle accounting, consume it).
*Discharged* and *moot* entries appear once, in the ledger where the
transition happened, then drop.

**Restatement cap:** an *accepted* entry prints in full once — in the
ledger where acceptance happened. Thereafter it compresses to one
collective line per ledger: `{n} accepted, unchanged (full text: ledger at
{site})`. It prints in full again only in the ledger where a scan actually
consumes it — a no-re-trigger match, a Later-firing scope hit, a state
change — and then only that entry. *Open* entries never compress: each is a
live input to the projected-basis check and to offer strength, and every
scan must dispose of each one individually.

### Interrupt threshold

A flag qualifies for the critique interrupt when acting on the intended
work would waste substantial effort — defined as more than ~30 minutes of
effort by the route's executor — or when it involves irreversible side
effects. **The executor is route-relative:** this session under do it now,
the receiving session under handoff, the user where the work is theirs to
carry out. Before a route exists, the estimate names the executor it
assumes.

In phases before a confirmed output exists, evaluate against the intended
work as described so far and state the basis for the cost estimate in the
flag marker itself (e.g., *"⚑ Flag: [issue]. Projected cost if this
direction proceeds: [brief estimate]."*). **A basis is an anchor, not a
license to invent:** it names what the estimate leans on — the dump's
stated scope, a named system, the assumed route. When nothing yet exists to
anchor on — a Phase 2a tier-mismatch flag can fire before any scope does —
write *"basis: unknown — no scope to estimate against yet."* An
unknown-basis flag qualifies for the interrupt on irreversibility only; its
projection falls due at the first scan with a confirmed output in hand,
where the projected-basis check fills the basis from the actual plan and
the same scan's interrupt clause consumes the result. A stated unknown is
honest input to that check; an invented number poisons it — the
confabulation move the **Felt-sense ladder**'s step 1 exists to catch in
users, not to model for them.

Phase 5 references the flag's stated basis rather than re-deriving the
threshold.

When a flag meets this threshold, surface it in Phase 5 before presenting
the route (one or two sentences only). Route still happens after the flag.
The full critique is offered in Phase 6.

**Delivery boundary — flag surface vs. full critique.** What the interrupt
delivers is a **flag surface**: it names the problem and states its cost
basis — nothing more. No analysis, no recommendations, no editorial
content. The **full critique** is the analytical content — the tier read,
mechanical gaps, highest-leverage improvements, pushback — and it fires
only on solicitation. The principle: **critique requires solicitation; flag
surfaces do not, once a flag meets this threshold.** The
one-to-two-sentence bound is this content limit expressed as length — a
surface that begins analyzing or recommending has crossed into critique
whatever its sentence count. The boundary governs both unsolicited delivery
sites: the Phase 5 interrupt and Phase 6's pre-scan backstop. (The spine's
"explicit and named" offer level is likewise a flag surface — naming
without analysis — so the offer levels and this rule are consistent under
the same boundary.)

**Deadline invariant:** Phase 5 is the designed surfacing site — not the
deadline. The invariant: **every qualifying flag is surfaced before the
execution gate fires.** Phase 5 and Phase 6's pre-scan are two enforcement
points of one deadline, not a sequence that assumes its first step
succeeded. A qualifying flag Phase 5 missed is still caught pre-commitment
when Phase 6's pre-scan finds it — but it must be caught there. (The
**Gate check** reroute's gate-fire ⚑ is the one sanctioned late mint: its
surface is the reroute statement itself, same turn, and execution never
follows that gate.)

On any Phase 5 scan with a confirmed output in hand: check each open
projected-basis flag against the actual plan — fill an unknown basis from
the plan first, then state whether the flag is discharged or confirmed. Do
not re-derive the threshold itself; check the projection against what the
plan actually commits to.

### Re-entry conditions

Three types of correction, each requiring different handling:

**Premise break** — Phase 4 reveals the output was built on a wrong
premise: not a refinement, a broken foundation. Distinguishing test: *if
the user's correction changes what the output is FOR — not just what's in
it — that's a premise break.* Name what failed, say so explicitly, and
re-enter Phase 2 with the corrected premise — from the top: a fresh 2a
tier-and-mode statement against the corrected premise, since both readings
may have been artifacts of the premise that broke. The most recent Phase 2
opener is thereby always the live one. Do not silently patch the existing
output.

On premise-break re-entry, reconcile open markers in the same turn: print a
ledger disposing each open entry as **survives** (stays open; enters the
corrected pipeline's chain) or **moot** (attached to the dead premise).
Without this pass, markers placed against the dead premise resurface at
later scans as live. Format and ordinary corrections change no marker
state — no reconciliation fires.

**Format correction** — the structure is wrong for the content, but the
premise holds. Distinguishing test: *if the correction changes the
structure of what's in the output without changing what it's for, that's a
format correction.* Re-select format per the **Format table**, rebuild the
output, restart the Phase 4 loop against the new version.

**Ordinary correction** — facts, scope, wording. Edit in place within
Phase 4. No re-entry needed.

When the type is unclear, apply the tests above. If still ambiguous, ask:
*"Is this a change to what you want the output to be, or a change to what
you want it to say?"*

### Discard test

A binary test on a pair — **standing referent** and **incoming statement**
— that determines whether the incoming statement can coexist with the
standing referent or requires replacing it.

**Canonical glosses:**
- **Incorporates:** narrows, adds context, specifies further, confirms.
  The standing referent's essential content survives into the next state.
- **Requires discarding:** contradicts, reverses direction, replaces the
  goal type, makes the referent infeasible. The standing referent cannot
  survive.

**Scope:** the test runs on the *desired state* only. A corrected
constraint, timeline, or scope detail is an ordinary correction unless it
makes the desired state itself infeasible — in which case it is a discard
of the desired state, not of the detail.

**Quote-on-apply:** when running the test, quote the standing referent
explicitly in the question. This makes the test auditable — the user sees
what they're being tested against and can correct a stale or misparaphrased
referent on the spot. Referent drift becomes self-catching rather than
silent.

*Cardinality note — explanatory only, not a procedure:* extraction mode
holds exactly one candidate desired state; generative mode holds several
live forks. The forward switch (generative → extractive) is the set
collapsing to one — a statement passes the switching criterion and becomes
the candidate. The reverse switch (extractive → generative) is the one
destabilizing back into several — two consecutive discards mean two
incompatible directions are both live. The discard test detects these
cardinality events.

**Per-site referent table:**

| Site | Standing referent | On incorporates | On requires discarding |
|---|---|---|---|
| **Phase 2b** — extractive-to-generative switch | The **current candidate desired state** — the most recent statement that passed the switching criterion (quotable, holdable) | Candidate survives. If the statement narrows or specifies it, update the candidate accordingly. No switch. | **Replace** the current candidate with the incoming statement. Count the discard. Two consecutive discards — each tested against the candidate current *at the time of testing* — mean the desired state is unstable: switch to generative mode and name it. |
| **Phase 4** — constraint check | What the plan **assumed** about the referenced system, resource, or prior artifact | Ordinary correction — edit in place and continue the diff loop | Surface the conflict in this turn. Mark `⚑ Flag:` naming it. Apply **Re-entry conditions**. |
| **Phase 4** — felt-sense ladder, step 2 | The output's **desired-state element** as written | Ordinary correction — continue localizing or edit in place | Premise-break candidate — escalate to step 4 of the ladder |

**Phase 2b-only rules:**

*Before any candidate exists:* the test is inert — there is no referent to
run it against. Statements accumulate. The first statement that passes the
switching criterion — generative to extractive (quotable, holdable) —
establishes the candidate; the test activates from that point.

*Lean symmetry:* a lean ("I think I want X") cannot establish a candidate
and cannot destroy one. A lean that appears to contradict the current
candidate is a fallback-question event — not a discard-count event.

*Counter semantics:* "successive" means consecutive test runs with a
**requires-discarding** result — an intervening **incorporates** resets the
count to zero. A candidate that absorbed a refinement between two discards
is being sharpened, not thrashed; elapsed time and turn count are
irrelevant — only interposed results matter. The count follows candidate
lineage: replacement-by-discard continues the lineage (it is the thing
being counted); any event that establishes a candidate afresh — the forward
switch, a premise-break re-entry to Phase 2 — starts a new lineage with the
count at zero. Lean events (→ lean symmetry) are not test runs and leave
the count untouched.

### Non-convergence taxonomy

Five distinct causes underlie what might appear as non-convergence.
Identify the cause before proposing any action; the correct response
depends on which it is.

**Trigger:** run this diagnostic when the termination condition is provably
unreachable with what this session can produce — a cause identifiable in
round 1 fires in round 1 — or after multiple rounds without progress.
Round count is the backstop, not the license.

| Cause | Signal |
|---|---|
| **Scope creep** | The scope keeps expanding — answers or corrections add new territory rather than refining existing territory |
| **Mode mismatch** | Desired state keeps reframing rather than refining; or a clear direction has emerged in generative mode without being named |
| **Missing external input** | A specific piece of information is needed to close the gap and doesn't exist in this session |
| **Unresolved fork** | Two incompatible directions are both live and the user hasn't decided between them |
| **Format wrong** | The output structure doesn't match the type of work (Phase 4 only — Phase 2 has no output) |

**Missing external input — canonical handling** (both phase tables point
here): **decidability probe first** — an input the user could supply by
deciding is not missing until they decline to own the decision. Ask before
classifying. Once declined or genuinely external: name the specific input
and its source(s). Always name the force option and its cost — an output
built on an invented, ◈-marked answer (→ **Forced version format**); park
is the recommendation (→ **Park artifact format**).

**Handling per cause — Phase 2:**

| Cause | Handling |
|---|---|
| **Scope creep** | Name it explicitly — expansion, not failure to converge. Ask: commit to the current scope or expand? If expand, update the scope ceiling, clear what's been added, restart the phase against the new scope. Not non-convergence; no forced version offered. |
| **Mode mismatch** | Name the switch. Move to divergent questioning and proceed generatively — or, if extractive intent has crystallized, name the direction and move to convergent questioning. |
| **Missing external input** | → canonical handling (this section). |
| **Unresolved fork** | The output will be an option map, not a plan — the correct exit for this input, not non-convergence. Proceed to Phase 3 in generative mode. |
| **Format wrong** | Does not apply — no output exists yet. If the type of work is genuinely unclear, ask. |

**Handling per cause — Phase 4:**

| Cause | Handling |
|---|---|
| **Scope creep** | Name it explicitly. Ask: commit or expand? If expand, update the scope ceiling and re-present the output against it. No forced version — the scope will keep growing after any forced version too. |
| **Mode mismatch** | A desired state that keeps reframing is a premise break. Mark `⚑ Flag:` naming the premise that broke **in this turn, before re-entering**. Trigger Phase 4 → Phase 2 re-entry (→ **Re-entry conditions**). |
| **Missing external input** | → canonical handling (this section). |
| **Unresolved fork** | A new fork emerged during verification: premise break — mark `⚑ Flag:` naming the fork and what it conflicts with in the current output **before re-entering**. Re-enter Phase 2 with the new fork surfaced (→ **Re-entry conditions**). |
| **Format wrong** | Trigger the format re-entry (→ **Re-entry conditions**). Not non-convergence. |

**Catch-all** — only after the diagnostic fails (no specific cause
identifiable, loop cycling without nameable reason): name that you cannot
locate the cause, and offer the user a choice between forcing a version
(→ **Forced version format**) and parking (→ **Park artifact format**).
A park from either phase is a pre-confirmation exit: in a multi-topic
session the queue check runs first (→ choreography.md: Queue check).

### Park artifact format

When parking — whether at a Phase 2 exit, a Phase 4 park, or the topic
gate — produce this artifact:

```
**Parked: [topic or intent name]**
*Context to re-enter:* [One to three sentences — what this is about, any
relevant dependency on prior outputs, and what would need to be true to
begin Phase 2. Do not summarize prior outputs here — that belongs in a
handoff document if needed. This is just enough to re-invoke the skill
without reconstructing from memory.]

*Depends on prior output:* [yes — briefly how | no]
> When yes: parking suspends any cross-topic reconciliation — it can't run
> until both outputs exist. When you re-invoke the skill for this topic in
> a new session, surface the prior output as context before Phase 2 runs.

*Deferred reconciliation:* [yes — briefly what interaction to watch for | no]

*Open markers:* [ledger lines for entries still open at park | none]
> On re-invocation, these seed the new session's first scan — the
> chain-start alongside the re-entry context.
```

The park artifact is the deliverable. No execution gate fires. The
**topic** closes after the user acknowledges it — the session too, when no
topic remains queued.

*Design position, named:* the *Open markers* field carries **open** entries
only, so acceptance state does not survive a park — a re-invoked session
re-earns acceptance.

### Forced version format

A forced version is **not a distinct artifact type**. It is the Phase 3
format for the type of work — selected per the **Format table**, if Phase 2
hadn't settled one — with every unresolved point marked inline per the
**Marker convention**:

- **`◈ Assumption:`** at each point where the structure required an answer
  that doesn't exist yet. Name the invented answer and what would validate
  it.
- **`⚑ Flag:`** at each point where the unresolved issue is structural — an
  unsettled dependency, constraint, or fork — rather than a missing answer.
  (These are pre-confirmation flags: they carry the projected-cost basis
  per the **Interrupt threshold**.)

Rules:
- Markers are inline. A forced version has no separate "open questions"
  section — the marker convention governs.
- Append **`(forced)`** to the header's first line so the status survives
  into any diff round or handoff.
- A forced version runs the remaining pipeline as normal. From Phase 2's
  catch-all: proceed through Phases 3–4. From Phase 4's: re-present once
  for confirmation. In both cases, **confirming a forced version means the
  open points are correctly named — not that they are resolved.** The
  markers stand through confirmation.
- Its markers enter Phase 5's interrupt scan and Phase 6's pre-scan like
  any others; under the spine's offer levels, a live `◈` the output leans
  on puts the critique offer at "explicit and named" at minimum (later
  firings key on the scope-filtered set → choreography.md: Cycle
  accounting). Forcing trades resolution for motion; it does not trade
  away scrutiny.
- When a forced version routes to handoff, the `/handoff` argument names
  it as forced.

### Execution context

**What it is:** the environmental state an executor needs that does not
come from the plan itself — everything required to orient *where* the work
runs and *what* the executor can touch, before reading the plan's *what*
and *how*. It is distinct from the plan in two ways: it doesn't change when
the plan changes, and a fresh executor needs it *before* reading the plan,
not embedded within it.

**Two-phase capture:**
- **Phase 2 (broad):** gather the environment as a whole. What system does
  this work operate in? What tools and connectors are in the session? What
  prior artifacts exist? Environmental orientation — no plan exists yet,
  so no plan-specific references are expected.
- **Phase 4 (specific):** as plan details surface, fill in exact
  references — precise paths, named services, specific endpoints — and
  apply the constraint check. Phase 4 adds precision; it does not restart
  Phase 2's capture.

**Gather by who holds the fact:** session-side facts — which tools,
connectors, and skills are loaded right now — are directly observable; fill
them into the block unprompted, spending no question on them. Questions go
to user-side facts only: repos and paths, prior artifacts and their
locations, access state, where the output should land. Asking the user to
inventory the session's own tooling burns a clarification slot on something
already in view.

**Skip condition:** greenfield work with no existing surface to reference —
no repos, no prior artifacts, no environmental dependencies. When skipping
on this judgment, mark `◈ Assumption:` that the environment is assumed to
have no relevant prior surface (a listed trigger → **Marker convention**).

**Format and location:** → **Execution context block**.

### Execution context block

A fixed-schema block appended to the verifiable output, separated from the
plan content by a horizontal rule. Its position is always after the plan —
execution context is environmental scaffolding, not part of the plan's
logic, and a fixed location makes it extractable by `/handoff` without
parsing the plan.

```
---
**Execution Context**

**Environment:** [where this runs — local, staging, prod, named cloud env, etc.]
**Repos / paths:** [repos, directories, branches, file paths in scope]
**Tools / connectors / skills:** [session-side — self-filled, never asked]
**Prior artifacts:** [outputs this plan depends on — name, location, status]
**Expected output:** [format, location, or destination of what gets produced]
**Access state:** [what is confirmed available; what still needs to be obtained]
**Notes:** [anything else an executor would block on without knowing]
```

**Fields not gathered:** mark `[not gathered]`, do not omit. An explicit
gap reads as a completed check; an absent field reads as an implicit
confirmation. (*Tools / connectors / skills* is session-side and
self-filled per **Execution context** — it is `[not gathered]` only when
the session genuinely cannot inventory itself.)

**Phase 4 additions:** when Phase 4 surfaces a specific system reference,
add it to the appropriate field in place. Do not create a second block —
one block, updated in place across both phases.

**Forced versions:** if the work is forced, a `[not gathered]` field
converts to an inline `◈ Assumption:` only when the plan leans on that
field — name the invented answer as what the plan assumes of it (*assumed
available*, *assumed unchanged*, *assumed irrelevant to this work*) and
what would validate it, per the forced version format. Fields the plan does
not lean on stay `[not gathered]`: an ungathered irrelevance is a gap, not
a load-bearing assumption, and converting it would inflate the marker set
that offer strength keys on. Gathered fields stay as-is. The block's status
follows the output's.

## `references/definitions.md` — Part 2: phase annexes

*(Append directly after Part 1's `### Execution context block` section.)*

---

```markdown
---

## Phase annexes

*Annex title = spine pointer name, verbatim. Annexes are consulted at pointer
sites, not preemptively.*

---

### Format table

**Naming convention:** the artifact is the *verifiable* output before Phase 4
confirmation and the *verified* output after — one artifact, one state change,
two names. Every use of either term in this file applies this convention; there
is no second artifact.

| Type of work | Format |
|---|---|
| Plan / project | Hierarchical outline with current → desired state framing |
| Technical architecture | Dependency tree or component map |
| Decision | Decision tree or weighted criteria matrix |
| Process / workflow | Step-by-step process map with inputs, outputs, and gates |
| Creative concept | Concept brief: core idea, key dimensions, open edges |
| Problem statement | Problem / solution frame with constraints and success criteria |
| **Intent still forming** | **Option map:** the forks that matter, what each commits the user to, what evidence or decision would resolve each |
| Ambiguous / mixed | Whichever format best isolates the load-bearing structure; state the choice and why |

Every format must make explicit:
- **Current state** — what is true now
- **Desired state** — what the user wants to be true *(or: the live candidate
  states, in generative mode)*
- **The gap** — what has to happen in between
- **Execution context** — appended as the execution context block after the
  plan content, separated by a horizontal rule. Omit only when the skip
  condition applies (→ **Execution context**); otherwise include all fields,
  marking ungathered ones `[not gathered]`.

---

### Headers

Two variants — use the correct one for the mode. `(forced)` is appended to
the first header line for a forced version.

**Extractive mode:**

```
## Intent Verification — [type of work] | [brief subject]
The structure below represents my understanding of what you want.
Look at this and give me your thoughts. Tell me what works and what
doesn't, what feels right and what feels wrong, etc.
```

**Generative mode (option map):**

```
## Intent Verification — Option Map | [brief subject]
The structure below maps the live forks in what you shared — what each
direction commits you to, and what would help decide between them. Tell
me whether I've named the right forks, what's missing or mislabeled,
and where the framing feels off.
```

The output must be specific enough that the user can be *wrong* about it. If
they can't meaningfully declare it off, it isn't verifiable.

---

### Tier and mismatch tables

**Tier table:**

| Tier | Operating at | Native question direction |
|---|---|---|
| **1 — Symptom** | Reacting to a single instance. "This broke, fix this." | What's the broader pattern? Has this happened before? |
| **2 — Task** | A concrete unit of work. "Build this thing." | What does done look like exactly? What are the constraints and dependencies? |
| **3 — Mechanism** | The process that generates the tasks. "Why do we keep having to build these?" | What generates these instances? What would prevent the next one? |
| **4 — Structure** | The constraints and architecture that produce the mechanism. | What structural constraint makes this mechanism necessary? What would have to change for it to disappear? |
| **5 — Frame** | The problem definition itself. "Is this even the right problem?" | What are we actually optimizing for? What would solving the wrong problem look like here? |

The native-question column belongs to the **tier**, not automatically to the
user. The gap decides which move to use:

**Mismatch handling:**

| Gap | Question move |
|---|---|
| **Tiers match** | Use the matched tier's native direction as written. |
| **User below problem tier** | Ask in the native direction of the **problem's** tier. The user's row says where they are; the problem's row is where the questions pull. |
| **User above problem tier** | Ask **downward — ground the work:** *"What specifically needs to exist at the end? What would you have in your hands when this is done? What are the actual constraints — not the principles, the specific ones that apply here?"* Do not use the user's row — its native direction points further up. |

**Severity gate — canonical:** `⚑ Flag:` fires on a tier mismatch only when
it is **severe**. State the mismatch plainly in the Phase 2a reading regardless
of severity; the flag fires on severity alone. This is the canonical rule at
both sites — the trigger list in **Marker convention** ("and is severe") and
the spine's Phase 2a body. A mild mismatch (one tier, navigable by a single
grounding question) is stated but not flagged. A severe mismatch (two or more
tiers, or a one-tier gap where acting on the wrong framing would waste
substantial effort or produce irreversible output) is stated and flagged with
projected cost basis (→ **Interrupt threshold**).

---

### Switching criteria

**Mode question:** read the dump for the mode first. State the read alongside
the Phase 2a tier reading (→ **Message boundaries** — same message, same
correction path). Ask directly only when signals remain genuinely ambiguous
after reading. When needed:

> *"Do you already know what you want to be true at the end of this, or are
> you still working that out?"*

Weigh the dump's behavior over its self-description. *Directional pull* is
the distinguishing signal: if questions are rhetorical and the dump points
consistently in one direction, lean extractive; if questions are genuinely
open and the dump pulls toward multiple incompatible outcomes, lean generative.
A misread is not load-bearing: the criteria below exist to catch it in motion.

---

**Switching criterion — generative to extractive:** a statement that names a
specific outcome and could be quoted back to the user without protest. The
test: could you hold them to it?

- "I think I want X" is a lean — leans can't trigger the switch and can't
  destroy a candidate.
- "I want X" is a candidate.
- When uncertain, ask.

When the switch occurs, say so explicitly and name the triggering statement as
the **current candidate desired state**. Move to convergent questioning. The
candidate is now the standing referent for the discard test.

**Intermediate test (example move):** when the first quotable statement arrives
early — before the clarification loop has run — probe before triggering:

> *"Is that a lean, or would you hold to it?"*

The switch fires on the confirmed answer, not on the probe. This prevents a
first-impression answer from collapsing the generative mode prematurely. On
confirmation, state the switch and move; on "that's a lean," continue
generative questioning as normal.

---

**Switching criterion — extractive to generative:** apply the **Discard test**
against the current candidate desired state (→ **Discard test**, Phase 2b row
— for counter semantics, lean symmetry, and pre-candidate inertness).

A single reframe may be a late correction rather than a mode signal. When
uncertain, quote the candidate: *"Does [current candidate] still hold — or
does [new statement] replace it?"* When a second correction also requires
discarding, name the switch and move to divergent questioning.

---

### Signal table

One to three questions per round, prioritized by what most changes the
output's format or substance.

| Signal | What to gather |
|---|---|
| **Current state** | What exists right now? What's been tried? What's the context? |
| **Desired state** | What does the user want to be true when this is done? *(Generative mode: the candidate desired states, and what would decide between them.)* |
| **Type of work** | Plan, decision, technical design, process, creative concept, problem statement, or mixed? |
| **Constraints** | Hard limits — time, resources, dependencies, non-negotiables |
| **Scope** | How deep does this need to go? What is explicitly out of bounds? |
| **Execution context** | Repos, file paths, environment, prior artifacts, expected output format. Phase 2 is the broad pass — gather environment as a whole. Session-side facts self-fill; spend questions on user-side facts only (→ **Execution context**). |

**When to gather execution context:** when the work touches existing systems or
depends on prior artifacts. Greenfield with no existing surface: skip, and mark
`◈ Assumption:` noting that the environment is assumed to have no relevant
prior surface. Work an executor would block on without environmental knowledge:
gather now.

---

### Felt-sense ladder

"This feels wrong but I can't say why" is valid diff input. Do not treat the
round as inconclusive until this ladder runs to exhaustion.

**Default sequence:** 1 → 2 → 3 → 4. **Forward-skips** permitted only when a
step's output already exists: a self-localized reaction (user names *which
element* while voicing it) skips to step 3; a named-but-unverified reason
skips to the confabulation check in step 1. Never skip backward.

**Step 1 — Gate: name it or surface it**

*"Can you point at precisely what's wrong? If you can't, say so — that's
useful information too, and we'll locate it a different way."*

Legitimizing failure is not optional: without it, users confabulate a reason
rather than admitting they can't find one, and a confabulated correction is
worse than a vague one because it gets incorporated as though true.

- **They name it** → confabulation check before incorporating:
  *"If I fixed [named thing], would the wrongness be gone?"*
  - **Yes** → ordinary diff input. Classify per **Re-entry conditions** and
    proceed.
  - **"No, something would still be off"** → the named reason is partial or a
    proxy. Carry it as a localization hint; drop into step 2.
- **They can't name it** → step 2. State that this is why they're receiving
  structured options rather than another open prompt.

**Step 2 — Section triangulation**

> *"Where does the wrongness sit closest: what I said is true now, what you
> want to be true, how we get between them, or the environment and context?
> Or is it the whole thing — none of those?"*

State "the whole thing" as an explicit option, not a trailing fallback.
Then classify:

| Localizes to | Likely classification |
|---|---|
| Current state | Ordinary correction — factual |
| Desired state | **Discard test** against the output's desired-state element (→ **Discard test**, Phase 4 — felt-sense ladder row): incorporates → ordinary; requires discarding → premise-break candidate |
| The gap / steps | Ordinary — or format if the *shape* of steps is wrong rather than their content |
| Execution context | Ordinary — or triggers the Phase 4 constraint check if it implicates a system's actual state |
| "The whole thing" / won't localize | Premise-break candidate — skip to step 4 |

**Step 3 — Contrast probe within the implicated section**

> *"If [element] instead said [variant] — closer to right, or further?"*

One perturbation per question. Movement signals direction; treat it as a
direction signal and continue the loop. "Both feel wrong" or no movement
at this depth → step 4.

**Step 4 — Premise test (terminal)**

> *"I've been building this as [X, for Y]. Is that the wrong target?"*

- **Wrong target** → premise break. Mark `⚑ Flag:` naming the failed premise
  **in this turn**. Apply **Re-entry conditions**.
- **Target confirmed, wrongness still unlocated** → the round is genuinely
  inconclusive. Name this explicitly — do not silently continue iterating.
  A confirmed-target felt sense that won't localize at step 4 is most often
  a mode-mismatch signal; identify the cause before proposing action
  (→ **Non-convergence taxonomy**).

**Bound:** steps 2 and 3 together are two or three questions maximum before
step 4 fires. The premise test is one sentence; it should not sit behind an
extended perturbation loop.

---

### Fork selection

Fires in Phase 4 when an option-map fork is selected. Two steps before routing.

**Step 1 — Confirm the decision and its commitments**

> *"You've chosen [fork]. That commits you to [what Phase 3 said it commits
> them to]. It rules out [the alternatives]. Is that right?"*

If any stated commitment depends on an external condition not yet validated —
a resource that must exist, an API that must work, a person who must agree —
mark `◈ Assumption:` naming it at the point in the confirmation where the
commitment appears.

One-round check — not a new loop. If the user corrects it, revise and
re-confirm once. If they confirm, proceed.

**Step 2 — Deliverable or input?**

> *"Is the decision itself what you needed — or do you want to turn this into
> a plan now that you've chosen?"*

- **Decision is the deliverable** — **fork-as-deliverable** path: route to
  Decided Fork in Phase 5. The output is a decision record: (1) fork selected,
  (2) what it commits the user to, (3) what was ruled out and why, (4)
  execution context if gathered. The execution gate offers planning-accepted
  (opens a new cycle → choreography.md: Cycle accounting) or park.

- **Decision enables a plan** — **fork-as-input** path: state the mode switch
  (generative → extractive) and return to Phase 3, using the selected fork as
  the new basis; select a plan-appropriate format per the **Format table**;
  run Phase 4 fresh against the new output. Firing accounting →
  choreography.md: Cycle accounting.

---

### Gate check

Runs when the execution gate fires, before execution begins.

Read availability off the execution context block — the *Tools / connectors /
skills* and *Access state* fields — rather than re-judging from memory.

**Inspection:** whatever the session can verify directly — a tool that is
loaded, a file path that lists, an artifact that opens — verify at gate-fire
by read-only inspection (nothing that mutates state runs before the gate
clears). Fill verified values into the block in place; discharge and note any
open `◈` resolved by inspection, stating how. The discharged entry appears in
the current ledger and drops in subsequent ones.

**User-pre-provided values:** if the user supplied a required value alongside
the Phase 6 clearing response — a DSN, a credential, a token — treat it as
obtained at gate-fire. Discharge the `◈`, naming the source (*"pre-provided by
user in clearing response"*), without re-asking.

**What inspection cannot reach:** credentials not yet exercised, external
services, anything user-side — stays open. State it at the gate and put the
question to the user rather than proceeding silently. A `[not gathered]` in
*Tools / connectors / skills* or *Access state* means the route-selection `◈`
is still open: state it at the gate rather than proceeding.

**If execution is actually unavailable** — a required capability is missing
from this session — do not improvise a degraded execution. Reroute to
**hand it off** in the same turn:

- Discharge the `◈` and mark `⚑ Flag:` naming the unavailable capability —
  "materially changes whether the planned route is viable" is a listed trigger
  (→ **Marker convention**). Both entries land in the current ledger.
- Derive the `/handoff` argument per the **Handoff argument** annex, plus one
  clause naming what was unavailable here, so the receiving session verifies
  availability first.
- **No new firings** — the confirmed output is unchanged; only the route moved
  (→ choreography.md: Cycle accounting).

*Deadline invariant edge:* this `⚑` mints at gate-fire, not before — but the
reroute statement is its surface, in the same turn, and execution never follows
that gate. The invariant's intent (nothing commits unsurfaced) holds.

---

### Clearing scripts + acknowledgment threshold

**Clearing scripts — phrased for the route's terminal step:**

End every delivered critique by naming both clearing moves.

**Routes with an execution gate** (do it now, hand it off, decided fork):

> *"Say **go** to proceed as-is, or **clean up the vomit** to fold this into
> the output first."*

**Park** (no gate — the park artifact is the terminal step):

> *"Say **go** to park this as-is — I'll produce the park artifact and this
> topic closes there — or **clean up the vomit** to fold this in first, so
> what re-enters later re-enters clean."*

---

**Acknowledgment threshold:**

- **"go"** — or most explicit affirmative acknowledgments (*"got it, proceed,"
  "makes sense, move on," "noted — go ahead"*). The taught phrases are the
  interface, not a passphrase check.
  - *At the offer stage* (before the critique has been delivered): a bare "go"
    is a decline — same-turn clear; no gate fires.
  - *After critique delivery:* clears Phase 6; unincorporated points stand as
    the user's accepted risk; the route's terminal step runs.

- **"clean up the vomit"** — or any clear request to incorporate, including
  partial ones (*"fix the second point, skip the rest"*). Does **not** clear
  yet. Fold the named points into the output: ordinary corrections as a Phase
  4 round; a premise or format break per **Re-entry conditions**
  (→ choreography.md: Cycle accounting governs what re-fires). The cleaned
  output's Phase 6 scopes per Later-firing scope to the incorporated points —
  so that offer is typically one line.

- **Combined instruction** (*"fix 2, then go"*): incorporate the named points,
  present the cleaned output, clear without re-offering.

- **Not acknowledgment:** silence, a topic pivot, or an ambiguous reaction
  (*"interesting," "hm"*). Hold the gate; restate the two moves once, one
  line. If the user pivots past that too: note briefly that the critique stands
  unacknowledged and the route's terminal step never ran — no gate fired; for
  park, no artifact was produced — then follow their new direction rather than
  blocking.

---

### Critique dimensions

When the critique offer is accepted. Never softened to make it easier to
decline; never delivered unsolicited — flag surfaces are the sole unsolicited
delivery (→ **Interrupt threshold**, delivery boundary).

**1. Cognitive tier**

Name the user's tier, the problem's tier, and the cost of the gap. A matched
tier is worth confirming, not skipping.

Mismatch cuts both ways:
- **Too low:** patching symptoms of a structural problem. The fix works once
  and the problem returns. Signal: the user has done this before.
- **Too high:** theorizing about frame and structure when the actual need is a
  concrete action taken today. Signal: no artifact would exist at the end.

**2. Mechanics as stated**

Does the plan work *as described*? Name logical gaps, circular dependencies,
and unstated load-bearing assumptions — things that must be true for the
mechanics to hold and that nobody has checked.

**3. Highest-leverage improvements**

The single change that most alters the outcome — specifically the one the
current framing most obscures. If a second change is genuinely distinct and
comparably important, name it. Stop there.

**4. Pushback on hard asks**

Asks that are underspecified, harder than stated, or that quietly assume
something unvalidated. Name the implicit assumption out loud. Do not soften.

---

### Handoff argument

*Supplementary — no spine pointer; the spine's Phase 5 hand-it-off row carries
the essentials inline. Consult this for detail when composing.*

**What the argument names:** type of work and desired state, one to three
sentences. A bare `/handoff` produces a generic document; a targeted argument
produces a targeted one.

**What rides with the verified output, not in the argument:**

- The execution context block — already a distinct, extractable section; do not
  compress it into the argument. It carries environmental orientation; the
  argument carries intent.
- The current marker ledger — appended after the execution context block, same
  extractability rationale. Surviving assumptions and flags ride into the
  handoff as ledger entries, not as ad-hoc clauses.

**Recommended position in the handoff document:** execution context after the
objective/intent block, before the plan content — a fresh model needs
environmental orientation before reading the plan. This is a recommendation to
pass to the user when invoking `/handoff`; that skill owns its own structure.

**Special cases:**

- **Forced version:** name it as forced in the argument, so the receiving
  session opens knowing the open points are correctly named but unresolved.
- **Unavailability reroute** (gate check discovers a missing capability and
  reroutes): add one clause naming what was unavailable here, so the receiving
  session verifies availability first.
- **Multi-topic dispatch ordering** (→ choreography.md: Dispatch ordering):
  arguments state resolved dispositions only — executed, dispatched, parked,
  declined — never a merely-stated route. Two handoffs in flight each name
  their ordering in one argument clause, so neither receiving session assumes
  the other's work is already done.

**Model tier and effort** for the receiving session are `/handoff`'s call — do
not specify them in the argument.