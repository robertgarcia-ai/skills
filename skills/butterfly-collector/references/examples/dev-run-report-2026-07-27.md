> **SANITIZED EXEMPLAR.** Personal names, usernames and machine-specific identifiers were replaced (Operator, REDACTED-USER, ExampleCorp, Sample); the app identity was additionally fictionalized (SampleApp / sample-app / Nudge Queue and their kin) and the timezone and personal context generalized; everything else — structure, numbers, wording — is verbatim from a completed real campaign (2026-07). Read for shape and conventions, not as instructions to execute.
>
> **Take from this:** the verdict written last but placed first; interim verdicts preserved with inline supersession notes; Run conditions recording the capability probe's adopted mechanism and a scribe error *with the rule it produced*; the run-day delta table; findings in the full protocol with Harnessable-now; the claims table with every claim exactly once; the Handoff written to be read cold. Map: header/verdict · run conditions · delta table · preflight · stage results · findings · claims · known-open · product calls · destructive-stage status · handoff · commit plan · transcripts.

# Dev run — 2026-07-27

**Final verdict — the run is COMPLETE (two sittings, 2026-07-27 21:43 → 2026-07-28 02:13 local).**
Stages 0–5 and the R1 characterization all executed; Stage 6 (the scrap and fresh start) is
deliberately still pending with Operator — see "Stage 6 — fresh start" below. The run produced
**thirteen findings** (2 high · 1 medium-high · 8 medium · 2 low-medium), dispositioned **all
twelve** unverified fan-out claims (5 confirmed — one latent with its precondition now live — 1
confirmed dead code, 2 refuted, 1 unconfirmed after a written retraction, the rest closed by the
observed launch), and characterized R1 against real data: the 60-day boundary is exact, and a file
parked for June 28 2027 was nudged in a year early, ingested and **destroyed**. Three campaign fixes
were confirmed against the real API for the first time. The canonical, complete record — including
findings **F5–F13**, which postdate the sitting-1 sections below — is `docs/bug-fix-log.md`
§ "The dev run — 2026-07-27/28"; this report preserves sitting 1 as recorded live and indexes
sitting 2. What happens next, all with Operator: the fix pass (see "Handoff"), the §7 #15
decision, the waiting-only-stall call, Stage 6, and gated commits B/C (see "Commit plan").

