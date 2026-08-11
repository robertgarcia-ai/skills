> **SANITIZED EXEMPLAR.** Personal names, usernames and machine-specific identifiers were replaced (Operator, REDACTED-USER, ExampleCorp, Sample); the app's identity was additionally fictionalized (SampleApp / sample-app / Nudge Queue and the like) and timezone and personal context generalized; everything else — structure, numbers, wording — is verbatim from a completed real campaign (2026-07). Read for shape and conventions, not as instructions to execute.
>
> **Take from this:** the five-category scope with counts up front ("sixteen effects that closing the app does not undo"); Stage 1 as a diff against an expectation table with mandatory neutralization of outbound effects; per-effect irreversibility notes and immediate-check ordering in Stage 2; known-open "do not chase" framing; build-freshness warnings. Map: context/categories · Stage 0 pins · Stage 1 rehearsal · Stage 2 one-way · Stage 3 model quality · Stage 4 perception · Stage 5 claims · known-open · restore.
>
> Predates the current dev-run-plan contract: it lacks the Mutation-enumeration section, `once-only` tags, and the surface-delta line the template now mandates — the template wins where they differ; do not imitate their absence.

# Dev run — what to test, and in what order

## Context

Phase 4 is done: 78 findings closed, 5 regressions found by the fan-out (4 fixed, 1 reverted and
pinned), all five adversarially reviewed. The automation covers store logic, dates, IPC shapes, the
golden paths and the settings/provider lanes — ~500 checks across nine harnesses in multiple zones.

So **the dev run's job is only what a harness structurally cannot reach**:

1. **Real model calls.** Every proof used a fake daemon or ran store-level. Nobody has seen a real
   Claude triage since the prompts changed.
2. **Real data, once.** First launch is a **one-way migration** — `user_version` 0→2 with no
   down-migration, 7 named rows frozen forever, `memory.json` overwritten, files written into a
   sync-tool share. Sixteen effects that closing the app does not undo.
3. **Four startup effects with zero test coverage anywhere.**
4. **Perception.** A harness can prove a string is set; only a person can say whether it is understood.
5. **Twelve fan-out claims** that never had a refuter run against them.

Staging (decided): **rehearse on a copy, then go hot.**

> ⚠️ **`out/` is stale — it predates the R1 revert.** `npm run build` first or the run tests code that
> is no longer in the tree. Also delete the 0-byte `out/main/index.js.probe-backup` left by a probe.

---

## Stage 0 — before anything launches

