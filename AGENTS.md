# Deliberation — Codex Working Agreement

This repository develops **Deliberation**, a cross-environment coding-agent
work mode that changes how an agent collaborates with a user. It is not a
task-specific coding capability.

## Start every session here

Read these files in order before proposing or making project changes:

1. `docs/CURRENT_STATE.md` — current phase, latest progress, and next decision.
2. `DELIBERATION_MANIFEST.md` — product vision and intended agent behaviour.
3. `docs/PROJECT_CONTEXT.md` — rationale and context distilled from the
   original design conversation.
4. `docs/DECISIONS.md` — decisions already made and their consequences.
5. Inspect the working tree and preserve unrelated user changes.

Do not depend on access to an earlier chat. Durable project context belongs in
this repository.

## Source-of-truth order

When instructions conflict, use this precedence:

1. The user's current request.
2. This `AGENTS.md`.
3. Accepted entries in `docs/DECISIONS.md`.
4. `DELIBERATION_MANIFEST.md`.
5. Explanatory material in `docs/PROJECT_CONTEXT.md`.

Flag meaningful conflicts instead of silently choosing a different product
direction.

## How to work on this project

Apply the project's own deliberative model while developing it:

1. Identify the next small, coherent milestone.
2. Explain what it changes, why it is useful, and how it will work.
3. Surface only meaningful alternatives and recommend one.
4. Ask for explicit approval before a consequential product, architecture, or
   behaviour decision.
5. Implement only the approved milestone.
6. Explain and verify the result before advancing.

Approval is required for decisions such as:

- Plugin and skill naming.
- The public activation or invocation contract.
- Checkpoint, approval, continuation, and exit semantics.
- Repository or plugin architecture.
- New dependencies, integrations, hooks, or marketplace changes.
- Behaviour that changes the balance between autonomy and user control.

Routine inspection, validation, and small documentation maintenance do not need
an artificial checkpoint when they merely support an already approved task.

Do not expose private chain-of-thought. Provide concise rationale, assumptions,
tradeoffs, and evidence sufficient for an informed user decision.

## Current scope

Product definition and interaction design are complete. The project is entering
cross-environment skill and adapter design. Do not treat the present
documentation layout as the final package structure.

The next milestone is an explicit architecture proposal for the shared core,
Codex adapter, Claude Code adapter, OpenCode adapter, distribution layout, and
validation fixtures. Do not create an installable plugin, marketplace entry,
environment adapter, production skill, or new dependency until that
architecture has been approved.

The intended first implementation is one shared Agent Skills-compatible core
that activates Deliberation across specification, implementation, debugging,
refactoring, and review, with thin adapters for Codex, Claude Code, and
OpenCode.

## Keeping context durable

After an accepted decision:

- Add or update an entry in `docs/DECISIONS.md`.
- Update `docs/CURRENT_STATE.md` if the phase, completed work, next milestone,
  or open questions changed.
- Update `DELIBERATION_MANIFEST.md` when the product philosophy or behavioural
  contract changed.
- Keep `README.md` accurate when the repository structure or usage changes.

Record conclusions and rationale, not conversation transcripts. Do not duplicate
the full manifest in other files.

## Quality bar

- Keep the core work mode independent of any one programming language,
  framework, or task type.
- Distinguish meaningful decisions from mechanical edits to avoid approval
  fatigue.
- Optimize for shared understanding and user agency as well as task quality.
- Make behaviour concrete enough to test with scenarios.
- Validate changed artifacts in proportion to their risk.