*(Finalized 2026-07-28 ~02:45 local by Claude Code per cowork-plan §9.3, from the canonical log, the
`.devrun\done\` transcripts and read-only profile probes. Sitting-1 sections below stand as written
live at 23:30; where sitting 2 superseded them, an inline note says so. F-numbers in the final log
supersede this report's interim numbering — F1 is unchanged; interim F2 is superseded, see its
note.)*

**Interim verdict (sitting 1 of ≥2, as written at 23:30 local).** The run opened by discovering that its central premise was
already false: Stage 2's one-way hot launch had been consumed on **2026-07-26 at 15:36 local**, and
the app had been in ordinary daily use since. Risk-register row 1 materialised. Rather than accept
the loss, the migration observation was **reconstructed and re-run in full** on a scratch profile
built from the surviving byte-identical pre-migration database — `devrunCheck pre` and `post` both
ended `ALL CHECKS PASSED` against real history, so every Stage-1 and Stage-2 assertion the runbook
makes is now evidenced rather than forfeited.

**3.1 passes**, on two gate-valid samples taken from opposite sides of the UTC boundary — the
date regression the stage was written to catch does not occur. One new high-severity finding
(**F1**) surfaced before a single command ran, and one of the twelve unverified claims (**5.8**)
closed CONFIRMED off the settings file. One candidate finding (**F2**) was raised and **withdrawn**
when a second sample refuted it, and one claim (**5.3**) was reported CONFIRMED and **retracted**
as a scribe error — both recorded rather than quietly dropped. Stages 3 (remainder)–6 and R1 remain.

Operator: Operator · Scribe: Claude Cowork (**claude-opus-5**, effort **high**) ·
Repo: HEAD `615e638`
Runbook: `docs/dev-run-runbook.md` (untracked, 66 boxes, verified 0 ticked at preflight) ·
Plan: `docs/dev-run-cowork-plan.md`
Sittings: **1 — 2026-07-27, 21:43 → 23:30 local** (runner jobs 001–005 through the 23:52 config
restore) · **2 — 2026-07-27/28 overnight, 23:58 → 02:13 local** (runner jobs 006–015; log-canonical)

## Run conditions

The plan assumed Cowork could drive a terminal. It cannot: computer-use grants terminals the
**`click` tier only** — *"you can see and left-click, but cannot type, press keys, or paste."*

Mechanism adopted instead, at Operator's direction: a **persistent job runner**. Cowork writes
numbered `.ps1` jobs into `.devrun\queue\` through the read-write folder bridge; `.devrun\runner.ps1`
— launched once by Operator in a visible terminal at the repo root — executes them sequentially
and writes each job's console output and exit code to `.devrun\done\<job>.out.txt`, which Cowork
stages and reads verbatim. No screen-scraping; the executed script is preserved beside its output.
`?? .devrun/` is **sanctioned** in the preflight tree check. App launches use `Start-Process` with
redirected output so the queue never blocks. Read-only `node:sqlite` probes on staged database
copies are used as a fast supplement, **never** for checker gates — every gate ran on Windows
through the runner.

Reserved to Operator throughout: 2.2, 6.3, 6.4, every in-app gesture, and every destructive
command (shown in chat before queueing).

⚠️ **Scribe error, and the rule it produced.** At 23:45–23:51 a settings rollback was reported as
claim 5.3 confirming itself. It was false: `device_stage_files` returned the **current** mtime while
serving **stale bytes** from an earlier fetch of the same path, and the same path had been staged
three times in fifteen minutes. Job 005, reading on Windows, showed both settings files correct.
Retracted in full — `_run-evidence\RETRACTION-claim-5.3.md`.

**Rule adopted:** no claim about file content becomes a finding until the **runner** has read that
file on Windows. Staged copies are for orientation and read-only database probes only. Where a
staged read must carry weight, corroborate against `device_list_dir`'s independent `size` /
`mtimeMs` fields, which are served separately from file bodies. F1 and claim 5.8 were re-checked
against this rule and stand.

App configuration under test: `engine=agent`, `chatModel=claude-sonnet-5`, `effort=max` on the
recovered Stage-2 profile — the pinned premise, satisfied. The **live** profile has drifted to
`claude-haiku-4-5` / `xhigh` and will be restored through the Settings UI before Stage 3
(Operator's decision).

## Run-day delta table — run day **2026-07-27 (Monday)**

| Runbook literal | As written (for 2026-07-26) | This run day |
|---|---|---|
| 3.1 "tomorrow" (`:46`, `:283`) | Mon Jul 27 | **Tue Jul 28** |
| 3.1 "end of the month" | Fri Jul 31 | Fri Jul 31 (unchanged) |
| 3.1 "next Friday" | Jul 31 / Aug 7 | Jul 31 / Aug 7 — the tested bug is a ±1-day shift, not which Friday |
| 3.1 evening gate | "local evening" | UTC had already rolled to Jul 28; the Jul 27 evening gate window went **not used** — reopens the local evening of Jul 28 |
| 2.3d "last opened" (`:254`) | Fri Jul 24, 5:23 PM | **Fri Jul 24, 5:23 PM** — confirmed live: the recovered profile still carried the original stored UTC `lastOpenedAt` |
| 3.8 fixture "August" (`:328-330`) | parks ~Aug 1 | unchanged — valid through Jul 31 |
| R1 window (`:436`) | "April–June 2027" | **2027-05-28 … 2027-07-26.** Per plan §3.4's formula: month/days whose 2026 occurrence falls in `[run-day − 60d, run-day)` = `[May 28, Jul 27)`. The runbook's "April–June" literal is **wrong** — April 27 2026 is 91 days back, outside decision #10's 60-day lookback. Boundary probe ~9 months out ≈ **2027-04-27** |
| Backup dir names `-2026-07-26` | as written | **keep as written** (`:543`'s restore block hard-codes it) |

Stages 3–5 run on a later day; **this table is recomputed at the start of each sitting.**

## The four preamble corrections — all now empirically verified

| # | Correction | Status |
|---|---|---|
| 1 | `draft_key IS NULL` goes 151 → **32**, not 0 (goal + user rows stay NULL by design) | ✅ **verified** — `post`: "draft_key NULL on exactly 32 rows" |
| 2 | "2,724 chars" is the `profile` string; the file is 2,872 bytes | ✅ **verified** — `pre`: `profile=2724 chars`; file 2,872 B |
| 3 | 1.2's neutralization is mandatory or the rehearsal overwrites the real sync-tool lists | ✅ **honoured, by a stronger mechanism** — see Stage 2 below |
| 4 | List counts are exactly **26 / 0 / 1** | ✅ **verified twice** — `pre` and `post`, disk bullets matching DB active counts |

## Preflight

| # | Item | Result |
|---|---|---|
| 1 | Repo state | ✅ HEAD `615e638` *"Revert R1: the parked-file year heuristic, and pin the bug it left open"*. **No tracked-file modifications.** Untracked: `docs/dev-run-cowork-plan.md`, `docs/dev-run-runbook.md`, `src/spike/devrunCheck.ts`, plus sanctioned `.devrun/` |
| 2 | Runbook virginity | ✅ **66 total / 0 ticked** |
| 3 | `devrunCheck pre` on the **real** profile | ❌ **FAILED — Stage 2 already consumed.** See "The consumed launch" |
| 3′ | `devrunCheck pre` on the **recovered** profile | ✅ `ALL CHECKS PASSED (pre)` — all ~30 assertions |
| 4 | Run-day delta table | ✅ above; R1 window corrected against the runbook literal |
| 5 | Four preamble corrections | ✅ above — all four verified rather than restated |
| 6 | Environment quiescence | ✅ **no Electron process at all.** `sample-*` sweep: `sample-devrun-backup-2026-07-26` (the surviving pre-launch snapshot), `sample-rehearsal` (dirty — completed launch + play), `sample-worktrees` (Phase 1–4 campaign, unrelated). ⚠️ two `notepad.exe` hold `docs/bug-fix-plan.md` open — must be closed before the §9.5 edit |
| 7 | Create the report | ✅ this document |
| 8 | Optional Commit A | **not taken** — deferred into Commit B |

### Preflight 3 info lines — the pinned premises, from the recovered profile

```
engine=agent chatModel=claude-sonnet-5 effort=max
lastListExportDay=2026-07-24 today-key=2026-07-27 → plan-lists export WILL fire on next launch
lastOpenedAt=(stored UTC value) → home view must show Fri Jul 24, 5:23 PM
memory enabled=true updatedAt=2026-07-24T18:06:05.758Z (84.0h old) profile=2724 chars → refresh WILL fire
```

Both **WILL fire** predictions held. Neither read "will not".

## The consumed launch — what preflight found

`devrunCheck pre` on `%APPDATA%\sample-app` fails on roughly a dozen assertions. Evidence:

| Probe | Premise | Live profile |
|---|---|---|
| `PRAGMA user_version` | 0 | **2** |
| chats / messages / projects / items | 75 / 251 / 41 / 151 | **97 / 299 / 50 / 228** |
| `status='suggested'` | 20 | **80** |
| `user_touched = 1` | 7 after launch | **32** |
| `capture-ledger.json` | absent | present, 2,178 B |
| `settings.bak.json` | absent | present |
| `seededCommandIds` | absent | `["summon-helper","orchestrator"]` |
| `lastListExportDay` | `2026-07-24` | `2026-07-27` |
| `memory.json` | 2,872 B / 2,724 chars | **81 B / empty** → **F1** |

Reconstructed timeline: rehearsal launched **Sun Jul 26 12:56:29 local** (scratch ledger, 4 `seen`
entries); **hot launch Sun Jul 26 15:36:04 local** (live ledger's first four entries stamped
`.262–.268` within the same UTC second); ordinary daily use from later that hour onward; memory wiped **Mon Jul 27
16:03:56**; further launches Mon 18:11; last DB write Mon 19:48.

**Not a stop, because nothing was lost that mattered.** The pre-migration database survives in
three byte-identical copies — sha256 `a27a5a7bdfe11240b1d282720cd34557…`, 1,101,824 B,
`user_version 0`, 75/251/41/151 — at `%APPDATA%\…\data\backups\sample.sqlite.2026-07-24-pre-bugfix.bak`
and both copies inside `sample-devrun-backup-2026-07-26`. `repairOnce` runs once **per database file**,
and that file had never been migrated.

**Reversal of a standing instruction:** the Stage-0 backup is **not** refreshed at 0.2. It is the
only surviving pre-launch snapshot; refreshing it would overwrite it with today's migrated state.

## Stage results

### Stage 0 — build & backup

| Box | Actor | Result | Evidence |
|---|---|---|---|
| 0.1 typecheck + build | C | ✅ | `tsc --noEmit` exit 0; `electron-vite build` exit 0. Run as a **hard precondition**, not skipped: `out\main` and `out\preload` carried an unexplained 22:53 mtime while `out\renderer` was still 07-26. All three now share 23:07:3x |
| 0.2 three robocopy backups | C | ✅ **pre-existing and validated** | `sample-devrun-backup-2026-07-26` hash-verified against the live pre-bugfix backup. Deliberately **not** refreshed |
| 0.3 `pre` gate | C | ⚠️ | Fails on the live profile (consumed). Satisfied on the recovered profile — see 2R |

### Stage 2R — the recovered hot launch  ✅

Scratch profile `%USERPROFILE%\sample-stage2`, built from `sample-devrun-backup-2026-07-26\userData`.

**Neutralization, stronger than runbook 1.2.** Rather than stamping `lastListExportDay` to suppress
the export, the scratch `captureFolder` was redirected to `%USERPROFILE%\sample-stage2-capture`, seeded
with the backup's `_captured` (all 5 files, including the two 108-byte `blah.txt` twins that
collapse to one ledger key) and `plan-lists`. Verified at `index.ts:1336` —
`planListsDir() = join(captureFolder, "plan", "lists")` — and every capture path (`:376`, `:610`,
`:1023`, `:1194`, `:1870`) reads the same setting. Sync-tool blast radius zero **and** the export
still fires where it can be measured. The stamp would have suppressed a measurement worth keeping.

**Proof the redirect held**, from the app's own log:

```
#278  2026-07-24T18:05:47.915Z  Exported plan lists to C:\Users\REDACTED-USER\Desktop\sample_in\plan\lists
#279  2026-07-28T06:23:54.219Z  Exported plan lists to C:\Users\REDACTED-USER\sample-stage2-capture\plan\lists
```

Exactly one new entry; six historical ones carried in the Jul-24 database.

#### Timeline — t0 = the scratch launch instant (Mon Jul 27, late evening local)

| t | Event |
|---|---|
| **t+3.2 s** | `settings.bak.json` born · `data\sample.sqlite.bak` born · first `settings.json` write (`stampOpened`) |
| **t+11.5 s** | `capture-ledger.json` created — the +8 s stranded-recovery sweep |
| **t+19.8 s** | `memory.json` rewritten — the memory refresh landed |
| t+26 s | artifact gate met, 6 s settle, graceful quit (4 processes, `CloseMainWindow` on the windowed one, none forced) |

⚠️ **Instrument limitation, not a finding:** the runbook predicts **two** `settings.json` writes
(`stampOpened`, then the export's). The poll ran at 500 ms granularity and saw one; both landed
inside the same second (final mtime in the same second as log entry #279). The export's write is independently proven by
`lastListExportDay` moving 07-24 → 07-27 and by log entry #279.

#### `devrunCheck post` — `ALL CHECKS PASSED (post)`

| Assertion | Result |
|---|---|
| `user_version` = 2, all four new columns present | ✅ |
| chats/messages/projects/items **still** 75/251/41/151 | ✅ no chats, no model calls from recovery |
| `user_touched = 1` on **exactly 7** rows | ✅ six game-design steps from one project + the portfolio row |
| `suggested` = 20 · portfolio duplicate 2 live / 1 qualifying | ✅ |
| `draft_key` filled on every chat-sourced row · NULL on **exactly 32** | ✅ correction #1 |
| both repairs 0-candidate · `triage_log` has **zero** `repair` entries | ✅ |
| capture ledger: **4** entries, every one `seen` | ✅ |
| capture log line | ✅ verbatim: *"Recovered 0 capture(s) stranded in `_captured\` by an earlier version; 4 were already captured, so they were left alone"* |
| `seededCommandIds` persisted · `orchestrator` present **exactly once** · `summon-helper` unchanged | ✅ **2.3c mechanically verified** |
| list files 26 / 0 / 1 matching DB active counts | ✅ |
| memory refresh | ✅ **2,694-char profile** — third healthy sample |

**The 7 frozen row ids** (P-5 baseline for Stage 3.7):
`cc40ffc2-bdf7-4cfb-9d67-1b97525f6c1e` · `c69ac0ea-9e09-4325-bc58-19f0dcac3f11` ·
`93beba04-5fa9-473d-ba9e-eb54e8fe0bc6` · `f300ef45-d91b-4cad-9fb5-a0a74d9e7a4b` ·
`da6f4343-92f4-44eb-91f6-9d74a7e96f9f` · `41882c5e-1152-4225-b67a-451162703a19` ·
`c541cf9a-ca7b-4501-83a7-2b101821102b`

#### 1.6-equivalent — proving nothing real moved  ✅

Read-only comparison of the real profile against the snapshot taken at 22:45 local, after the scratch
launch (23:23:51 → 23:24:20):

| Real-profile artifact | Before | After the scratch launch |
|---|---|---|
| `capture-ledger.json` | 2,178 B @ 19:24:41 | **unchanged** |
| `memory.json` | 81 B @ 16:03:56 | **unchanged** |
| `Desktop\sample_in\plan\lists\*` | 13:16:52 | **unchanged — the redirect held, proven from the receiving side** |
| `data\sample.sqlite` | 19:48:00 | 22:53:08 — **28 minutes before** the scratch launch |

Every real-profile mtime is ≤ 22:55:33; the scratch launch began at 23:23:51. Nothing real moved.
The real `next-actions.md` is 4,165 B against the scratch export's 3,694 B — separate files,
separate content, no crossover.

⚠️ **Accounted-for real-profile activity at 22:53:08 – 22:55:33**: `settings.json`,
`settings.bak.json`, `Preferences`, `DIPS` written and `sample.sqlite` rotated to `sample.sqlite.bak`.
Consistent with the app being quit at Cowork's request before job 001; P-1 at 22:57:16 found no
Electron process. Recorded rather than assumed — pending Operator's confirmation.

#### Stage 2 boxes — honest disposition

| Box | Disposition |
|---|---|
| 2.1 preconditions | ✅ met on the recovered profile (backup verified, no process running, gates green) |
| 2.2 hot launch on the real profile | ⚠️ **executed unobserved 2026-07-26 15:36 local.** Re-observed instrumented on the reconstructed profile |
| 2.3a `maybeRefreshMemory` | ✅ on scratch (2,694 chars). On the real profile → **F1** |
| 2.3b `maybeExportPlanLists` | ✅ content verified 26/0/1. Sync-tool cross-device check **N/A** — redirected by design |
| 2.3c `seedBuiltinCommands` | ✅ mechanically. UI half (`/` menu shows Orchestrator once) **pending Operator's eyes** |
| 2.3d `stampOpened` | ⏳ **pending** — the window was up 26 s; re-observable free on any relaunch now that `post` has banked |
| 2.4 quit → `post` | ✅ `ALL CHECKS PASSED (post)` |
| 2.5 closes four Stage-5 claims | ✅ see claims table |

### Stage 3 — partial

**3.1 local dates — ✅ PASS.** Two gate-valid samples, both read on Windows by job 006, both with
UTC already rolled ahead of local at the moment of sending:

| Phrase | Sample A — Sun Jul 26, 22:26:31 local (`466abce4`) | Sample B — Mon Jul 27, 23:58:25 local (`a13caec5`) |
|---|---|---|
| "tomorrow" | expect Jul 27 → **`2026-07-27` Mon** ✅ | expect Jul 28 → **`2026-07-28` Tue** ✅ |
| "end of the month" | expect Jul 31 → **`2026-07-31` Fri** ✅ | expect Jul 31 → **`2026-07-31` Fri** ✅ |
| "next Friday" | Jul 31 / Aug 7 → **`2026-08-01` Sat** ⚠️ | Jul 31 / Aug 7 → **`2026-07-31` Fri** ✅ |

**The regression 3.1 exists to catch does not occur.** "tomorrow" resolved to the *local* calendar
day in both samples, including an evening send 95 seconds before local midnight when UTC had
already advanced. `anthropic.ts:215-221` supplies `todayLocalISO()` rather than `toISOString()`, and
the behaviour confirms the fix holds under exactly the condition that used to break it.

**Model attribution settled** (job 007): `extractTriage` takes no model from its caller
(`index.ts:226`) and defaults at `anthropic.ts:231` to `defaultTriageModel()` =
`ANTHROPIC_MODEL ?? "claude-sonnet-5"`. `.env` sets `ANTHROPIC_MODEL=claude-sonnet-5`. **Both
extractions ran on the same model**, with the same prompt and the same correct local date. The
`chatModel` drift never touched triage. Sample A's odd date is therefore not a configuration
difference — see F2.

Sample B also produced a **clarification item** — *"Confirm whether 'next Friday' means July 31 or
August 7"* — recognising the ambiguity the runbook itself concedes at `:48-49`. Recorded as a
quality positive, not a defect.

Its assistant turn returned 760 characters on `claude-sonnet-5`, against Sample A's **0 characters**
on `claude-haiku-4-5`. Noted under the empty-turn observation below.

**Observation — empty assistant turns, and they correlate with `claude-haiku-4-5`.** Five chats
carry no assistant content: `466abce4` persisted an assistant row with `content` length 0 and
`thinking` length 0 on `claude-haiku-4-5`, and the four 19:21–19:47 chats below have no assistant
row at all — all sent while `chatModel` was `claude-haiku-4-5`. Sample B, the first chat sent after
`chatModel` returned to `claude-sonnet-5`, produced a normal 760-character reply.

Five empty against one healthy is suggestive, not conclusive — the stop button and ordinary
cancellation produce the same on-disk signature, and Operator may simply have triaged without
waiting. But it is the same shape as F1 (empty content committed, nothing catching it) and the
correlation is worth a deliberate test. **Carried into 3.6b**, where the runbook already predicts
*"a genuinely blank bubble here is a new finding… nothing anywhere catches it"* — with the added
instruction to run that check on **both** chat models, not just the configured one.

**3.2 text capture — ✅ PASS.** Fixture dropped 00:07, captured 00:12:38. All four assertions:
became chat `68a6cf1a`, `triaged yes`, moved to `_captured\1785222758048-…` with an epoch prefix,
ledger `how=watch` with the chat id. Five items, correctly routed — 2 `next`, 2 `buy`, 1 `call`.

**3.3 image capture — ✅ PASS, strongly.** Transcript 1,184 chars, complete through "Sheet 1 of 1".
**13 of 13 verbatim strings survived exactly**, including the phone number `555-0173` — the
Phase-0 trap that eliminated Haiku. No truncation marker, correctly. Four items matching the four
ACTIONS ARISING.

**3.4 oversize capture — ✅ PASS, with two observations.** A 1.2 MB / ~300k-token text file was
captured whole (all 1,200,676 bytes stored, tail marker intact), moved to `_captured`, ledgered
`how=watch`. Triage failed and **said so**: `Captured "FIELD LOG…" but couldn't triage`. Because the
capture succeeded, `noteIngestFailure` was never invoked, so there is **no** retry loop — the
predicted failure mode did not occur.

- ⚠️ The database grew to **2,670,592 bytes**. The app exports the whole database after every write
  (`dev-plan-review.md:27`), so every later mutation now rewrites 2.6 MB. `index.ts:804` reads a
  captured file with no size cap; a few large captures make routine edits expensive. **Scaling risk.**
- ⚠️ The chat holds 1.2 MB and **0 items**, permanently — re-triage fails identically every time.
- **Runbook correction:** 3.4 expects "a visible truncation marker rather than a silent cut". There
  is no truncation and no marker on the text path (`index.ts:803-805`), confirmed empirically. The
  only marker in the codebase is `anthropic.ts:516-517`, on the **image** path, and a single image
  cannot realistically reach the 8192-token cap because images are downscaled to ~1568px before the
  model sees them. **3.4 as written tests a behaviour that does not exist.**

**Pre-existing R1-window probes** run by Operator at 19:21–19:47 local, before Stage 3 opened:

| Sent | Prompt | Result | |
|---|---|---|---|
| 19:21:17 | "call Alice **May 27** of next year" | `Call Alice` → `2027-05-27` (Thu) | ✅ |
| 19:22:17 | "call Bella **May 28** of next year" | **`Park for May 21?`** — no call item | ❌ |
| 19:24:41 | "call Carol **June 26** of next year" | `Call Carol` → `2027-06-26` (Sat) | ✅ |
| 19:47:57 | "Call dana on **June 28, 2027**" | **no items at all** | ❌ |

May 27 correct / May 28 broken lands exactly on the 60-day boundary of decision #10 (May 28 2026 is
precisely 60 days before the run day), which is where the recomputed R1 window predicts the flip and
where the runbook's "April–June 2027" literal does not. But **Carol, deeper inside the same window,
came back correct** — so the mechanism is not simply the lookback. These are chat/item deadlines,
not files parked into day folders, so they are *not* R1 proper. Recorded as leads for the R1 stage,
which needs a real parked file.

