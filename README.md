# Deliberation

Deliberation is a cross-environment coding-agent work mode that turns
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
architecture are complete. The canonical skill core, host adapter templates,
deterministic standard-library assembler, semantic-integrity checks, and
validation-fixture skeleton are implemented.

The assembler currently writes complete local previews under ignored `build/`
output. No generated publication package, marketplace entry, or public release
metadata is committed yet.

Run the implementation checks with:

```text
python tooling/deliberation.py check
```

Generate and validate local host artifacts with:

```text
python tooling/deliberation.py assemble
```

The next milestone is to promote the reviewed generated packages to the
committed publication surfaces and add a stale-generation check. It requires a
separate checkpoint.

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
- [`core/deliberation/SKILL.md`](core/deliberation/SKILL.md) — canonical
  behavioural source for all environments.
- [`tooling/deliberation.py`](tooling/deliberation.py) — deterministic
  assembler and integrity validator.
