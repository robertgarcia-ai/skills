> **SANITIZED EXEMPLAR.** Personal names, usernames and machine-specific identifiers were replaced (Operator, REDACTED-USER, ExampleCorp, Sample), the app identity was additionally fictionalized (SampleApp / sample-app / Nudge Queue etc.), and timezone + personal context generalized; everything else — structure, numbers, wording — is verbatim from a completed real campaign (2026-07). Read for shape and conventions, not as instructions to execute.
>
> **Take from this:** §2's actor split ("the user acts only where the act is irreversible or their eyes are the instrument"); §3 preflight with the checker's info lines transcribed; §4's three stop classes and session-death recovery; §5's per-box actor map; Appendix B's read-only probe kit. Map: §0 mission · §1 read-first · §2 cast/rules · §3 preflight · §4 loop+stops · §5 actor map · §6 findings · §7 log gate · §8 models · §9 post-run · §10 risks · App. A skeleton · App. B probes.

# Dev run — Cowork execution plan

This document directs a **Claude Cowork session** executing `docs/dev-run-runbook.md` side-by-side
with Operator. The runbook is the single source of truth for every command and expected value — this
plan never restates them; it says **who does each step, what gets measured automatically, what gets
recorded where, and what happens when something goes wrong**. Deliverables of the run: all 66
runbook checkboxes ticked with evidence, `docs/dev-run-report-<runday>.md` (created at preflight
from Appendix A), a findings section in `docs/bug-fix-log.md`, and the Phase-4 handoff inside the
report. The findings are the only thing that survives Stage 6's scrap; the database is scaffolding.

**Address Operator as Operator** (their set preference, `docs/dev-plan-review.md:34`; working style
per `:39` — challenge when wrong, tag confidence, no sycophancy, uncomfortable answer first).

---

## 0. Mission and ground truth

The Phase-4 campaign is complete at `615e638`; the one open item on `docs/bug-fix-plan.md:158` is
"Operator dev-runs." `user_version` is still 0: the one-way hot launch has never happened, and
Stage 2 is the only execution the migration/repair code will ever have on real data — a fresh
database migrates over zero rows, so there is no second chance to observe it.

Expected tree: HEAD `615e638`; untracked `docs/dev-run-runbook.md`, `src/spike/devrunCheck.ts`,
this file, and (from preflight on) the report. Anything else modified → stop and ask.

## 1. Read first, in order

1. This document, fully.
2. `docs/dev-run-runbook.md`, fully — especially the four plan-corrections (`:8-22`), the
   disposable-data premise (`:24-42`), the ground rules (`:60-74`), and the findings protocol
   (`:558-567`).
3. `docs/bug-fix-plan.md` — §3 (model reasoning), §5.1/§5.2 (fixer and verifier prompt templates
   the handoff points at), §7 #15 (R1).
4. `docs/bug-fix-log.md:1678-1697` (the 12 unverified claims) and `:1882-1913` (the R1 revert).
5. The header comment of `src/spike/devrunCheck.ts` (what the checker is and is not).

Do **not** search `src/main/store.ts` with Grep — it trips ripgrep's binary heuristic. Use the
Read tool or `Select-String`.

## 2. Cast and hard rules

**Operator** acts only where the act is irreversible or their eyes are the instrument:

- The three irreversible acts: **2.2** the hot launch, **6.3** the scrap, **6.4** the first fresh
  launch.
