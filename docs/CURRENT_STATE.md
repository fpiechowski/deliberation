# Current State

**Last updated:** 2026-07-19

## Phase

Product definition and interaction design.

## Completed

- Selected **Deliberation** as the working product and plugin name.
- Defined the product as a cross-cutting work mode rather than a task-specific
  coding skill.
- Captured the product vision and high-level behavioural principles in
  `DELIBERATION_MANIFEST.md`.
- Distilled the original design conversation into durable project context and
  decisions.
- Prepared the repository for continuity across Codex sessions.

## Current implementation

There is no installable plugin or production skill yet. This is intentional:
the mode's behavioural contract should be defined before selecting its final
package structure.

## Recommended next milestone

Define the behavioural contract for the primary skill that activates
Deliberation mode.

That milestone should settle:

1. Skill name, description, and activation cues.
2. The mode's lifetime and explicit exit behaviour.
3. How a task is decomposed into milestones.
4. What constitutes a meaningful checkpoint.
5. The proposal format and amount of explanation.
6. What user language counts as approval, revision, rejection, or a question.
7. What work is authorized by one approval.
8. How progress and changed decisions are tracked.
9. How completion is reported.
10. Representative scenarios and failure cases used to test the behaviour.

## Open questions

- Should the skill itself be named `deliberation`, `deliberate`, or something
  that describes activation more directly?
- Does activation apply to one task, the current session, or until explicitly
  disabled?
- Should every session begin by agreeing on the entire milestone plan, or only
  the immediate next milestone?
- How should the agent proceed when the user gives broad approval such as “do
  the rest”?
- What precise guardrails prevent both excessive autonomy and approval fatigue?
- Which Codex surfaces and plugin distribution workflow should be supported
  first?

## Repository hygiene

The `.idea/` directory is currently untracked and is treated as user-owned IDE
state. Do not add, modify, or remove it unless the user explicitly asks.

