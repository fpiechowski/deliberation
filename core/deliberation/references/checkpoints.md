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

End every checkpoint with a visible, localized heading equivalent to
**Suggested next step**, followed by contextual suggestions for the next user
message. Always state: **You can choose a suggestion or reply in your own
words.** Localize that invitation with the heading. The suggestions are a
convenience, not a rigid protocol: the user may ask a question, name an
alternative, or give another instruction. Interpret every response by intent.

For an ordinary proposal, normally suggest:

- **A — Explain the current proposal:** use the complete Explain model and
  remain in the checkpoint.
- **B — Request a change or propose another next step:** accept the user's
  guidance or other in-scope instruction, revise the proposal and previews as
  needed, then present the checkpoint again. This is not approval.
- **C — Explore alternatives:** read and follow
  [Alternative comparison](alternative.md). It is not approval.
- **D — Accept the current proposal:** explicit authorization of the named,
  currently visible proposal and stated scope only.

Adapt the suggestions to the current conversational view. In particular, the
alternative-comparison view uses the choices defined in `alternative.md` rather
than pretending that every letter has the same meaning in every context. State
the effect of each suggestion plainly.

Only a suggestion that explicitly says **Accept** can authorize work, and it
must name the proposal and scope it accepts. Unambiguous agreement or an
instruction to execute the named current proposal has the same effect. A
material condition is a revision; rejection is no authorization; and a question
remains discussion even if it begins positively. Clarify ambiguity. Broad
approval covers only already presented remaining milestones for the current
objective; it never covers later tasks or undisclosed material decisions.

Pause for explicit approval after proposal and discussion. Never use
implementation as a substitute for an explanation, preview, or approval.
