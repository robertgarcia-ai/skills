#!/usr/bin/env python3
"""Validate docs/butterfly/state.json against schema v1.

Usage: python3 validate_state.py [path/to/state.json]
Exit 0 = valid (warnings allowed, printed to stderr). Exit 1 = invalid.

The single most important rule enforced here: `gates` may contain ONLY the
keys A, B, C. The hard gate has no configuration surface by design — its
behavior lives only in the skill's SKILL.md, and editing that file is the
sole way to change it. A state file claiming hard-gate automation is invalid
state, not authorization.
"""
import json
import os
import sys

PHASES = {"hunt", "execute", "devrun", "synthesize", "done"}
STATUSES = {"pending", "in_progress", "artifacts_done", "stamped"}
GATE_KEYS = {"A", "B", "C"}
GATE_VALUES = {"ask", "auto"}
FLOORS = {"low", "medium", "high"}
KNOWN_TOP = {
    "schema", "campaign", "iteration", "phase", "phase_status", "gates",
    "hunter", "hunter_downshift", "severity_floor", "scope",
    "repo_head_at_stamp", "artifacts", "snapshot", "trend", "history", "notes",
}
SNAPSHOT_KEYS = ("manifest", "location", "taken_at", "keep_until")
KNOWN_EVENTS = {
    "init", "hunt_started", "execute_started", "devrun_started",
    "synthesize_started", "hunt_report_done", "plan_done",
    "gate_A_ask", "gate_B_ask", "gate_C_ask",
    "gate_A_auto_pass", "gate_B_auto_pass", "gate_C_auto_pass",
    "gate_A_declined", "gate_B_declined", "gate_C_declined",
    "gate_B_demoted_snapshot_unverified", "gate_C_demoted_plateau",
    "gate_C_demoted_apparatus_loop", "gate_C_demoted_empty_set",
    "gates_changed", "gate_session_reconfirm", "hunt_session_reconfirm",
    "execute_done", "bundle_done",
    "snapshot_taken", "snapshot_verified", "snapshot_pruned",
    "cowork_run_started", "cowork_run_summary", "restore_verified",
    "user_run_recorded", "user_run_skipped", "devrun_vacuous", "hunter_ab",
    "synthesis_done", "termination_pass", "termination_fail",
    "hard_gate_presented", "hard_gate_restart", "hard_gate_close",
    "campaign_archived", "campaign_abandoned",
}

errors, warnings = [], []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def is_pos_int(v):
    return isinstance(v, int) and not isinstance(v, bool) and v >= 1


def check_gates(gates):
    if not isinstance(gates, dict):
        err("`gates` must be an object with keys A, B, C.")
        return
    for k, v in gates.items():
        if k not in GATE_KEYS:
            hint = " (this looks like an attempt to configure the hard gate)" \
                if k.strip().lower() in {"hard", "hardgate", "hard_gate", "d", "restart"} else ""
            err(
                f"ILLEGAL GATE KEY '{k}'{hint}: the loop has exactly three "
                f"configurable gates (A, B, C). The hard gate has no "
                f"configuration surface by design — its behavior lives only in "
                f"the skill's SKILL.md, and editing that file is the sole way "
                f"to change it. Remove this key."
            )
        elif v not in GATE_VALUES:
            err(f"gates.{k} must be 'ask' or 'auto', got {v!r}.")
    for k in GATE_KEYS - set(gates.keys()):
        err(f"gates.{k} missing (must be 'ask' or 'auto').")


def check_hunter(h, name="hunter"):
    if not isinstance(h, dict):
        err(f"`{name}` must be an object.")
        return
    req = ("model", "effort") if name == "hunter_downshift" else ("surface", "model", "effort")
    for k in req:
        if not isinstance(h.get(k), str) or not h.get(k):
            err(f"{name}.{k} must be a non-empty string.")
    if "lenses" in h and not (isinstance(h["lenses"], list) and all(
            isinstance(x, str) and x for x in h["lenses"])):
        err(f"{name}.lenses must be a list of non-empty strings when present.")