## Findings

### F1 — `generateMemory` writes an empty profile over the real one, silently — **high**
`src/provider/anthropic.ts:396-417` · `src/main/index.ts:167-174` · **New**, beyond campaign scope ·
Needs migration-history DB: **no**

Full entry: `F1-memory-refusal-wipe.md`, to be transposed into `docs/bug-fix-log.md` at §7.

**What we saw.** At 2026-07-27 16:03:56 local the real `memory.json` went from 2,872 B to 81 B —
a 2,724-character profile replaced with `""`, `enabled` still true. No error, no toast, no log.

**Not a user action:** `memory:clear` (`index.ts:1860`) writes `profile: ""` **and** `updatedAt: ""`.
The file carries an empty profile with a *real* timestamp — only `refreshMemory` (`index.ts:173`)
produces that pair.

**Mechanism.** `anthropic.ts:412-416` builds its return as
`resp.content.filter(text).map(...).join("").trim()` with **no `stop_reason` check**; a contentless
200 yields `""` as a *successful* return. `index.ts:172-173` commits it unconditionally and stamps
a fresh `updatedAt`, **resetting the 24-hour clock** so the loss is not self-healing.
`maybeRefreshMemory`'s `try/catch` catches nothing, because nothing throws.

The file already documents the mechanism it fails to guard (`anthropic.ts:32-34`): *"A refusal
arrives as HTTP 200 with stop_reason 'refusal' and (usually) no content at all."* That handling
exists in exactly one place — `streamChat` (`:385-389`). The same unguarded shape sits in
`generateTriageMemory` (`:421-442`), `generateLogDigest` (`:445-459`) and `transcribeCapture`
(`:516`, which checks `max_tokens` but not `refusal`). `generateMemory` is the worst of the four
because it is the only one that writes its empty result over durable user content.

