# Deliberation

Deliberation is a planned Codex plugin that turns an autonomous agent workflow
into an incremental, consultative collaboration.

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

Knowledge transfer and shared understanding are first-class outcomes alongside
the quality of the completed work.

## Project status

The project is currently in product-definition and design. No installable
plugin or skill has been scaffolded yet.

The next design milestone is to define the exact behavioural contract of the
single skill that activates and maintains Deliberation mode.

## Repository guide

- [`AGENTS.md`](AGENTS.md) — instructions for Codex sessions working on this
  repository.
- [`DELIBERATION_MANIFEST.md`](DELIBERATION_MANIFEST.md) — product vision and
  behavioural principles.
- [`docs/PROJECT_CONTEXT.md`](docs/PROJECT_CONTEXT.md) — the reasoning and
  background that led to the current direction.
- [`docs/DECISIONS.md`](docs/DECISIONS.md) — durable decision log.
- [`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md) — current phase, open
  questions, and the recommended next milestone.