- [ ] `npm run build` (see above).
- [ ] Back up, because several of these have **no** backup of their own:
      `%APPDATA%\sample-app\data\sample.sqlite` · `settings.json` · **`memory.json`** ·
      `Desktop\sample_in\plan\lists\*.md` · the whole `Desktop\sample_in\_captured\` folder.
- [ ] Note the pre-state you will diff against: `memory.json` is **2,724 chars**; `settings.json` has
      **no** `seededCommandIds`; there is **no** `sample.sqlite.bak`, **no** `settings.bak.json`, **no**
      `capture-ledger.json`; `_captured/` holds **5 .txt files**.

---

## Stage 1 — rehearsal on a copy (nothing real moves)

Copy `%APPDATA%\sample-app` to a scratch dir and launch with `--user-data-dir=<scratch>`. The
outcome is already predicted from read-only queries, so this is a **diff against an expectation**, not
exploration. Anything that differs is a real finding *before* your data is touched.

| Check | Expected |
|---|---|
| `PRAGMA user_version` | `0` → **`2`** |
| New columns | `chats.parked_from`, `items.user_touched`, `items.draft_key`, `items.parked_from` |
| `draft_key IS NULL` | **151 → 0** |
| `user_touched = 1` | **0 → exactly 7** |
| Tickler repair (batch 1) / inbox repair (batch 2) | **0 rows each** — safety nets, not rescues |
| `capture-ledger.json` | created, **4 entries**, all `seen` |
| Chats created by recovery / model calls by recovery | **0 / 0** (all 5 files are evidenced in the DB) |
| Row counts | chats 75, messages 251, projects 41, items 151 unchanged |

- [ ] **Read the 7 rows that get frozen and decide if you are happy with them.** Six are game-design
      steps from one project; the seventh is *"Prepare a portfolio to present at an upcoming
      ExampleCorp meeting"*. After the hot launch the model can **never** refresh or replace these —
      only you can dismiss them. Nothing sets `user_touched` back to 0.
- [ ] One oddity worth eyeballing: *"Prepare a portfolio…"* appears **twice** among the 20 suggested
      rows. One copy qualifies for freezing and the other does not, so they will sit side by side with
      different rules. Confirm that is acceptable rather than a sign the predicate is wrong.

---

## Stage 2 — the hot launch, watched (the four never-tested effects)

These fire in the **first ~8 seconds** and are gated by state that the launch itself consumes — after
this run they will not fire again. Watch, or check the artifacts immediately.

- [ ] **`maybeRefreshMemory`** — fires because `memory.json` is >24 h old. Makes a **model call** and
      **overwrites `memory.json` with a plain `writeFileSync`** — no temp, no `.bak`. Compare the new
      profile against your backup: is the distillation as good? This is the one irreversible *content*
      loss in the whole launch.
- [ ] **`maybeExportPlanLists`** — fires because `lastListExportDay` is stale. Overwrites three files in
      **`Desktop\sample_in\plan\lists\`**, plain `writeFileSync`, no temp, no backup — **and that is a
      sync-tool share, so it propagates to every device.** Check the three files are complete and
      correct (`next-actions.md` should hold ~26 active next actions, `things-to-buy.md` 1,
      `phone-calls.md` `_(none)_`), and that nothing on another device got a truncated version.
- [ ] **`seedBuiltinCommands`** — **new code**, never tested. `seededCommandIds` is absent today, so it
      defaults to the era-correct `["summon-helper"]` and then adds the **Orchestrator** command.
      Confirm: Orchestrator appears in the `/` command list exactly once, `summon-helper` is untouched,
      and nothing you previously deleted came back.
- [ ] **`stampOpened`** — the home view's "last opened" should show the *previous* launch, not this one.
- [ ] **Settings backup semantics** — `settings.json` is written **twice** this launch, so
      `settings.bak.json` is created holding the original and then immediately overwritten by the
      post-`stampOpened` version. Confirm you do not care, or keep your own copy.
- [ ] **The `.bak` window** — `sample.sqlite.bak` is created for the first time holding *pre-migration*
      bytes, then destroyed by the very next persist (seconds). Your only durable pre-migration copy is
      `data\backups\sample.sqlite.2026-07-24-pre-bugfix.bak`. Do not rely on `.bak`.

---

## Stage 3 — real triage quality (the whole point of a human run)

Nothing in the campaign has exercised a real Claude call through the changed prompts.

- [ ] **Local dates.** Triage a chat that says *"tomorrow"*, *"next Friday"*, *"end of the month"* —
      **in the evening**, which is when the old UTC bug bit. Deadlines and park dates must resolve to
      *your* calendar day, not Greenwich's (`anthropic.ts:191`).
- [ ] **A capture, end to end.** Drop a note into `sample_in`; confirm it becomes a chat, gets triaged,
      the file lands in `_captured/`, and the items are sane.
- [ ] **An image capture** — exercises `transcribeCapture`. Check the transcript is complete; the cap
      went 2048 → 8192 and a truncation now says so in the text.
- [ ] **A long/large capture**, if you have one — confirm a truncation marker appears rather than a
      silently cut transcript, and note whether the triager then proposes something odd about it
      (the marker reaches the model; that is new input it never had).
- [ ] **The effort picker.** Switch the chat model to Opus 4.6 or Sonnet 4.6 with effort on **Extra**:
      the option must show *"Extra — not on this model"*, stay selected, and the send must succeed
      (the provider clamps to `high`) rather than 400.
- [ ] **A refusal**, if you can provoke one — should arrive as a visible message, not a blank reply.
- [ ] **Re-triage a chat that has one of the 7 frozen rows.** The row must survive, and the model should
      be *told* about it (`retriageExisting`) rather than proposing a reworded duplicate.
- [ ] **Auto-park.** Give a chat clearly deferred content ("tickets go on sale in August"). With no
      confirmed items it should park; with confirmed items it should degrade to a *"Park for <date>?"*
      suggestion in IN rather than hiding them (decision #4).
- [ ] If you run with `ANTHROPIC_MODEL` set to **Fable**: thinking is always-on inside `max_tokens:
      8192`, so a structured-output truncation is newly possible where the old code gave a hard 400.
      Watch for a triage that returns nothing useful.

---

## Stage 4 — the new messages and cues (perception, not mechanism)

Each is proven to *fire*. The question is whether it reads right mid-task.

- [ ] **Relocation sentences (R2, just fixed after review).** File one item under a project via ⋯ →
      Move to project, where its chat has siblings filed elsewhere: *"Filed under Admin — 2 items filed
      under Taxes moved with it."* Then drag a chat onto a chatless item row: *"Linked — the chat and 2
      items moved to Kitchen Reno."* Both should be **true** — count the rows that actually moved. Do
      it once from a **project page** too: the destination name must be the project, not "IN".
- [ ] **The reunite case specifically** — drop a chat onto an item of the project its make-project steps
      already live in. It must say **nothing** (nothing moved). This reported "2 items filed under Reno
      moved to Reno" until an hour ago.
- [ ] **Permission swap notice.** With a connector set to "ask", get a request up, let that chat finish
      so the dialog is replaced by another chat's request — the first press must acknowledge, not
      answer, and the notice must be *noticeable*.
- [ ] **Enter while streaming** — draft preserved, brief cue, nothing sent (decision #8).
- [ ] **Move to IN → ↩ Restore** on an active item, and on an accepted project candidate: both must come
      back visible (decision #6), not vanish.
- [ ] **Goal-stall banner** — on a goal project holding only a suggested `inbox` row, the banner and
      "Suggest a step" must render (that was R5). Note: a project whose only work is **waiting** still
      reads as stalled — known, pre-existing, and a product call you may want to make.
- [ ] **Export with a dateless event** — the message must *name* the skipped event, not inflate a count.
- [ ] **A non-URL buy link** shows a chip labelled not-a-URL; clicking edits (decision #12).
- [ ] **Events ⋯ → Happens on / Starts / Ends** on a hand-made event, then export it (decision #11).
- [ ] **Capture toasts** — a batch where everything fails must still say something
      ("Nothing captured from your folder — check the file type").

---

## Stage 5 — the 12 unverified fan-out claims

No refuter was ever run against these; they are **claims, not findings**. Four bear on this launch.

**Check during/just after the migration:**
- [ ] `store.ts:189/211` — `repairOnce` persists repairs **before** stamping `user_version`, so a crash
      between them leaves repairs applied with an unapplied version and they re-run. *On your data both
      logging branches are 0-row, so the window is closed by luck, not design* — confirm `user_version`
      is 2 and the counts match Stage 1 exactly.
- [ ] `store.ts:154` — `draft_key` freezes the row's **current kind**, which may make it inert for the
      kind-move case it exists for. Rename an item **and** move it to another list, then re-triage: does
      the model's original extraction come back as a duplicate?
- [ ] `index.ts:1220` — stranded **images** are judged by **filename alone** and the decision is
      permanent. Your `_captured/` is all `.txt` so this is dormant now; it matters the next time two
      different photos share a name.
- [ ] `settings.ts:120-171` — a momentarily unreadable `settings.json` (AV, sync lock) is treated as
      corrupt and rolled back to `.bak` **with no dialog after startup**. Your capture folder is a
      sync-tool share, so transient locks are realistic here.

**Check in normal use:**
- [ ] `store.ts:1403` + `App.tsx:3696` — a Nudge Queue row in the Activity Log opens the day folder
      as a **full project page**, where "Delete project" would take every chat parked on that date.
      Open one; confirm whether that button is reachable.
- [ ] `App.tsx:4291` — set a **time** on an **undated** event: does it vanish from the field and wipe
      the item's detail line?
- [ ] `App.tsx:3682` — hit Regenerate on the daily digest with the API key wrong: silent, or an error?
- [ ] `App.tsx:1169` — change sort key on one list, then visit another: does an ascending direction leak
      across?
- [ ] `Settings.tsx:693` — type a custom capture interval below 0.5 min: the box clamps the display, but
      does the **stored** value clamp too?
- [ ] `index.ts:266`/`:1869` — `parkChat`'s `suggestedOnly` has no production caller; confirm no park
      ever leaves confirmed items behind.

---

## Known-open, do not chase

**R1 (plan §7 #15) is live and deliberate.** A file parked **10–12 months out** (60 of 365 calendar
cells) lands on the wrong row, nags, and "Triage this date" ingests and **deletes** it months early.
Avoid parking *files* that far out during the run, or park a throwaway one to see it. It is pinned as
`OPEN` in `phase4Smoke` so the suite cannot go green over it. Fixing it needs the year recorded **and**
`ticklerDayFolders` made year-aware — its own piece of work.

---

## If something is wrong

Restore in this order: quit the app **first** (it rewrites the DB on every launch and every mutation),
then `sample.sqlite` from `data\backups\sample.sqlite.2026-07-24-pre-bugfix.bak` (byte-identical to your
pre-launch file), then `settings.json`, `memory.json`, and `plan\lists\*.md` from your Stage 0 backups,
and delete `capture-ledger.json`. Restoring the DB alone is not enough — the ledger and settings have
moved independently of it.

Anything found here goes into `docs/bug-fix-log.md` under Phase 4, with the same discipline as the rest
of the campaign: reproduce it, then fix it, then falsify the fix.
