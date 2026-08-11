# Contract — bug-fix plan (`bug-fix-plan.md`, produced via /orchestrator)

Exemplar: `references/examples/bug-fix-plan.md`. butterfly-collector does not reimplement
/orchestrator; it hands /orchestrator the findings set plus this contract and the exemplar. A plan
missing any section below is returned for completion before Gate A.

## Header
Source pointer to the hunt report (or log section for post-synthesis plans) with counts; write
date; a **Status** stamp that the execute phase updates in place (the exemplar's stamp records
completion and points at the log as canonical — copy that convention); and a **Remaining** line —
the plan's live worklist, initialized to the full item list. EXECUTE keeps it honest as lanes
land; SYNTHESIZE rewrites it as the honest successor list and appends the compressed verdict
block beneath it.

## §1 Principles the whole plan obeys
Minimum set, each with its why: git before anything (baseline commit + tag); cluster by root
cause, not by finding; **one owner per file, ever**; repro → fix → prove, every time (a fix
without a before/after proof doesn't merge); adversarial verification before merge; minimal diffs
(no drive-by refactors); product decisions belong to the user — lanes flag, never invent policy.

## §2 Phases and lanes
Time flows down; lanes inside a phase run in parallel and own disjoint files (name the exclusive
files per lane). Each lane lists its findings by `file:line`, its proof obligation, and its
`Tier · effort` (models concretized only by §3's pinned mapping). Phase 0 is always the safety net: git init/tag, data backups, green
typecheck+build, one smoke launch. Approved prevention nominations (habitat changes from
synthesis) run as their own lanes; their proof obligation is the bug classes they extinguish.

## §3 Tier assignment table + the pinned mapping
Tier | cost | use for | why — assignments per /orchestrator's **Cognitive tiers**
(frontier / heavy / workhorse / mechanical) and **Assignment law** (oracle strength × blast
radius), with each lane's (oracle, blast) classification recorded so the reasoning is checkable.
Close with the current tier→model mapping, pinned and dated at write time (/orchestrator's Local
operational notes supply it); model names enter the plan only through that mapping. (The
exemplar's §3 predates this contract's tier form and closes with a model-name rhyme — the
contract wins; do not imitate it.)

## §4 Parallel execution mechanics
Orchestrator session + subagent lanes with worktree isolation; lanes launch per phase in one
batch; merge **one lane at a time, smallest diff first**, with typecheck + build + the lane's
proof after each merge; standing environment footguns included **by reference from the
campaign's tracked footgun file** — never re-typed, paraphrase decays rules — (never kill the
user's own app instance; isolated `--user-data-dir` only; known
tool-breaking files and their workarounds). Verdict routing follows /orchestrator's escalation
table, its round-two user gate included: a FLAWED verdict returns the fix to its originating
lane with the refutation attached; after **two FLAWED verdicts on the same item, no further
refutation round runs without the user's explicit say-so** — the ask carries the refutations,
spend so far, and a recommendation (escalate one tier in a fresh session — once, ever — versus
scope out and pin; the default lean is pin, landing as `PINNED-OPEN`/`BLOCKED`, building no
further mechanism).

## §5 Prompting instructions (all four, verbatim-adaptable)
- **5.1 Fixer-lane prompt**: exclusive file list; paste full finding entries; discipline per
  finding (reproduce first — skip if unreproducible, never fix blind; fix minimally; prove and
  re-run the exact repro; sweep the fixed defect's class for siblings in the owned files —
  same shape, same module — before closing; `NEEDS-DECISION` when behavior is a product call);
  report every finding
  as `FIXED/SKIPPED/NEEDS-DECISION`, no silent drops.
- **5.2 Adversarial verifier prompt**: job is to **refute**; attack three fronts (repro still
  reproduces? neighbors broken? contradicts the spec/rubric?); **report everything, filter
  downstream** — include uncertain issues with confidence + severity (conservative-reporting
  phrasing suppresses recall); verdict `SOUND` or `FLAWED: <mechanism>` — routed per §4
  (two FLAWED on one item → user gate).
- **5.3 Mechanical-sweep prompt** (mechanical tier): give it only the files it edits, spell out
  each exact change, forbid interpretation; ambiguity stops the item and returns it
  (escalation table), never guesses.
- **5.4 Orchestrator self-instructions**: the **coverage check** — a lane list is a proposal, not
  a partition; before each phase, list every finding per owned file and diff against the lanes
  (findings hide in this gap); "a fix that adds a step adds a state — ask what the world looks
  like *between* the steps"; full task spec up front per lane; NEEDS-DECISION items go to the
  user while other lanes keep running; keep `docs/bug-fix-log.md` current
  (finding → lane → commit → proof → verifier verdict → actual model).

## §6 Estimated shape
Wall-clock and dominant-cost per phase.

## §7 Product decisions
Every NEEDS-DECISION item with options and a recommended default. Once answered, decisions are
**spec** — a lane implements the decision, not its own judgment; flag any answer that departs
from the recommended default so nobody later "fixes" it back. Habitat nominations from synthesis
arrive here as NEEDS-DECISION like any other product call; at synthesis, answered decisions are
consolidated into the project's living rubric (this section is a waiting room, not an archive).
