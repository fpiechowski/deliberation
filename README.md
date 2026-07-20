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
validation-fixture skeleton are implemented. Generated publication packages
are present under `plugins/`, `claude-plugins/`, and `opencode-bundles/`.

The assembler writes complete local previews under ignored `build/` output.
Repository publication surfaces are synchronized explicitly and validated
against fresh deterministic assembly. Marketplace entries and public release
metadata are not present yet.

Standalone Codex desktop activation evidence is recorded under
`validation/runs/`. The retained `0.1.0-dev.0` failure led to an activation
acknowledgement clarification; the `0.1.0-dev.1` rerun passes C-01 and A-01.
The standalone desktop checkpoint fixture also passes C-03, C-04, C-06, and
C-07.
The desktop lifetime-and-exit fixture passes C-02 and C-15 across two fresh
conversations.
The desktop response-intent and broad-approval fixture passes C-10 and C-11.
The staged desktop Drift and routine-execution fixture passes C-08 and C-09.
The real-file desktop execution-lifecycle fixture passes C-12, C-13, and C-14.
The desktop journey, durable-state, and resumed-conversation fixture passes
C-05, C-16, and A-04. Together, the retained desktop runs cover every core
scenario C-01–C-16 and complete the Specification row of cross-task-type
acceptance.
The real-file desktop Implementation fixture passes C-03, C-04, C-08, C-09,
and C-13 in an implementation context.
The seeded real-file desktop Debugging fixture passes C-06, C-08, C-09, and
C-14 in a debugging context.
The seeded real-file desktop Refactoring fixture passes C-04, C-06, C-07, and
C-13 in a refactoring context.
The seeded real-file desktop Review fixture passes C-04, C-05, C-10, and C-13
in a review context.

All five cross-task-type rows now pass in standalone Codex Desktop. Together
with direct C-01–C-16, A-01, and A-04 evidence, the current desktop-only
live-host validation scope is complete.

An additional natural-use fixture combines `$deliberation` and a short Polish
specification request in the first message. It passes autonomous roadmap and
bounded execution behavior, but is retained as a failure against C-01 and C-04:
the acknowledgement omits the explicit exit boundary and the compact
checkpoint omits response alternatives and a complete approval boundary.

Current live-host validation is intentionally limited to the Codex Desktop app.
CLI, IDE, Claude Code, OpenCode, and other clients are deferred until that scope
is explicitly reopened.

Run the implementation checks with:

```text
python tooling/deliberation.py check
```

Generate and validate local host artifacts with:

```text
python tooling/deliberation.py assemble
```

Regenerate the repository publication surfaces after changing the canonical
core, an adapter template, or `VERSION` with:

```text
python tooling/deliberation.py sync-publication
```

The next decision is whether to correct and rerun the failed Polish
single-message fixture. Other clients and distribution work remain deferred
pending a new explicit decision.

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
  assembler, publication synchronizer, and integrity validator.
