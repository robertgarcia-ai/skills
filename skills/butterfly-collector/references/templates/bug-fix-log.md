# Contract — the bug-fix log (`docs/bug-fix-log.md`)

The log is **canonical**: reports, plans, and synthesis documents index it; when they disagree
with it, the log wins. It is created at campaign initialization if absent, lives at the repo
root's `docs/`, spans campaigns (it is never archived with `iter-*/`), and its write is a
**gate** before any destructive step anywhere in the loop. The exemplar campaign's log was not
sanitized for bundling; its shape is reconstructed here and echoed by every `Log anchor` line in
`examples/dev-run-report-2026-07-27.md`.

## Creation (initialization, when absent)

```
# Bug-fix log — <project>

Canonical, append-only record of findings, fixes, dispositions, and retractions across all
butterfly-collector campaigns on this repo. Reports and plans index this file; this file wins.
```

## Append-only, precisely

- Entries are never deleted or rewritten. A correction is a **new entry** referencing the old
  anchor; the only permitted edit to an existing entry is a single inline supersession pointer
  (`*superseded by §… — see F<n>*`). Retractions follow discipline 11: the withdrawn entry
  stays, marked **WITHDRAWN**, with its refuting evidence appended.
- Sections append chronologically: `## <event> — <date>` — e.g. `## Hunt — 2026-07-23`,
  `## Phase 2 fixes — 2026-07-25`, `## The dev run — 2026-07-27/28`,
  `## Campaign 1 closed — <date>`.
- Anchors are load-bearing and permanent: reports link `F#` → log anchor, and pins in the
  harness cite them. F-numbers are unique **per campaign**; where an interim report numbering
  was superseded, the log's final numbering wins and the report notes it (exemplar report,
  header parenthetical).

## Entry shapes (house style)

**Finding entry** (dev runs, hunts confirming into the log at synthesis):

```
### F<n> — <one-line user-consequence title> (<file>:<line>) — <severity>
What we did: …
What we saw: …
What should happen: … (per <plan/code ref>)
Repro: <fresh-state phrasing — executable as a fixer's test case>
Disposition: <FIXED in <commit> / PINNED-OPEN at <pin location> / NEEDS-DECISION §7#<n> /
BLOCKED(<reason>) / WITHDRAWN — <refuting evidence>>
```

The four parts (did / saw / should / repro) are the runbook's findings protocol — the log and
the runbook deliberately share one shape so entries transpose without rewriting.

**Fix entry** (EXECUTE, as lanes land — one block per finding):

```
- F<n> / <file>:<line> — lane <name> — commit <short-hash> — proof: <before/after evidence> —
  verifier: SOUND | FLAWED: <mechanism, and what happened next>
```

**Decision entry**: the NEEDS-DECISION question, the options presented, the user's answer,
and where it was consolidated (the living rubric section) — the log records that the decision
happened and what it was; the rubric holds its current form.

## What does not go here

Plans, gate cards, state, and trend live in `docs/butterfly/` — the log records findings,
fixes, dispositions, decisions' outcomes, and retractions. The findings are the deliverable;
everything else is scaffolding (discipline 6).