def check_scope(s):
    if not isinstance(s, dict):
        err("`scope` must be an object: {include?: [str], exclude?: [str]}.")
        return
    for k in s:
        if k not in ("include", "exclude"):
            warn(f"scope.{k} is not a recognized key (only include/exclude).")
    for k in ("include", "exclude"):
        if k in s and not (isinstance(s[k], list) and all(
                isinstance(x, str) and x for x in s[k])):
            err(f"scope.{k} must be a list of non-empty path-prefix strings.")


def check_snapshot(sn):
    if not isinstance(sn, dict):
        err("`snapshot` must be an object "
            "{manifest, location, taken_at, keep_until}.")
        return
    for k in SNAPSHOT_KEYS:
        if not isinstance(sn.get(k), str) or not sn.get(k):
            err(f"snapshot.{k} must be a non-empty string.")


def check_trend(t):
    if not isinstance(t, list):
        err("`trend` must be an array of {iter, new_findings}.")
        return
    missing_split = missing_cost = 0
    for i, row in enumerate(t):
        if not (isinstance(row, dict) and is_pos_int(row.get("iter"))
                and isinstance(row.get("new_findings"), int)
                and not isinstance(row.get("new_findings"), bool)
                and row["new_findings"] >= 0):
            err(f"trend[{i}] must be {{iter: int>=1, new_findings: int>=0}}.")
            return
        for opt in ("regressions", "devrun_surface", "target_findings",
                    "apparatus_findings"):
            if opt in row and not (isinstance(row[opt], int)
                                   and not isinstance(row[opt], bool)
                                   and row[opt] >= 0):
                err(f"trend[{i}].{opt} must be an int >= 0 when present.")
                return
        if "cost" in row and not (isinstance(row["cost"], str) and row["cost"]):
            err(f"trend[{i}].cost must be a non-empty string when present.")
            return
        if "target_findings" not in row:
            missing_split += 1
        if "cost" not in row:
            missing_cost += 1
    if missing_split:
        warn(
            f"{missing_split} trend row(s) lack the target_findings/"
            f"apparatus_findings split (legacy rows are valid; the advisories "
            f"fall back to new_findings, which conflates target yield with "
            f"apparatus hygiene — see state.md migration notes)."
        )
    if missing_cost:
        warn(
            f"{missing_cost} trend row(s) lack a cost note — the exemplar "
            f"campaign recorded it on 2 of 6 cards when it rode the card as "
            f"prose; the row is its structured home."
        )
    # Plateau advisory: t[-1] >= t[-3] over target_findings, falling back to
    # new_findings on legacy rows (state.md Trend advisory — same test there
    # and in phases/synthesize.md).
    series = [r.get("target_findings", r["new_findings"]) for r in t]
    tail = series[-3:]
    if len(tail) == 3 and tail[2] >= tail[0]:
        warn(
            "ADVISORY: the last three recorded iterations show no net "
            "decrease in target findings — surface this plateau on the next "
            "Gate C card, recomputed from the trend rows on that card (never "
            "carried from a prior document). The user judges its meaning, but "
            "a due plateau demotes a Gate C 'auto' pass to 'ask' (log "
            "gate_C_demoted_plateau; see state.md Trend advisory)."
        )
    # Apparatus-loop advisory: the last two rows carry an explicit
    # target_findings: 0 while still finding things — the detector now yields
    # only against the campaign's own apparatus.
    last2 = t[-2:]
    if len(last2) == 2 and all(
            r.get("target_findings") == 0 and r["new_findings"] > 0
            for r in last2):
        warn(
            "ADVISORY: the last two recorded iterations found nothing against "
            "the target — every finding is against the campaign's own "
            "apparatus. The next Gate C card carries the graduated options "
            "(continue / raise severity_floor / narrow scope or set lenses / "
            "aim at a vacuous dev run / elect the hard gate), and a Gate C "
            "'auto' pass demotes to 'ask' (log gate_C_demoted_apparatus_loop; "
            "see SKILL.md Gate law)."
        )


def check_history(hist):
    if not isinstance(hist, list):
        err("`history` must be an array of {ts, event}.")
        return
    unknown = []
    for i, row in enumerate(hist):
        if not (isinstance(row, dict) and isinstance(row.get("ts"), str)
                and isinstance(row.get("event"), str)):
            err(f"history[{i}] must be {{ts: string, event: string}}.")
            return
        if row["event"] not in KNOWN_EVENTS and row["event"] not in unknown:
            unknown.append(row["event"])
    if unknown:
        warn(
            "history event(s) not in the documented vocabulary (state.md): "
            + ", ".join(repr(e) for e in unknown)
            + " — typo'd events silently break resume branching and the "
              "hard-gate saturation counts."
        )


