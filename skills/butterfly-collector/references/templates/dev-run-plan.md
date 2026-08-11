# Contract — dev-run plan (`dev-run-plan.md`)

Exemplar: `references/examples/whimsical-enchanting-willow.md`. The willow exemplar predates this contract's Mutation-enumeration section, `once-only` tags, and surface-delta line — the contract wins; do not imitate their absence. The plan's one scope rule: **only
what a harness structurally cannot reach.** Everything a harness can prove stays in the harness.

## Context block
What the automation already covers (checks, harnesses, zones), then the run's job as the five
categories — each present with content or explicitly declared empty this iteration:
1. **Real model calls** through the changed prompts/providers.
2. **Real data, once** — every one-way effect (migrations, consumed flags, overwrites into shared
   folders), with the count of irreversible effects stated up front (the "N effects that closing
   the app does not undo" discipline).
3. **Never-tested code paths** (zero coverage anywhere), individually named.
4. **Perception** — "a harness can prove a string is set; only a person can say whether it is
   understood."
5. **Unverified claims** — every fan-out claim that never had a refuter run against it.

State the staging decision (e.g. "rehearse on a copy, then go hot") and any build-freshness
warnings (stale build dirs, stray probe artifacts — the exemplar's `out/` warning pattern).
State the **surface delta** vs the previous iteration's plan up front, and give every entry its
*why it is structurally unreachable* — the harness-growth audit reads these, and entries that
stop qualifying move into the harness next iteration. Bundle-lite iterations may merge this
document with the runbook (`phases/execute.md`); the sections below still bind.

## Mutation enumeration — the derivation source
Every effect the run will cause, harness-reachable or not — the five categories above are only
the harness-*unreachable* subset of this list. One line per effect: what changes, where,
reversible or not, and what covers it (snapshot path · checker pin id · runbook box). The
snapshot manifest and the checker are generated from this list and from nothing else; a manifest
path or pin with no line here is a defect, and so is an effect with no coverage entry. Never
collapsed in bundle-lite.

## Stage 0 — before anything launches
Build; back up everything the mutation enumeration names (call out items with **no** backup of
their own); pin the pre-state facts the checker will assert — sizes, counts, and *absences*
("there is **no** `.bak`", "folder holds exactly 5 files").

## Stage 1 — rehearsal on a copy (nothing real moves)
Scratch copy + isolated data dir. "A **diff against an expectation**, not exploration": an
expected-value table (before → after) for every observable the launch changes. **Mandatory
neutralization** of any outbound-propagating effect (synced/shared folders) in the scratch copy —
verify the rehearsal is actually inert before calling it one. Include the human-judgment items
(rows about to be frozen forever, oddities worth eyeballing) with the question each answers.

## Stage 2 — the one-way effects, watched
Per effect: trigger condition, artifact written, exact check, and its irreversibility note (no
temp file, no backup, propagates to other devices, window before the next persist destroys the
evidence). Order matters; state what must be checked *immediately*.

**Never-tested paths (category 3) get a named home.** One-way ones ride Stage 2 under its watch
discipline; reversible ones take rows in Stage 1's expectation table or a dedicated stage of
their own — never left implicit. (The exemplar folded all four into Stage 2 because its untested
paths happened to be launch effects; that was a property of that codebase, not of this
contract.)

## Stage 3 — real model quality
The calls a fake daemon faked: date resolution at the timezone boundary (run in the local
evening), end-to-end captures, truncation markers, per-model parameter clamps, refusal rendering,
re-triage against protected rows, model-driven state changes — adapted to this iteration's diffs.
That list is the exemplar campaign's, not a checklist: derive this iteration's from its own
diffs, and for codebases outside the exemplar's class (a local app owning user data), translate
the nouns per SKILL.md → "Target class" — the category headings stay, the contents are
re-derived, and empty is declared, never assumed.

## Stage 4 — perception, not mechanism
Each new user-facing message/cue: the gesture that produces it, what it must say, and the truth
condition ("count the rows that actually moved"). Include the must-say-**nothing** cases.

## Stage 5 — the unverified claims
Each claim as `file:line — claim — how this run tests it`, split into check-during-migration vs
check-in-normal-use. "These are **claims, not findings**."

## Known-open — do not chase
Every deliberately-open item: what it does, how to avoid tripping it, its harness pin, and what a
real fix requires. The run characterizes known-opens; it does not fix them.

## If something is wrong — restore, in this order
Numbered, app-quit-first, covering **all** independent state ("restoring the DB alone is not
enough"), ending with the checker `pre` pass as restore verification. Tag every once-only check
`once-only` and point at the reconstruct-on-scratch procedure for second observations.
