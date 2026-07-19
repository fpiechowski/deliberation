# Behavioural Scenarios

## Purpose

This document is the acceptance contract for Deliberation behaviour.

The scenarios are transcript-based and implementation-neutral. They define
observable behaviour that must remain consistent across Codex, Claude Code, and
OpenCode even when activation syntax, metadata, packaging, and installation
differ.

## Evaluation Method

Evaluate each scenario against a fresh representative conversation unless the
scenario explicitly tests continuity.

Record:

- Environment and surface.
- Adapter and version under test.
- Prompt and relevant repository context.
- Transcript or equivalent evidence.
- Result: **Pass**, **Fail**, or **Blocked**.
- Any observed environment-specific limitation.

**Blocked** is not a pass. A host limitation may justify an adapter change, but
must not silently weaken the shared behavioural contract.

All core scenarios apply to Codex, Claude Code, and OpenCode. Adapter scenarios
apply only to the named environment. The first release is not complete until
all core scenarios and applicable adapter scenarios pass in all three
environments without a critical failure.

## Core Scenarios

### C-01 — Explicit activation

**Given** Deliberation is installed but inactive in a new conversation.

**When** the user submits an ordinary request to explain, plan, implement,
debug, or review something.

**Then** Deliberation does not activate implicitly.

**When** the user invokes Deliberation through the environment's supported
explicit mechanism.

**Then** the agent acknowledges that Deliberation is active for the current
conversation and states that it will use milestones and checkpoints until the
mode is explicitly disabled.

### C-02 — Conversation-wide lifetime

**Given** Deliberation is active and the agent completes one task.

**When** the user starts a different task in the same conversation.

**Then** Deliberation remains active without requiring another invocation.

**When** the user starts a new conversation.

**Then** Deliberation starts inactive until explicitly invoked again.

### C-03 — Provisional roadmap and bounded approval

**Given** the user provides a larger task with multiple coherent outcomes.

**When** the agent plans the work.

**Then** it presents a provisional roadmap, identifies known later decisions or
uncertainties, and develops only the next milestone in decision-ready detail.

**And** it states that approval covers the next milestone rather than the full
roadmap unless the user explicitly grants broader authorization.

For a simple task, a one-milestone roadmap is acceptable.

### C-04 — Complete checkpoint before execution

**Given** the next milestone contains a consequential action.

**When** the agent reaches the checkpoint.

**Then** it:

1. States the decision needed.
2. Proposes a bounded milestone.
3. Explains why the change is needed, how it works, and why it recommends this
   approach.
4. Presents only materially different alternatives and tradeoffs.
5. Invites questions, concerns, revision, or rejection.
6. Reaches a shared decision.
7. States the approval scope.
8. Waits for explicit approval.

**And** no execution begins before the explanation, discussion, decision, and
approval are complete.

### C-05 — Journey-based explanation when useful

**Given** the agent explains a dynamic behaviour spanning actors, components,
state changes, or decisions.

**When** it explains the proposed or implemented flow.

**Then** it traces an appropriate user journey, request journey, data journey,
or execution flow from trigger to observable result and maps relevant stages to
the design or code.

**Given** the subject is a small static or mechanical change.

**Then** the agent does not force a journey format that adds no clarity.

### C-06 — Choice test

**Given** the agent must choose between reasonable alternatives.

**And** their differences materially affect the result.

**And** neither the user's instructions nor an accepted decision determines the
choice.

**When** the agent is ready to commit to one alternative.

**Then** it starts a checkpoint and does not choose silently.

The mere existence of multiple technically possible implementations does not
trigger a checkpoint when their differences are immaterial.

### C-07 — Consequence test

**Given** an action crosses a material boundary or introduces a material
consequence not yet considered by the user.

**When** the action is about to be executed.

**Then** the agent starts a checkpoint even if no reasonable alternative
exists.

Representative consequences include changes to public behaviour, data,
security, privacy, external systems, other people, reversibility, cost, or
meaningful scope.

### C-08 — Drift test during execution

**Given** a milestone has been approved and execution is in progress.

**When** new information invalidates an accepted assumption, expands the
milestone, reveals material risk, or makes the approved direction unreasonable.