**Four samples now bound the behaviour:**

| Sample | Model | Transcript | Profile |
|---|---|---|---|
| Real, pre-run | — | Jul-24 messages | 2,724 chars |
| Rehearsal (scratch, Jul 26) | — | Jul-24 messages | 2,640 chars |
| **Real, Jul 27 16:03** | live config | **live messages incl. Jul 26–27 captures** | **0 chars** |
| Recovered Stage 2 (scratch, Jul 27 23:24) | `claude-sonnet-5` | Jul-24 messages | 2,694 chars |

Three healthy samples all ran over the **Jul-24** message set; the only failure ran over the
**live** set. That is the discriminator: the decisive diagnostic is to log `resp.stop_reason` while
calling `generateMemory` against the live database's `recentMessages(200)`. One model call settles it.

**Lane → model:** `anthropic.ts` + the `index.ts` memory path → **Opus 5, xhigh**. Adversarial
verifier → **Fable 5, high**.

### F2 — **WITHDRAWN as a finding.** Downgraded to a quality observation — *low, watch only*
Surfaced by 3.1 · **not a code defect** · Needs migration-history DB: no

> **Sitting-2 supersession note.** With ten samples instead of two, the pattern resolved: precise
> anchors went 6/6 while bound-naming phrases went 1/4 clean, always erring **at or past** the
> bound. Sample A's Saturday is now evidence inside the **final F2** in the log — *"bounded-window
> deadlines resolve to or past the bound"*, **medium**, a confirmed class finding, not a wobble.
> The withdrawal below was correct on the two-sample evidence it had; it no longer stands.

