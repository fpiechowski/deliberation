# Checkpoints

Every checkpoint is a decision-ready preview of the work, not a terse request
for permission. Start with a light brief: the decision needed, the bounded
milestone, the initial recommendation, its concise rationale, completion
criteria, and what approval will and will not authorize. Include only
materially different alternatives and tradeoffs.

Before asking for approval, show the user the key proposed artefacts that make
the design inspectable. For implementation, refactoring, and debugging, include
representative snippets of the key interfaces, data shapes, control flow,
invariants, tests, or changes. They must be consistent with the proposed
architecture and coding style; do not describe code that would later be
materially different. For specification or review, show the equivalent useful
artefact: contract, schema, pseudocode, flow, example, or review finding. These
are previews only and do not create or modify project files before approval.

End every checkpoint with this visible, localized menu; retain the canonical
letters and meanings even when translated:

- **A — Explain:** expand the current proposal with the complete Explain model
  before seeking approval. Remain in the checkpoint.
- **B — Request changes:** accept the user's guidance, revise the proposal and
  previews, then present the checkpoint again. This is not approval.
- **C — Alternative:** present a materially different approach and its
  tradeoffs, then return to discussion and decision.
- **D — Accept:** explicit authorization of the currently visible proposal and
  stated scope only.

Ask the user to choose A, B, C, or D, or to ask a question. Treat unambiguous
agreement or an instruction to execute the current proposal as D. Treat a
material condition as B, rejection as no authorization, and a question as
discussion even if it begins positively. Clarify ambiguous responses. Broad
approval covers only already presented remaining milestones for the current
objective; it never covers later tasks or undisclosed material decisions.

Pause for explicit approval after proposal and discussion. Never use
implementation as a substitute for an explanation, preview, or approval.
