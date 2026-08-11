# Choreography — gates and multi-topic coordination

Single owner of every cross-topic and gate-ordering rule. The spine and
definitions files point here and never restate a gate rule. **A coordination
behavior with no row here is undefined — add the row before adding prose.**

---

## Topic lifecycle

queued → active → terminal.

Terminal states: **executed** · **dispatched** (handed off) · **decided**
(record delivered, planning declined) · **parked-post** (output confirmed,
then parked) · **parked-pre** (parked before any confirmed output) ·
**declined**.

**The one partition that matters:** did the topic reach a confirmed output?

- **Yes** → it closes through Phases 5–6: route, offer, gates. Cycle
  accounting governs firings.
- **No** (parked-pre) → it closes through the **queue check** at the exit
  site. No route, no Phase 6, no gate — inline markers carry all scrutiny.

No topic reaches both mechanisms.

---

## Ordering spine — confirmed-output topic

1. Phase 4 confirmation
2. Phase 5: ledger → interrupt surface (if any) → route stated
3. Phase 6: pre-scan → offer → clear
4. **Reconciliation** — only when this is the final *interacting* topic
5. **Topic gate** — when topics remain queued
6. **Execution gate** — unless held; a held gate's release precedes firing
7. Execute / dispatch

---

## Gate hold and release

**Hold:** when the Phase 1 dependency record is non-empty — or topics are
otherwise not fully independent — an interacting topic's execution gate
does not fire at step 6. State the route; hold.

**Deadlock guard:** a do-it-now topic whose *executed result* a queued
topic needs fires its gate normally — holding it would deadlock the queue
the hold protects.

**Release events — any one suffices:**

1. **Reconciliation resolves in-session** (accepted or declined). Held
   gates fire in the artifact's recommended sequence, else topic order.
2. **The interacting counterpart leaves at the topic gate** (hand off /
   park): a park defers the comparison via its *Deferred reconciliation*
   field; a handoff names the pending interaction in one argument clause.
3. **The interacting counterpart parks pre-confirmation** — no output will
   exist to reconcile; release, deferring the comparison via that park
   artifact's *Deferred reconciliation* field.

**Release timing:** a release event fires held gates at the event itself —
in artifact sequence if a sequence was recommended, otherwise in topic
order — before any later step of the topic whose closing produced the
event. "Later step" includes the topic gate: a held gate resolves *within*
the releasing topic's closing sequence, not after it. The ordering spine's
step 6 placement is where a gate fires in a *single* topic's run; under a
hold, release event timing overrides that placement.

**Late interaction:** interaction discovered after a gate fired doesn't
unfire it — reconciliation runs scoped to informing the later topic,
stating plainly the earlier one is committed.

---

## Reconciliation

**In-session trigger:** after the final **interacting** topic's Phase 6
clears — independent topics still queued neither delay nor join it.

**Deferred trigger:** session re-invoked from a park artifact with
*Deferred reconciliation: yes* — after this session's final Phase 6 clears.

In either case, offer before any held gate releases:

> "Before anything gets handed off: these two outputs might interact —
> shared constraints, sequencing, or resource conflicts. Want me to surface
> the cross-topic dependencies first?"

**Reconciliation artifact** (produced on acceptance — not a Phase 1–6
pipeline):

- Dependencies between the two outputs (what one plan assumes that the
  other's might violate, or vice versa)
- Sequencing recommendation — which to execute first and why
- Shared constraints both plans must respect
- Whether to hand off together or sequentially

This artifact is offered as input to the handoff, not as a standalone
deliverable.

**Gate release:** reconciliation resolution — accepted or declined — is
release event 1. Held execution gates fire once this offer resolves, in
the artifact's recommended sequence if one exists, otherwise in topic order.

---

## Topic gate (confirmed-output topics only)

Fires at ordering spine step 5. Consume the dependency record
**defeasibly**: re-ask an *unclear* needs field now, better-informed;
correct a contradicted one.

**Error asymmetry — when in doubt, ask:** a wrong *verified output*
classification is the expensive miss — Topic 2 proceeds as though
unblocked when it isn't. A wrong *executed result* classification merely
over-cautions.

**Before branching on the needs field:**

- *needs = unclear* → ask the object question now, better-informed:
  *"Does [Topic 2] need [Topic 1]'s plan, or the thing actually built from
  executing it?"*
- *Topic 1's pipeline contradicts the field* (e.g., the record says
  *verified output* but Phase 4 revealed Topic 2 actually requires
  execution) → correct and proceed.

