# Contract — generated state checker (`docs/butterfly/iter-NNN/checker/devrunCheck.*`)

Exemplar behavior throughout `references/examples/dev-run-runbook.md` and
`dev-run-cowork-plan.md` (the campaign's `devrunCheck.ts`). One checker is generated per
iteration, during EXECUTE's bundle step, from the dev-run plan's mutation enumeration and Stage-0
pins. It is the run's measurement instrument and the loop's most safety-critical artifact.
A minimal generic skeleton showing the modes, the contract line, and the read-only discipline is
`references/examples/devrunCheck-skeleton.ts` — start there, then derive every pin from this
iteration's mutation enumeration.

## Purpose (all three, in one tool)
1. **Premise pinning** — `pre` mode asserts the exact pre-run state the dev-run plan's
   predictions were derived from: file sizes/hashes, row counts, config values, and *absences*.
   A `pre` failure means the predictions no longer apply — measurement-gate stop (class A).
2. **Prediction gating** — `post` mode asserts the Stage-1/Stage-2 expectation table:
   every before→after value from the rehearsal diff and the one-way launch.
3. **Restore verification** — after any restore, `pre` must pass again; "the checker doubles as
   restore verification."

## Hard properties
- **Read-only, always.** Opens data stores read-only; writes nothing anywhere; makes no model or
  network calls. If it cannot verify something read-only, it reports UNVERIFIABLE rather than
  probing destructively.
- **App-quit precondition.** Refuses (or loudly warns) if the app under test is running — a live
  app rewrites state under the checker. `post` results are valid only immediately post-launch;
  say so in the output.
- **Deterministic contract line.** Ends `ALL CHECKS PASSED (pre|post)` or a failure list naming
  each failed pin with expected vs observed. Scripts and humans key off that exact line. A
  thrown probe is a FAIL, never a crash — the contract line must always print (the skeleton's
  runner shows the catch).
- **UNVERIFIABLE is a third result, not a failure — but only when delegated.** Anything
  *permanently* unverifiable read-only belongs in the runbook as a box, never here as a pin. A
  pin may return UNVERIFIABLE only when its read-only probe cannot run this time, and it must
  name the runbook box that verifies the fact by hand. UNVERIFIABLE results are listed and
  summarized *before* the contract line; they never appear on it and never flip the exit code —
  the run's gates key off pass/fail alone, and the delegated box carries the check. An
  UNVERIFIABLE with no named runbook box **is** a FAIL, so a lazy generation cannot pass
  vacuously by declaring everything unverifiable.
- **Info lines.** Prints the pinned premises (config under test, last-opened timestamps,
  will-fire predictions) so preflight can transcribe them into the report verbatim.
- **Self-describing.** Header comment states what the checker is and is not, its modes, and its
  preconditions — the cowork plan's read-first list points at it.

## Generation rules
- Every pin traces to a line in the dev-run plan (Stage 0 pins, Stage 1 expectation table,
  Stage 2 effects). No pin without a source; no plan expectation without a pin, unless the plan
  explicitly marks it human-perception-only.
- Exact values, not ranges, wherever the read-only probe can produce one ("~26" became "exactly
  26" during runbook verification — the checker is where that precision lives).
- Language/runtime: whatever the target repo already runs (the exemplar used `tsx` +
  `node:sqlite`); zero new dependencies if possible; runnable from the repo root with one
  command, and that command appears in the runbook.
- Known-open pins live in the *harness* (smoke suite), not here — but the checker's `post` must
  not contradict them.
