/**
 * devrunCheck-skeleton.ts — GENERIC SKELETON for the per-iteration state checker.
 * Contract: references/templates/checker-spec.md. This file demonstrates shape only;
 * every real pin is derived from the iteration's mutation enumeration — no pin
 * without a source line in the dev-run plan.
 *
 * WHAT THIS IS:  the run's measurement instrument. Modes:
 *   pre   — asserts the exact pre-run state the plan's predictions derive from
 *           (a `pre` failure = measurement-gate stop, class A; also doubles as
 *           restore verification after any restore).
 *   post  — asserts the Stage-1/Stage-2 expectation table (before → after).
 * WHAT THIS IS NOT: a fixer, a prober of last resort, or a harness. It opens data
 *   stores read-only, writes nothing anywhere, makes no model or network calls.
 *   If something cannot be verified read-only, it reports UNVERIFIABLE — it never
 *   probes destructively. UNVERIFIABLE is a third result, not a failure: it must
 *   name the runbook box that verifies the fact by hand, it is summarized BEFORE
 *   the contract line, and it never flips the exit code. An UNVERIFIABLE with no
 *   delegated box counts as a FAIL (templates/checker-spec.md). Anything
 *   PERMANENTLY unverifiable read-only belongs in the runbook, not here.
 * PRECONDITION: the app/service under test is quit/quiesced. A live writer
 *   invalidates every read; `post` results are valid only immediately post-launch.
 * USAGE: run from the repo root — `npx tsx devrunCheck.ts pre|post`
 *   (language/runtime rule: whatever the target repo already runs; zero new deps.)
 */
import { createHash } from "node:crypto";
import { existsSync, readFileSync, readdirSync, statSync } from "node:fs";
// import { DatabaseSync } from "node:sqlite"; // if the repo runs Node >= 22

type Verdict = {
  ok: boolean;
  expected: string;
  observed: string;
  // When set (non-empty), this check is UNVERIFIABLE read-only *this time* and is
  // delegated to the named runbook box — neither pass nor fail. Empty string = FAIL.
  unverifiable?: string;
};
type Pin = {
  id: string;          // traces to a dev-run-plan line, e.g. "S0.3"
  desc: string;        // human-readable, names the plan source
  modes: ("pre" | "post")[];
  check: () => Verdict;
};

const sha256 = (p: string) =>
  createHash("sha256").update(readFileSync(p)).digest("hex").slice(0, 12);
const V = (ok: boolean, expected: string, observed: string): Verdict => ({ ok, expected, observed });
const U = (runbookBox: string): Verdict =>
  ({ ok: false, expected: "n/a", observed: "n/a", unverifiable: runbookBox });

// ---------------------------------------------------------------------------
// PINS — every entry below is a *shape*; replace wholesale from the mutation
// enumeration. Exact values, not ranges, wherever a read-only probe can give one.
// ---------------------------------------------------------------------------
const PINS: Pin[] = [
  {
    id: "S0.1", desc: "config file byte-identical to pinned pre-state (plan Stage 0)",
    modes: ["pre"],
    check: () => {
      const p = "data/config.json";
      if (!existsSync(p)) return V(false, "exists, sha 1a2b3c4d5e6f", "MISSING");
      return V(sha256(p) === "1a2b3c4d5e6f", "sha 1a2b3c4d5e6f", `sha ${sha256(p)}`);
    },
  },
  {
    id: "S0.2", desc: "ABSENCE pin: no .bak exists before the run (plan Stage 0)",
    modes: ["pre"],
    check: () => V(!existsSync("data/store.bak"), "absent", existsSync("data/store.bak") ? "PRESENT" : "absent"),
  },
  {
    id: "S1.4", desc: "watched folder holds exactly 5 files (expectation table, before)",
    modes: ["pre"],
    check: () => {
      const n = readdirSync("data/inbox").length;
      return V(n === 5, "5 files", `${n} files`);
    },
  },
  {
    id: "S2.1", desc: "one-way effect: migration marker written, exact size (plan Stage 2)",
    modes: ["post"],
    check: () => {
      const p = "data/migrated.flag";
      if (!existsSync(p)) return V(false, "exists, 26 bytes", "MISSING");
      return V(statSync(p).size === 26, "26 bytes", `${statSync(p).size} bytes`);
    },
  },
  // DB row-count pin (uncomment where node:sqlite is available; open READ-ONLY):
  // { id: "S2.3", desc: "rows migrated: user_version 0→2, items intact", modes: ["post"],
  //   check: () => { const db = new DatabaseSync("data/app.db", { readOnly: true });
  //     const n = (db.prepare("select count(*) c from items").get() as any).c;
  //     db.close(); return V(n === 7, "7 rows", `${n} rows`); } },
  {
    id: "S3.2", desc: "example UNVERIFIABLE: external share state not readable from here",
    modes: ["post"],
    check: () => U("runbook box 3.2"),  // delegated — listed, but never fails the run
  },
];

// ---------------------------------------------------------------------------
const mode = process.argv[2] as "pre" | "post";
if (mode !== "pre" && mode !== "post") {
  console.error("usage: devrunCheck.ts pre|post"); process.exit(2);
}

// App-quit precondition — implement a real read-only process/lock probe for the
// target; refuse (or loudly warn) if the app under test is running.
const appLooksLive = existsSync("data/.lock");
if (appLooksLive) console.log("WARNING: data/.lock present — app may be running; results untrustworthy.");

// INFO LINES — pinned premises, printed so preflight can transcribe them verbatim
// into the report (config under test, will-fire predictions, timestamps).
console.log(`INFO: mode=${mode} cwd=${process.cwd()}`);
console.log("INFO: config under test = data/config.json (see pin S0.1)");

const run = PINS.filter(p => p.modes.includes(mode));
const failures: string[] = [];
const unverifiable: string[] = [];
for (const p of run) {
  let r: Verdict;
  try {
    r = p.check();
  } catch (e) {
    // A thrown probe is a FAIL, never a crash — the contract line must always print.
    r = V(false, "probe runs", `THREW: ${e instanceof Error ? e.message : String(e)}`);
  }
  if (r.unverifiable !== undefined) {
    if (r.unverifiable.trim() === "") {
      // Undelegated UNVERIFIABLE is a FAIL — otherwise a lazy generation passes vacuously.
      const line = `FAIL [${p.id}] ${p.desc} — UNVERIFIABLE with no delegated runbook box`;
      console.log(line);
      failures.push(line);
    } else {
      const line = `UNVERIFIABLE [${p.id}] ${p.desc} — verify per ${r.unverifiable}`;
      console.log(line);
      unverifiable.push(line);
    }
    continue;
  }
  const line = `${r.ok ? "PASS" : "FAIL"} [${p.id}] ${p.desc} — expected ${r.expected}, observed ${r.observed}`;
  console.log(line);
  if (!r.ok) failures.push(line);
}

// UNVERIFIABLE summary prints BEFORE the contract line and never appears on it.
if (unverifiable.length > 0) {
  console.log(`${unverifiable.length} UNVERIFIABLE — delegated to runbook boxes (lines above); counted as neither pass nor fail.`);
}

// DETERMINISTIC CONTRACT LINE — scripts and humans key off this exact text.
if (failures.length === 0) {
  console.log(`ALL CHECKS PASSED (${mode})`);
  process.exit(0);
} else {
  console.log(`${failures.length} CHECK(S) FAILED (${mode}):`);
  failures.forEach(f => console.log("  " + f));
  process.exit(1);
}
