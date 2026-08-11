# Worked example 2 — generative path, multi-cycle

> **Print vocabulary:** dependency record · marker ledger (opening/scoped/
> queue-check variants) · [Queue check] block. These and no others. Every
> state print in this transcript is one of the three. An edit introducing a
> fourth is a normalization error → spine: priority hierarchy, rung 5.

**How to read this file.** `USER` blocks are user input; `MODEL` blocks are
the model's visible reply; `⚙` blockquotes are executor-facing annotations
citing the rule that licenses the beat — they are never part of a reply.
Citations: *spine* = SKILL.md · *definitions* = references/definitions.md ·
*choreography* = references/choreography.md.

**Scenario.** One dump, one topic: error visibility in tgd-api. Intent is
forming — three directions live, two survive Phase 2. After an option map and
fork selection (fork-as-deliverable path), the session produces a decision
record, accepts planning, and executes a Sentry integration in-session. Two
cycles: Cycle 1 ends at the decision record; Cycle 2 ends at execution.

**Coverage.** Generative mode · option map · fork-as-deliverable path ·
decision record · later-firing Phase 6 · do-it-now gate check · switching-
criterion intermediate test · combined instruction. Not exercised here:
multi-topic protocol, pre-confirmation park, queue check, reconciliation,
premise-break re-entry, forced versions, discard test under pressure.

## Mechanism index

| Mechanism | Fires at | Owner |
|---|---|---|
| Tier + mode co-statement; mild upward mismatch — stated, no ⚑ | Phase 2a | definitions: Tier and mismatch tables · definitions: Message boundaries |
| Mode question — ambiguous signals | Phase 2a | definitions: Switching criteria |
| Divergent then eliminative questioning | Phase 2c | spine: Phase 2b |
| Switching-criterion intermediate test | Phase 2c round 2 | definitions: Switching criteria |
| Mode switch: generative → extractive | Phase 2c round 2 | definitions: Switching criteria |
| Option map, generative header | Phase 3, Cycle 1 | definitions: Format table · definitions: Headers |
| Option-map loop: correction, then fork selected | Phase 4, Cycle 1 | definitions: Fork selection |
| Commit confirmation + ◈ on conditional commitment | Fork selection, step 1 | definitions: Fork selection |
| Fork-as-deliverable path | Fork selection, step 2 | definitions: Fork selection · choreography: Cycle accounting |
| Decision record at Decided Fork | Phase 5, Cycle 1 | choreography: Cycle accounting |
| Phase 6 first firing — explicit and named | Phase 6, Cycle 1 | spine: Phase 6 · definitions: Interrupt threshold |
| Critique minting boundary — findings stay prose | Phase 6, Cycle 1 | definitions: Marker convention |
| Combined instruction → incorporate + clear, no re-offer | Phase 6 → Phase 4, Cycle 1 | definitions: Clearing scripts + acknowledgment threshold |
| Gate Cycle 1 → planning accepted → new cycle | Execution gate, Cycle 1 | choreography: Cycle accounting |
| State test: confirmed record upstream → later firing | Phase 6 pre-scan, Cycle 2 | choreography: Cycle accounting |
| Phase 3 plan format, Phase 4 fresh | Cycle 2 | choreography: Cycle accounting |
| ◈ minted at route statement (after Phase 5 ledger) | Phase 5, Cycle 2 | choreography: Ordering spine · definitions: Marker convention |
| Phase 6 Cycle 1 pre-scan: delta-only print, no change | Phase 6, Cycle 1 | choreography: Cycle accounting |
| Phase 6 Cycle 2 pre-scan: delta print + scope-filtered offer (later-firing) | Phase 6, Cycle 2 | choreography: Cycle accounting |
| Gate check: self-fill · inspect · user-pre-provided value | Execution gate, Cycle 2 | definitions: Gate check · definitions: Execution context |
| Single-topic session close | Session end | definitions: Park artifact format |

---

## Phase 1 — Absorb

**USER**

```
/word-vomit okay so we keep getting support emails from users about things
going wrong and we can't reproduce any of it. our logging is basically useless
— timestamps and status codes, that's it. i've been going back and forth all
week. options are like: add sentry, write better logs, write better error
messages so users can actually tell us what happened. but maybe those are all
the wrong framings. i honestly don't know what right looks like here and i
don't want to just cargo-cult whatever the Continuing from the cut — Phase 1 USER block through Phase 2 mode switch. Subsequent pieces follow.

---

**Piece 1 of 5 — Phase 1 through Phase 2 mode switch**

````markdown
last dev blog i read recommended.
```