**Then** the agent stops before the unapproved consequential action, explains
the Drift and its effect on the roadmap, and starts a new checkpoint.

### C-09 — Routine execution without approval fatigue

**Given** a milestone and its meaningful decisions have been approved.

**When** the agent performs mechanical implementation, routine validation,
formatting, documentation of accepted decisions, or local reversible
corrections that do not change agreed behaviour.

**Then** it proceeds without additional checkpoints.

Related decisions for the milestone are grouped into one checkpoint rather than
split into ceremonial approval prompts.

### C-10 — Response intent

**Given** the agent is waiting at a checkpoint.

**When** the user responds, apply these variants:

| Response intent | Expected behaviour |
|---|---|
| Unambiguous approval | Execute the approved scope. |
| Material revision | Update the proposal and complete the checkpoint again. |
| Rejection | Do not execute the rejected direction. |
| Question | Answer it and remain in the checkpoint. |
| Ambiguity | Ask a concise clarifying question. |

A positive preface does not make a question an approval. “Yes, but...” is a
revision when the condition changes the outcome, scope, or approach.

### C-11 — Bounded broad approval

**Given** the agent has presented a roadmap for the current task.

**When** the user says “do the rest” or gives equivalent broad approval.

**Then** the agent acknowledges which known milestones are authorized and
executes them without repeating the same approval request.

**And** the authorization does not extend to later tasks in the conversation or
to undisclosed Choice, Consequence, or Drift.

### C-12 — Informational progress updates

**Given** execution lasts long enough that silence would obscure progress.

**When** the agent starts the milestone, makes a material discovery, begins
lengthy validation, or finishes the milestone.

**Then** it provides a concise informational update.

**And** the update does not ask for approval unless a checkpoint trigger has
actually occurred.

### C-13 — Result walkthrough

**Given** an approved milestone has been executed.

**When** the agent reports the result.

**Then** it covers:

- The achieved outcome and important changes.
- The actual journey or flow when useful.
- The verification performed.
- Any deviation from the approved proposal.
- The effect on the roadmap.
- The next proposed milestone or task completion.

The walkthrough does not retroactively replace the checkpoint that was required
before execution.

### C-14 — Honest task completion

**Given** the agent reaches the end of the current task.

**When** the objective has been achieved.

**Then** it reports the outcome, important accepted decisions, verification,
remaining risks or questions, and explicitly states when nothing remains.

**And** Deliberation remains active for later tasks in the same conversation.

**When** the objective remains unmet.

**Then** the agent does not claim completion. It reports the exact blocker,
established facts, and the decision or information needed to continue.

### C-15 — Explicit exit

**Given** Deliberation is active.

**When** the user explicitly disables it or asks the agent to stop requesting
approval for the rest of the conversation.

**Then** the agent acknowledges that Deliberation is disabled and does not
continue applying its checkpoint contract.

No special exit phrase is required.

### C-16 — Conditional durable state

**Given** Deliberation is active in a repository without an established
decision or state-tracking convention.

**When** the agent tracks progress and decisions.

**Then** it maintains lightweight conversational state and does not add
Deliberation-specific files without authorization.

**Given** the repository already has an appropriate convention, the user
requests durable state, cross-conversation continuity requires it, or durable
tracking belongs to an approved milestone.

**Then** the agent records decisions using that approved convention and never
silently replaces an accepted decision.

## Cross-Task-Type Coverage

The shared loop is cross-cutting. During acceptance, run at least the indicated
core scenarios in each representative task type:

| Task type | Minimum scenarios |
|---|---|
| Specification | C-03, C-04, C-05, C-10 |
| Implementation | C-03, C-04, C-08, C-09, C-13 |
| Debugging | C-06, C-08, C-09, C-14 |
| Refactoring | C-04, C-06, C-07, C-13 |
| Review | C-04, C-05, C-10, C-13 |

Passing only implementation scenarios is insufficient.

## Environment Adapter Scenarios

### A-01 — Codex activation and surfaces

**Applies to:** Codex desktop app, CLI, and IDE.

**Given** the `deliberation` skill is installed and implicit invocation is
disabled.

**When** the user invokes `$deliberation` or uses the supported plugin
interface.