def check_artifacts(a):
    if not isinstance(a, dict) or not all(
        isinstance(k, str) and isinstance(v, str) for k, v in a.items()
    ):
        err("`artifacts` must map logical names to repo-relative path strings.")
        return
    if os.path.isdir("docs"):  # only meaningful when run from the repo root
        for k, p in a.items():
            if not os.path.exists(p):
                warn(f"artifacts.{k} points at missing file: {p}")


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        "docs", "butterfly", "state.json")
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            state = json.load(f)
    except FileNotFoundError:
        print(f"INVALID: state file not found at {path}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"INVALID: not parseable JSON ({e})", file=sys.stderr)
        return 1
    if not isinstance(state, dict):
        print("INVALID: state root must be a JSON object", file=sys.stderr)
        return 1

    if state.get("schema") != 1:
        err(f"`schema` must be 1, got {state.get('schema')!r}.")
    if not is_pos_int(state.get("campaign")):
        err("`campaign` must be an integer >= 1.")
    if not is_pos_int(state.get("iteration")):
        err("`iteration` must be an integer >= 1.")
    if state.get("phase") not in PHASES:
        err(f"`phase` must be one of {sorted(PHASES)}, got {state.get('phase')!r}.")
    if state.get("phase_status") not in STATUSES:
        err(f"`phase_status` must be one of {sorted(STATUSES)}, "
            f"got {state.get('phase_status')!r}.")
    if state.get("phase") == "done" and state.get("phase_status") in STATUSES \
            and state.get("phase_status") != "stamped":
        err("`phase: done` pairs only with `phase_status: stamped` — the "
            "hard-gate close writes them together, and a closed campaign has "
            "no pending work. Any other status here is illegal state "
            "(state.md, resume table), not a resumable position.")
    check_gates(state.get("gates"))
    gates = state.get("gates")
    if isinstance(gates, dict):
        autos = sorted(k for k in GATE_KEYS if gates.get(k) == "auto")
        if autos:
            warn(
                f"gate(s) {', '.join(autos)} set to 'auto' — reminder: on a "
                f"cold resume, the first loop gate reached this session is "
                f"presented as 'ask' regardless (gate_session_reconfirm; see "
                f"SKILL.md Gate law)."
            )
    if "hunter" not in state:
        err("`hunter` missing — must be an object {surface, model, effort}.")
    else:
        check_hunter(state["hunter"])
    if "hunter_downshift" in state:
        check_hunter(state["hunter_downshift"], "hunter_downshift")
    if state.get("severity_floor") not in FLOORS:
        err(f"`severity_floor` must be one of {sorted(FLOORS)}, "
            f"got {state.get('severity_floor')!r}.")
    if "scope" in state:
        check_scope(state["scope"])
    if "repo_head_at_stamp" in state and not isinstance(
            state["repo_head_at_stamp"], str):
        err("`repo_head_at_stamp` must be a string.")
    if "artifacts" in state:
        check_artifacts(state["artifacts"])
    if "trend" in state:
        check_trend(state["trend"])
    if "history" in state:
        check_history(state["history"])
    if "snapshot" in state:
        check_snapshot(state["snapshot"])
    if "notes" in state and not isinstance(state["notes"], str):
        err("`notes` must be a string.")
    for k in state:
        if k not in KNOWN_TOP:
            warn(f"unknown top-level key '{k}' (ignored; forward-compat).")

    for w in warnings:
        print(f"WARNING: {w}", file=sys.stderr)
    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        print("STATE INVALID — fix the errors above before proceeding.",
              file=sys.stderr)
        return 1
    print(
        f"STATE OK — campaign {state['campaign']}, iteration "
        f"{state['iteration']}, phase {state['phase']} "
        f"({state['phase_status']}); gates "
        f"A={state['gates']['A']} B={state['gates']['B']} C={state['gates']['C']}."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
