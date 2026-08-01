# Deliberation — Codex Working Agreement

This repository develops **Deliberation**, a cross-environment coding-agent
work mode that changes how an agent collaborates with a user. It is not a
task-specific coding capability.

## Start every session here

Read the documentation map below in order before proposing or making project
changes. These are the durable project sources; do not depend on an earlier
chat or on an agent's unstored working memory.

1. `docs/MANIFEST.md` — the most important document: product vision, context,
   behavioural contract, and collaboration philosophy.
2. `docs/ARCHITECTURE.md` — technical architecture, repository topology,
   adapter boundaries, packaging, and validation design.
3. `docs/ACCEPTANCE.md` — observable verification and testing
   contract, including critical failure cases.
4. `docs/TODO.md` — current next steps and open questions.
5. Inspect the working tree and preserve unrelated user changes.

## Documentation map

Keep the documents focused and use each one for its stated purpose:

- `docs/MANIFEST.md` is the source of truth for product intent and behavioural
  principles.
- `docs/ARCHITECTURE.md` is the source of truth for technical structure and
  cross-environment implementation constraints.
- `docs/ACCEPTANCE.md` is the source of truth for acceptance,
  verification, and test scenarios.
- `docs/TODO.md` contains only current next steps and open questions; it is
  not a historical work log.

When a change affects more than one concern, update every affected source in
the same change. Do not recreate separate decision-log, current-state, or
project-context files unless the user explicitly requests a new document.

## Source-of-truth order

When instructions conflict, use this precedence:

1. The user's current request.
2. This `AGENTS.md`.
3. `docs/MANIFEST.md` for product intent and behavioural principles.
4. `docs/ARCHITECTURE.md` for technical architecture.
5. `docs/ACCEPTANCE.md` for observable acceptance criteria.
6. `docs/TODO.md` for current priorities, which must not override the other
   sources.

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

Product definition, interaction design, the canonical core, adapter templates,
deterministic assembly, semantic-integrity checks, and publication packages are
implemented. The accepted technical architecture is documented in
`docs/ARCHITECTURE.md`; the next work is tracked in `docs/TODO.md`.

Codex Desktop is the supported live-host validation surface. Claude Code and
OpenCode remain experimental distribution adapters generated from the shared
core. Do not make new support claims or change the public activation,
checkpoint, lifetime, or adapter architecture without following the approval
rules below and updating the relevant documentation.

## Keeping context durable

After a meaningful accepted change or a change to the project's durable
contract:

- Update `docs/MANIFEST.md` when product philosophy or behavioural contract
  changes.
- Update `docs/ARCHITECTURE.md` when repository structure, adapters,
  dependencies, packaging, or validation architecture changes.
- Update `docs/ACCEPTANCE.md` when observable behaviour, acceptance,
  or test coverage changes.
- Update `docs/TODO.md` when next steps or open questions change.
- Keep `README.md` accurate when the repository structure or usage changes.

Record conclusions and rationale, not conversation transcripts. Keep each fact
in the narrowest authoritative document and do not duplicate the full manifest
in other files.

## Quality bar

- Keep the core work mode independent of any one programming language,
  framework, or task type.
- Distinguish meaningful decisions from mechanical edits to avoid approval
  fatigue.
- Optimize for shared understanding and user agency as well as task quality.
- Make behaviour concrete enough to test with scenarios.
- Validate changed artifacts in proportion to their risk.
