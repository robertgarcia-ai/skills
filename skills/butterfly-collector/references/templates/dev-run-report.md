# Contract — dev-run report (`dev-run-report-<YYYY-MM-DD>.md`)

Exemplar: `references/examples/dev-run-report-2026-07-27.md`. Created at preflight from the cowork
plan's skeleton; grows live; the **verdict paragraph is written last**. The report is the run's
crash-recovery state and its index; `docs/bug-fix-log.md` is canonical for findings.

## Header
Verdict paragraph (what ran, counts by severity, claims dispositioned, known-open characterized,
what happens next — all named). Then: Operator · Scribe (model, effort) · repo HEAD · runbook
pointer with box count · plan pointer · sittings (date/time ranges, timezone). Interim verdicts
from earlier sittings stand as written, with inline supersession notes — never rewritten.

## Run conditions
Environment reality vs plan assumptions: the capability probe's outcome and the **adopted
mechanism** for any gap, spelled out so a cold reader could reproduce the setup. Any scribe error
gets recorded **with the rule it produced** (the exemplar's stale-staged-bytes retraction became
the host-read rule) — errors are data, not embarrassments. The app/system config under test,
stated as pinned premise satisfied or deviation handled.

## Run-day delta table
Every date-sensitive runbook literal: | literal | as written | this run day |. **Recomputed at
the start of every sitting**; note gates not usable this sitting and when they reopen.

## Preflight
| item | result | — including the checker's transcribed info lines.

## Stage results
Per stage: | Box | Actor | Result | Evidence | with ⚠️ = observation, ❌ = finding ref F#. The
one-way stage additionally gets a timestamped timeline paragraph from the launch transcript.

## Findings
`### F<n> — <title> (file:line) — <sev>` then: Surfaced by · What we did · What we saw ·
Mechanism (with the code path, and the family of sibling call sites sharing the defect shape) ·
evidence table where samples exist · What should happen (per plan/code ref) · Repro
(fresh-state phrasing) · Needs migration-history: yes/no · **Harnessable now: yes (how) / no
(why)** · Suggested lane → tier · New / confirms claim N · Log anchor. Withdrawn findings stay in the report, marked **WITHDRAWN**, with
the refuting evidence — recorded rather than quietly dropped.

## Claims — dispositions
| Claim (file:line) | Vehicle | Verdict | Evidence | with verdicts from:
`CONFIRMED-BUG (→F#)` / `REFUTED` / `CLOSED-BY-<box>` / `UNTESTED (reason)` / `DEAD-CODE`.
Every claim from the dev-run plan appears exactly once.

## Known-open characterization
"A repro under <plan ref>, NOT a new finding." Boundaries measured, artifacts' fate on disk
proven, comparison against the harness pin's expected values, options memo for the pending
product decision (decision is the user's).

## Product calls surfaced
Each as NEEDS-DECISION with options only. No lane implements before the answer.

## Fresh-start / destructive-stage status
What is pending vs done, the mandatory-first ordering, and the keep-until rule for backups
("until the fix pass completes and its verifiers report — the fresh app being healthy is
necessary, not sufficient").

## Handoff — the fix pass (read this cold in the coding surface)
Inputs · lane table (exclusive files | findings/claims | tier · effort | verifier) with the
reminder that **this table is a proposal, not a partition — the orchestrator's first job is the
coverage check** · environment rules incl. how needs-migration-history items get fixed
(captured evidence or a scratch restore, never the real profile) · the full gate list to run
after every merge · the known-open pin rule (fixing it converts the pin to a real check; never
delete the pin).

## Commit plan (gated — the user authorizes each)
Prepared commands + messages; nothing committed until authorized; nothing pushed unless asked.

## Transcripts appendix
Every checker transcript, launch transcript, and probe output backing the verifications, by name
and location, with the evidence-archive keep-until rule.