- Every in-app gesture (triage clicks, drags, Settings changes, `/` menu, "Triage this date",
  Enter-mid-stream, 5.4's Delete).
- Perception judgments: does a message read right, is a notice noticeable, does a banner render.
- 1.7's "did I ever touch these rows", 2.3's other-sync-tool-device check, and every product
  decision.

**Cowork** does everything else: all commands, all backups, the entire Stage-1 rehearsal
(including launching and quitting its own scratch Electron instance), all capture-fixture drops,
all read-only DB/file probes, all report/log/checkbox writing.

Hard rules for Cowork, no exceptions:

- **The real profile's Electron is never launched, killed, or CDP-driven by you.** The standing
  campaign rule (`src/spike/cdp.ts:9-11`): never touch `%APPDATA%\sample-app`; only pids you
  spawned. Never run `src/spike/cdp.ts` or `src/spike/phase4Smoke.ts` during the run — a smoke run
  can answer a real save dialog.
- **Scratch instances** (rehearsal only): launch in the background from the repo root with console
  captured to a file; quit via the artifact gate (§5, Stage 1); scope every process lookup and
  termination by a `CommandLine` match on the scratch `--user-data-dir` — a process whose command
  line lacks it is not yours.
- **Real-profile quits are Operator closing the app**, verified by you with a read-only process
  check (Appendix B, P-1) — never assumed, never induced.
- Never `npm run dev`. Every command from the repo root (`cd C:/Users/REDACTED-USER/sample-app`).
- **Never write `settings.json` while the app is running** — a mid-run write could trigger claim
  5.3's rollback and contaminate its own measurement. Settings change through the UI (Operator).
  The one sanctioned settings write is 1.2's neutralization stamp, into the **scratch** copy,
  before the rehearsal launch.
- No commits except the gated ones in §9. The only runbook edits are `- [ ]` → `- [x]`.
- Stage 3.6's two refusal prompts (VX synthesis / ransomware) are **test fixtures quoted from the
  runbook** (`:306-310`), deliberately shaped to trip the classifier-level hard stop — that is the
  behavior under test. Operator types them into the app; you never author, vary, or send them
  anywhere; you record what renders.
- Nothing lands in `Desktop\sample_in` — from you or any device — until 2.4 passes (`:70`).

**Access grants before Stage 0** (so no permission prompt lands mid-hot-launch): the repo;
`%APPDATA%\sample-app` (read; write only during a restore); `%USERPROFILE%` for the `sample-*`
dirs (backup, rehearsal, archives, launch logs); `Desktop\sample_in` (read; write only post-2.4).

## 3. Preflight — all green before Stage 0; results are the report's first section

1. **Repo state.** `git status --short` + `git log -1 --format=%h`: HEAD `615e638`, untracked set
   as expected (§0). A tracked-file modification → stop and ask. If the tree changed since
   2026-07-26, runbook 0.1's typecheck+build is mandatory, not skippable.
2. **Runbook virginity.** 0 of 66 boxes ticked. A ticked box means a partial prior attempt —
   reconcile with Operator before anything else.
3. **`npx tsx src/spike/devrunCheck.ts pre`** must end `ALL CHECKS PASSED (pre)`. This is the
   single most important preflight item: it proves nobody casually launched the app and silently
   consumed the one-way Stage 2. (Needs Node 22+ for `node:sqlite`; Node 24 is present.)
   **Transcribe the info lines into the report** — four of them are pinned premises:
   - `engine=agent · chatModel=claude-sonnet-5 · effort=max` — any deviation → stop and ask
     (Stage 3's conclusions would be about the wrong config);
   - `lastOpenedAt` — re-derive 2.3's "last opened" expectation from this **live** value in
     Operator's timezone (the user's local timezone), don't trust the runbook literal;
   - the memory-refresh and list-export **"WILL fire"** predictions — either reading "will not"
     voids the Stage-1/2 predictions → stop.
4. **Compute the Run-Day Delta Table** (recompute *every* run day — Stages 3–5 may span days):

   | Runbook literal | Written for 2026-07-26 | Recompute for run day |
   |---|---|---|
   | 3.1 "tomorrow" (`:46`, `:283`) | Mon Jul 27 | run day + 1 |
   | 3.1 "end of the month" | Fri Jul 31 | last day of run month |
   | 3.1 "next Friday" | Jul 31 / Aug 7 | the next two Fridays; the tested bug is a ±1-day shift, not which Friday |
   | 3.1 gate "local evening" | — | the rule means *UTC has rolled to tomorrow* — recheck, don't copy a clock time |
   | 2.3 "last opened" (`:254`) | Fri Jul 24, 5:23 PM | derive from live `lastOpenedAt` (preflight 3) |
   | 3.8 fixture "August" (`:328-330`) | parks ~Aug 1 | valid through Jul 31; in August, advance the month in the sentence and the expected folder |
   | R1 window (`:436`) | April–June 2027 | month/days in `[run-day − 60d, run-day)` projected into next year; boundary probe ~9 months out |
   | Backup dir names `-2026-07-26` (`:93`, `:244`, `:470`, `:543`) | as written | **keep as written** — `:543`'s restore block hard-codes the name; renaming is risk for zero benefit |

   Announce-time substitutions are marked inline: `[delta: expect Jul 28]`.
5. **Restate the four preamble corrections** in the report, one line each: `draft_key IS NULL`
   goes 151 → **32**, not 0; "2,724 chars" is the `profile` string, the file is 2,872 bytes;
   **1.2's neutralization is mandatory** or the rehearsal overwrites the real sync-tool list files
   on every device; list counts are exactly 26 / 0 / 1.
6. **Environment quiescence.** Your process check (Appendix B, P-1): no Electron on the real
   profile or any `sample-*` dir; no leftover `%USERPROFILE%\sample-rehearsal`. Operator confirms the one
   thing you can't see: no *other device* is about to drop into `sample_in` (rule `:70` binds all
   devices until 2.4).
