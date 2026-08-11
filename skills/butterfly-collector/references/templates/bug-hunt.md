# Contract — bug-hunt report (`bug-hunt-<YYYY-MM-DD>.md`)

Exemplar: `references/examples/bug-hunt-2026-07-23.md`. The hunt finds and adjudicates; it fixes
nothing. Every section below is mandatory unless marked optional.

## 1. Methodology preamble (one paragraph)
State the fleet shape (e.g. N subsystem auditors + M cross-cutting lenses — dates/timezones,
filesystem races, IPC/contract drift, legacy-data tolerance, model-API usage — adapt lenses to the
codebase, and name any opted-in scope lenses: security/abuse-facing, silent data-integrity
drift, performance), raw→merged finding counts, and the adjudication rule: every finding is attacked by two
independent adversarial verifiers — one checks the code mechanism, one walks the user repro end to
end. Define the verdicts: **Confirmed** = both upheld · **Disputed** = split · **Refuted** = not a
bug. Close with "Nothing has been fixed."

## 2. Totals line
`**X confirmed** (h high / m medium / l low), **d disputed**, **r refuted**.`

## 3. Confirmed findings, tiered `## Confirmed — high | medium | low`
Per finding:
```
### <file>:<line> — <one-line user-consequence title>
<mechanism paragraph: exact code path, why it fails, neighboring code it interacts with>
**Repro:** <a concrete user-visible walk from normal use to the failure — this line later becomes
the fixer lane's test case, so it must be executable as written>
```
Severity is judged by user impact (data loss / silent wrong behavior > visible error > cosmetic),
not by code ugliness. Titles name the consequence, not the defect class.

## 4. `## Disputed (one verifier confirmed, one refuted)`
Same entry shape, severity tag in brackets, plus `**Why disputed:**` — the refuting verifier's full
mechanism, with evidence (the exemplar cites V8 source to kill a claimed crash). Disputes are
recorded, never silently dropped; the execute phase re-reads them after related files change.

## 5. `## Refuted (verified not to be bugs)`
One line each: `file:line — claim — why it fails`. Refuted items matter later: the fresh-eyes rule
escalates any refuted item a future blind hunt re-reports.

## Rules
- Findings are claims until verified; only Confirmed entries feed /orchestrator.
- `file:line` anchors everywhere; line numbers may drift — fixers re-verify before editing.
- No fix suggestions inside findings (that is the plan's job); repro phrasing must not depend on
  the hunter's private state ("a chat that says 'tomorrow'", never "chat #45").
