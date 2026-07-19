# Project Context

## Origin

The project began with dissatisfaction with the default interaction pattern of
coding agents:

1. The user gives the agent a task.
2. The agent works autonomously for a long time.
3. The agent returns a large result or diff.
4. The user must understand and review many hidden decisions after the fact.

Deliberation explores a different interaction model. The user participates in
important decisions while the work is being shaped, and learns the resulting
solution throughout the conversation.

## Intended interaction model

The recurring pattern is:

```text
understand → plan → propose → explain → consider alternatives
           → decide → approve → execute one step → repeat
```

This is meant to apply to several kinds of work:

- **Specification:** discover requirements, expose ambiguities, elicit
  decisions, and build the specification incrementally.
- **Implementation:** introduce one coherent part at a time, explain its design
  and tradeoffs, and avoid surprising the user with a large final diff.
- **Review:** walk through changes with the user, explain their intent and
  consequences, identify issues, and formulate useful review comments.
- **Other engineering work:** use the same interaction model for debugging,
  refactoring, research, and planning.

## Core product qualities

The design combines several qualities that no single common label fully covers:

- **Proposal:** the agent surfaces a direction before consequential action.
- **Explanation:** the user learns what is proposed, how it works, and why.
- **Deliberation:** reasonable options and tradeoffs are considered together.
- **Decision:** the agent actively elicits choices rather than merely reporting
  progress.
- **Approval:** consequential steps wait for explicit user consent.
- **Incremental execution:** work advances through understandable milestones.
- **Knowledge transfer:** user understanding is an output of the work.

## Naming rationale

Several candidate terms were considered:

- **In the loop** communicates keeping someone informed, but does not
  necessarily imply shared decisions.
- **Feedback-driven** overstates feedback as the engine of the process. The user
  may simply approve a sound proposal; feedback is possible but not mandatory.
- **Guided** is approachable but ambiguous about who guides whom and says little
  about decision rights.
- **Collaborative** is directionally correct but too broad.
- **Consultative** and **facilitative** capture important aspects of the agent's
  role but not the complete model.
- **Socratic** emphasizes learning through questions, while this agent must also
  propose, explain, implement, and review.
- **Deliberative** best captures conscious consideration and shared decisions
  before action.

The working product and plugin name is therefore **Deliberation**.

## Product boundary

Deliberation changes **how the agent works**, not **what it works on**.

It should not become separate modes for specification, development, and review
unless later evidence shows that a single cross-cutting behaviour cannot serve
them well. The current direction is one primary skill that activates the work
mode.

The design must also avoid turning collaboration into bureaucracy. Mechanical,
low-risk edits should not generate constant approval prompts. A central design
challenge is defining a predictable boundary between a meaningful decision and
a routine execution detail.

## What the original conversation did not settle

The list below records the historical gap at the end of the original
conversation. It is not the current open-question list. Subsequent resolutions
are authoritative in `docs/DECISIONS.md` and summarized in
`docs/CURRENT_STATE.md`.

- The exact name and invocation phrase of the activating skill.
- Whether the work mode persists for a whole session, one task, or until an
  explicit exit command.
- The exact format used to present milestones and proposals.
- How approval is recognized and how revised proposals are handled.
- How checkpoints are selected without creating approval fatigue.
- Whether state is represented only conversationally or with project artifacts.
- How the skill should interact with stronger system or repository
  instructions.
- The concrete Codex plugin layout, packaging, tests, and distribution method.
