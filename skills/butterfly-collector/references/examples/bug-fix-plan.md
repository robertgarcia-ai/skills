> **SANITIZED EXEMPLAR.** Personal names, usernames and machine-specific identifiers were replaced (Operator, REDACTED-USER, ExampleCorp, Sample), and the app identity was additionally fictionalized (SampleApp, sample-app, Nudge Queue and kin) with timezone and personal context generalized; everything else — structure, numbers, wording — is verbatim from a completed real campaign (2026-07). Read for shape and conventions, not as instructions to execute.
>
> **Take from this:** §1's principles each carrying their *why*; lanes with exclusive file ownership; §5's four verbatim-adaptable prompts (fixer / adversarial verifier / mechanical sweep / orchestrator self-instructions, incl. the §5.4 coverage check); §7 as a decisions waiting room; the Status stamp updated in place. Map: header/Status · §1 principles · §2 phases+lanes · §3 models · §4 mechanics · §5 prompts · §6 estimates · §7 decisions.

# Bug-Fix Orchestration Plan

Source: [`docs/bug-hunt-2026-07-23.md`](bug-hunt-2026-07-23.md) — **78 confirmed** (17 high / 30 medium / 31 low) + **5 disputed**. Nothing has been fixed yet; this document is the execution plan. Written 2026-07-24.