7. **Create the report** from Appendix A; fill metadata, delta table, preflight results.
8. **Offer optional Commit A** (pre-run): the runbook at 0/66, `devrunCheck.ts`, and this plan,
   as verified — provenance, so the post-run diff shows exactly the ticks. Pre-run, so ground
   rule `:73` ("commit nothing during the run") is respected. If declined, these ride in Commit B.

## 4. The pair-run loop

Per checkbox: **announce** (step number, the step quoted from the runbook with delta substitutions
marked, the command if any, the actor, what "pass" looks like) → **act** (you by default; for
Operator-steps, prompt them with concrete observation questions — e.g. 2.2: "read me nothing; the
transcript has it — tell me when the window is up and anything that surprises you") → **capture**
(transcripts and probe outputs verbatim into the report the moment they exist; UI narration
condensed to observable facts vs. expected) → **tick** (only on evidence, never on intention) →
**advance**, honoring the ordering constraints: 0→1→2 in one sitting; 3.1 evening-gated; 5.4 and
R1 late, after the stages that want a populated database; Stage 6 last of all.

**Stop rules — three classes:**

- **A — measurement gates** (0.3, 1.5, 1.6, 2.4, any checker run): a FAIL **stops the run**
  (`:113` — the predictions were derived from that exact state). The restore procedure (`:525`)
  rescues *the run*, not the data; past Stage 5, skipping straight to Stage 6 usually beats
  restoring (`:527-530`). If invoked: you run restore steps 2–4 (app quit verified first), and
  step 5's `pre` gate is mandatory before resuming.
- **B — app misbehavior in Stages 3–5/R1: never a stop.** It is the point of the run. File a
  finding (§6), restore any setting the test changed (3.5/3.6), continue. One exception: damage
  to the *measurement environment* — settings silently rolled back is claim 5.3 confirming
  itself; file it **and** re-verify current settings before continuing.
- **C — a state neither document predicted:** pause, present the evidence and 2–3 options,
  Operator decides. Never improvise a destructive recovery.

**Session-death recovery:** a fresh session reads this plan, reads the report, counts ticked
boxes, re-runs the *last passed* checker mode to confirm state, and resumes at the first unticked
box. An orphaned rehearsal instance is harmless: terminate by scratch-dir match, delete
`sample-rehearsal`, redo Stage 1 hands-off — the real profile is untouched by design.

## 5. Who does what — the per-box actor map

**C** = Cowork, **R** = Operator. Probes reference Appendix B.

| Box | Actor | Notes |
|---|---|---|
| 0.1 typecheck+build | C | mandatory if the tree changed (preflight 1) |
| 0.2 three robocopy backups | C | writes outside app dirs; **exit 0–7 = success** |
| 0.3 `pre` | C | Class-A gate |
| 1.1 copy to scratch | C | |
| 1.2 neutralization stamp | C | MANDATORY before 1.4 — sync-tool protection |
| 1.3 memory-refresh decision | C | runbook-recommended default: let it fire (second `generateMemory` sample); Operator may override to the `:141` opt-out |
| 1.4 rehearsal launch | **C** | background, console to `%USERPROFILE%\sample-rehearsal-launch.log`; hands-off is the *requirement* (`:146` "without touching the UI"). Quit gate: scratch `capture-ledger.json` exists **and** (if 1.3 fired) scratch `memory.json` mtime advanced, or 120 s — then close gracefully (P-2), scoped to the scratch dir |
| 1.5 `post` on scratch | C | Class-A gate |
| 1.6 `pre` on real | C | Class-A gate — proves nothing real moved |
| 1.7 the 7 frozen rows | C presents, **R judges** | the list is in 1.5's output; the question — "did you ever touch these?" — only Operator can answer; a "never touched it" row **is** a finding |
| 1.8 portfolio duplicate | C | note it from checker output; no decision |
| 1.9 profile diff | C drafts, R ratifies | run the `:194` command; draft the quality verdict; one wobble ≠ finding, consistent weakness across samples = finding |
| 1.10 sandbox play | R optional | C relaunches/re-copies on request; keep `sample-rehearsal` until the run ends |
| 2.1 preconditions | C | backup exists · rehearsal terminated (P-1) · 1.5+1.6 green |
| 2.2 hot launch | **R** | from their terminal at repo root, wrapped in a transcript so the console survives: `Start-Transcript -Path "$env:USERPROFILE\sample-devrun-hot-launch.log"` → `npx electron .` → (after the 2.4 quit) `Stop-Transcript`. C tails the file live and timestamps the `:230-237` timeline |
| 2.3 (parent) | C coordinates | app stays running |
| 2.3a memory refresh | C (+R ratifies) | `:194` command with the backup path; third sample verdict |
| 2.3b plan-lists export | C + **R** | C reads the three files, counts bullets 26/0/1 and checks mtimes; **R** checks another sync-tool device got complete files |
| 2.3c command seed | **R** | type `/` in-app: Orchestrator exactly once, `summon-helper` untouched |
| 2.3d stampOpened | **R** | home view shows the *previous* launch — C supplies the expected rendering from preflight 3 |
| 2.4 quit → `post` | R quits, **C** verifies quit (P-1) then runs `post` immediately | Class-A gate; before *any* Stage-3 activity; eyeball the `:261-266` INFO lines |
| 2.5 closes four Stage-5 claims | C | record CLOSED-BY-2.4 in the report's claims table |
| 3.1 evening dates | R sends (C supplies paste text), **C proves** | after the gesture, P-3 reads the created items' dates — the ±1-day check is an exact ISO comparison against the delta table |
| 3.2 text capture | **C drops**, R glances, C proves | C writes the `.txt` into `sample_in` (post-2.4 only), confirms chat+items exist (P-3) and the file moved into `_captured\` with an epoch prefix (P-4) |
| 3.3 image capture | C drops, **R judges transcript**, C checks | transcript completeness is R's read; C checks the text + truncation notice in the DB (P-3) |
| 3.4 long capture | C drops, C checks marker, R notes triager oddity | the marker reaches the model as input — that's the watch |
| 3.5 effort picker | **R** | Settings UI; "Extra — not on this model"; send must not 400; restore after — C re-verifies config via checker info or P-3 after quit, or R confirms visually |
| 3.6a refusal, direct API | **R** | engine switch in Settings; ⚠️ note must appear |
| 3.6b refusal, Agent SDK | **R** | a genuinely blank bubble = **new finding** beyond campaign scope |
| 3.7 attack the frozen rows | **R** re-triages (multiple rounds, renames, restatements), **C proves after each round** | P-5: the 7 frozen ids' survival + no near-duplicates beside them — cheapest chance ever to break this |
| 3.8 auto-park both halves | R sends fixtures, C proves | P-3: parked chat's `location='tickler'` + `tickler_due`; suggestion-degrade case: items still visible; across *every* park in the run confirm nothing confirmed vanished (the 5.9 fold-in) |
| 3.9 Fable truncation watch | R optional config | passive; C records any nothing-useful triage |
| 4.1 relocation sentences | **R** gestures + reads, **C counts** | the sentence's number is verified by P-3 row-diff, not by recall; project-page variant: destination name must be the project |
| 4.2 reunite case | **R** | must say **nothing**; the pre-R2-refix false report is the regression |
| 4.3 permission-swap notice | **R** | two chats, connector on "ask"; acknowledge-not-answer |
| 4.4 Enter while streaming | **R** | draft preserved, cue shown, nothing sent |
| 4.5 Move to IN → Restore round-trips | **R** gestures, **C proves** | P-3 status/visibility after each of ≥3 round-trips on real long-lived rows |
| 4.6 goal-stall banner | **R** | C may pre-verify the project state qualifies (P-3); known wrinkle (waiting-only) is a product call, not a new finding |
| 4.7 dateless-event export | **R** reads message, **C reads the export** | the message must *name* the skipped event |
| 4.8 non-URL buy link | **R** | chip labelled, click edits |
| 4.9 Events ⋯ dates + `.ics` | **R** gestures, **C reads the `.ics`** | P-6 |
| 4.10 all-fail capture batch | **C drops the `.pdf`**, R reads the toast, C removes the file after | |
| 5.1 `draft_key` kind-move | **R** renames/moves/re-triages 3–4 rows incl. one frozen + one post-migration control, **C proves** | P-3: does the original extraction come back as a duplicate? |
| 5.2 stranded images by filename | C | dormant by design — tick with note, no action (all `_captured` files are `.txt`) |
| 5.3 settings rollback | C passive | any silent revert = the claim confirming itself; file + re-verify |
| 5.4 Nudge-Queue delete blast radius | R parks throwaways + clicks Delete; **C measures** | P-7: full DB snapshot before the click, diff after — chats, items, anything recoverable, and whether the UI warned; **late in the run** |
| 5.5 time on undated event | **R**, C checks `data` JSON | P-3 |
| 5.6 offline digest Regenerate | **R** | network toggle is theirs; silent vs. visible error |
| 5.7 sort-direction leak | **R** | pure UI observation |
| 5.8 capture-interval clamp | R types, **C probes** | the `:418` stored-value command; restore 0.5 min after |
| 5.9 | — | folded into 3.8; tick with note |
| R1-a park 10–12 months out | **C stages** (writes the file into the month/day folder tree — deliberately user-owned and hand-editable, §7 #15), **R reads the calendar row** | record landing row vs. target |
| R1-b the nag | **R** | wording + where it appears |
| R1-c "Triage this date" | **R clicks, C proves** | ingested + deleted months early; **gone from disk or merely unlinked** (P-4) — this decides how bad the bug report reads |
| R1-d ~9-month boundary probe | C stages, R clicks, C proves | pins where the behavior flips; compare against the `knownOpen` pin's expectation (`phase4Smoke.ts:833-838`: `{iso: past, due: true}`) and flag any mismatch for reconciliation |
| 6.0 findings written up first | **C**, R reviews | §7 — the gate on the scrap |
| 6.1 `_captured` aside + lists decision | **C** moves; **R decides** whether to clear the three list files (they propagate) | |
| 6.2 secrets copy | C | |
| 6.3 the scrap | **R** | `Remove-Item` on the real profile — user-reserved, app quit verified first (P-1) |
| 6.4 fresh launch | **R** launches + the `/` and greeting glances; **C** runs the `:510` fresh-DB probe and verifies the captureFolder sweep recovers nothing | |
| 6.5 keep backups | C bookkeeping | until the fix pass completes (§9.7) |

## 6. Findings and evidence

Per finding, the runbook's four-part protocol (`:558-560`): what you did · what you saw · what the
plan/code says should happen · the repro line a fixer lane can run. Report-side extensions:
severity (high/medium/low, hunt convention) · `file:line` where known · **fresh-DB phrasing**
("park any file 11 months out", never "park the Sample file") · **needs-migration-history:
yes/no** — yes means capture it exhaustively *before* 6.3, because after the scrap nobody has such
a database · suggested fix lane → model (§8) · new vs. confirms-claim-N.

An app misbehavior is a finding, not a stop. A checker failure is a stop, not a finding.

## 7. The log write — the gate before 6.3

Before the scrap, transpose the report's finding stubs into `docs/bug-fix-log.md` as one new
top-level section appended at the end — `## The dev run — <date>` (noting it closes plan `:158`'s
remaining item) — in the log's house style: tables, ✅/⚠️, backticked `file:line`, §N / decision #N
refs. Subsections: the findings (full four-part entries); the 12-claim disposition table; the R1
characterization **as a repro under R1, not a new finding** (`:445`), plus a one-line pointer
under the existing `### R1 — REVERTED` heading (`docs/bug-fix-log.md:1882`): "Characterized during
the dev run — see below." Then verify nothing still needs the old database, and only then allow
6.3. The report's findings index links each F# to its log anchor — the log is canonical.