**Branch on the confirmed needs value:**

---

**Independent:** present all three options:

- **Continue here** — inherits Topic 1's output as context; the noise
  caveat applies for complex topics.
- **Hand off now** — clean window; see Dispatch ordering below.
- **Park Topic 2** — separate invocation when ready.

---

**Needs verified output (it now exists):** all three, reframed:

- **Continue here** — Topic 1's output is already in context; inheritance
  is the benefit here, not a risk. The noise caveat still applies for
  complex topics.
- **Hand off now** — the `/handoff` argument must name Topic 1's verified
  output and its execution context as primary context for Topic 2's session.
- **Park Topic 2** — *Depends on prior output:* yes, *Deferred
  reconciliation:* yes, re-entry context names Topic 1's output as
  required input.

---

**Needs executed result (work not done):** Topic 2 is blocked, not queued.
Offer two options:

- **Park Topic 2** — unblock condition: the specific completion of Topic
  1's work, named in the artifact.
- **Conditional-proceed** (continue here or hand off) — only with an
  explicit `◈ Assumption:` that Topic 1's plan executes as specified; that
  assumption rides every downstream artifact via the marker ledger.

If Topic 1's work was executed in-session, its result exists — use the
verified-output case above.

---

**Deferrals:**

- *Decided fork topic* → defer the gate until the fork's disposition
  settles (after the plan cycle's Phase 6 if planning is accepted).
- *Do-it-now topic with an executed-result dependent* → defer until its
  execution gate resolves:
  - Executed: result exists — use the verified-output branch.
  - Rerouted to handoff: the dependent is blocked again — use the blocked
    branch.

---

**Dispatch ordering:** selecting "hand off now" queues the second topic's
dispatch behind this topic's execution gate — resolve that gate first (for
a held gate, this selection is itself release event 2), then issue the
second `/handoff` argument. Arguments state **resolved dispositions** only
— executed, dispatched, parked, declined — never a merely-stated route. Two
handoffs in flight each name their ordering in one argument clause, so
neither receiving session assumes the other's work is already done.

**Continue here:** print a scoped opening ledger at the new topic's Phase
2 — carried entries or "none carried." The new topic's chain never keys off
the previous topic's last ledger; it keys off this opening ledger. A marker
from Topic 1 that is directly relevant to Topic 2 is carried deliberately
and printed in that opening ledger.

**If the user parks Topic 2:** produce the park artifact
(→ definitions: Park artifact format), then close the topic. The session
closes only when no topic remains queued.

---

## Queue check — pre-confirmation park exits

**Trigger:** any pre-confirmation park — Phase 2 pipeline exit or Phase 4
non-convergence park — in a multi-topic session, **including when the queue
is empty**: the empty print proves the check ran. (Option-map "no fork
selected" and decided-fork "park" route through Phase 5 and are not this
check's business — those are confirmed-output closes, governed by the
ordering spine.)

**Runs before the park artifact is produced.** Anchored print:

```
[Queue check — {topic}]
Parking: {topic} — blocker: {one line}
Queue: {per queued topic: independent → offered | dependent → blocked, parked} | empty
Artifacts: {list in dependency order, this topic first} | this topic's only
```

**Empty case:** `Queue: empty` with `Artifacts: this topic's only`. The
print is not omitted. An explicit empty result proves the check ran;
absence is ambiguous between "scanned, clean" and "skipped."

**Disposition per queued topic:**