**MODEL**

**Phase 1 — Absorb**

This is about error visibility: production errors are unreproducible from
support emails because current logging is too thin to reconstruct what
happened. One topic.

---

## Phase 2 — Mode + clarify

**MODEL**

**Phase 2a — Tier and mode read**

Tier: you're at Tier 3 — asking about the mechanism that keeps generating
support emails. The problem lives at Tier 2: a concrete capability needs to
exist (when an error occurs, you can see what happened). One tier above; right
move is downward: what would you actually have *in your hands* when this is
done?

Mode: genuinely ambiguous — the dump lists three directions and then questions
all of them. Going generative and asking directly:

> Do you already know what you want to be true at the end of this, or are
> you still working that out?

Three questions, aimed at the problem's tier:

1. When a user emails you "I got an error" — what do you *wish* you had in
   front of you right now?
2. Is the goal to see errors *before* the email lands, or to understand them
   better *after*?
3. What's the most important thing this *doesn't* become — what failure mode
   are you most trying to avoid?

> ⚙ Definitions, Tier and mismatch tables — severity gate: a one-tier upward
> gap is mild; state plainly, no ⚑ (doesn't clear the threshold condition).
> Ask downward per the user-above-problem row. Definitions, Message
> boundaries: both reads, the mode question, and round-1 questions ride the
> same message. Definitions, Switching criteria: signals genuinely ambiguous
> after reading the dump → ask directly.

**USER**

```
1. Stack trace and what the request looked like. That's it.
2. Before. I don't want to be sitting there reacting after the fact.
3. Don't want to add infrastructure I have to maintain. Keep it lean.
```

**MODEL**

Before I lock it in: "stack trace and request context before the email lands"
— is that a lean toward what you want, or a statement you'd hold to?

> ⚙ Definitions, Switching criteria — intermediate test: round-1 answers are
> specific and quotable ("That's it"). Probing before triggering — the switch
> fires on a confirmed declaration, not a first-impression answer; this
> prevents generative mode from collapsing prematurely on early convergent-
> sounding language.

**USER**

```
That's the goal. I'd hold to it.
```

> ⚙ Definitions, Switching criteria: "That's the goal. I'd hold to it." is a
> confirmed declaration. Mode switch: generative → extractive. Current
> candidate desired state established: *when an error occurs in tgd-api, you
> see the stack trace and request context before the user emails.* Switch
> stated; moving to eliminative questioning.

**MODEL**

Got it. One more to narrow things: the three directions you named — Sentry,
better logs, better error messages — are they all still live, or has anything
already ruled itself out for you?

**USER**

```
Error messages is a different problem — that's what the user sees, not what
I see. Out. The other two are live. Though "better logs" is vague — could
mean adding more console.errors or could mean a whole structured logging
library.
```

> ⚙ Three distinguishable forks visible: additive logging · structured
> logging · Sentry. Termination condition for an option map met — no invented
> answers needed. Spine, Phase 2b: unresolved fork → "proceed to Phase 3 in
> generative mode" with an option map.
````

---

**Piece 2 of 5 — Phase 3 (option map) through fork selection**

````markdown
---

## Phase 3 — Option map (Cycle 1)

**MODEL**

```
## Intent Verification — Option Map | Error Visibility

The structure below maps the live forks in what you shared — what each
direction commits you to, and what would help decide between them. Tell me
whether I've named the right forks, what's missing or mislabeled, and where
the framing feels off.

**Desired state (confirmed):** when an error occurs in tgd-api, you see the
stack trace and request context before the user emails.

---

### Fork A — Additive logging
*More console.error calls at error sites with structured context: request ID,
user ID, error shape, stack.*

**Commits you to:** reading raw platform logs to diagnose. You find the
errors; they don't find you.

**Rules out:** automatic grouping, alerting, trend visibility.

**Lean toward this if:** you're already in logs regularly; errors are rare
enough to hunt manually; zero new dependencies is the priority.

---

### Fork B — Structured logging foundation
*Introduce a logging library (Pino); consistent schema; queryable locally;
aggregator optional later.*

**Commits you to:** 1–2 days of upfront integration; schema decisions that
compound in value if the team grows.

**Rules out:** automatic error grouping without a separate aggregator.

**Lean toward this if:** logging will be a recurring surface — for a future
hire, or your own long-term debugging workflow. Ahead of need if you're solo
and errors are still infrequent.

---

### Fork C — Error tracking service (Sentry)
*SDK integration; errors captured automatically with stack traces and full
request context; grouping and alerting built in; dashboard outside the
codebase.*

**Commits you to:** one external dependency; free tier generous at low volume
(~$0 for < 5k events/month); one init call plus two Express middleware lines.

**Rules out:** nothing — compatible with any logging approach.

**Lean toward this if:** you want the confirmed goal met in an afternoon and
you're comfortable with one external service.

---

**The real question:**
Do you want to *find* errors yourself (A or B) — or do you want errors to
*find you* (C)?
```

> ⚙ Definitions, Format table: option map for intent still forming.
> Definitions, Headers: generative-mode header. Execution context block
> omitted — judgment call: in the fork-as-deliverable path, the option map is
> consumed as the decision's basis and never routes through Phase 5
> (→ choreography: Cycle accounting, option-map exits). A block here would
> be entirely [not gathered] with no actionable content before a fork is
> selected; the decision record's block (Phase 5, Cycle 1) is the first
> formal environmental capture.

---

## Phase 4 — Cycle 1: option map loop

**USER**

```
"Found by them" — yes, that's exactly it. C. But one note: Forks A and B
aren't really exclusive from C — you could do A as well eventually. Should
that be in the map?
```

**MODEL**

A as a future addition doesn't change the fork selection and doesn't belong
in the map — the map surfaces what commits you to *different things*, and
A-later-with-C commits you to the same thing as C-alone plus more work.
Keeping the map clean; it can go in the plan as a future note.

Confirming: **Fork C selected.** Moving to the fork selection protocol.

---

**Fork selection protocol — step 1: confirm commitments**

You've chosen Fork C (Sentry). That commits you to:
- `@sentry/node` SDK in tgd-api
- One external dependency (Sentry's infrastructure)
- Free tier: $0 for < 5k error events/month

◈ Assumption: error volume stays under the free tier threshold. What would
validate: check Sentry's current free tier terms; re-evaluate at launch if
error frequency is unexpectedly high.

It rules out nothing — Sentry coexists with any logging you add later. Is
that right?

> ⚙ Definitions, Fork selection, step 1: commit confirmation with ◈ on the
> conditional commitment (free tier threshold — an external condition not yet
> validated). One-round check; if corrected, revise and re-confirm once.

**USER**

```
Yes, that's right.
```

---

**Fork selection protocol — step 2**

Is the Sentry decision itself what you needed — or do you want to turn this
into a plan now that you've chosen?

**USER**

```
Both. The decision is what I needed first — but yes, let's plan it too.
```

> ⚙ Definitions, Fork selection, step 2: "the decision is what I needed
> first" → fork-as-deliverable path. Choreography, Cycle accounting: one set
> of firings for the decision record; a second, scoped set for the plan if
> planning is accepted at the record's execution gate. The option map is
> consumed as the decision's basis — it is not routed as an output and never
> reaches Phase 5.
````

---

**Piece 3 of 5 — Phase 5 Cycle 1 through Phase 6 Cycle 1 (including critique)**

````markdown
---

## Phase 5 — Cycle 1

**MODEL**

```
[Marker ledger — Phase 5 / Cycle 1]
◈ Sentry free tier threshold — open: error volume assumed < 5k/month;
  re-evaluate at launch
```

**Route: Decided Fork.**

```
## Decision Record — Error Visibility Approach

**Decision:** Fork C — Sentry error tracking service

**Commits to:**
- @sentry/node SDK in tgd-api
- Free tier ($0, < 5k error events/month)
- Errors automatically captured with stack traces and request context

**Ruled out (and why):**
- Forks A and B (logging-first): both require actively finding errors —
  they don't meet the confirmed goal of being notified before the email

**◈ Open:** free tier threshold — to re-evaluate at launch

---
**Execution Context**

**Environment:** tgd-api
**Repos / paths:** [not gathered — integration path TBD until plan is built]
**Tools / connectors / skills:** [self-filled at runtime]
**Prior artifacts:** none relevant to this integration
**Expected output:** Sentry capturing errors with stack traces and request
  context in tgd-api
**Access state:** Sentry DSN — [not gathered]; Sentry project must exist
  first (user-side prerequisite, Step 0)
**Notes:** [not gathered — to be filled during planning]
```

Moving to Phase 6.

> ⚙ Choreography, Cycle accounting: the decision record is the confirmed
> output for Cycle 1 — one Phase 5/6 set fires for it. The free-tier ◈
> entered the session at fork selection step 1; this is its first ledger
> print. The context block is provisional — specifics surface in Cycle 2's
> Phase 4. "Notes: [not gathered]" is correct; no execution specifics are
> known before the plan is built.

---

## Phase 6 — Cycle 1: first firing

**MODEL**

```
[Phase 6 pre-scan — Cycle 1]
No change since Phase 5 ledger.
Full open set: ◈ Sentry free tier threshold — open
```

There's something structural I'd push on before you act on this — beyond the
free tier assumption. Want the full read?

> ⚙ Spine, Phase 6: open ◈ (unvalidated assumption the output leans on) →
> explicit and named offer. The one-liner names a structural issue (mechanics
> gaps in the decision record) detected in the pre-scan analysis — naming
> without analysis, per definitions: Interrupt threshold, delivery boundary.
> Choreography, Cycle accounting — state test: no confirmed decision record
> upstream; this is the session's first cycle → first firing, full scope.

**USER**

```
Yes.
```

**MODEL**

**Critique — Decision Record: Error Visibility**

**1. Cognitive tier**

The decision is right at Tier 2 — a concrete thing now exists to build. The
Tier 3 question you walked in with doesn't fully go away: Sentry tells you
*what* failed; it doesn't tell you whether you can reproduce the conditions
locally. If the errors are environmental — timing-dependent, user-state-
dependent — Sentry gives you everything you need. If dev/prod parity is the
underlying issue, you'll have the stack trace and still not be able to
reproduce it. Worth treating as a live question after you see the first few
events, not an assumption to make now.

**2. Mechanics as stated**

"Errors captured with stack traces and request context" is true — but not
with just `Sentry.init()`. Request context (headers, user ID, request body
shape) requires two Express middleware calls: `Sentry.Handlers.requestHandler()`
before all routes, and `Sentry.Handlers.errorHandler()` after all routes and
before any other error-handling middleware. A minimal integration missing
these captures stack traces but not request context — half the confirmed
goal. These need to be explicit named steps in the plan, not assumed.

**3. Highest-leverage improvement**

Make the handler ordering non-negotiable in the plan. `errorHandler` must be
*after all routes* and *before any existing error middleware* — that placement
is the most common integration mistake and the one most likely to produce a
"Sentry isn't capturing anything" debugging session.

**4. Pushback**

The decision record has no "Step 0." Creating the Sentry project and obtaining
the DSN is a user-side prerequisite that must happen before any integration
code runs. It's not in the record, and it can't be done in-session. It needs
to be the first named step in the plan.

---

Say **go** to proceed with the record as-is, or **clean up the vomit** to
fold any of this in first.

> ⚙ Definitions, Clearing scripts: gate-route variant (decided fork has an
> execution gate). Definitions, Critique dimensions: all four dimensions
> delivered. Definitions, Marker convention — critique minting: checked —
> handler-order and Step-0 findings are mechanical gaps in the decision
> record; neither meets a ⚑ or ◈ trigger (the record commits to nothing that
> depends on them; they belong to the plan, which doesn't exist yet).
> Findings stay prose.

**USER**

```
Fold in points 2 and 4 (handlers as explicit steps, Sentry project as
Step 0). Point 1 I'm accepting — probably environmental, can't know yet.
Then go.
```

> ⚙ Definitions, Clearing scripts + acknowledgment threshold — combined
> instruction: incorporate points 2 and 4 as ordinary Phase 4 corrections;
> clear without re-offering. Point 1 explicitly accepted — prose; triggers no
> ◈ (the plan makes no commitment that depends on it). "Then go" is the
> acknowledgment; the gate fires after incorporation.

**MODEL**

**Incorporating:**

Decision record updated:

- *Step 0 (prerequisite, user-side):* create Sentry project at sentry.io;
  obtain DSN before integration begins
- *HTTP handlers required:* `Sentry.Handlers.requestHandler()` before all
  routes; `Sentry.Handlers.errorHandler()` after all routes, before any
  existing error-handler middleware — without both, request context is not
  captured, only stack traces
- *Accepted risk:* dev/prod parity may be a secondary issue; investigate
  after first Sentry events

Phase 6 clears. **Execution gate — Cycle 1.**
````

---

**Piece 4 of 5 — Execution gate Cycle 1 through Phase 5 Cycle 2**

````markdown
---

## Execution gate — Cycle 1

**MODEL**

The Sentry decision is confirmed and the record is clean. Want me to build
the integration plan now?

**USER**

```
Yes.
```

> ⚙ Choreography, Cycle accounting: planning accepted — new cycle opens.
> Mode: extractive (fork decided, desired state clear). Decision record is
> the current-state anchor; the confirmed commitment is the desired state.
> Phase 3 selects plan format per definitions, Format table. State test for
> Cycle 2's Phase 6: a confirmed decision record now exists upstream in this
> topic → later firing.

---

## Phase 3 — Cycle 2: plan

**MODEL**

```
## Intent Verification — Plan | Sentry Integration (tgd-api)

**Current state:** No error tracking. Logs contain timestamps and status
codes only. Errors unreproducible from support emails.

**Desired state:** Unhandled errors in tgd-api automatically captured by
Sentry with stack traces and full request context (user ID, request shape).
Error appears in Sentry before the support email lands.

**Gap — what has to happen:**

0. *Prerequisite (user-side):* create Sentry project; obtain DSN
1. npm install @sentry/node
2. Create src/lib/sentry.js — Sentry.init({ dsn: process.env.SENTRY_DSN })
3. Import src/lib/sentry at the top of the Express app entry point,
   before anything else
4. Mount Sentry.Handlers.requestHandler() before all route handlers
5. Mount Sentry.Handlers.errorHandler() after all routes, before any
   existing error-handler middleware
6. Append SENTRY_DSN= to .env file; add real value to production env
   (not committed to repo)
7. Smoke test: throw a deliberate error; confirm it appears in Sentry
   with request context populated

---
**Execution Context**

**Environment:** tgd-api, local dev + production
**Repos / paths:** [not gathered — inspect at gate]
**Tools / connectors / skills:** [self-filled at runtime]
**Prior artifacts:** Decision Record — Error Visibility (this session)
**Expected output:** Sentry initialized; handlers mounted; DSN in env;
  smoke test confirms request context capture
**Access state:** Sentry DSN — [not gathered; Step 0 user-side];
  production env write access — [not gathered]
**Notes:** Step 5 placement is the most common integration mistake — must
  be after all routes, before any existing error middleware; inspect
  src/app.js at gate-fire to target precisely
```

---

## Phase 4 — Cycle 2

**USER**

```
Entry point for Express setup is src/app.js; src/server.js is the listen
call. Sentry init goes at the top of src/app.js. And we already have
.env.example — just append to it, don't create a new one.
```

**MODEL**

**Phase 4 — incorporating**

Updating execution context block in place:

- **Repos / paths:** `src/app.js` (Express setup; init site) · `src/server.js`
  (listen — not modified) · `src/lib/sentry.js` (new file, step 2)
- Step 3 clarified: import `./lib/sentry` at top of `src/app.js`, before
  route registration
- Step 6 revised: "Append `SENTRY_DSN=` to existing `.env.example`"

Anything else?

**USER**

```
No, that's it.
```

**MODEL**

Confirmed. Anything the verification pass surfaced that's still unresolved?

**USER**

```
No.
```

> ⚙ Spine, Phase 4: explicit confirmation — "no, that's it" closes the
> correction; "no" closes the post-confirmation question. Two beats.

---

## Phase 5 — Cycle 2

**MODEL**

```
[Marker ledger — Phase 5 / Cycle 2]
Chain from: Phase 6 pre-scan / Cycle 1 + markers since

◈ Sentry free tier threshold — discharged: the plan makes no commitment
  contingent on the threshold; the accepted-risk note in the decision record
  covers the launch-time re-evaluation. No plan constraint to evaluate.
```

**Route: Do it now.** Seven focused steps in one repo; no multi-session need;
this session has file-edit and execution capability. Conditions met.

◈ Assumption: Sentry DSN — route-selection assumption: do it now, execution
environment not fully confirmed. Step 0 (create project, obtain DSN) is
user-side and unconfirmed at route selection.

Moving to Phase 6.

> ⚙ Choreography, Ordering spine step 2: ledger prints before the route
> statement. Definitions, Marker convention — trigger: "a do it now route is
> selected but execution tooling or environment wasn't confirmed during Phase 2"
> → ◈ mints at the route statement, after the ledger. This is precisely the
> late-placement class Phase 6's pre-scan backstop exists to catch
> (→ choreography: Cycle accounting, pre-scan description).
````

---

**Piece 5 of 5 — Phase 6 Cycle 2 through close, mechanism log, deviations**

````markdown
---

## Phase 6 — Cycle 2: second firing (later-firing scope)

**MODEL**

```
[Phase 6 pre-scan — Cycle 2]
◈ Sentry DSN — open (minted at Phase 5 route statement)
No other changes since Phase 5 / Cycle 2 ledger.
```

> ⚙ Choreography, Cycle accounting — state test: a confirmed decision record
> exists upstream in this topic → later firing. Scope: plan mechanics +
> markers the new output leans on. Not re-litigating: Sentry decision, free
> tier check (discharged), reproducibility risk (accepted, Cycle 1).
> Choreography, Cycle accounting — offer strength under later-firing scope:
> key on the scope-filtered set (markers the plan leans on), not the full
> chain-rule set. The ◈ DSN is in both — execution blocks on it — so the
> filtered and full sets agree here; no conflict between them.

One open assumption before anything runs — the DSN, without which step 2
can't complete. Want a read of the plan mechanics first?

> ⚙ Spine, Phase 6: ◈ DSN is an unvalidated load-bearing assumption the plan
> leans on → explicit and named offer under later-firing scope.

**USER**

```
Yes.
```

**MODEL**

**Critique — Sentry Integration Plan (later-firing scope)**

**Plan mechanics**

Seven steps are correctly sequenced. One thing to pin at gate-fire: step 5
says "before any existing error middleware" — the gate check will inspect
`src/app.js` to find the exact line, so handler placement is targeted rather
than approximate. Nothing to clean up now; it'll be in hand before the first
line is written.

Step 3 → 4 ordering matters: Sentry must be initialized (step 3) before
`requestHandler` is mounted (step 4). As written, that ordering is correct.

**The DSN**

The only open item. Step 0 covers it — create the project, get the DSN. If
you have it ready or can create the project now, the gate can fire immediately.

**Nothing from Cycle 1 re-litigated.** Handler requirement and Step 0 were
incorporated; reproducibility risk was accepted. Both stand.

---

Say **go** to proceed — or **clean up the vomit** if anything should change.

> ⚙ Definitions, Clearing scripts: gate-route variant (do it now has an
> execution gate). Definitions, Critique dimensions: later-firing scope —
> critique covers plan mechanics and markers the plan leans on only; earlier
> decisions and accepted findings are not re-examined.

**USER**

```
Go — project's created. DSN: https://abc123@o000000.ingest.sentry.io/000000
```

> ⚙ Definitions, acknowledgment threshold: "Go" clears Phase 6. Definitions,
> Gate check — user-pre-provided values: the DSN arrived alongside the Phase 6
> clearing response — treated as obtained at gate-fire; discharge the ◈
> without re-asking.

---

## Execution gate — Cycle 2

**Gate check:**

**Tools / connectors / skills:** code execution and file editing available in
this session ✓ [definitions, Execution context — session-side facts self-fill;
no question spent on them]

**Repo / path inspection** [definitions, Gate check — Inspection; read-only,
nothing mutated before the gate clears]:

- `src/app.js` found; Express setup confirmed
- Existing error handler: `app.use(errorMiddleware)` at line 52
- `Sentry.Handlers.errorHandler()` target: immediately before line 52
- `src/lib/` directory exists; `sentry.js` will be created there
- `package.json` confirmed: `@sentry/node` not yet installed ✓

**Sentry DSN:** pre-provided alongside Phase 6 clearing response —
`https://abc123@o000000.ingest.sentry.io/000000` — ◈ DSN discharged ✓

**All gate conditions met. Executing.**

---

*Step 0:* Sentry project confirmed created; DSN in hand.

*Step 1:* `npm install @sentry/node`

*Step 2:* create `src/lib/sentry.js`:

```js
const Sentry = require("@sentry/node");

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV || "development",
});

module.exports = Sentry;
```

*Step 3:* top of `src/app.js`, before any other imports:

```js
require("./lib/sentry");
```

*Step 4:* after require calls, before route registration in `src/app.js`:

```js
const Sentry = require("@sentry/node");
app.use(Sentry.Handlers.requestHandler());
```

*Step 5:* immediately before line 52 (`app.use(errorMiddleware)`):

```js
app.use(Sentry.Handlers.errorHandler());
app.use(errorMiddleware); // existing handler — unchanged
```

*Step 6:* append to existing `.env.example`:

```
SENTRY_DSN=
```

Add `SENTRY_DSN=https://abc123@o000000.ingest.sentry.io/000000` to production
env. Not committed to repo.

*Step 7:* smoke test — throw a deliberate error; confirm it appears in the
Sentry dashboard with request context (user ID, headers, request body shape)
populated.

---

Integration complete. Errors in tgd-api now captured with stack traces and
request context. The next unreproducible support email should have a Sentry
event to open instead.

**Session close:** single topic, confirmed output, executed. No queued topics.

> ⚙ Definitions, Park artifact format: topic and session close together — no
> queued topics remain. Choreography, Cycle accounting: Cycle 1 — one set of
> firings (decision record); Cycle 2 — one set of firings (plan). Option map
> received no firings as designed — never a confirmed output.

---

## Mechanism log

| Mechanism | Status |
|---|---|
| Tier + mode co-statement; mild mismatch stated, no ⚑ | ✓ |
| Mode question on genuinely ambiguous signals | ✓ |
| Switching-criterion intermediate test before triggering | ✓ |
| Mode switch stated on confirmed declaration | ✓ |
| Option map, generative header; block omitted (pre-decision, judgment call) | ✓ |
| Correction in Phase 4 Cycle 1 — future note excluded from map | ✓ |
| Commit confirmation + ◈ on external-condition commitment | ✓ |
| Fork-as-deliverable path | ✓ |
| Decision record at Decided Fork; Cycle 1 firings | ✓ |
| Phase 6 Cycle 1 — first firing, full scope | ✓ |
| Critique minting boundary — findings stayed prose | ✓ |
| Combined instruction → incorporate + clear, no re-offer | ✓ |
| Gate Cycle 1 → planning accepted → new cycle opens | ✓ |
| State test: confirmed record upstream → later firing | ✓ |
| ◈ minted at route statement, after Phase 5 Cycle 2 ledger | ✓ |
| Phase 6 Cycle 1 pre-scan: delta-only print, no change | ✓ |
| Phase 6 Cycle 2 pre-scan: delta print; scope-filtered offer (later-firing) | ✓ |
| Gate check: self-fill · inspect · pre-provided DSN discharged | ✓ |
| Single-topic session close | ✓ |
| Discard test | — not exercised |

---

**Deviations and decisions, flagged:**

| # | What | Why |
|---|---|---|
| 1 | Patch-letter citations (AA, AC, AD, AE and others) → owning-file anchors throughout, including the mechanism log | Relocation-pass principle: letters referenced the dev conversation, which doesn't ship with the file |
| 2 | Post-mortem dropped; mechanism log kept | Development history, not executor guidance |
| 3 | Phase 5 Cycle 2 restructured: the DSN ◈ moved out of the Phase 5 ledger and into the route statement | Original had the ◈ inside the ledger, but the ordering spine (ledger → interrupt → route) means the do-it-now ◈ mints at route selection — after the ledger has printed. Phase 6's pre-scan correctly picks it up as the delta |
| 4 | Phase 6 Cycle 2 pre-scan format: delta-only print with full open set noted for offer-strength computation; Cycle 1 pre-scan: delta-only print with full open set shown (same set, no later-firing filtering needed on first firing) | Mirrors choreography: Cycle accounting's "print policy: delta only; offer strength computes on the full open set" — and for later-firing, the scope-filtered set |
| 5 | ⚙ notes for AD (intermediate switching test) and AE (user-pre-provided value at gate-fire) rewritten as citations | Both behaviors are now in the spec — definitions: Switching criteria and definitions: Gate check respectively — no longer deviations |
| 6 | Step 6 in Phase 3 Cycle 2 says ".env file" (generic); Phase 4 updates to "existing .env.example" | Original Phase 3 already named ".env.example" before the user mentioned it; corrected so the specificity arrives where the information does |
| 7 | Option map execution context block omitted; ⚙ cites judgment call, not the skip condition | The skip condition (greenfield, no existing surface) doesn't technically apply; omission is justified by the option map's pre-decision purpose and its non-output status in the fork-as-deliverable path |