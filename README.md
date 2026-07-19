# Deliberation

Deliberation is a planned cross-environment coding-agent work mode that turns
an autonomous workflow into an incremental, consultative collaboration.

Instead of completing a large task in one opaque run, the agent decomposes it
into meaningful steps. At each consequential checkpoint it proposes a
direction, explains the reasoning and realistic alternatives, reaches a
decision with the user, waits for approval, and then executes the approved
step.

The mode is intended to work across:

- Specification and planning.
- Implementation and refactoring.
- Debugging.
- Code and pull-request review.

The first version targets Codex, Claude Code, and OpenCode through one shared
Agent Skills-compatible behavioural core and thin environment-specific
adapters.

Knowledge transfer and shared understanding are first-class outcomes alongside
the quality of the completed work.

## Project status

Product definition, interaction design, and the cross-environment package
architecture are complete. No installable plugin, adapter, marketplace entry,
or production skill has been scaffolded yet.

The next milestone is a bounded implementation proposal for the canonical skill
core, adapter templates, deterministic assembly, and validation-fixture
skeleton. Production scaffolding begins only after that milestone is explicitly
approved.

## Repository guide

- [`AGENTS.md`](AGENTS.md) — instructions for Codex sessions working on this
  repository.
- [`DELIBERATION_MANIFEST.md`](DELIBERATION_MANIFEST.md) — product vision and
  behavioural principles.
- [`docs/PROJECT_CONTEXT.md`](docs/PROJECT_CONTEXT.md) — the reasoning and
  background that led to the current direction.
- [`docs/DECISIONS.md`](docs/DECISIONS.md) — durable decision log.
- [`docs/BEHAVIORAL_SCENARIOS.md`](docs/BEHAVIORAL_SCENARIOS.md) — observable
  acceptance scenarios and critical failure cases.
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — accepted shared-core,
  adapter, distribution, versioning, and validation architecture.
- [`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md) — current phase, open
  questions, and the recommended next milestone.
