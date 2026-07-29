# Explain model

The light checkpoint brief is not the Explain model. Use the complete Explain
model when the user asks to explain the current proposal or a named
alternative. It always uses both of these complementary views:

1. **Four questions:** **What?** What is being proposed; **Why at all?** what
   problem or decision makes it necessary; **How?** the essential mechanism;
   **Why this way?** the decisive tradeoff or rationale.
2. **Journey:** trace the relevant user, request, data, or execution journey
   from its initiating trigger through the affected components, state changes,
   and decisions to the observable result. Connect the stages to the proposed
   design or previewed code. For a small mechanical change, keep the journey
   correspondingly short rather than omitting it.

Explain is not a lecture. All four questions get their own clear answer, and
the journey covers the relevant normal path plus a material alternative or
failure path when needed for understanding. It stays grounded in the proposal
and its visible artefacts, then returns to the contextual checkpoint suggestions
rather than assuming approval.

Use the journey that fits the work: a user journey for user-visible behaviour,
a request journey across components or services, a data journey for
transformation or movement, or an execution flow for internal code and
algorithms.
