# Deliberation — evolution direction

## Target positioning

Deliberation should evolve from a guided software-development workflow into a lightweight human-in-the-loop decision protocol for coding agents.

It should **not** replace native planning, execution, task tracking, worker spawning, or review features provided by Codex, Claude Code, OpenCode, and similar hosts.

Its durable value should come from improving decision quality, exposing assumptions and trade-offs, challenging plans, helping the user understand the system, and preserving important rationale.

> Deliberation is a decision-quality and understanding layer on top of native agent workflows.

## Core problem to solve

Native plan modes are increasingly good at:

- exploring repositories,
- asking clarifying questions,
- producing implementation plans,
- delegating research to workers,
- transitioning from planning to implementation.

They are still less reliable at:

- framing the actual decision correctly,
- making decision drivers and constraints explicit,
- presenting genuinely distinct alternatives,
- comparing trade-offs against agreed criteria,
- surfacing unverified assumptions,
- adversarially challenging a plausible plan,
- explaining decisions to the human operator,
- preserving rationale that will matter months later.

Deliberation should focus only on this gap.

## Proposed product shape

A single portable skill or mode, invoked on demand for high-impact or ambiguous decisions.

Conceptual command:

```text
/deliberate [decision, question, architecture, or existing plan]
```

Possible operations:

```text
/deliberate --decide <decision>
/deliberate --challenge <existing plan>
/deliberate --explain <system, change, decision, or risk>
/deliberate --record <accepted decision>
```

These do not need to be host-specific commands. They can remain conceptual operations implemented by one skill.

## Core capabilities

### 1. Decision framing

Before proposing a solution, identify:

- the decision to be made,
- decision drivers,
- constraints,
- non-goals,
- stakeholders or affected systems,
- reversibility and expected lifetime,
- unknowns that materially affect the choice.

Do not proceed with an ambiguous decision statement when clarification or repository inspection can resolve it.

### 2. Alternatives and trade-offs

Generate only genuinely distinct alternatives. Avoid artificial variants created merely to satisfy a fixed number of options.

For each viable option describe:

- how it works,
- advantages,
- disadvantages,
- operational and maintenance costs,
- migration or rollback implications,
- assumptions,
- conditions under which it becomes the preferred choice.

Compare options against the previously established drivers and constraints.

### 3. Plan challenge

Accept a plan created by the host's native Plan Mode and review it adversarially.

Check for:

- hidden or unverified assumptions,
- omitted requirements,
- unnecessary abstractions,
- failure to reuse existing mechanisms,
- migration and compatibility risks,
- missing rollback strategy,
- weak verification criteria,
- excessive scope,
- decisions that require product or user preference rather than agent inference.

Return either:

- accepted as sufficiently robust,
- accepted with explicit risks,
- revision required, with concrete changes.

### 4. Explain

Provide focused explanation modes rather than generic prose.

#### Explain decision

Explain why a decision was made, which alternatives were considered, and which costs were accepted.

#### Explain change

Explain an implementation from a reviewer perspective, preferably file by file or component by component.

#### Explain system

Explain control flow, boundaries, invariants, data ownership, extension points, and failure paths.

#### Explain risk

Explain what can fail, how failure will be detected, how impact is limited, and how the change can be rolled back.

#### Teach-back

Optionally ask the user to restate the solution in their own words, then identify discrepancies or missing concepts. This keeps the human in the cognitive loop rather than only in an approval loop.

### 5. Decision capture

For important accepted decisions, optionally produce a concise decision record containing:

- status and date,
- context,
- decision,
- rationale,
- rejected alternatives,
- consequences,
- assumptions,
- conditions that should trigger reconsideration.

Do not create a document for every task. Persist only decisions likely to matter beyond the current session.

## Adaptive deliberation

Deliberation should be risk-based, not a mandatory sequence of checkpoints.

Suggested policy:

```text
Low impact      -> agent decides and continues
Medium impact   -> agent states the assumption and continues
High impact     -> agent proposes deliberation
Critical impact -> explicit user decision is required
```

Signals that deliberation is appropriate:

- high cost of reversal,
- broad architectural impact,
- uncertain assumptions,
- data, security, compatibility, or migration risk,
- difficult verification,
- conflict with established architecture,
- a choice dependent on product or user preference.

Signals that it is unnecessary:

- local naming decisions,
- straightforward refactors,
- obvious tests,
- implementation of an already accepted pattern,
- inexpensive and easily reversible choices.

## Minimal architecture

Prefer a small, host-neutral structure:

```text
deliberation/
├── SKILL.md
├── references/
│   ├── decision-record.md
│   ├── challenge-checklist.md
│   └── explanation-patterns.md
└── scripts/
    └── validate-decision-record.sh  # optional
```

The skill should define:

1. when deliberation should be invoked,
2. how to frame a decision,
3. how to generate and compare alternatives,
4. how to challenge a plan,
5. when to ask the user,
6. when to write a decision record,
7. when to stop without additional ceremony.

Host adapters should be avoided unless they provide real mechanics that cannot be expressed portably.

## Explicit non-goals

Deliberation should not contain:

- a custom planner,
- a `spec -> plan -> dev -> test -> review` workflow,
- its own orchestrator,
- a catalogue of specialized subagents,
- mandatory approval after every step,
- automatic documentation for every task,
- its own task-management system,
- implementation logic,
- session-state persistence,
- adapters that merely mirror native host features.

Planning, implementation, worker orchestration, task state, and repository operations remain responsibilities of the host.

Task checkpointing and cross-session handoff belong to the separate Artifact concept.

## Relationship to Artifact

Keep the concerns separate:

- **Deliberation** preserves why an important decision was made.
- **Artifact** preserves where an ongoing task currently stands.

A Deliberation decision record may be referenced by an Artifact checkpoint, but neither should duplicate the other's responsibilities.

## Initial implementation backlog

- [ ] Rewrite the project description around decision quality and human understanding.
- [ ] Audit the existing plugin and mark planner/workflow responsibilities for removal.
- [ ] Reduce the project to one primary skill.
- [ ] Define invocation heuristics based on impact, uncertainty, and reversibility.
- [ ] Implement the decision-framing protocol.
- [ ] Implement criteria-driven comparison of alternatives.
- [ ] Implement plan-challenge mode.
- [ ] Extract Explain into the focused modes described above.
- [ ] Add an optional teach-back interaction.
- [ ] Add a concise decision-record template.
- [ ] Add rules preventing unnecessary artifact generation.
- [ ] Define clean boundaries between Deliberation and Artifact.
- [ ] Test the skill against native Codex and Claude Code planning rather than replacing them.
- [ ] Create example scenarios demonstrating when deliberation adds value and when it should remain inactive.
- [ ] Remove host adapters that provide no capability beyond prompt translation.

## Validation criteria

The redesigned project is successful when:

- native Plan Mode remains the primary planning mechanism,
- Deliberation can improve or reject a plausible but flawed plan,
- the user can understand important architectural choices without reading the full session,
- recorded decisions remain useful in a later session,
- small tasks receive no additional ceremony,
- the skill remains portable across hosts,
- using it costs less effort than manually reviewing the decision without it.

## One-sentence project definition

> A human-in-the-loop decision protocol for coding agents that improves decision quality, exposes assumptions and trade-offs, challenges plans, and records important rationale without replacing native planning and execution workflows.
