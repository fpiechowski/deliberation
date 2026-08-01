# Acceptance

## Purpose

This document is the acceptance contract for Deliberation and its explicit
standalone `explain` companion skill.

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

**Then** the agent acknowledges that Deliberation is active for the task in the
invocation prompt and states that it will use milestones and checkpoints until
that task is achieved, blocked, or cancelled.

**When** an invocation names no task and does not explicitly request
conversation-wide activation.

**Then** the agent asks which task to apply Deliberation to; it does not create
a persistent mode.

### C-02 — Task-scoped default and explicit persistent activation

**Given** Deliberation is active and the agent completes one task.

**When** the user starts a different task in the same conversation.

**Then** the task-scoped mode has ended and the agent does not apply its
checkpoint contract without another explicit invocation.

**Given** the user explicitly requested conversation-wide activation.

**When** the agent completes one task and the user starts another task in the
same conversation.

**Then** Deliberation remains active until the user explicitly disables it.

**When** the user starts a new conversation.

**Then** Deliberation starts inactive until explicitly invoked again.

### C-03 — Provisional roadmap and bounded approval

**Given** Deliberation is active and the user provides a new objective.

**When** the agent has understood the objective and gathered the information
needed to plan it.

**Then** before its first checkpoint or consequential execution, it presents a
provisional roadmap in the main substantive conversation content. The roadmap
shows the currently foreseeable scope as ordered milestones, identifies the
milestone being developed now, identifies known later decisions or
uncertainties, and develops only that current milestone in decision-ready
detail.

**And** it states that approval covers the current milestone rather than the
full roadmap unless the user explicitly grants broader authorization.

For a simple task, the roadmap is one concise milestone rather than artificial
stages.

Before a checkpoint for a later milestone, the agent shows the current roadmap.
If Choice, Consequence, or Drift changes it, it shows the revision and its
effect before that checkpoint. It does not mechanically repeat the roadmap
while the same checkpoint remains open for discussion.

### C-04 — Complete checkpoint before execution

**Given** the next milestone contains a consequential action.

**When** the agent reaches the checkpoint.

**Then** it:

1. States the decision needed.
2. Proposes a bounded milestone.
3. Provides a light milestone brief and an initial solution proposal.
4. Presents only materially different alternatives and tradeoffs.
5. Shows representative code or equivalent design artefacts that reveal the
   proposed architecture, design, and style before approval.
6. Presents visible, contextual next-message suggestions, including a clearly
   named acceptance action for the current proposal.
7. Reaches a shared decision.
8. States the approval scope.
9. Waits for explicit approval.

**And** no execution begins before the explanation, discussion, decision, and
approval are complete.

### C-05 — Explain model on explicit request

**Given** the agent prepares or explains a checkpoint for a proposed or
implemented milestone.

**When** the user selects an explanation suggestion or asks for an explanation
in their own words.

**Then** the agent explains What, Why at all, How, and Why this way, plus an
appropriate user, request, data, or execution journey from trigger to
observable result mapped to the design or code. It remains in the checkpoint
and returns to contextual suggestions. For a small static or mechanical change, the
journey remains short and concrete rather than being omitted.

### C-19 — Standalone Explain

**Given** the explicit `explain` skill is installed and Deliberation is
inactive.

**When** the user invokes `explain` through the host's explicit mechanism with
a named technical topic.

**Then** it answers What, Why at all, How, and Why this way. For dynamic
subjects, it adds the appropriate concise user, request, data, or execution
journey from trigger to observable result, including a material failure or
alternative path only when useful.

**And** it remains a standalone explanation: it does not activate
Deliberation, open a checkpoint, request approval, create state, or modify
files unless separately asked.

### C-18 — Structured checkpoint controls and inspectable previews

**Given** a consequential checkpoint for a proposed milestone.

**Then** the user sees contextual next-message suggestions and an inspectable
pre-approval preview: representative key code for implementation, refactoring,
or debugging; or an equivalent contract, schema, pseudocode, flow, example, or
finding for specification or review. The suggestions are optional shortcuts;
free-text responses are interpreted by intent.

**When** the user requests changes or explores alternatives.

**Then** the agent revises the proposal or keeps the checkpoint open and
compares the proposed approach with two to four feasible, materially different
approaches. For alternatives it gives each a short explanation and assessment,
includes the original proposal, shows a compact advantages/disadvantages table
using relevant decision criteria, and marks the current recommendation.

**Then** the alternative view suggests: explain a named alternative, choose a
named alternative as the new proposal, find more alternatives, or accept the
named current recommendation. Choosing is not approval; acceptance authorizes
only the named recommendation and stated scope.

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

**And** task-scoped Deliberation ends. It remains active for later tasks only
when the user explicitly requested conversation-wide activation.

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

### C-17 — Observable loop and detailed trace

**Given** Deliberation is active for a task.

