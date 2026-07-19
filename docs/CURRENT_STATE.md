# Current State

**Last updated:** 2026-07-19

## Phase

Cross-environment skill and adapter design — **architecture approved**.

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

## Current implementation

There is no installable plugin, production skill, adapter, marketplace entry,
or assembly tooling yet. The accepted architecture is documented in
`docs/ARCHITECTURE.md`; implementation has not started.

## Recommended next milestone

Propose a bounded implementation milestone that scaffolds:

1. The canonical `core/deliberation/SKILL.md`.
2. Host adapter templates without marketplace publication.
3. The standard-library assembler and semantic-integrity check.
4. The validation fixture skeleton.

The implementation scope and exact generated files require a separate
checkpoint before scaffolding begins.

## Open questions

No unresolved product-contract or architecture questions are currently known.

Public marketplace names, publisher metadata, release automation, and final
distribution entries remain later decisions. They are intentionally outside
the approved architecture milestone.

## Repository hygiene

The `.idea/` directory is currently untracked and is treated as user-owned IDE
state. Do not add, modify, or remove it unless the user explicitly asks.
