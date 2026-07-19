# Current State

**Last updated:** 2026-07-19

## Phase

Product definition and interaction design — **complete**.

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

## Current implementation

There is no installable plugin or production skill yet. This is intentional:
the completed behavioural contract now provides the basis for selecting and
validating the package structure in the next phase.

## Recommended next milestone

Design the repository and package architecture for:

1. One shared Agent Skills-compatible behavioural core.
2. A Codex adapter and plugin package.
3. A Claude Code adapter and plugin package.
4. An OpenCode command and skill distribution bundle.
5. Shared scenario fixtures and environment-specific validation.

The architecture must be proposed and explicitly approved before production
scaffolding begins.

## Open questions

No unresolved product-contract questions are currently known.

The next phase must decide package layout, how adapters consume the shared core,
versioning, installation workflows, and how transcript-based scenarios become
repeatable environment-specific validation.

## Repository hygiene

The `.idea/` directory is currently untracked and is treated as user-owned IDE
state. Do not add, modify, or remove it unless the user explicitly asks.
