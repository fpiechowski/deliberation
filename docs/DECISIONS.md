# Decision Log

This file records durable product and architecture decisions. Add a new entry
when a meaningful decision is accepted; do not use it as a chronological work
log.

## D-001 — Use “Deliberation” as the working product name

- **Date:** 2026-07-19
- **Status:** Accepted

### Context

“In the loop” emphasizes awareness, “feedback-driven” makes feedback sound
mandatory, and “guided” is too ambiguous. The defining behaviour is conscious,
shared consideration before consequential action.

### Decision

Use **Deliberation** as the working name of the product and planned plugin.

### Consequences

Terminology should center proposals, reasoning, decisions, and approval. The
name can still be revisited before public release, but it is authoritative for
current design work.

## D-002 — Build a cross-cutting work mode

- **Date:** 2026-07-19
- **Status:** Accepted

### Context

The same interaction pattern is useful for specification, implementation,
debugging, refactoring, and review.

### Decision

Deliberation changes how the agent performs work rather than specializing in a
single task type. Begin with one primary skill that activates this mode.

### Consequences

The core behaviour must remain task- and technology-agnostic. Domain-specific
guidance may later be expressed as scenarios or extensions, but should not
fragment the initial model.

## D-003 — Treat user understanding as a first-class output

- **Date:** 2026-07-19
- **Status:** Accepted

### Context

Returning correct code is insufficient if the user receives a large,
hard-to-review result and cannot explain the decisions behind it.

### Decision

Optimize for solution quality, shared understanding, user agency, and knowledge
transfer while completing the task.

### Consequences

Proposals should explain intent and meaningful tradeoffs. Explanations should
remain concise and relevant so that knowledge transfer does not become a
lecture.

## D-004 — Require checkpoints for meaningful decisions, not every edit

- **Date:** 2026-07-19
- **Status:** Accepted

### Context

Approval is central to shared ownership, but asking before every mechanical edit
would produce bureaucracy and approval fatigue.

### Decision

Require explicit approval before consequential steps and allow routine,
low-risk mechanics within an approved step.

### Consequences

The skill contract must define useful checkpoint criteria and give the user a
clear expectation of what an approval authorizes.

## D-005 — Keep the product philosophy in a dedicated manifest

- **Date:** 2026-07-19
- **Status:** Accepted

### Context

The project needs a stable statement of purpose that is separate from
short-lived implementation state.

### Decision

Use `DELIBERATION_MANIFEST.md` as the source of truth for product vision and
high-level behavioural principles.

### Consequences

Session instructions and state files should point to the manifest rather than
duplicating it. Material changes to the philosophy must update the manifest and
the decision log together.