- **Independent:** all three options (continue here / hand off / park) as
  a single collective offer covering all independent queued topics together.
  Weight toward hand off or park for anything non-trivial — context at a
  pre-confirmation park is more stalled than at a clean post-confirmation
  close. Continue-here marker scoping: open a scoped opening ledger at the
  new topic's Phase 2 carrying only entries directly relevant to it, or
  "none carried."
- **Dependent on this topic:** blocked — neither output nor executed result
  can exist. Park it: *Depends on prior output:* yes, *Deferred
  reconciliation:* yes, re-entry context names both blockers (this topic's
  blocker and the dependency itself). Artifacts produced in dependency
  order, this topic first.

**No gate fires.** The topic closes on acknowledgment; the session closes
only when no topic remains queued.

---

### Known-open — O [PROPOSED ROW, UNTESTED]

Transitive blocking (3+ topics): a queued topic's disposition should key
on whether its *needs* is reachable through **every** topic on its
dependency path — not only its relation to the topic now closing. Proposed:
treat a topic as blocked if its dependency chain passes through any parked
or blocked topic. No transcript has exercised a three-chain; write that
test before trusting this row.

---

## Cycle accounting

**A cycle** is a pass through Phases 3–4 ending in a confirmed output.
Phases 5 and 6 attach to cycles, not to the session: **every confirmed
output passes through Phase 5 and Phase 6 before its execution gate —
once per cycle.**

**Option-map exits** — an option map's Phase 4 loop has three terminal
exits. The second and third split at exactly one event: the fork selection
protocol's second question (*"Is the decision itself what you needed — or
do you want to turn this into a plan?"*).

| Option-map exit | Confirmed output(s) | Firings |
|---|---|---|
| **No fork selected → Park** | The option map itself | One set, for the option map |
| **Fork-as-input** — answered "turn it into a plan" | The plan only; the option map is consumed as basis — it is not routed as an output, never reaches Phase 5 | One set, at the plan — its **first** firing |
| **Fork-as-deliverable** — answered "the decision is what I needed" | The decision record; then the plan, if planning is accepted at the record's execution gate | One set per output — the record's own, then the plan's own |

**Identifying the path — state test.** Two keying moments:

- *At the branch* (second question just answered): the answer itself is the
  discriminator.
- *Later* (a plan's Phase 4 just confirmed — is its Phase 6 a first or
  later firing?): does a confirmed decision record exist upstream in this
  topic? **No → first firing, full scope. Yes → later firing,** scoped per
  Later-firing scope below.
- *Path unreconstructable* (ambiguous history, cold transcript): treat as
  first firing. Asymmetry: a wrongly full-scoped critique re-litigates
  accepted material — redundant but safe; a wrongly later-scoped critique
  silently drops the only adversarial pass the plan will ever get.

**Re-entry paths:**

- *Late re-entry* (a delivered critique surfaces a premise break and the
  user re-enters Phase 2): the re-entered pipeline produces a new confirmed
  output → new firings.
- *Re-entries before confirmation* (premise break or format correction
  inside Phase 4): extend the current cycle. No new firings.

**Later-firing scope:** a second or later Phase 6 scopes its pre-scan and
critique to what the new output changes — its own mechanics, plus
unresolved markers the new output leans on. Material critiqued in an
earlier firing and accepted by the user is not re-litigated unless the new
output changes its basis.

**Offer strength under later-firing scope:** key on the open marker set
**filtered by scope** — markers the new output leans on — not the full
chain-rule set. A marker the plan doesn't lean on stays in the chain
(available for ledger continuity and the state test) but does not elevate
offer strength or drive critique content in a later-firing Phase 6.

For Phase 5's interrupt scan under a later firing: flags surfaced at an
earlier interrupt and knowingly accepted do not re-trigger — but with a
confirmed output now in hand, check each open projected-basis flag against
the actual plan, fill an unknown basis from the plan first, then state
whether the flag is discharged or confirmed.