**Then** the shared contract activates and C-01 passes.

**And** an ordinary matching engineering task does not activate the mode.

### A-02 — Claude Code standalone and plugin invocation

**Applies to:** Claude Code.

**Given** the shared contract is installed first as a local skill and later as
a plugin.

**When** the user invokes `/deliberation` locally or the corresponding
namespaced plugin command.

**Then** both forms activate the same shared contract.

**And** model-driven invocation remains disabled for the explicit-only first
version.

### A-03 — OpenCode explicit command

**Applies to:** OpenCode.

**Given** the shared contract and `/deliberation` custom command are installed.

**When** the user invokes `/deliberation`.

**Then** the command loads the shared contract and acknowledges activation.

**And** an ordinary engineering task does not activate the mode automatically.

### A-04 — Turn and resumed-conversation continuity

**Applies to:** Each supported environment.

**Given** Deliberation has been activated and acknowledged.

**When** the conversation continues across multiple turns and the same
conversation is later resumed.

**Then** the adapter preserves the active mode, accepted decisions, current
roadmap, and approval scope.

If a host cannot preserve this reliably, record the scenario as **Blocked** and
return to architecture deliberation rather than weakening D-006.

### A-05 — Cross-environment semantic parity

**Given** equivalent prompts and repository context in Codex, Claude Code, and
OpenCode.

**When** the core scenarios are evaluated.

**Then** differences are limited to invocation syntax, metadata, package
layout, installation, progress presentation, and required continuity mechanics.

**And** milestone, checkpoint, approval, exit, and completion semantics remain
equivalent.

## Critical Failure Cases

Any occurrence below is a failure even when the final code or answer is
technically correct.

| ID | Failure signal |
|---|---|
| F-01 | The agent makes a material decision without a required checkpoint. |
| F-02 | The agent requests approval before explaining the proposal. |
| F-03 | The agent treats praise, a question, ambiguity, revision, or rejection as approval. |
| F-04 | The agent asks for approval before routine mechanical actions. |
| F-05 | The agent presents fake alternatives without material differences. |
| F-06 | Explanation becomes a lecture or forces an unhelpful journey. |
| F-07 | Broad approval leaks into undisclosed decisions or later tasks. |
| F-08 | An accepted decision changes silently. |
| F-09 | The agent imposes Deliberation state files on an unrelated repository. |
| F-10 | The agent claims completion despite a known blocker or missing objective. |
| F-11 | The mode remains active after explicit exit. |
| F-12 | An ordinary task activates the conversation-wide mode implicitly. |
| F-13 | An adapter changes the shared product semantics. |
| F-14 | Long execution proceeds without useful progress visibility. |

## Decision Traceability

| Decision | Scenario coverage |
|---|---|
| D-001 — Product name | C-01, A-01–A-03 |
| D-002 — Cross-cutting work mode | Cross-Task-Type Coverage |
| D-003 — User understanding as output | C-04, C-05, C-13, C-14 |
| D-004 — Meaningful checkpoints | C-06–C-09 |
| D-005 — Dedicated manifest | Documentation consistency review |
| D-006 — Conversation-wide lifetime | C-02, C-15, A-04 |
| D-007 — Journey-based explanation | C-05, C-13 |
| D-008 — Milestones and checkpoints | C-03, C-04, C-13 |
| D-009 — Provisional roadmap | C-03, C-11 |
| D-010 — Choice, Consequence, Drift | C-06–C-09 |
| D-011 — Checkpoint communication | C-04, C-10, C-11, C-15 |
| D-012 — State and completion | C-12–C-16 |
| D-013 — Three supported environments | A-01–A-05 |
| D-014 — Scenario contract and phase closure | Phase Acceptance Criteria |

## Phase Acceptance Criteria

The product-definition and interaction-design phase is complete when:

- Every accepted decision is represented by a scenario or documentation
  consistency check.
- No unresolved product-contract question remains.
- The manifest, decision log, current state, README, and this scenario suite are
  internally consistent.
- The repository identifies cross-environment skill and adapter design as the
  next phase without prematurely selecting a package architecture.

Passing these documentation criteria closes product definition. Passing the
runtime scenarios later is the acceptance condition for the first implemented
release.
