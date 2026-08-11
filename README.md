# Claude Code Skills — a working library

Four production skills for [Claude Code](https://claude.com/claude-code), authored the way everything in this library was built: **by directing Claude**. I supply design intent, constraints, review, and verification; the model implements. Every skill here has survived its own adversarial review, been revised against measured campaign evidence, or been A/B-tested against its predecessor before installation — the same discipline the skills themselves enforce.

Skills use the open `SKILL.md` format — a cross-vendor standard readable by a growing set of agent tools, not a single-platform artifact.

## The skills

### `orchestrator`
Generates execution-ready orchestration plans for multi-agent work: cognitive-tier model assignments (the "Oracle Blast"), parallel lanes with exclusive file ownership, gate-based loops with stop conditions, an adversarial review of the plan itself, and ready-to-adapt prompt templates. Born from a real bug-fix plan worth canonizing; later measured against nine campaign plans and amended where reality disagreed with doctrine.

### `butterfly-collector`
Governs an iterating bug-eradication campaign: hunt a codebase with a frontier model at maximum effort, plan fixes via `orchestrator`, execute, generate a dev-run bundle (plan, human runbook, state checker, snapshot/restore), synthesize findings, and repeat until nothing new remains — ending at a hard gate only a human can pass. State lives in a repo file that structurally cannot imitate consent. Before first use, a 17-agent adversarial review of this skill found 9 defects (including a consent-bypass); all were fixed before it ever governed a campaign. Its first real campaign ran nine iterations and closed on evidence with full cost accounting.

### `handoff`
Compacts a session into a handoff document a fresh agent can continue from cold: current state, artifacts in play, open questions, and a suggested model tier and effort level with reasoning. Continuity engineering for long-running work, built from need before the industry settled on a name for it.

### `word-vomit`
Converts raw, excited, disorganized thought into a structured, verifiable representation of intent — extractive when intent exists, generative when it's still forming — then routes it to execution, handoff, or an explicit park. Ships with full annotated worked transcripts. The deliberate industrialization of the author's own creative method.

## Install

Copy each skill **as an extracted directory** into your skills folder:

```
~/.claude/skills/
├── butterfly-collector/
│   ├── SKILL.md
│   ├── references/
│   └── scripts/
├── handoff/
│   └── SKILL.md
├── orchestrator/
│   └── SKILL.md
└── word-vomit/
    ├── SKILL.md
    └── references/
```

> Practical note discovered the hard way: zipped `.skill` archives do not load — only extracted directories do. If a skill misbehaves after an update, check that every install location actually got the new version; silent version skew between channels is real.

## Provenance and privacy

The worked examples inside `butterfly-collector/references/examples/` are **sanitized exemplars from real completed campaigns**: personal names, usernames, machine identifiers, and application identities were replaced or fictionalized (marked in each file's banner), then the result was verified by an adversarial de-anonymization pass. Structure, numbers, and wording are otherwise verbatim. Read them for shape and conventions, not as instructions to execute.

## Author

Robert García — I build and operate AI systems for the un-artificial; I don't hand-write code. This library documents the operating method: decompose the ambition, assign the right grade of model to the right shape of work, gate what's irreversible behind human checkpoints, verify behavior rather than trusting reports, measure what it cost, and rewrite the doctrine when the measurements disagree. This library is one piece of a larger portfolio at https://robertgarcia.ai .