## 8. Model assignments

Rule of thumb (plan §3): **Opus writes what's dangerous, Sonnet what's numerous, Haiku what's
mechanical, Fable attacks what's irreversible.** Mapped to the current family:

| Task | Model | Effort | Why |
|---|---|---|---|
| Cowork live-run session (operator/scribe) | **Opus 5** | **high** | Long-horizon disciplined execution — the campaign's proven workhorse (Phase 4: all-Opus-5 fleet, 18 agents, 0 errors). The hard thinking went into the runbook; xhigh would slow a loop Operator waits on, and the irreversible acts are theirs. Fable 5 is the wrong shape here: minutes-long turns against a live pairing loop, at 2× the price. |
| Report + log write-up (same session) | Opus 5 | high | Deliberately not downgraded: the findings are the only thing that survives the run, and fresh-DB phrasing is judgment work. |
| In-app triage under test (Stage 3) | `claude-sonnet-5` | — | The app's configured engine/model/effort — recorded, not chosen. 3.5 briefly switches to Opus 4.6/Sonnet 4.6; 3.9 optionally exercises Fable via `ANTHROPIC_MODEL`. |
| Fix-pass orchestrator (later, in Claude Code) | Opus 5 | high | Mirrors Phase 4's actual zero-error run. |
| Fixer lanes — `store.ts` / `main/index.ts` (persistence, park/ingest-delete, migration-adjacent) | Opus 5 | **xhigh** | "Opus writes what's dangerous" — a wrong fix here moves or deletes user data; Phase-1/2 precedent ran DB/MAIN at xhigh. |
| Fixer lane — the R1 design change (year recorded **and** `ticklerDayFolders` year-aware), if green-lit | Opus 5 | xhigh | "Its own piece of work" (§7 #15); the obvious heuristic already failed adversarial review once. Options memo first; the decision is Operator's. |
| Fixer lanes — numerous renderer items (`App.tsx`, `Settings.tsx`) | **Sonnet 5** | high (medium for sweeps) | "Sonnet writes what's numerous"; intro pricing through 2026-08-31; the all-Sonnet Phase 3 merged clean. |
| Mechanical sweeps (spelled-out one-liners, doc/table edits) | **Haiku 4.5** | n/a — accepts no effort parameter; 200K context → give it files, not the repo (§5.3) | "Haiku writes what's mechanical" — it executes specs, it does not interpret bug reports. |
| Adversarial verifiers — data-destroying diffs (store/index, anything R1-adjacent) | **Fable 5** | high | "Fable attacks what's irreversible" — the two-Fable Phase-4 review correctly broke R1 and R2 (`docs/bug-fix-log.md:1775`). Cost note from §3: one or two review calls, not a lane ($10/$50, 30-day retention, thinking always on). |
| Adversarial verifiers — everything else | Opus 5 | high | Adequate at half Fable's price; keep §5.2's report-everything/filter-downstream phrasing — it exists because models follow conservative-reporting instructions literally. |
| R1 *product decision* (#15) | **Operator** | — | Decisions are spec; models implement them. |

If Cowork's model picker lacks Opus 5, use the strongest available Claude 5 model and record it in
the report's Run conditions. Where no effort knob exists, "effort" maps to extended thinking on.

## 9. Post-run sequence

1. **Before 6.3:** the log write (§7).
2. Stage 6 per the actor map; 6.4 evidence into the report.
3. Finalize the report: verdict paragraph, every ⚠️/❌ row cross-linked to a finding or
   disposition, handoff and commit plan filled.
4. Runbook reconciled: 66/66 ticked, or unticked-with-report-note. Never tick what didn't happen.
5. `docs/bug-fix-plan.md`: rewrite the `:158` **Remaining** line as the honest successor list
   (the fix pass over the run's findings; §7 #15 if still open; the waiting-only-stall call) and
   append the campaign-convention compressed `>` verdict block under Phase 4 — counts by severity,
   claim dispositions, R1 boundary, fresh-start verdict, report pointer. If Operator makes the R1
   call mid-run, #15 gets its resolution paragraph in the same edit.
6. **Gated commits** — you propose, Operator authorizes each individually; no push unless asked;
   repo style (evocative imperative title, prose body):
   - **A** (optional, pre-run — preflight 8): runbook 0/66 + checker + this plan, as verified.
   - **B** (post-run): the run's artifacts — ticked runbook, the report (+ checker and this plan
     if A was skipped). Shape: "Execute the dev run: N findings, the 12 claims dispositioned, R1
     characterized."
   - **C** (post-run): bookkeeping — the log section + the plan `:158`/verdict edits (separate,
     per the `b0b55df` log-the-phase precedent).
7. **Backups outlive the run:** the Stage-0 backup, the `_captured` archive, and
   `sample-secrets-keep.bin` are kept until the fix pass completes and its verifiers report —
   extending 6.5. The fresh app being healthy is necessary, not sufficient.

## 10. Risk register

| Risk | Mitigation |
|---|---|
| Stage 2 is one-way; a casual pre-run launch consumes it **silently** | preflight `pre` the same day as Stage 0; app closed from preflight to 2.2, enforced by process check, not memory |
| Sync-tool blast radius — `plan\lists` propagates to every device | 1.2 mandatory before 1.4; 2.3b checks another device; restore step 3 propagates *intentionally* |
| The `_captured` zombie landmine (4 chats re-ingest on the fresh app) | 6.1 hard-gates 6.3; 6.4's last box verifies the sweep recovers nothing |
| No single-instance guard | process check before every launch; rehearsal terminated before 2.2 (2.1's precondition) |
| Scratch-instance mismanagement | artifact-gated quit, never inside the memory-write window (bare `writeFileSync`, no temp file); every process op scoped by scratch-dir `CommandLine` match; orphan after session death → re-copy, redo Stage 1 |
| Measurement contamination | checker runs require the app quit (`:68`); `post` counts valid only immediately post-launch (`devrunCheck.ts:90`); no `settings.json` writes while the app runs; nothing into `sample_in` until 2.4 |
| Date staleness if the run slips | the delta table is recomputed every run day; the Jul→Aug boundary flips 3.8's fixture and end-of-month |
| robocopy semantics | exit codes 0–7 all mean success — do not misread exit 1 as failure |
| Session mortality | the report is the crash-recovery state; resume procedure in §4 |
| The refusal fixtures | Operator types them in-app; a hard stop is the expected outcome; you record only |

---

## Appendix A — report skeleton

Copy out at preflight as `docs/dev-run-report-<runday>.md`; fill as the run proceeds.

```markdown
# Dev run — <YYYY-MM-DD>

<verdict paragraph — written last: what ran, what it found, what happens next>

Operator: Operator · Scribe: Claude Cowork (<model>, effort <x>) · Repo: HEAD `615e638`
Runbook: docs/dev-run-runbook.md (untracked, verified 2026-07-26, 66 boxes) · Plan: docs/dev-run-cowork-plan.md
Sittings: <date/time ranges, local>

## Run-day delta table
| Runbook literal | As written | This run |
|---|---|---|

## Preflight
| Item | Result |
|---|---|
<incl. transcribed `pre` info lines: engine/model/effort · lastOpenedAt → derived rendering · WILL-fire predictions>

## Stage results
### Stage 0 — build & backup
| Box | Actor | Result | Evidence |
|---|---|---|---|
| 0.1 | C | ✅ | typecheck+build green (appendix) |
<one row per box; ⚠️ = observation, ❌ = finding ref F#. Repeat per stage 1–6, R1.>

### Stage 2 — timeline
<timestamped paragraph from the hot-launch transcript: t0 migration/repairs · stampOpened ·
settings.bak.json · window · export + second settings write · t+5 s poll · t+8 s recovery ·
memory refresh landing>

## Findings
### F1 — <title> (`file:line`) — <sev>
Surfaced by: <box> · What we did: · What we saw: · What should happen (per <plan/code ref>): ·
Repro (fresh-DB): · Needs migration-history DB: yes/no · Suggested lane → model: ·
New / confirms claim <n> · Log anchor: <## The dev run — date / F1>

## The 12 claims — dispositions
| Claim (`file:line`) | Vehicle | Verdict | Evidence |
|---|---|---|---|
<CONFIRMED-BUG (→F#) / REFUTED / CLOSED-BY-2.4 / UNTESTED (reason)>

## R1 — characterization (a repro under plan §7 #15, NOT a new finding)
Staged parks: · Landing row vs target: · Nag: · "Triage this date" outcome: ·
Gone from disk or merely unlinked: · ~9-month boundary: ·
Matches the `knownOpen` pin (`phase4Smoke.ts:833-838`, expects `{iso: past, due: true}`): yes/no ·
Options for #15 (decision is Operator's):

## Product calls surfaced
<the standing two — waiting-only-stall (log:1830), R1 fresh decision (plan:282) — plus any new,
each NEEDS-DECISION with options only>

## Stage 6 — fresh start
<the four 6.4 checks · secrets restored? · archive locations · keep-until rule>

## Handoff — the Phase 4 fix pass (read this cold in Claude Code)
Inputs: this report + `docs/bug-fix-log.md` § "The dev run — <date>".
| Lane | Owns (exclusive) | Findings | Model · effort | Notes |
|---|---|---|---|---|
Fixers: bug-fix-plan.md §5.1 verbatim, paste the log entries. Verifiers: §5.2.
Environment: §5.1's rules apply, plus — post-scrap there is no migration-history DB; findings
flagged needs-migration-history are fixed against captured evidence, or against the Stage-0
backup restored into a SCRATCH --user-data-dir (never the real profile).
Gates after every merge: typecheck · build · laneStore 186 · laneUiA 135 · laneProv 34/33 ·
laneIpc 34 · laneEvents 36 (both zones) · laneSet 25 · laneSetUi 15 · laneIpcUi 7 ·
phase4Smoke 29 pass + 1 known-open, no skips.
knownOpen rule: fixing R1 = convert pin B to a real check AND update plan §7 #15 AND the
`ticklerFileCounts` warning comment; re-pinning a corrected boundary = update the pin's values +
the log; never delete the pin.
Backups: <locations> — keep until this fix pass completes and its verifiers report.

## Commit plan (gated — Operator authorizes each)
<prepared commands + messages for B and C (and A if taken pre-run)>

## Transcripts appendix
<verbatim: preflight pre · 1.5 post · 1.6 pre · 2.4 post · 6.4 probe · any restore verification ·
the hot-launch transcript · the ad-hoc probe outputs backing Stage 3–5 verifications>
```

## Appendix B — probe kit (read-only, run from repo root)

All DB access `{ readOnly: true }` via `node:sqlite` — the pattern is `devrunCheck.ts`. The app
exports the DB to disk after every write (`docs/dev-plan-review.md:27`), so a probe after a
gesture sees that gesture. Probes are informational; they never replace a checker gate.

- **P-1 process check** (quiescence, quit verification, single-instance):
  `Get-CimInstance Win32_Process -Filter "Name LIKE 'electron%'" | Select-Object ProcessId, CommandLine`
  — real-profile instances have no `--user-data-dir`; scratch instances name theirs. Observe only.
- **P-2 scratch quit** (rehearsal only): among P-1 rows whose `CommandLine` contains
  `sample-rehearsal`, call `CloseMainWindow()` on the windowed process; wait for exit; after a grace
  period `Stop-Process` any stragglers **matching the same dir filter**. Never touch a row that
  doesn't match.
- **P-3 DB probe template**: discover first, then query —
  `node -e "const{DatabaseSync}=require('node:sqlite');const d=new DatabaseSync(process.env.APPDATA+'\\sample-app\\data\\sample.sqlite',{readOnly:true});console.log(d.prepare('SELECT ...').all())"`
  (schema via `PRAGMA table_info(items)` etc. — don't guess column names; for the rehearsal copy,
  substitute the scratch path). Uses: 3.1 created-item dates; 3.2/3.3/3.4 chat + item rows and
  transcript text; 3.8 `location='tickler'` + `tickler_due`; 4.1 moved-row counts; 4.5 status
  round-trips; 5.1 duplicate detection; 5.5 `data` JSON.
- **P-4 capture-folder listing**: `Get-ChildItem "$env:USERPROFILE\Desktop\sample_in\_captured"` —
  epoch-prefixed names; for R1-c, prove the parked file's presence/absence on disk.
- **P-5 frozen-row survival** (after each 3.7 round): P-3 on the 7 ids printed by the checker —
  status, title unchanged, and no near-duplicate rows beside them.
- **P-6 export artifact read**: `Get-Content` on the exported `.ics`/list files.
- **P-7 blast-radius snapshot** (before/after 5.4's Delete): P-3 dumping id+title+kind+status for
  chats, items, projects to a JSON file in the report's transcript appendix dir; diff the two
  dumps — the blast radius gets measured, not recalled.

---

*Written 2026-07-27 against HEAD `615e638`. This plan is untracked until Commit A/B (§9.6); the
runbook and checker it orchestrates are untracked the same way. The findings are the deliverable —
the database is scaffolding.*
