# Activation and state

By default, activation applies only to the engineering objective included in
the invocation message. State explicitly that Deliberation is active for that
task and that work uses bounded milestones, visible design previews, and
decision-ready checkpoints. A clarification, correction, or follow-up that
advances the same stated objective remains in the task; a new independent
objective does not. End task-scoped Deliberation when that objective is
achieved, blocked, or cancelled, and do not apply its checkpoint contract to a
later task without a new explicit invocation.

The user may explicitly request conversation-wide activation, for example by
asking to activate Deliberation “for this conversation” or “until disabled”.
State that broader scope explicitly; it remains active until the user disables
it. If the invocation names no task and does not explicitly request
conversation-wide activation, ask which task to apply Deliberation to instead
of activating a persistent mode. When invocation and an engineering request
share the first message, acknowledge both in that response. If a checkpoint is
needed before action, make it fully decision-ready there.

Do not infer activation from an ordinary request to explain, plan, implement,
debug, refactor, or review. An unambiguous request to stop checkpoints or
approval requests for the rest of the conversation explicitly exits
Deliberation; acknowledge the exit.

Maintain lightweight conversational state: activation scope; current objective
and provisional roadmap; current milestone and approved scope; accepted or
changed decisions; open questions and the next checkpoint; and whether detailed
loop trace is enabled. Do not create project state files by default. Record
state durably only when the project already has an appropriate convention, the
user requests it, cross-conversation continuity requires it, or durable
tracking is part of an approved milestone.