**When** the agent enters a main boundary of understanding and gathering,
planning, checkpoint, approved execution, or result walkthrough with
verification and roadmap update.

**Then** it provides a concise, localized phase signal without forcing the
substantive response into a fixed template.

**And** the Planning signal or a detailed-trace `[Plan]` entry does not replace
the roadmap required by C-03; the roadmap remains visible in the main
substantive content rather than only in trace, commentary, or another progress
surface.

**When** the user asks in natural language to show the detailed loop or stage
trace.

**Then** the agent preserves that preference for the conversation and exposes
each actual canonical transition: Understand, Gather, Plan, the applicable
Checkpoint stages, Execute, Walk through and verify, and Update plan before
Repeat or completion.

**And** the trace labels do not substitute for the associated behaviour.

**And** a checkpoint that is not required is identified as such rather than
simulated, while questions, revisions, rejections, and approvals show their
actual checkpoint transitions.

**When** the user asks to hide the trace.

**Then** the detailed trace stops but Deliberation remains active. An explicit
exit from Deliberation disables both.

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

**Then** the adapter preserves the active mode, its scope, accepted decisions,
current roadmap, approval scope, and any enabled detailed-loop-trace preference.

If a host cannot preserve this reliably, record the scenario as **Blocked** and
return to architecture deliberation rather than weakening the task-scoped
activation contract.

### A-05 — Cross-environment semantic parity

**Given** equivalent prompts and repository context in Codex, Claude Code, and
OpenCode.

**When** the core scenarios are evaluated.

**Then** differences are limited to invocation syntax, metadata, package
layout, installation, progress presentation, and required continuity mechanics.

**And** milestone, checkpoint, approval, exit, and completion semantics remain
equivalent.

### A-06 — Standalone Explain invocation

**Applies to:** Codex, Claude Code, and OpenCode.

**Given** the generated package is installed.

**When** the user invokes `$explain` in Codex, the standalone or namespaced
`/explain` skill in Claude Code, or `/explain` in OpenCode.

**Then** the equivalent C-19 contract loads with model-driven invocation
disabled where the host supports that control.

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
| F-06 | Explanation becomes a lecture, fails to provide the requested Explain model, or makes a small change's journey needlessly elaborate. |
| F-07 | Broad approval leaks into undisclosed decisions or later tasks. |
| F-08 | An accepted decision changes silently. |
| F-09 | The agent imposes Deliberation state files on an unrelated repository. |
| F-10 | The agent claims completion despite a known blocker or missing objective. |
| F-11 | The mode remains active after explicit exit. |
| F-12 | An ordinary task activates Deliberation implicitly or task-scoped Deliberation leaks into a later task. |
| F-13 | An adapter changes the shared product semantics. |
| F-14 | Long execution proceeds without useful progress visibility. |
| F-15 | The agent uses phase labels to falsely imply work or authorization, or forces every response into a process template. |

## Contract Traceability

| Contract area | Scenario coverage |
|---|---|
| Product name | C-01, A-01–A-03 |
| Cross-cutting work mode | Cross-Task-Type Coverage |
| User understanding as an output | C-04, C-05, C-13, C-14 |
| Meaningful checkpoints | C-06–C-09 |
| Canonical manifest | Documentation consistency review |
| Former conversation-wide lifetime | Historical evidence only |
| Task-scoped default and explicit persistent activation | C-01, C-02, C-14, C-15, A-04 |
| Journey-based explanation | C-05, C-13 |
| Milestones and checkpoints | C-03, C-04, C-13 |
| Provisional roadmap | C-03, C-11 |
| Choice, Consequence, and Drift | C-06–C-09 |
| Checkpoint communication | C-04, C-10, C-11, C-15 |
| Conversational state and completion | C-12–C-16 |
| Cross-environment adapters | A-01–A-05 |
| Acceptance contract and documentation readiness | Repository Acceptance Criteria |
| Observable loop and detailed trace | C-17, A-04 |
| Visible roadmap before checkpoint | C-03, C-04, C-08, C-17 |
| Journey consideration at checkpoints | C-05 |
| Modular checkpoint Explain and preview contract | C-04, C-05, C-18, A-01–A-05 |
| Standalone Explain companion skill | C-19, A-06 |

## Repository Acceptance Criteria

The current repository is ready for supported release work when:

- Every applicable core and supported-environment scenario has validation
  evidence, with failed or blocked scenarios reported honestly.
- No unresolved product-contract or architecture question is hidden; open
  questions are recorded in `docs/TODO.md`.
- `AGENTS.md`, `README.md`, and the canonical documents under `docs/` agree on
  the current structure, behaviour, support status, and next steps.
- The shared core, adapters, fixtures, and committed publication surfaces pass
  deterministic structural and semantic-integrity validation.
- Experimental adapter boundaries and supported-host claims are stated
  consistently across the repository.

Passing these documentation criteria establishes documentation readiness;
passing the applicable runtime scenarios is the acceptance condition for a
supported release.