**What we saw.** In sample A, *"The project proposal is due next Friday."* produced
`deadline: 2026-08-01` — a **Saturday**, wrong under every reading of the phrase.

**Why it is not filed as a bug.** Sample B ran the identical sentence, through the identical code
path, on the identical model (`claude-sonnet-5`, confirmed by job 007), with the same correct local
date supplied, and returned `2026-07-31` — a Friday. Same input, same configuration, different
output. That is model nondeterminism on a genuinely ambiguous phrase, not a defect in the app.
Plan §5's own rule for exactly this situation: *one wobble ≠ finding; consistent weakness across
samples = finding.* One of two samples wobbled.

**Why it is still worth recording.** Picking the wrong *Friday* would be defensible. Landing on a
**Saturday** is not, and nothing downstream noticed — the app stored a weekday that contradicts the
phrase it came from without complaint.

**Cheap hardening, if a lane is nearby anyway:** validate that a date resolved from a named weekday
actually falls on that weekday, and re-ask or drop the deadline when it does not. That is a
post-extraction assertion, not a prompt change, so it costs one model call's worth of nothing and
converts an invisible wrong answer into a visible one.

**Repro.** Not reliably reproducible — 1 occurrence in 2 attempts. Any fixer should treat the
validation above as the deliverable rather than chasing the specific date.

## The 12 claims — dispositions