**Status 2026-07-28 — the campaign is COMPLETE.** Phases 0–4 all executed, merged and adversarially
reviewed, and the closing dev run (the last item on Phase 4's **Remaining** line) ran 2026-07-27/28;
its canonical record is [`docs/bug-fix-log.md`](bug-fix-log.md) § "The dev run — 2026-07-27/28".
What outlives this plan is the successor list under Phase 4 → **Remaining** below.

The plan answers three questions: what order to fix things in, which Claude model runs each lane, and how to run lanes in parallel without them trampling each other — plus the exact prompts to hand each worker.

---

## 1. Principles the whole plan obeys

1. **Git before anything.** The repo is not version-controlled. Seventy-eight fixes without revert, diff, or branch isolation is how one bad fix silently poisons the next thirty. Phase 0 initializes git; parallel lanes then run in **worktrees**, so no lane can see another's half-finished edits.
2. **Cluster by root cause, not by finding.** Six-plus findings are one timezone disease; four are one "claim the file before ingesting it" disease; three are one "re-triage deletes suggestions" disease. Fixing root causes collapses the list and prevents whack-a-mole.
3. **One owner per file, ever.** `App.tsx` (27 findings) and `main/index.ts` (23) dominate. Two agents editing a 4,000-line file in parallel is merge hell even with git. Every lane below has exclusive ownership of its files; lanes that share no files run simultaneously.
4. **Repro → fix → prove, every time.** A lane may not fix a bug it hasn't first demonstrated (via the CDP harness against a built app on an isolated `--user-data-dir`, or a `tsx` spike for pure logic). The bug report's own *Repro* line is the test case. A fix without a before/after proof doesn't merge.
5. **Adversarial verification before merge.** Every merged lane gets a fresh-context reviewer whose job is to *refute* the fix — the same discipline that made the bug hunt trustworthy.
6. **Minimal diffs.** Fix the defect; no drive-by refactors, no "while I'm here." The newer models follow this literally when told — so tell them (prompts below).
7. **Product decisions are Operator's.** Eight findings encode "what *should* happen?" questions, not just "the code is wrong" (list in §7). Lanes flag these instead of inventing policy.

---

## 2. Phases and lanes

Time flows down; lanes inside a phase run **in parallel** (disjoint files). Each lane lists its findings by `file:line` from the report.

### Phase 0 — Safety net (serial, ~an hour)

One session, no parallelism, nothing to conflict with.

- `git init`, commit everything as the baseline, tag `pre-bugfix`.
- Copy `%APPDATA%\sample-app\data\sample.sqlite` to a dated backup (the fixes touch persistence itself).
- Confirm gates: `npm run typecheck` + `npm run build` green; one CDP smoke launch of the built app.

**Model:** Sonnet 5 — mechanical work. | **Effort:** low.

### Phase 1 — Foundations (2 parallel lanes)

Everything later leans on these two, so they go first.

**Lane DB — data durability** (`src/main/store.ts` — exclusive owner)
- `store.ts:67` persist() non-atomic whole-file rewrite → write temp + rename, keep a rotating `.bak`.
- `store.ts:30` corrupt DB = silent no-window zombie → detect load failure, fall back to the `.bak`, and show an error dialog instead of nothing.
- Proof: harness that truncates a copy of the DB mid-file and asserts recovery.

**Model:** Opus 4.8, effort **xhigh** — this is the scariest correctness work in the plan, and the failure mode of a wrong fix is losing the database. | Fable 5 as the *reviewer* of this lane's diff (§5) if you want the strongest adversarial eyes on it.

**Lane DATE — the timezone foundation** (new file `src/shared/dates.ts` + `src/triage/schema.ts` only)
- Build the local-date helpers: `todayLocalISO()`, local `ymd`, next-occurrence logic that handles Feb 29 (`index.ts:260` low), and a documented rule: *user-facing dates are always local; `toISOString()` is for storage timestamps only.*
- Pure functions, spike-tested across the boundary cases the hunt flagged: evening US-Eastern, New Year, DST, leap day.
- This lane deliberately does **not** touch the call sites — those belong to the lanes that own each file (Phase 2), which keeps ownership clean.

**Model:** Opus 4.8, effort high — small code, but every later lane inherits its correctness.

### Phase 2 — High-severity clusters (3 parallel lanes)

**Lane MAIN — capture, tickler, calendar** (`src/main/index.ts` — exclusive owner)
Sequential within the lane; one root-cause family at a time.
1. Claim-before-ingest family: `659` (quit strands file), `664` (failure strands file) → invert the flow: ingest first, move to `_captured/` only on success; add a startup reconciliation for anything stranded historically.
2. `463` tickler mojibake + **deletes the file** → type-check before ingest; unsupported types surface as a "file is waiting" chat instead of being decoded and destroyed; never delete on a failed ingest.
3. `385` missed tickler day rolls a year + `260` UTC day math → adopt Lane DATE's helpers; overdue = "due," never "next year." **Use `ticklerDueISO` for resolving a year-less day-folder to its nag date — NOT `nextOccurrenceISO`, which by contract never returns a past date and therefore reproduces `385` byte-for-byte** (`nextOccurrenceISO(7,20)` on 2026-07-21 → `2027-07-20`, identical to the old bug). See §7 decision #10 for the 60-day window. Also note `nextOccurrenceISO` can now return `""` for a month/day that can never occur (a hand-made `02 February/30/` folder) where the old code always returned a string: guard it at `index.ts:424`, but **do not simply `continue`** — silently dropping the folder means it never appears in the calendar or the nag at all, which is worse than the old wrong-day behavior. Surface it.
4. `1195` calendar export counts dropped events + user-created events can never get a date.
5. `1357` marking an item done awaits `triageChat` unguarded, so completing it offline rejects the IPC *after* the DB mutation and the UI never refreshes → catch around the post-mutation triage: the status change is already committed, so it must still resolve and refresh. Same unhandled-rejection family as `877` and `421` below. *(Added 2026-07-24 — a high finding the original plan's lists missed.)*
6. `827` + `841` — the half of `store.ts:320` that actually produces the harm. `listItemsForProjects` omits `"waiting"`, so outstanding waits are invisible to the model (it proposes a duplicate step), and `hasOpenAction` excludes `waiting`, so `goalMet` archives a project to Reference with a wait in flight. **Neither site appeared in any lane's list** — the same coverage-gap class as the two highs found in Phase 1. Lane STORE fixed the store half, which turned out to be dead code: `projectsNeedingGoalAction` has no production consumer, and the batch pass iterates `activeGoalProjects()` without consulting the stall gate. *(Added 2026-07-25, from Lane STORE's adversarial review.)*
7. Mediums in the same file: `178`, `index.ts:874`, `571`, `877`, `208`, `425`, `421`, `878`, `852`; lows `653`, `472`, `1004`, `656`, `1126`, `1267`.

**Model:** Opus 4.8, effort xhigh. This lane is concurrency + lifecycle + filesystem — exactly where the strongest model earns its price.

**Lane STORE — semantics of items and projects** (`src/main/store.ts` after Lane DB merges — sequential handoff, same owner)
1. `360` re-triage wipes user edits on suggestions (+ `365` title-match dedup) → preserve user-touched suggestions; dedup by identity, not exact title.
2. `160` deleting a parked chat strands items; `742` parking destroys project filing.
3. `460` belongs_to name-matching steals items globally; `250` cross-project chat claim; `320` waiting items not counted as open.
4. Lows: `872`, `990`, `186`.
- ✅ The four §7 decisions this lane depends on (1, 2, 3, 5-adjacent) are **resolved** — see §7. **Schema note:** decision #1 (user-touched suggestions are sacrosanct) needs a way to tell a hand-edited suggestion from a purely model-generated one. If no such signal exists, this lane's first task is to add one (an `edited`/`user_touched` flag on items, set whenever the user renames / pins / sets a deadline), migrated in via the same ALTER-TABLE-if-missing pattern as `pinned`. That migration is a prerequisite for the `store.ts:360` fix and must land first within the lane.

**Model:** Opus 4.8, effort high. The SQL is easy; the *semantics* are subtle.

**Lane UI-A — renderer traps** (`src/renderer/src/App.tsx` — exclusive owner; the biggest lane)
Ordered by user pain:
1. `350` file drop navigates the whole window to the file (add window-level `dragover`/`drop` preventDefault outside real drop zones).
2. `3524` "Move to IN" makes confirmed items invisible forever.
3. `3977` Enter mid-stream silently discards the typed message (queue or block, never clear).
4. `App.tsx:874` project filter silently filters IN/WEEKLYSWEEP; `325` stale menu closure blanks lists. *(Spelled with its file because `index.ts:874` is a different finding in Lane MAIN's list — the two collide on line number only.)*
5. `1096` UTC park targets (adopt Lane DATE helpers) + `1087` month/day-only calendar match.
6. Mediums `969`, `1832`, `1421`, `3671`, `651`; lows `1760`, `2167`, `3869`, `3638`, `3647`, `3982`, `3712`, `3834`, `3274`, `3077`, `458`, `436`, `626`, `3064`, `1163`.

**Model:** split. Items 1–5 + `969`/`1832`: Opus 4.8, effort high (state races, closures, memoization). The low sweep at the end: hand the lane to **Sonnet 5** with the itemized list — well-specified small diffs are exactly its lane, at a third the price.

### Phase 3 — Peripheral files (3 parallel lanes, all small) — ✅ COMPLETE 2026-07-25

Run **sequentially in one session** rather than as parallel subagents (the §4 "interactive alternative"):
the three lanes total ~2,900 lines across nine files, so worktree isolation bought nothing, and one
context is what made the file-by-file coverage cross-check possible. See `docs/bug-fix-log.md`.

**Lane PROV** (`src/provider/*`, `src/shared/effort.ts`): `anthropic.ts:186` (**high**, *added 2026-07-24 — the original plan's lists missed it*) the triage prompt hands the model the UTC date as "Today's date", so evening captures resolve "tomorrow" a day late → adopt Lane DATE's `todayLocalISO()` (this is why the lane runs after Phase 1, not before); **`ollama.ts:296`** (*added 2026-07-25*) the identical line in the local provider, in no finding list because the hunt report contains no `ollama.ts` findings at all; `effort.ts:15` xhigh sent to 4.6-era models → gate per model; `anthropic.ts:437` transcribe truncation (check `stop_reason`, continue or raise cap); `335` refusal → visible message not silent empty reply; `198` + `11` env-override footguns; disputed `claudeAgent.ts:138` (verify empirically against the Agent SDK first — it may be a non-bug). **Model:** Sonnet 5, effort high.
> ✅ Merged `8aafdcd`. Disputed `claudeAgent.ts:138` **refuted** against the shipped binary and the file left untouched — the SDK converts `thinking:{disabled}` to `--thinking disabled` and the bundled CLI omits the wire param for `claude-fable-5`. Note for anyone touching the effort gate: the level list agrees with the CLI's own `xhigh_effort` predicate, and the picker **disables** the unavailable level rather than removing it, because removing the selected option is the `App.tsx:3991` mechanism.

**Lane SET** (`src/renderer/src/Settings.tsx`, `src/main/settings.ts`): `526` custom interval never syncs, `140` duplicate connector ids, `164` update discards edits, `settings.ts:33` corrupt file silently resets — **both halves**: write with temp+rename so a crash mid-save cannot tear the file at all (`store.ts`'s `persist()` is the proven pattern; `saveSettings` at `settings.ts:120-122` is still a bare `writeFileSync`), *and* on a read failure back up the corrupt file and tell the user instead of silently returning defaults, which the next save then makes permanent. *(The temp+rename half added 2026-07-25 — the finding text names only the recovery, and prevention is the half that saves the data.)*, disputed `settings.ts:12` args guard (cheap hardening regardless). **Plus two the plan assigned to nobody** (*added 2026-07-25*, found by checking every finding whose file this lane owns rather than sweeping by severity): `Settings.tsx:572` re-export ignores the typed folder and misreports every failure as "set a folder first", and `Settings.tsx:192` clearing "Your name" is undone on the next load by a first-run fallback that fires on any empty name. **Model:** Sonnet 5, effort medium.
> ✅ Merged `92d9a59`. ⚠️ **A read-only `settings.json` no longer stops the app** — temp+rename succeeds where `writeFileSync` threw, so Lane MAIN round 2's `r-h` fault injection no longer faults. The startup guard is intact (re-verified with `settings.json.tmp` made a directory). The review then found a flaw in this lane's own fix: an interrupted save leaves no `settings.json` beside a good `.bak`, which read as a first run — fixed in `08070f0`.

**Lane IPC** (`src/preload/index.ts`, `src/renderer/src/useChat.ts`, `src/shared/ics.ts`): `preload:21` dropped `parked` flag ("No items found" while silently parked), `useChat:136` wedged streaming state, `ics.ts:60` DTEND before DTSTART, `ics.ts:38` emoji fold split, disputed `ics.ts:53` (spike V8's actual date rollover first). **Model:** Sonnet 5, effort medium.
> ✅ Merged `1b7504e`. Disputed `ics.ts:53` splits: the **crash is refuted** (the spike runs the old helper and shows `2026-06-31` → `2026-07-02`, no throw), but its **residual defect was real** — an impossible date reached the export as an RFC-invalid `DTSTART`, and `HHMM` accepted `24:00`/`99:59` as timed while the UI called it All day. `eventDetails` now asks whether the date is a day that exists.

### Phase 4 — Regression pass (the verify fleet) — ✅ COMPLETE 2026-07-25

Re-ran the bug-hunt workflow scoped to the changed files — 6 finders + 2 adversarial verifiers per
finding — plus the coverage check, the two disputed re-reads, all gates, and a new full-app CDP smoke
of the golden paths. See `docs/bug-fix-log.md`.

> ✅ **The coverage check came back clean** — the first time in the campaign. All 83 findings
> (78 confirmed + 5 disputed) across 11 files have an owner and a closing commit. The more useful
> half of that check was the inverse: **7 of the 17 changed product files carry zero findings from the
> original hunt**, which is where the fan-out was pointed.
>
> ✅ **Both disputed findings re-read; both refutations stand.** `index.ts:926`'s refutation rests on
> machinery that survived Phase 2 intact (`App.tsx:775-778`, `408-412`). `App.tsx:3991` stays latent
> only because `models.ts` is untouched by the whole campaign — trimming `CHAT_MODELS` would activate
> it, and the model picker is the one `<select>` with no fallback for a stored value outside its list.
>
> ⚠️ **The fan-out found 5 real regressions, all high, every one re-confirmed in code by the
> orchestrator — and all five are now fixed.** Three immediately (`App.tsx` — a private un-tightened
> `eventDetails` copy; a widened query silently killing the goal-stall banner; a swap gate that misses
> the ordinary case). Two after Operator's decisions (§7 **#15** and **#16** below): `index.ts:499`
> infers a parked file's year from the folder's oldest mtime, and `moveItemToProject`/`claimItemChat`
> now report what they carried. Proof in `laneUiA` (133), `laneStore` (181) and `phase4Smoke` (33),
> each falsified against pre-fix code.
> **12 further findings were never verified** — the fan-out capped verification at six — so they are
> claims, not findings. All listed in the log.
>
> ✅ **All five adversarially reviewed** (two Fable reviewers, §5.2). **R3/R4/R5 SOUND.**
> **R2 FLAWED** — the carried count was measured against the chat's own project instead of the
> destination, so the flagship make-project reunite gesture reported "2 items filed under Reno moved
> to Reno" with nothing moved; plus a wrong destination name on project pages; plus **a guard that
> could not fail** (its own function definition counted toward its `>= 3`). All fixed and re-proved.
> **R1 FLAWED → REVERTED** (decision **#15**): mtime reads the last *write*, not the park, so
> re-saving a parked file silently defers a due folder by a year (decision #10's exact harm), and the
> roll changed only the calendar row while `ticklerDayFolders` stays year-blind, so the early
> ingest-and-delete it was written to stop still happened whenever a chat shared the month/day.
> `ticklerFileCounts` is byte-identical to its pre-R1 self again; **the underlying bug is live**, with
> a warning at the site and a pinned `OPEN` case in `phase4Smoke` so the suite cannot go green over it.
>
> **The reviews earned their price twice over**, and the standing lesson is sharper than before: two
> checks written *this phase* to prove a fix could not have detected its absence — a CRLF regex that
> matched nothing, and a guard whose own definition satisfied it. **A guard is not evidence until it
> has been run against code that should fail it.**
>
> **Probe notes for next time.** The golden-path smoke is `src/spike/phase4Smoke.ts`, **25 checks, no
> skips**: it drives the built app on a throwaway `--user-data-dir` with a **fake local-model daemon**
> (`engine: "ollama"` + `localTriage: true` pointed at 127.0.0.1), so triage is deterministic, free
> and offline while still exercising real main/store/provider code. Driving Electron's native save
> dialog on Windows took four wrong turns, all worth knowing: UIA's `RootElement.FindAll(Children)`
> does **not** list it (only Win32 `EnumWindows` finds it — `Save As`, class `#32770`); it has **no
> Win32 child windows**, so `FindWindowEx`/`GetDlgItem` find nothing; `UIA FindAll(Descendants)` on it
> never returns in time because it enumerates the whole file listing; and its controls are **not typed
> as controls** — Save is a `Pane` with `AutomationId = 1`, so a ControlType search picks up the
> *Search Box* and no Save button. Match on `AutomationId`, walk breadth-first with a depth cap, and
> answer with `SendMessage(WM_COMMAND, IDOK)` — which, unlike keystrokes, needs no foreground focus and
> so cannot be defeated by a fullscreen app or land its input somewhere else.

> ✅ **The dev run is complete — 2026-07-27/28, two sittings, operator Operator, Claude Cowork
> (`claude-opus-5`) scribing.** Canonical record: `docs/bug-fix-log.md` § "The dev run —
> 2026-07-27/28"; report: `docs/dev-run-report-2026-07-27.md`. Preflight found Stage 2's one-way
> hot launch **already consumed** (2026-07-26 15:36 local, unobserved, ordinary use since); the
> migration observation was reconstructed on a scratch profile built from the byte-identical
> pre-migration backup and re-run in full — `devrunCheck` `pre` **and** `post` ended
> `ALL CHECKS PASSED`, so every Stage-1/2 assertion is evidenced rather than forfeited
> (`user_version` 0→2, rows 75/251/41/151 intact, exactly 7 frozen rows, `draft_key` NULL on
> exactly 32, zero `repair` log entries).
>
> ⚠️ **Thirteen findings** — 2 high, 1 medium-high, 8 medium, 2 low-medium, each with a fresh-DB
> repro and a lane → model assignment in the log. The highs: **F1** `generateMemory` treats a
> contentless 200 as success and silently overwrote the real 2,724-char memory profile with `""`
> (the unguarded empty-result family spans six call sites, one guarded); **F5** decision #16's
> relocation sentences never render on the `moveItemToProject`/`claimItemChat` paths — R2 is
> re-opened in effect. **F3** (medium-high): the Agent SDK engine dresses a policy refusal as
> "Couldn't reach Claude" — the exact framing `anthropic.ts:32-34` forbids.
>
> ✅ **The twelve unverified fan-out claims are all dispositioned** — 5 CONFIRMED (`store.ts:154`
> kind-move, `Settings.tsx:693` interval, `App.tsx:4291` undated-event time, `App.tsx:1169` sort
> leak, `index.ts:1220` latent with its precondition now live in `_captured`), 1 confirmed dead
> code (`parkChat suggestedOnly` — decision #4 holds by a different guard), 2 REFUTED
> (`App.tsx:3682` already fixed; the 5.4 blast radius — a day view has no "Delete project"),
> 1 UNCONFIRMED (the settings-rollback claim; a mid-run CONFIRMED verdict was retracted as a
> scribe error), and the `repairOnce` persist-before-stamp claim CLOSED by the observed launch,
> along with the ledger/seed/export trio.
>
> ⚠️ **R1 characterized** (§7 #15 — run against real data, destructively, as the runbook asked):
> decision #10's 60-day window is **exact** (files 62 and 61 days back are silent; 60 nags). Three
> distinct defects: a file parked for June 28 **2027** was nudged in as `2026-06-28`, ingested and
> **destroyed** — only its text survived as the chat body; chats whose `tickler_due` records the
> correct year are nudged in early anyway (the resurface path never reads it — one sixty seconds
> after parking); and the year is lost non-deterministically because the tickler prompt asserts
> the parked date "is today" while the content says 2027. Closure options and a recommendation
> are in the log; **the #15 decision is still Operator's.** *(Taken 2026-07-28: a fourth design —
> the **Later holder** + destruction guard; spec at #15.)*
>
> ✅ **What the run proved works:** the migration's only meaningful execution; the UTC date fix
> under the exact condition that used to break it (a send 95 s before local midnight); the refusal
> note against the real API for the first time; the frozen-row guarantee under deliberate attack
> (four re-triages, a rename, a restatement — nothing lost); capture end-to-end including a 1.2 MB
> oversize degrading gracefully. Runbook 3.4's "truncation marker" tests a behaviour that does not
> exist.
>
> ⚠️ **Stage 6 — the scrap and fresh start — has NOT run** (pending, Operator; runbook 6.1–6.5).
> 6.1 (move `Desktop\sample_in\_captured` aside) is **mandatory first**: it holds
> `20260726_233750.jpg` twice with different bytes, so a post-scrap recovery sweep would judge one
> already-captured and never recover it (claim 5.2's precondition, live today). The Stage-0
> backup, `_run-evidence\`, the `_captured` archive and `sample-secrets-keep.bin` are kept until the
> fix pass completes **and its verifiers report**.

**Remaining (updated 2026-07-28 — decisions in):** the fix pass over the run's findings — **13
findings + 5 confirmed claims**, plus the decisions taken 2026-07-28: **#15's Later holder +
ingest destruction guard** (its own cross-file slice) and **#17's** stall-banner alignment;
lane → model per finding in the log, handoff in the report. **Runbook Stage 6** (scrap + fresh
start — Operator, 6.1 first). Commits: B `a951422` and C `14e4bde` landed; **D** (these decision
recordings) proposed and gated.

**Models used:** finders and verifiers both Opus 5 (inherited from the orchestrator session) rather
than the Sonnet/Opus split planned below — 18 agents, 0 errors, ~2.1M subagent tokens.

---

## 3. Model assignment — the reasoning

| Model | $/MTok in/out | Use for | Why |
|---|---|---|---|
| **Opus 4.8** | 5 / 25 | Orchestrator session; Lanes DB, DATE, MAIN, STORE, UI-A hard half; verifying high-sev fixes | Best long-horizon agentic execution; races/lifecycle/semantics need it. Run effort **high** by default, **xhigh** for DB + MAIN. |
| **Sonnet 5** | 3 / 15 (intro 2 / 10 through 2026-08-31) | Lanes PROV, SET, IPC; UI-A low sweep; Phase-4 finders; Phase 0 | Near-Opus on well-specified coding at a fraction of the cost — the workhorse for itemized fix lists. Effort high for fixes, medium for sweeps. |
| **Haiku 4.5** | 1 / 5 | Optional: the most mechanical slice of the low sweep (feedback toasts, guards) with per-item instructions; doc updates | Cheapest; fine when the diff is spelled out. Don't hand it anything requiring judgment — the hunt's own severity data says the low cluster is mostly mechanical. 200K context: give it files, not the repo. |
| **Fable 5** | 10 / 50 | One adversarial review of the Lane DB diff (and optionally Lane MAIN) | The strongest reviewer for the two lanes where a wrong fix destroys data. Overkill as a *fixer* here; use it to try to break the fix. Note: needs 30-day retention; pricey — one or two review calls, not a lane. |

Rule of thumb: **Opus writes what's dangerous, Sonnet writes what's numerous, Haiku writes what's mechanical, Fable attacks what's irreversible.**

## 4. Parallel execution mechanics (how this actually runs in Claude Code)

- **One orchestrator session** (Opus 4.8 — what you're in now). It runs Phase 0 itself, then dispatches lanes.
- **Lanes = subagents via the Agent tool**, each with a `model` override (`opus` / `sonnet` / `haiku`) and — once git exists — `isolation: "worktree"` so each lane edits an isolated copy. Lanes within a phase launch in one batch and run concurrently; the orchestrator merges finished worktrees **one at a time**, running typecheck + build + the lane's proof after each merge.
- **Merge order within a phase:** smallest diff first (fewer conflicts land on the big lanes' merges).
- **Phase 4 uses the Workflow tool** (the same harness as the original hunt) for the deterministic fan-out of finders/verifiers.
- **Interactive alternative:** for phases you want to watch, skip subagents and run lanes sequentially in-session, flipping `/model` per lane. Slower, more controllable — good for Lane STORE where your product calls land mid-lane.
- **Standing footguns for every lane:** never `npm run dev` or kill Electron by window title (your dev app is running — match the isolated `--user-data-dir` instead); `store.ts` trips ripgrep, use Read/`Select-String`; verify against the **built** app.

## 5. Prompting instructions

### 5.1 Fixer-lane prompt (template)

> You are fixing verified bugs in SampleApp, an Electron + React + TypeScript app at `<worktree path>`. `sample_rubric.md` at the repo root defines intended triage behavior — it is the source of truth when a fix needs to know what *should* happen.
>
> **Your lane owns these files exclusively: `<files>`. Do not edit any other file** — if a fix seems to require it, stop and report why instead.
>
> Fix these findings, in order. For each: the mechanism, then the user-visible repro, are quoted from an adversarially-verified bug report — trust the repro, re-verify the mechanism against current code before editing (line numbers may have drifted).
>
> `<paste the findings' full entries — title, description, repro — from docs/bug-hunt-2026-07-23.md>`
>
> Discipline, per finding:
> 1. **Reproduce first** — demonstrate the failure via a CDP run of the *built* app on an isolated `--user-data-dir` (never touch the real `%APPDATA%\sample-app`), or a `tsx` spike for pure logic. If you cannot reproduce it, say so and skip — do not fix blind.
> 2. **Fix minimally.** Only changes the defect requires: no refactors, no helpers for scenarios that can't happen, no formatting churn, match the file's existing idiom and comment density. Do not add features beyond the task.
> 3. **Prove.** Re-run the exact repro and show it now behaves correctly. Then `npm run typecheck` and `npm run build` — both must be green.
> 4. If the correct behavior is genuinely a product judgment call, implement nothing — describe the options and mark it `NEEDS-DECISION`.
>
> Environment rules: the developer's own app instance is running — never kill Electron by window title, never run `npm run dev`; kill only processes whose command line contains your isolated user-data-dir. `src/main/store.ts` breaks ripgrep — read it with the Read tool.
>
> Report per finding: `FIXED file:line — one-line what changed — proof: <repro before/after>`, or `SKIPPED/NEEDS-DECISION — why`. Report every finding; do not silently drop any.

### 5.2 Adversarial verifier prompt (template)

> You are reviewing a bug-fix diff in `<worktree/branch>`. Your job is to **refute** it. The original finding: `<paste finding>`. The claimed fix: `<lane's report>`.
>
> Attack on three fronts: (1) does the original repro *actually* fail to reproduce now — walk it through the changed code line by line; (2) does the fix break any neighbor — trace every caller of the changed functions; (3) does the fix contradict `sample_rubric.md` or an intended behavior noted in `docs/`.
>
> Report every issue you find, including ones you are uncertain about — include confidence and severity per issue; a downstream filter decides, your job is coverage. If the fix survives, say exactly what you tried and failed to break. Verdict: `SOUND` or `FLAWED: <mechanism>`.

*(The "report everything, filter downstream" framing is deliberate: the current models follow conservative-reporting instructions literally, which suppresses recall — this phrasing is what kept the original hunt's recall high.)*

### 5.3 Haiku sweep prompt (only if using Haiku for the mechanical slice)

Same as 5.1, plus: give it **only the files it edits** (not the repo), spell out the exact change per item ("in `X` around line N, wrap the `await` in try/catch and call `setMsg(...)` on failure — mirror the pattern at line M"), and forbid touching anything not itemized. Haiku executes specs; it should not be interpreting bug reports.

### 5.4 Orchestrator self-instructions

- **A lane's finding list is not a partition of the report — check this before every phase.** For each file a phase owns, list *every* finding in that file and diff it against the lane lists. Six findings hid in this gap across the campaign (two highs in Phase 1, `store.ts:320`'s harmful half in Phase 2, two lows in Phase 3, plus `ollama.ts:296`, which is in no list because its file has no findings at all). Sweeping by severity finds the highs and misses the tail; sweeping by file finds both.
- **A fix that adds a step adds a state.** Replacing a one-step write with a two-step one creates an intermediate the old code never saw, and the old code's reading of it silently becomes wrong — Phase 3's interrupted-save flaw and Phase 2's Lane MAIN H1 are the same shape. After any such change, ask what the world looks like *between* the steps.
- Full task spec up front per lane (the models do markedly better with one well-specified kickoff than with drip-fed scope).
- Merge one lane at a time; gates between merges; a lane's `NEEDS-DECISION` items go to Operator *while other lanes keep running*.
- After Phase 2, re-read the disputed-findings list — two of the five sit in files Phase 2 rewrites and may become moot.
- Keep a running `docs/bug-fix-log.md`: finding → lane → commit → proof → verifier verdict. That file is the Phase-4 regression pass's input.

## 6. Estimated shape

| Phase | Wall-clock (parallel) | Dominant cost |
|---|---|---|
| 0 | ~1 hr | negligible |
| 1 | ~2–3 hrs | Opus (2 lanes) |
| 2 | ~1–2 days | Opus (3 lanes, the big ones) |
| 3 | ~half day | Sonnet (3 lanes) |
| 4 | ~2–4 hrs | mixed fleet |

Roughly 60–70% of total tokens land in Phase 2; Sonnet's intro pricing makes Phase 3 + the sweeps cheap. Fable adds two review calls, not a lane.

## 7. Product decisions — RESOLVED by Operator 2026-07-24

All ten answered; no lane is blocked. These are now the **spec** — a lane implements the decision, not its own judgment. **#8 and #10 did not follow the recommended default** (flagged below so nobody reverts them). #9 and #10 were raised during Phase 1 and are not part of the original eight.

1. **Re-triage vs user edits** (`store.ts:360/365`) → **Suggestions the user has renamed / pinned / deadlined SURVIVE AS-IS. Never auto-delete or auto-modify a user-touched suggestion on re-triage.** (The current bug hard-deletes all still-suggested items every re-triage.) An untouched, purely model-generated suggestion may still be replaced by the fresh draft; a user-touched one is sacrosanct → Lane STORE needs a "user-touched" signal (e.g. an edited/renamed/pinned/deadline-set flag) to distinguish them.
2. **Deleting a parked chat** (`store.ts:160`) → confirmed items **become unclaimed but are not deleted with the chat**. ⚠️ **REVISED 2026-07-25: they go back to the project they were parked FROM, not to IN.** The original answer was "orphan to IN", written before decision #3 existed — at that point a day folder recorded nothing about where its contents came from, so IN was the only destination that could not lose them. Once #3 added the park memory, keeping IN meant deleting a chat filed under "Kitchen Reno" left its items in Kitchen Reno while the chat was awake and dumped them in IN while it was asleep: one gesture, two answers, decided by something the user cannot see. Each item's own memory wins over the chat's; `''` (parked from IN) and a since-deleted project both resolve to IN.
3. **Parking a chat with filed items** (`store.ts:742`) → **remember each item's original project and restore it on resurface** (don't dump everything unfiled into IN).
4. **Model auto-park of confirmed items** (`index.ts:178`) → **auto-park applies to SUGGESTED items only; never hide a confirmed/active item.**
5. **"Triage all changed" vs manual parks** (`index.ts:874`) → **skip tickler-parked chats entirely** in the triage-all sweep.
6. **"Move to IN" on an active item** (`App.tsx:3524`) → **demote the item to `suggested`** (genuine re-inbox), so it reappears in IN rather than vanishing.
7. **Unsupported tickler file types** (`index.ts:463`) → **surface as a "file waiting for you" chat with an open-file link.** Never decode a binary file as UTF-8, and never delete the source on a failed/again unsupported ingest.
8. **Enter while streaming** (`App.tsx:3977`) → **BLOCK the send with a visible hint** (⚠ NOT the recommended "queue" — Operator chose block). Enter mid-stream must neither send nor clear the draft; show a brief inline cue that the reply is still generating, and preserve the typed text.
9. **Feb 29 in the rolling tickler calendar** (`shared/dates.ts nextOccurrenceISO`, from `index.ts:260`) → **resolve to the next REAL leap day** — Feb 29 2028 from July 2026. Never the nonexistent `2027-02-29` the old code produced, and never a clamp to Feb 28 or a roll to Mar 1: either would map two distinct day-folders onto one ISO, and `ticklerFileCounts` merges counts by ISO, so a Feb 29 park would silently absorb into its neighbour's. **Accepted consequence:** that date is more than a year out, so `parkChat`→`snapTicklerISO` files it into the **January 2 overflow bucket** — and re-parking on resurface snaps it there a second time, so a Feb 29 park takes **three parks across two New Years** before it visibly sits on Feb 29. Confirmed with that consequence known. Resolved 2026-07-24. ⚠️ **The overflow-bucket consequence is superseded 2026-07-28 by #15's Later holder:** a >10-month resolution now parks in **Later** and is promoted by the 30-day sweep — the three-parks wart collapses to one sweep latency.
10. **A MISSED tickler day** (`index.ts:385` high, via `shared/dates.ts`) → **bounded lookback window: an occurrence that passed within the last 60 days still reads as DUE (overdue); only beyond that does the folder roll to its next occurrence.** (⚠ NOT the recommended "overdue stays due until the calendar year turns" — Operator chose the bounded window, so an ancient forgotten folder stops nagging rather than resurfacing forever.) A day-folder is year-less on disk, so a just-passed day is ambiguous between "you missed it" and "it comes round again next year"; rolling it a full year is the bug. Implemented as a **new** helper (`ticklerDueISO`) — `nextOccurrenceISO` keeps its strict "on or after today" contract, because `normalizeNudgeDate`→`nqFuture` needs a strictly-future date. 60 is an exported named constant, deliberately tunable. Resolved 2026-07-24.

*(11–14 were raised during Phase 2 and are not part of the original eight.)*

11. **A hand-added event's date** (`index.ts:1195`, second half) → **give the Events row editor a date field** writing `EventDetails` JSON into `items.data`. An event typed by hand could never acquire a date at all — no When sort key, no per-event calendar actions, never exported, while still counted in the export's total. Implemented as **Happens on** + optional **Starts**/**Ends** in the ⋯ menu, replacing the Deadline field that never applied to an event (`eventDetails` ignores `deadline` by design). Resolved 2026-07-25.
12. **A non-URL "buy link"** (`App.tsx:3274`) → **accept it and show a chip labelled as not-a-URL**, symmetric with how a Location pin already treats plain text. (⚠ NOT rejection at save time.) The chip says it cannot be opened and clicking it edits instead, because `item:open-pin` genuinely resolves a non-URL buy pin to nothing. Resolved 2026-07-25.
13. **"Make project" steps vs a later chat filing** (`store.ts:730/1289`) → **keep the behaviour, end the silence.** Items travel with their chat; the alternative is the split state finding `store.ts:250` was fixed *this campaign* to prevent. `moveChat` now reports what it carried out of another project and the explicit-filing caller names it ("Filed under Admin — 2 items filed under Taxes moved with it."). Parks and resurfaces use the same call and stay silent. Resolved 2026-07-25.
14. **Deleting a parked chat** — see the revision on decision #2 above. Resolved 2026-07-25.

*(15–16 were raised by the Phase 4 regression pass.)*

15. ⚠️ **REVERTED 2026-07-25. The mtime answer below does not work, the premise it was chosen on was
    wrong, and the bug it addressed is LIVE AND OPEN.** A file parked ~10–12 months out (60 of 365
    cells) shows on the wrong calendar row, nags, and "Triage this date" ingests and deletes it months
    early. `ticklerFileCounts` is back to `ticklerDueISO` alone, with a warning comment at the site and
    the defect pinned as `OPEN` in `phase4Smoke` so the suite cannot go green over it.
    **Closing it needs the year RECORDED *and* `ticklerDayFolders` made year-aware** — a design change
    to the year-less, hand-editable folder scheme, and its own piece of work. Why the obvious
    heuristic fails, so nobody re-derives it: mtime is the last **write**, not the park: re-saving a parked note (an
    atomic-save mints a new file), rotating a parked photo or re-downloading it gives an overdue
    folder's only file today's mtime, which postdates its due date, so it rolls a year and **silently
    stops being due** — decision #10's exact harm. The "can only move forward, so strictly safer"
    argument was the cover for it: forward *from due* is the year-swallowing direction. And it does not
    close the harm anyway — `ticklerDayFolders` matches month/day and never reads the year, so
    "Triage this date" on a same-month/day overdue **chat** still ingests and deletes the file the roll
    just assigned to next year. Recording the year properly does not close it either while the file
    operations stay year-blind: both halves together are a design change to the year-less,
    hand-editable folder scheme. **Needs a fresh decision: revert to the pre-fix behaviour, or take on
    the design change.** The original answer follows, for the record.
    ~~**A parked FILE's year** (`index.ts:499`, regression R1) → **infer it from the folder's OLDEST file
    mtime**~~: if that file was written *after* the past date `ticklerDueISO` chose, nothing in the folder
    can have been parked *for* that date, so it resolves to the next occurrence instead. A parked file
    records no year anywhere — the ISO picks the folder and is discarded — so decision #10's 60-day
    lookback, which is correct for chats, made any month/day inside the window unable to mean "10–12
    months from now"; a file parked for next June came due at once and "Triage this date" ingested and
    **deleted** it months early. (⚠ NOT the alternative of writing a year into a sidecar or the DB:
    the folders are deliberately user-owned and hand-editable in Explorer, so a sidecar would need the
    mtime fallback anyway.) **Oldest, not newest** — a past ISO is only offered by a cell whose folder
    already exists, so an overdue folder holds an older file and stays overdue after a new drop. The
    rule can only ever move a folder **forward**, which is what makes it safe: a hand-copied file with
    an unrelated mtime lands exactly where the old code put it. Resolved 2026-07-25.
    **Characterized during the dev run, 2026-07-28** — full detail in `docs/bug-fix-log.md`
    § "The dev run — 2026-07-27/28" → "R1 — characterized". The 60-day boundary is exact, and the
    harm was run to completion: a file parked for June 28 2027 was nudged in as `2026-06-28`,
    ingested and **destroyed**. Two further defects bound the fix space: chats with correctly
    recorded `tickler_due` years are nudged in early anyway (the `parkChat` resurface path never
    reads the year — files and chats are different paths, and only the file path honours the
    60-day spec), and the tickler prompt asserts a parked date "is today", so even an explicit
    year in the content is lost non-deterministically. Options on the table: (1) the full design
    change — record the year AND make `ticklerDayFolders` year-aware; (2) stop the destruction
    only — never delete the source on ingest, move it to `_captured` like every other capture
    path; (3) fix the `parkChat` resurface path — the one defect that fires on correctly-dated
    data. Scribe's recommendation: 2 immediately, 3 next, 1 when there is room.
    **RESOLVED 2026-07-28 — Operator chose a fourth design: the "Later" holder, plus the ingest
    destruction guard.** Anything parked or dropped that resolves **10+ months out** goes to a
    **Later** bucket instead of a month/day cell: in-app, Nudge Queue shows **Later** after
    December; on disk, `Desktop\sample_in\nudge_queue\` gains a `Later\` folder beside the twelve
    month folders, mirroring the month/day structure inside it — the scheme stays year-less and
    hand-editable, and a Later item's promotion date is computable from its month/day alone, no
    recorded year needed. Every **30 days**, automatically (an app-side sweep in the `maybeX`
    family; the interval an exported named constant, like the 60-day window), Later is reviewed:
    anything now **<10 months out** moves into its proper month/day location; anything still 10+
    months out stays. This closes defects 1 and 2 structurally, for files AND chats — the
    ambiguous 60-of-365 band never receives far-future content, so month/day matching is
    unambiguous for everything outside Later, with prod/resurface/"Triage this date" scoped to
    exclude Later until promotion — and starves defect 3 (content reaches the tickler prompt only
    when genuinely due). **Companion, confirmed the same day: the destruction guard** — ingest
    never deletes a source file; it moves it to `_captured` (epoch-prefixed, ledgered) like every
    other capture path, so the worst case of any future wrong-day resolution is a duplicate chat,
    never a destroyed file. Implementation notes (verify at the code; the design itself is not
    re-litigatable): derive the Later threshold from the lookback constant
    (≥ `365 − TICKLER_OVERDUE_WINDOW_DAYS` days ≈ 10 months) so the two knobs cannot drift apart
    and reopen the band; `snapTicklerISO`'s Jan-2 overflow bucket is superseded (see the note at
    #9); the sweep moves files inside a sync-tool share — benign, but write it to the Activity
    Log. Spans `index.ts` + `store.ts` + `App.tsx`: run as its own sequenced slice in the fix
    pass (Opus 5 · xhigh, **Fable 5** verifier), after the single-file lanes merge.
16. **The two silent relocations** (`store.ts:822`/`:1021`, regression R2) → **finish decision #13 on
    the paths it missed.** `moveItemToProject` and `claimItemChat` return `MoveCarried` and the
    renderer names it, sharing one sentence builder with `relocateChat` so a third wording cannot
    drift. Parks and resurfaces stay silent. **The count excludes the item the user acted on** — a new
    optional `exceptItemId` on `moveChat`, omitted by `chat:move` where every item is a passenger:
    reporting the row you just clicked as something that "moved with it" inflates the one number that
    is supposed to mean *and these came too*. Resolved 2026-07-25.
    ⚠️ **Dev run 2026-07-28: the sentences do not render in practice.** ⋯ → Move to project moved a
    chat's siblings silently, and a chat dropped onto a chatless item printed nothing; the one path
    that spoke was two items born from the same capture input. The decision stands; the
    implementation is re-opened as finding **F5 (high)** in the log's dev-run section.

*(17 was decided after the dev run, 2026-07-28.)*

17. **The waiting-only goal stall** (`docs/bug-fix-log.md:1830`, surfaced by the Phase-4 R5
    review) → **align the banner with the proposer: a `waiting` item counts as work in motion.**
    "Suggest a step" is not offered while a project's only open work is a waiting item — matching
    `openActionCount`, `hasOpenAction` and the auto-proposer's own gate, so the stall banner
    renders only when truly nothing is in flight. Lands in the fix pass (UI-B lane; verify the
    exact banner query against current code — the log records it asking for `active`/`suggested`
    only). Resolved 2026-07-28.
