# Contract — the user's findings doc (`dev-run-findings-user.md`)

The one artifact in the loop a human authors. Written by the user during their independent pass
(`phases/devrun.md` §3) — or by the skill, at the user's direction, when the pass is skipped. It
exists so the termination test consumes a declaration, never an absence: condition 2 reads this
file, and the hard gate counts `user_run_recorded` vs `user_run_skipped` when it states which
detectors saturation is claimed for.

## Header
Iteration · date(s) · snapshot pointer (what was restored from, per the runbook's
restore-in-order) · runbook pointer. Then the **detector table** — one row per detector the
actor map gives the user, because the termination test and the hard-gate summary read
participation from here, never from event names alone:

| Detector | Ran? | Findings? |
|---|---|---|
| User-reserved boxes (part of the main run) | yes / no / none-reserved | count, or `none` |
| Independent comparison pass (`phases/devrun.md` §3) | yes / skipped | count, or `none` |

Then one pass-verdict line — exactly one of:

- `Independent pass completed — findings below.`
- `Independent pass completed — no findings.`
- `Independent pass skipped — no user findings. (recorded by the skill at the user's direction, <date>)`

The skill writes only the third, verbatim, and only after the user says so; the first two are
the user's own words. The skip line covers the independent pass alone — it never claims the
user ran nothing, and the termination test's criterion 2 reads this file as a whole: every
detector the table says ran must have reported nothing. Record `user_run_recorded` if any
detector row says yes; `user_run_skipped` only when none did.

## Entries (when there are findings)
The runbook's four-part protocol, one block per finding — what you did · what you saw · what
the plan/code says should happen · the repro line a fixer lane can run — in fresh-state phrasing
("park any file 11 months out", never a named personal row), plus `needs-migration-history:
yes/no` (yes means capture exhaustively **before** any destructive stage). Severity and
`file:line` are welcome but optional: the user reports what they saw; SYNTHESIZE re-triages,
provenance-tags `[user]`, and dedupes against the Cowork report.

## Rules
- This file records findings, not progress — runbook ticks live in the runbook.
- Any `once-only` check the user could not observe live is noted as such, pointing at the
  reconstruct-on-scratch procedure; an unobserved check is `UNTESTED`, never silently omitted.
- The file is an input to SYNTHESIZE and the termination test; the log stays canonical.