*(Sitting-1 snapshot — every `pending` below was resolved in sitting 2; the final disposition
table is in the log's dev-run section and supersedes this one.)*

| Claim (`file:line`) | Vehicle | Verdict | Evidence |
|---|---|---|---|
| `store.ts:189/211` `repairOnce` persists before stamping | 2.4 | **CLOSED-BY-2.4** | `user_version` 2 **and** counts 75/251/41/151 intact, `triage_log` zero `repair` entries — nothing re-ran or half-ran |
| ledger creation | 2.4 | **CLOSED-BY-2.4** | 4 entries, all `seen` |
| seed | 2.4 | **CLOSED-BY-2.4** | `orchestrator` exactly once, `summon-helper` untouched |
| export | 2.4 | **CLOSED-BY-2.4** | one new `list-export` entry, 26/0/1 verified |
| `Settings.tsx:693` interval clamps display not stored value | settings file | **CONFIRMED — BUG** | `captureIntervalMs = 6000` (0.1 min) on disk, below the 0.5-min floor; Operator confirms they typed it into the Settings box. Restore to 30000 pending via UI |
| `index.ts:1220` stranded images by filename | — | **UNTESTED (dormant by design)** | all `_captured` files are `.txt` |
| `index.ts:266`/`:1869` `parkChat suggestedOnly` | 3.8 | pending | |
| `store.ts:154` `draft_key` inert for kind-move | 5.1 | pending | back-fill itself verified correct (119 scoped, 32 NULL) |
| `App.tsx:3682` silent digest Regenerate | 5.6 | pending | |
| `settings.ts:120-171` silent rollback to `.bak` | 5.3 | **pending (passive)** — a mid-run CONFIRMED verdict was **retracted**; see the scribe-error note | `_run-evidence\RETRACTION-claim-5.3.md`. Job 005: both settings files correct on Windows, no `settings.json.corrupt-*` anywhere, no handle held, no process running |
| `App.tsx:4291` time on undated event | 5.5 | pending | |
| `store.ts:1403` + `App.tsx:3696` Nudge Queue delete blast radius | 5.4 | pending | |
| `App.tsx:1169` sort direction leaks | 5.7 | pending | |

## R1 — characterization

**Done in sitting 2** (jobs 011–013 plus in-app probes; full characterization in the log — this is
the index). The 60-day window is **exact**: three identical files at 62 / 61 / 60 days back —
silent, silent, nag. The destructive half ran to completion: `06_june\28\` (content for June 28
**2027**) was nudged in as `2026-06-28`, ingested and **deleted** — gone from disk, `_captured` and
the Recycle Bin included; only its text survives as the chat body. Chats with **correct**
`tickler_due` years (`2027-05-27`, `2027-06-26`) were nudged into IN anyway — one sixty seconds
after parking — so recording the year does not close the bug while the resurface and file paths
stay year-blind. A file whose content named `5/29/2027` explicitly produced items dated
`2026-05-29` **and** `2027-05-29` in one session: the tickler prompt's *"set aside to resurface on
`<date>` (today)"* asserts a falsehood the model resolves differently each run. **F13** (the dead
"→ IN" control that duplicates on a second click) surfaced during route testing here.

Options for #15 — the decision is Operator's: **(1)** record the year AND make
`ticklerDayFolders` year-aware (the full design change); **(2)** never delete the source on ingest
— move it to `_captured` like every other capture path (a few lines; removes the only irreversible
harm); **(3)** fix the `parkChat` resurface path (the one defect that fires on correctly-dated
data). Scribe's view: 2 immediately, 3 next, 1 when there is room.

**Decision (2026-07-28): none of the three — the Later holder**, Operator's own design, with
the destruction guard folded in. Content resolving 10+ months out parks in a **Later** bucket
(after December in-app; `Later\` on disk beside the month folders, month/day-mirrored, so no year
is ever recorded), an automatic 30-day sweep promotes anything now <10 months out into its
month/day home, prod/resurface exclude Later until promotion, and ingest moves sources to
`_captured` instead of deleting — ever. Spec: plan §7 #15; supersedes #9's Jan-2 overflow bucket.

*(The sitting-1 staging window below was recomputed for run day 2026-07-28 before use.)*
Staging window recomputed to **2027-05-28 … 2027-07-26**; boundary probe ≈ **2027-04-27**.

## Product calls surfaced

- **NEEDS-DECISION** — restore the Jul-24 memory profile to the live app, or leave the empty one in
  place as living evidence of F1? Recoverable from `sample-devrun-backup-2026-07-26\userData\memory.json`.
  Operator's profile; Stage 6 discards it either way.
- Standing: waiting-only goal stall (`log:1830`); R1 fresh decision (`plan:282`).
- *Status at finalization (02:45 Jul 28): all three still open.* `memory.json` is still the 81-byte
  F1 artifact on the live profile; #15 now carries its characterization inline in the plan (§7 #15
  — the `plan:282` line number above has drifted after the 2026-07-28 plan edit).
- *Resolved 2026-07-28, post-commit-C — all three:* **#15** → a fourth design, Operator's own —
  the **Later holder** plus the ingest **destruction guard** (spec now lives in plan §7 #15);
  **waiting-only stall** → **aligned with the proposer** — a `waiting` item counts as work in
  motion (plan §7 **#17**); **memory.json** → **leave the artifact** — F1's live-mechanism
  diagnostic is knowingly forfeited at the scrap (the fix guards `stop_reason` regardless).
  Recorded across plan/report/log as proposed commit **D**.

## Next sitting (planned at 23:30) — outcomes

1. ✅ **Config restored and verified on Windows** at 23:52:52 — `engine=agent`,
   `chatModel=claude-sonnet-5`, `effort=max`, `captureIntervalMs=30000`. Held through sitting 2
   (job 007 pinned the triage model; sample B and all sitting-2 sends ran on `claude-sonnet-5`).
2. 2.3c UI half (`/` menu shows Orchestrator once) + a second 2.3d reading — **no written evidence
   in the final record**; left unticked in the runbook.
3. **3.1 confirming sample** — ✅ **satisfied early**: sample B landed 23:58:25 local Jul 27,
   gate-valid (UTC already rolled), 95 s before local midnight. 3.1 is PASS on two samples; the
   evening-of-Jul-28 session never became necessary.
4. Rest of Stage 3, then 4, 5, R1 — ✅ **done in sitting 2** (findings F5–F13, the claims table
   completed, R1 characterized). **Stage 6 remains pending** — see "Stage 6 — fresh start".
5. `sample-rehearsal` — still present at finalization; deletion optional, Operator's.
6. ⚠️ **Three `notepad.exe` instances were still running at finalization (02:30)** and the §9.5
   plan edit was made anyway (Notepad holds no write lock). **Do not save `docs/bug-fix-plan.md`
   from a stale Notepad buffer** — it would overwrite the 2026-07-28 closure edits.

## Sitting 2 — index (log-canonical)

Full entries live in `docs/bug-fix-log.md` § "The dev run — 2026-07-27/28"; this table is the
box-level index.

| Box | Outcome | Ref |
|---|---|---|
| 3.1 confirming sample | ✅ PASS — sample B gate-valid; ten date resolutions total across the run | final **F2** |
| 3.2 text capture | ✅ end to end — chat, triage, `_captured`, ledger, 5 items routed | log |
| 3.3 image capture | ✅ strongly — 13/13 verbatim strings incl. the Phase-0 trap phone number | log |
| 3.4 oversize capture | ✅ graceful — stored whole, honest failure note, no retry loop; ⚠️ DB → 2.67 MB rewritten per mutation; **runbook 3.4 tests a truncation marker that does not exist on the text path** | log |
| 3.6a refusal — direct API | ✅ refusal note correct against the real API; ❌ titling commentary became the title | **F4** |
| 3.6b refusal — Agent SDK | ❌ dressed as a connection failure, AUP URL + Request ID leaked | **F3** |
| 3.7 frozen-rows attack | ✅ guarantee holds — four re-triages, a rename, a restatement; nothing lost | log |
| 3.8 auto-park, both halves | ✅ decision #4 honoured; "next Friday" resolved correctly post-learning; ❌ ⏳ dead after reject-then-restore | **F10** |
| 4.1 relocation sentences | ❌ neither sentence renders | **F5** |
| 4.2 reunite case | **UNTESTED** — blocked on F5: asserting the app must say *nothing* is unfalsifiable while nothing ever speaks | F5 |
| 4.5 Move to IN → ↩ Restore | ❌ location data stripped, item filed twice; project-candidate half **UNTESTED** — the ⋯ menu renders behind active rows | **F8**, **F9** |
| 4.7 dateless-event export | ❌ "Export .ics" disappears entirely; time fields hidden | **F12** |
| 4.10 all-fail capture batch | ❌ silent | **F6** |
| 5.1–5.9 | ✅ all dispositioned — 5 CONFIRMED, 1 dead code, 2 REFUTED, 1 UNCONFIRMED (retracted) | final claims table, log |
| R1 | ✅ characterized — boundary exact, file destroyed; **F13** surfaced en route | "R1 — characterization" above |
| 2.3c UI · 2.3d · 3.5 · 3.9 · 4.3 · 4.4 · 4.6 · 4.8 · 4.9 | **no written evidence** — left unticked in the runbook; tick from memory only if actually run | — |
| Stage 6 | **PENDING** — Operator | below |

## Findings index — final (F-numbers per the log; full entries there)

| # | Finding | Sev | Lane → model · effort | Verifier |
|---|---|---|---|---|
| F1 | `generateMemory` writes an empty profile over the real one, silently | **high** | `anthropic.ts` + `index.ts` memory path → Opus 5 · xhigh | **Fable 5** |
| F2 | bounded-window deadlines resolve to or past the bound | medium | triage prompt + validation helper → Sonnet 5 · high | — |
| F3 | the Agent SDK dresses a policy refusal as a connection failure | med-high | `claudeAgent.ts` → Opus 5 · high | — |
| F4 | a model's refusal prose becomes the chat title | low-med | `index.ts:1552` → Sonnet 5 · high | — |
| F5 | relocation sentences never appear (R2 regression, decision #16) | **high** | `store.ts:822`/`:1021` → Opus 5 · high | **Fable 5** (store.ts) |
| F6 | the all-fail capture batch is silent | medium | `index.ts` capture batch → Sonnet 5 · high | — |
| F7 | a rejected item's correction cannot land in its own chat | medium | re-triage semantics → Opus 5 · high | — |
| F8 | "Move to IN" strips location data and files the item twice | medium | `App.tsx` → Sonnet 5 · high | — |
| F9 | a completed item's ⋯ menu renders behind active items | medium | `App.tsx` z-order → Sonnet 5 · high | — |
| F10 | the ⏳ park control is dead after reject-then-restore | low-med | `App.tsx` → Sonnet 5 · high | — |
| F11 | deleting a parked chat leaves no trace | medium | `store.ts` delete path → Opus 5 · xhigh | **Fable 5** |
| F12 | a dateless event cannot be exported; its time field is hidden | medium | `App.tsx` + `.ics` export → Sonnet 5 · high | — |
| F13 | "→ IN" gives no feedback; a second click duplicates the work | medium | Nudge Queue file actions → Sonnet 5 · high | — |

## Stage 6 — fresh start

**PENDING at finalization (02:45 local Jul 28).** The live profile is un-scrapped: migrated database
(2,686,976 B, including the 1.2 MB oversize capture), `memory.json` still the 81-byte F1 artifact,
`Desktop\sample_in\_captured` holding 24 files. All of Stage 6 is Operator's — destructive by
design. Sequence, from the runbook:

- **6.0 ✅ satisfied** — every finding is in the log with a repro (append verified on Windows by
  job 015).
- **6.1 MANDATORY FIRST** — archive the capture graveyard:
  `Move-Item "$env:USERPROFILE\Desktop\<capture-inbox>\_captured" "$env:USERPROFILE\sample-captured-archive-2026-07-26"`.
  Not advisory: `_captured` holds `20260726_233750.jpg` **twice with different bytes**
  (1,534,163 / 1,464,403). Skipping 6.1 would not merely resurrect the four zombie chats — with
  the collision present, `index.ts:1234` judges one of the two images already-captured by
  filename alone and it is **never recovered** (claim 5.2's mechanism, precondition live today).
- **6.2** — copy `secrets.bin` out (`sample-secrets-keep.bin`) or plan to re-enter the API key.
- **6.3** — with the app quit, `Remove-Item "$env:APPDATA\<app-userData>" -Recurse -Force`.
- **6.4** — first fresh launch: exactly two `/` commands (no duplicate Orchestrator);
  `user_version` stamps 2 over zero rows; a cleared name stays cleared; `captureFolder` starts
  empty and, once re-pointed, the +8 s sweep recovers nothing.
- **6.5, extended by §9.7** — keep the Stage-0 backup, `_run-evidence\`, the `_captured` archive
  and `sample-secrets-keep.bin` until the fix pass completes **and its verifiers report**. The fresh
  app being healthy is necessary, not sufficient.

## Handoff — the fix pass over the dev run's findings (read this cold in Claude Code)

Inputs: `docs/bug-fix-log.md` § "The dev run — 2026-07-27/28" (canonical, full four-part entries) ·
this report · `%USERPROFILE%\sample-devrun-backup-2026-07-26\_run-evidence\`. Fixer prompts:
`bug-fix-plan.md` §5.1 verbatim, pasting the log entries. Verifiers: §5.2. Campaign rules hold —
one owner per file, repro → fix → prove, minimal diffs, adversarial review before merge.

Grouping by exclusive file ownership; a lane runs at the strongest tier its findings demand
(per-finding tags above). **The fix-pass orchestrator's first job is §5.4's coverage check — this
table is a proposal, not a partition:**

| Lane (exclusive files) | Findings / claims | Model · effort | Verifier |
|---|---|---|---|
| PROV-2 — `src/provider/anthropic.ts`, `src/provider/claudeAgent.ts` | **F1** provider half — guard the whole empty-result family (`generateMemory`, `generateTriageMemory`, `generateLogDigest`, `transcribeCapture`); **F3** (refusal → `REFUSAL_NOTE`, never raw provider text); **F2** (`TRIAGE_SYSTEM` bound rule) | Opus 5 · xhigh | **Fable 5** · high |
| MAIN-2 — `src/main/index.ts` | **F1** commit guard at `:167-174` (never write an empty profile over a non-empty one) + emptiness guard at `:1799`; **F4** (`:1552`); **F6**; **F13**; **F7** (re-triage semantics — coordinate with STORE-2 if `retriageExisting` changes); claim `index.ts:1220` (latent) | Opus 5 · xhigh | **Fable 5** · high |
| STORE-2 — `src/main/store.ts` | **F5** (`:822`/`:1021`; renderer touchpoint — coordinate with UI-B); **F11**; claim `store.ts:154` (**needs-migration-history** — fix against `_run-evidence` or the Stage-0 backup restored into a SCRATCH `--user-data-dir`, never the real profile) | Opus 5 · xhigh | **Fable 5** · high |
| UI-B — `src/renderer/src/App.tsx` | **F8** · **F9** · **F10** · **F12** (absorbs claim `App.tsx:4291`) · claim `App.tsx:1169` | Sonnet 5 · high | Opus 5 · high |
| SET-2 — `src/renderer/src/Settings.tsx` | claim `Settings.tsx:693` | Sonnet 5 · medium | Opus 5 · high |
| R1 slice — **#15 RESOLVED 2026-07-28: the Later holder + ingest destruction guard** (spec: plan §7 #15) | `Later` bucket after December, in-app and on disk (`nudge_queue\Later\`, month/day-mirrored — no recorded year); 30-day promotion sweep (`maybeX` family, named constant); prod/resurface/"Triage this date" exclude Later; threshold derived from `TICKLER_OVERDUE_WINDOW_DAYS`; supersedes the Jan-2 overflow; ingest moves sources to `_captured`, never deletes | Opus 5 · xhigh — **cross-file** (`index.ts` + `store.ts` + `App.tsx`): its own sequenced slice after the single-file lanes merge | **Fable 5** · high |

F2's post-extraction weekday/bound assertion wants a shared helper — settle its file ownership
(`shared/dates.ts` vs `triage/schema.ts`) at kickoff, per the three-implementations lesson.

Environment: §5.1's standing rules, plus — post-scrap there is no migration-history database;
`needs-migration-history` items are fixed against captured evidence or a scratch restore.

Gates after every merge: `typecheck` · `build` · `laneStore` 186 · `laneUiA` 135 · `laneProv`
34/33 · `laneIpc` 34 · `laneEvents` 36 (both zones) · `laneSet` 25 · `laneSetUi` 15 · `laneIpcUi` 7
· **`phase4Smoke` 29 pass + 1 known-open, no skips**.

knownOpen rule: fixing R1 = convert pin B to a real check AND update plan §7 #15 AND the
`ticklerFileCounts` warning comment; re-pinning a corrected boundary = update the pin's values +
the log; never delete the pin.

## Commit plan (gated — Operator authorizes each; commit A was not taken)

Proposed 2026-07-28. Nothing is committed until authorized; nothing is pushed unless asked.
`.devrun\` stays untracked by default (its transcripts are archived in `_run-evidence\`) — say the
word to commit it as evidence, or to `.gitignore` it instead.

**B — the run's artifacts** (A was skipped, so the checker and cowork plan ride here):

```powershell
git add docs/dev-run-runbook.md docs/dev-run-report-2026-07-27.md docs/dev-run-cowork-plan.md src/spike/devrunCheck.ts
git commit -m "Execute the dev run: thirteen findings, the twelve claims dispositioned, R1 characterized"
```

Body: two sittings, 2026-07-27/28; Stage 2 found already consumed and reconstructed on a scratch
profile from the byte-identical pre-migration backup — `pre` and `post` both `ALL CHECKS PASSED`;
runbook committed unticked with its reconciliation note; report finalized; Stage 6 pending.

**C — bookkeeping** (separate, per the `b0b55df` log-the-phase precedent):

```powershell
git add docs/bug-fix-log.md docs/bug-fix-plan.md
git commit -m "Close the campaign: the dev run recorded, and the plan hands off its successor list"
```

Body: the log gains "The dev run — 2026-07-27/28"; the plan's Phase-4 **Remaining** becomes the
successor list (fix pass · §7 #15 · waiting-only stall · Stage 6), with the dev-run verdict block,
the #15 characterization note and the #16/F5 caveat.

## Transcripts appendix

`.devrun\done\` — sitting 1: `001-preflight-inventory` · `002-stage2-scratch-build` ·
`003-stage2-launch-and-post` (+ `.stdout.log`, `.stderr.log`) · `004-stage2-probe-and-archive` ·
`005-settings-rollback-forensics` — sitting 2: `006-check-31-dates` · `007-env-and-triage-model` ·
`008-verify-32-capture` · `009-verify-33-image` · `010-verify-34-oversize` · `011-r1-recon` ·
`012-r1-log-window` · `013-r1-file-fate` · `014-verify-34-result` · `015-verify-log-append` —
each `.out.txt` beside the exact `.ps1` that produced it.

Evidence archive `%USERPROFILE%\sample-devrun-backup-2026-07-26\_run-evidence\` — four `generateMemory`
samples, two capture ledgers, two settings snapshots, the three exported list files. **Keep until
the fix pass completes and its verifiers report** (§9.7).
