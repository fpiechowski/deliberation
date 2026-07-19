# Current State

**Last updated:** 2026-07-19

## Phase

Cross-environment implementation — **canonical core and assembly scaffold
complete**.

## Completed

- Selected **Deliberation** as the working product and plugin name.
- Defined the product as a cross-cutting work mode rather than a task-specific
  coding skill.
- Captured the product vision and high-level behavioural principles in
  `DELIBERATION_MANIFEST.md`.
- Distilled the original design conversation into durable project context and
  decisions.
- Prepared the repository for continuity across Codex sessions.
- Defined the mode lifetime: activation applies to the current conversation
  until the user explicitly disables it.
- Added journey-based explanation as a conditional technique for explaining
  dynamic code, design, and system behaviour.
- Defined milestones as bounded units of verifiable progress and checkpoints as
  decision-ready deliberation that ends with approval.
- Distinguished explanation before approval from the walkthrough and
  verification of the implemented result.
- Defined milestone planning as a provisional roadmap with detailed
  deliberation and default approval limited to the next milestone.
- Defined checkpoint triggers through Choice, Consequence, and Drift tests, and
  required related decisions to be grouped to limit approval fatigue.
- Defined the semantic content of checkpoints, intent-based response handling,
  bounded broad approval, and explicit mode exit when checkpoints are waived.
- Defined lightweight conversational state, conditional durable tracking,
  progress updates, result walkthroughs, and honest completion reporting.
- Selected `deliberation` as the primary skill name with explicit activation.
- Expanded the product to one shared behavioural core with distribution
  adapters for Codex, Claude Code, and OpenCode.
- Defined platform-neutral, cross-task-type, and adapter-specific behavioural
  scenarios with critical failure cases and decision traceability.
- Closed the product-definition and interaction-design phase.
- Approved the cross-environment package architecture.
- Selected one canonical Agent Skills-compatible core with deterministically
  generated Codex, Claude Code, and OpenCode adapters.
- Defined self-contained, committed publication packages for Git-hosted
  marketplaces and untracked temporary build output.
- Defined shared SemVer, structural validation, semantic-integrity checks, and
  transcript-based cross-environment fixtures.
- Implemented the canonical Agent Skills-compatible core at
  `core/deliberation/SKILL.md`.
- Added Codex, Claude Code, and OpenCode adapter templates.
- Added a deterministic Python 3 standard-library assembler and integrity
  validator.
- Added fixture metadata schema plus one core and three activation fixture
  skeletons.
- Established `0.1.0-dev.0` as the shared development version.

## Current implementation

The canonical core, adapter templates, and repository-local assembly tooling
are implemented. `python tooling/deliberation.py assemble` generates and
validates standalone and publication previews under ignored `build/` output.
`python tooling/deliberation.py check` independently assembles twice, proves
deterministic output, validates host structure and explicit-only activation,
and compares every normalized runtime payload with the canonical core.

Generated publication packages are not yet committed under `plugins/`,
`claude-plugins/`, or `opencode-bundles/`. There are no marketplace catalogs,
public publisher metadata, release automation, or recorded host transcripts.

## Recommended next milestone

Promote the reviewed publication previews to the committed `plugins/`,
`claude-plugins/`, and `opencode-bundles/` surfaces, then extend `check` so it
fails when committed generated artifacts differ from fresh assembly.

This milestone should still exclude marketplace catalogs, public publisher
metadata, release automation, and live host installation. Its exact committed
file set requires a separate checkpoint.

## Open questions

No unresolved product-contract or architecture questions are currently known.

Public marketplace names, publisher metadata, release automation, final
distribution entries, and live validation logistics remain later decisions.

## Repository hygiene

The `.idea/` directory is currently untracked and is treated as user-owned IDE
state. Do not add, modify, or remove it unless the user explicitly asks.
