---
name: handoff
description: Compact the current conversation into a .md handoff document for another agent to pick up. Use when the user invokes /handoff, asks to hand off a session, write a handoff doc, or prepare context for a fresh agent to continue this work.
argument-hint: "What will the next session be used for?"
---

Handle this yourself — do not spin up a sub-agent for it. The current model has the full conversation context a sub-agent would lack.

Write a handoff .md document summarising the current conversation or project state for immediate handoff to a fresh agent to continue. Save to the temporary directory of the user's OS — not the current workspace.

Include a "suggested tier and effort" section, which suggests the tier model of the generating agent for the next session — derived from the oracle × blast-radius matrix and adjusted for the conversation/project's current lifecycle state (see Lifecycle state adjustments below).

Do not duplicate content already captured in other artifacts (specs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead. If no file-system tool is available, output the document to the conversation and note the path to which it would have been saved.

Redact any sensitive information not relevant to the handoff's actionability, such as API keys, passwords, or personally identifiable information. Sensitive information that belongs in the handoff — artifacts in play, open questions, etc. (see Handoff document template below) — is okay.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly. If the user's argument conflicts with the current campaign state, note the discrepancy in Notes for the next agent rather than silently resolving it.

## Handoff document template

When this skill runs, produce a `.md` file with exactly these sections, in order.
Omit a section only if it is genuinely inapplicable; note the omission with one line explaining why.
Redact any sensitive information not relevant to the handoff's actionability.

**Filename convention:** `handoff-{project-slug}-{YYYY-MM-DD}.md`
Derive project slug from the project name in the current session context (ignore parent project/s; use conversation title if no project name is present): lowercase, kebab-cased, truncated to 30 chars. If no project slug is identifiable, use `handoff-{YYYY-MM-DD-HHmm}.md`.
On repeated runs in the same day, append `-2`, `-3`, etc. rather than overwriting.

---

```md
# Handoff — {Project or session title (use {YYYY-MM-DD-HHmm} if none identifiable)}

**Generated:** {ISO-8601 date-time}  
**Generating model (user should fill this in, or omit the line):** {tier} / {model name}  
**Next session focus:** {one sentence — from user's argument if supplied, inferred from state if not}

---

## Current state

{2–5 sentences. What is complete, what is mid-flight, what is blocked.
If mid-campaign and not at a gate, note what the interrupted step was and what remains.}

## Artifacts in play

Reference only — no duplication. List each artifact with its path or URL
and a one-line description of its role. If none, write: "None — no artifacts have been used."

| Artifact | Role |
|---|---|
| `path/or/url` | what it is and why it matters |

## Open questions

Things the next agent must resolve before or during execution.
If none, write: "None — state is clean."

- [ ] {question or blocker}

## Suggested tier and effort

**Campaign state:** {Fresh start | Mid-campaign at a gate | Mid-campaign not at a gate | Post-campaign}  
**Oracle:** {Strong | Weak} — {one sentence: what the discriminator is, or why none exists}  
**Blast radius:** {High | Low} — {one sentence: what the cost of a wrong result would be}  
**Recommended tier:** {frontier | heavy | workhorse | mechanical}  
**Recommended effort:** {low | medium | high | xhigh | maximum}  

**Reasoning:** {2–4 sentences: apply the matrix to the next session's task,
then adjust for campaign state. Name the adjustment explicitly
(e.g. "Fresh start pushes effort up one notch because the oracle is unconfirmed
and the frame hasn't been reviewed yet").}

> **Agentic-fleet note:** If this handoff is a plan for multiple model calls or an agent fleet,
> replace this callout with a per-agent plan table and the pinned tier→model mapping.
> See **"Agentic-fleet handoffs"** below for the full format and rules.

## Notes for the next agent

{Optional. Warnings, constraints, or tactical context that don't fit the above.
Three bullet points or fewer. If none, write: "None."}
```

---

## Cognitive tiers

Doctrine is written in tiers, not model names, so it survives model churn. An example of the most recent tier→model mapping lives in **Local operational notes** at the bottom — the only part of this file that rots. Before writing the handoff, check whether the Local operational notes model list looks stale against what you know. If you have write access to this file, update it in-place and note the revision in the handoff; if not, alert the user to the rot and ask if they would like to proceed, or stop and address the rot first.  Flag if you have any uncertainty about your own training recency. If the user confirms the mapping is current or provides corrected values, proceed. If unresolved, generate the handoff with a visible WARNING block at the top of the Suggested tier section.

| Tier | Characteristics |
|---|---|
| **frontier** | **Capability:** Strongest available; used sparingly — primarily as a gate and adversarial reviewer, not as a primary content generator.<br><br>**Route here to *generate* when:** opening framing or constitutional review where the oracle's strength is not yet established and a misframed plan compounds downstream (campaign-open plans, constitutional prompts and docs); or when an irreversible step needs a break-attempt before authorization and heavy cannot serve as its own adversarial reviewer.<br><br>**Route here to *review* when:** the oracle is weak and the blast radius is high (frontier adversarial review compensates for the absent oracle); any irreversible step regardless of quadrant; any step where blast radius is catastrophic (root-damaging, org-ending, health-adverse) — at catastrophic blast, frontier reviews *every* step, not only irreversible ones.<br><br>**Constraint:** Not a default escalation from heavy. If recommending frontier, include the explicit justification (gate, irreversibility check, or framing review) in Reasoning. |
| **heavy** | **Capability:** High-capability orchestrator and sustained generator.<br><br>**Route here to *generate* when:** the oracle is weak and the blast radius is high — concurrency issues, lifecycle edge cases, subtle semantic contracts, mutations to long-lived state; orchestrating any session that will call multiple agents.<br><br>**Constraint:** Not the default escalation from workhorse. Frontier adversarial review still applies at irreversible steps and at every step when blast radius is catastrophic, even when heavy is the generation tier. |
| **workhorse** | **Capability:** The default execution and verification tier.<br><br>**Route here when:** numerous well-specified items; systematic sweeps and triage passes; verification runs and peer spot-checks on weak-oracle / low-blast work; any session where the oracle is strong or the blast radius is low enough that a wrong result costs a correction pass, not a recovery operation.<br><br>**Constraint:** Not a substitute for mechanical when items are fully spec'd and file-scoped; not a substitute for heavy when oracle weakness and high blast radius combine. |
| **mechanical** | **Capability:** Spec-only execution.<br><br>**Route here when:** every item is fully specified, spelled out individually, and scoped to named files — execution only, no interpretation or adaptation required.<br><br>**Constraint:** Give it files, not the repo. Resolve all ambiguity before routing here; it executes specs, it does not interpret. |

> **Adversarial review:** a decorrelated agent attempts to break the output —
> find inputs, edge cases, or readings that cause it to fail — without access
> to the generating agent's reasoning. The goal is falsification, not improvement.

### Lifecycle state adjustments

The tier and effort recommendation is sensitive to where in the campaign lifecycle the next agent is picking up. Identify the campaign state below, apply the oracle × blast-radius matrix to the next session's task, then apply the adjustment rule for that state before writing the recommendation.

---

**Fresh start** — Framing hasn't happened; oracle strength is unconfirmed.

Apply the following adjustments *before* reading the matrix:

1. **Treat the oracle as weak**, regardless of apparent signals. Oracle strength is not confirmed until the frame survives its first gate.
2. **Treat the blast radius as high**, regardless of task scope. A misframed plan that reaches execution compounds across the whole campaign; the frame is still live.
3. **Apply the weak-oracle / high-blast cell as a floor.** The matrix can only push you higher from here, not lower.
4. **Disqualify mechanical.** If the unadjusted matrix would return mechanical, escalate to workhorse. Framing work requires interpretation; mechanical cannot do it.
5. **Push effort up one notch** from what the unadjusted matrix would recommend. Spend the notch on framing, not generation.
6. **Include in the handoff doc a recommendation that the next agent's first gate be a framing review**, not an execution checkpoint.

---

**Mid-campaign, at a gate** — The frame has survived review; oracle is established.

Apply the matrix directly — no adjustment.

- Use oracle and blast-radius signals as assessed at the last gate; do not second-guess them.
- If the oracle was declared absent at a prior gate, apply the weak column without re-litigating it.

---

**Mid-campaign, not at a gate** — Frame exists; an item is mid-execution.

Apply the matrix to the *remaining* work only, then apply these adjustments:

1. **Scope the oracle and blast assessment to what's left**, not what's been done. An oracle that was strong for completed steps may not apply to the next.
2. **If any oracle question is unresolved**, treat the oracle as weak for the remaining work until a gate closes it.
3. **Do not treat an incomplete item as a gate.** The next agent picks up mid-step. Surface what's done, what's blocked, and what remains; the recommended tier and effort apply to the remaining work only.
4. **Carry over the effort level from the completed portion only if the remaining work is in the same matrix cell.** If the remaining steps are in a different cell, re-derive effort from that cell.

---

**Post-campaign / consolidation** — Next agent is sweeping, folding, or retrospecting.

Apply the matrix, then apply these downward adjustments:

1. **Drop to workhorse** if the matrix returns heavy — unless the consolidation itself touches high-blast concerns (irreversible merges, data-integrity passes, schemas consumed by external systems). If it does, hold the matrix recommendation.
2. **Drop to mechanical** if every item in the consolidation is fully spec'd and file-scoped, even if the campaign ran at workhorse or above.
3. **Scale effort down one notch** from what the matrix would recommend. Consolidation operates on the known; deliberation spend is lower.
4. **Exception — if the consolidation is itself a gate** (a final integrity check, a retrospective that updates a source of truth), apply the matrix without adjustment. It is a gate-class task, not a sweep.

### Assignment law: Oracle × Blast-Radius Matrix

**Oracle** — what checks the output. **Strong:** a mechanical discriminator exists (a repro that flips, tests, typecheck, schema validation, a diffable ground truth). **Weak:** judgment-scored; no repro; right and wrong are only visible to a person after the fact.

**Blast radius** — the cost of being wrong. **High:** data integrity, irreversible effects, wide contract surface, long-lived state. **Low:** localized and reversible; a wrong result costs a correction pass, not a recovery operation.

#### Reading the conversation for oracle and blast signals

Before applying the matrix, assess the two inputs. Neither announces itself — you have to infer from the transcript.

**Oracle strength**

Look for evidence of a mechanical discriminator: something that will flip unambiguously from fail to pass when the output is correct.

*Strong oracle signals:*
- A test suite, type-checker, linter, schema validator, or other automated check is in scope or already exists
- The task has a diffable ground truth (a target output, a reference implementation, a spec with acceptance criteria stated as conditions)
- Correctness is binary — it runs or it doesn't, it passes or it doesn't, the numbers match or they don't
- The session has already produced a repro that fails in the current state

*Weak oracle signals:*
- Correctness requires a person reading the output and judging it ("does this feel right," "is this tone appropriate," "is this analysis sound")
- There is a rubric, but the rubric was authored for this task and has not itself been validated
- The acceptance criterion is something like "the user is satisfied" or "it matches the intent"
- No one in the session has named a check — the implicit standard is "I'll know it when I see it"

If a rubric exists but was assembled for this campaign with no external grounding, treat it as weak until proven otherwise. A rubric is not automatically an oracle.

**Blast radius**

Look for signals about the cost of a wrong result that survives to the next gate.

*High blast signals:*
- Irreversible or hard-to-reverse operations: deletes, migrations, deploys, publishes, sends
- Shared contract surface: a public API, a schema consumed by other systems, a configuration file with downstream readers
- Long-lived state: a database, a document that will be used as a source of truth by others, a spec that will be acted on by multiple agents
- The session is mid-recovery from a prior failure — another wrong move compounds the damage

*Low blast signals:*
- Changes are scoped to a private working directory, a branch, or a throwaway artifact
- The output can be discarded and regenerated at negligible cost
- No external system or person depends on this result until the user explicitly promotes it
- The task is exploratory: its purpose is to produce a draft, not a landing

If signals are mixed — say, the output is reversible but will be read by other agents before the user reviews it — weight toward high. Downstream propagation turns a locally reversible action into a wide-radius one.

> **Tier the generation by what checks it, not by task adjectives.**

| | **Strong oracle** | **Weak oracle** |
|---|---|---|
| **High blast** | **Tier:** Workhorse generates; Heavy reviews<br>**Effort:** Generation → high; verification → high–maximum<br>**Posture:** The oracle is the arbiter — spend on verification and gates, not on generation. Heavy review compensates for the one thing the oracle cannot catch: a misframed task that produces a wrong-but-valid output.<br>**Gates:** Oracle gate at every step. Irreversible steps additionally require Frontier review and explicit user authorization before execution. | **Tier:** Heavy generates; Frontier adversarial review<br>**Effort:** Maximum throughout — no oracle exists to compensate for deliberation failures, so deliberation must be the safeguard<br>**Posture:** Smallest possible steps; keep each atomic so rollback remains possible despite high blast. Adversarial review is not optional — it substitutes for the absent oracle. High effort on a misframed task buys elaborate wrongness; invest effort in framing first.<br>**Gates:** User gate before anything lands; no exceptions. |
| **Low blast** | **Tier:** Mechanical or Workhorse generates<br>**Effort:** Low–medium on generation; scale up only if the oracle reveals systematic failure<br>**Posture:** Lean on the oracle — it is cheap, fast, and sufficient. Human review is optional; when applied, keep it lightweight. Do not overspend on generation when the oracle catches errors anyway. A pattern of oracle failures is the signal to escalate tier, not individual misses.<br>**Gates:** Oracle gate only. No peer review required unless failures are appearing at a pattern level across items. | **Tier:** Workhorse generates; Workhorse peer spot-checks<br>**Effort:** Medium on generation; low on review — wrong is recoverable, so the cost of a miss is a correction pass, not a recovery operation<br>**Posture:** Keep review lightweight; a second Workhorse pass is the check, not Heavy or Frontier. If a pattern of errors emerges across items, escalate the review posture — not the generation tier. The low blast is what keeps this affordable; do not let weak-oracle anxiety push spend beyond what the stakes justify.<br>**Gates:** No formal gate; peer judgment is the check. |

## Non-code campaigns: same mechanics, different nouns

The oracle × blast-radius framework applies to any campaign regardless of substrate.
Translate the code vocabulary into your campaign's terms:

| Code noun | Non-code equivalent |
|---|---|
| **Isolation** | Disjoint artifact ownership — each lane works on its own copies |
| **Worktree** | A lane's private working directory |
| **Merge** | A sequential consolidation pass that folds a lane's artifacts into the deliverable and re-runs accumulated checks |
| **Gate** | Whatever oracle grounding found or built — a validator run, rubric pass, ground-truth diff, or explicit user authorization |
| **Repro** | The failing example or violated criterion, committed as a runnable check |

**If no oracle exists and none can be built, declare it explicitly in the "Suggested tier and effort" section and route through the weak-oracle column. Never assert a rubric exists when none has been validated.**

One structural difference from code campaigns: a flawed verdict in non-code work is as often a judgment disagreement as a broken mechanism. Gates are where competing readings get adjudicated — bring the competing interpretations alongside the refutations. If disagreement persists past two rounds, gate on the user; adjudication belongs to the gate, not the generation loop.

What transfers unchanged: the oracle × blast-radius matrix, round counts, checkpoints, and user gates.
What transfers with translation: the nouns above. Keep the handoff oriented to the campaign's own goal — the matrix measures oracle strength and blast radius, not task shape.

> **Framing note:** Effort multiplies wherever deliberation points. High effort on a misframed task compounds errors out of frame downstream. Spend effort where framing happens — clustering, triage, foundational gates, tasks upstream of a campaign — and let lane effort scale with problem depth only after the frame survives review.

> **Agentic-fleet handoffs — pin the model mapping**
>
> If the handoff this skill is producing is itself a plan intended for an agentic fleet
> or multiple sequential model calls, apply these three rules before writing the document:
>
> 1. **Pull the current tier→model mapping from Local operational notes and pin it with
>    today's date into the plan.** Do not leave tier names unresolved — a fleet executes
>    the plan without a human in the loop to interpret "workhorse." The pinned mapping is
>    the execution contract.
>
>    *Example pin block:*
>    ```
>    Tier→model mapping (pinned 2026-08-04)
>    frontier  → Fable 5 / GPT-5.6 Sol (latest)
>    heavy     → Opus 5 / Gemini Flash 3.6 (latest)
>    workhorse → Sonnet / GPT-5.6 Terra (latest)
>    mechanical → Haiku / GPT-5.6 Luna (latest)
>    ```
>
> 2. **Recommend a tier/effort for every planned agent, using the oracle x blast radius matrix.**
>    List the agents in a table in the planned order they will be called. 
>
>    *Example tier/effort table:*
>    ```
>    | Work | Tier | Model | Effort | Why |
>    |---|---|---|---|---|
>    | Orchestrator | heavy | Opus 5 | high | Holds campaign state; dispatches lanes; merges |
>    | Generation lane | workhorse | Sonnet 5 | medium | Well-specified items; oracle catches errors |
>    | Adversarial review | frontier | Fable 5 | maximum | Irreversible step; frontier justification: irreversibility check |
>    | Mechanical sweep | mechanical | Haiku 4.5 | low | Fully spec'd, file-scoped; no interpretation required |
>    ```
>    
> 3. **Treat any tier→model staleness as a blocker**, not a warning. If the mapping
>    in Local operational notes looks stale and you do not have write access to update it,
>    halt and surface the issue to the user before generating the agentic-fleet handoff plan. A fleet that
>    executes against a stale mapping may route work to the wrong tier with no human to
>    catch the error mid-run.
>
> This rule does not apply to handoffs destined for a single next agent; those can
> leave tier names unresolved and rely on that agent's own Local operational notes.

## Local operational notes — edit per deployment; keep out of the doctrine

Deployment-specific facts live here and only here so the rest of this file stays shareable.
Replace placeholder values with your deployment's actuals. When the model menu changes,
update the mappings here and in new plans; the doctrine above should not need to change.

**Last updated:** 2026-08-03 *(replace with your deployment's values)*

---

**Tier→model mapping**

```
frontier   → Fable 5 / Mythos / GLM 5.2 / Kimi K3 / GPT-5.6 Sol (latest)
heavy      → Opus 5 / Gemini Flash 3.6 (latest)
workhorse  → Sonnet / GPT-5.6 Terra / Gemini 3.5 Flash-Lite (latest)
mechanical → Haiku / GPT-5.6 Luna (latest)
```

**Effort ladder**

```
low → medium → high → xhigh → maximum
```

**Cost multipliers** *(per completed item relative to mechanical; blend of per-token price and tokens consumed — re-measure when menu or pricing changes)*

| Tier | Multiplier |
|---|---|
| mechanical | 1× |
| workhorse | 3–5× |
| heavy | 10–20× |
| frontier | ≈ one heavy item at maximum deliberation |

**Deployment constraints** *(pricing caps, quota limits, compliance terms — add rows as needed)*

| Constraint | Detail |
|---|---|
| *(none recorded)* | — |
