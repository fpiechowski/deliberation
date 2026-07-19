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

## D-006 — Keep Deliberation active for the current conversation

- **Date:** 2026-07-19
- **Status:** Accepted

### Context

Scoping activation to one task would require the agent to decide where a task
ends. That boundary becomes unclear when work contains follow-ups, changes
direction, or moves between related objectives. The user needs a predictable
and directly controllable mode lifetime.

### Decision

Once activated, Deliberation remains active throughout the current conversation
until the user explicitly disables it. Completing a task does not disable the
mode. A new conversation starts without the mode unless it is activated again.

Activation and deactivation are acknowledged explicitly. An unambiguous
natural-language request is sufficient; leaving the mode does not require a
special command.

### Consequences

The contract should use “current conversation” or “thread” rather than the
ambiguous term “session.” The initial skill must be tested for reliable
continuity across turns and resumed conversations. Any technical limitation in
skill activation should be treated as an implementation concern rather than
silently changing the product semantics.

## D-007 — Use journey-based explanation when it improves understanding

- **Date:** 2026-07-19
- **Status:** Accepted

### Context

Explaining components in isolation often makes dynamic code and design harder
to understand. Tracing a flow from its trigger to its outcome gives the user a
mental model in which implementation details have a clear place. This supports
the project's knowledge-transfer objective.

Journey-based explanation serves a different purpose from a proposal. A
proposal supports a decision; an explanation builds understanding.

### Decision

Treat journey-based explanation as a separate, conditional explanation
technique rather than a mandatory part of every proposal.

When useful, trace the initiating actor or event through relevant components,
state changes, and decisions to the observable result. Use a user journey,
request journey, data journey, or execution flow according to the subject, and
connect its stages to the corresponding design or code.

### Consequences

The behavioural contract should call for journey-based explanation when
describing dynamic flows, architecture, state transitions, or interactions
across components. It should not force this format onto small static or
mechanical changes where it adds no clarity.

## D-008 — Separate milestones, checkpoints, and result walkthroughs

- **Date:** 2026-07-19
- **Status:** Accepted

### Context

The earlier language could make a checkpoint sound like the approval prompt
alone and could suggest that implementation happens before the agent fully
explains its proposal. The manifest also described the main loop with
explanation before approval while its development section listed explanation
after implementation.

The contract needs distinct concepts for organizing work, supporting a
decision, and explaining the implemented result.

### Decision

A **milestone** is a bounded, coherent unit of execution that produces an
independently understandable and verifiable result. It is defined by its
outcome, boundaries, completion criteria, and verification rather than by a
list of implementation activities.

A **checkpoint** is the period of deliberation before a consequential action.
It includes proposal, explanation, meaningful alternatives and tradeoffs,
discussion, and a shared decision. Explicit approval is the final part of the
checkpoint and must precede execution.

After executing an approved milestone, the agent walks through and verifies the
actual result. This result walkthrough complements but never replaces the
pre-approval explanation.

### Consequences

Milestones organize work; checkpoints organize decisions and authorization.
The standard loop is:

```text
understand → gather information → plan the next milestone
→ checkpoint (propose → explain → discuss → decide → approve)
→ execute → walk through and verify → update the plan → repeat
```

A milestone may need no checkpoint when it is purely diagnostic or already
authorized and contains no consequential decision. If execution reveals a new
consequential decision outside the approved scope, the agent starts another
checkpoint before continuing.

## D-009 — Show the roadmap but approve the next milestone by default

- **Date:** 2026-07-19
- **Status:** Accepted

### Context

Agreeing on an entire detailed plan before starting can create false certainty
and imply authorization for decisions that have not yet been explored. Showing
only the immediate step would avoid that problem but leave the user without a
useful view of the intended direction.

### Decision

For a larger task, present a provisional roadmap of milestones so the user can
understand and question the overall direction. Identify known later decisions
and uncertainties, but develop only the next milestone in enough detail for an
informed checkpoint.

By default, approval authorizes only the next milestone. It does not authorize
the rest of the roadmap. The user may explicitly grant broader authorization
for a known set of milestones. For a simple task, the roadmap may contain one
milestone.

### Consequences

The first checkpoint should distinguish clearly between the provisional roadmap
and the milestone currently proposed for approval. After execution, the agent
walks through the result and updates the roadmap before proposing the next
milestone.

## D-010 — Trigger checkpoints through Choice, Consequence, and Drift

- **Date:** 2026-07-19
- **Status:** Accepted

### Context

Requiring approval for every technical choice would cause approval fatigue,
while relying only on the agent's general judgment about “meaningful changes”
would make its autonomy unpredictable. The contract needs an operational test
for when deliberation must pause before execution.

### Decision

A checkpoint is required when at least one of three tests applies:

1. **Choice:** the agent would otherwise make an unresolved choice between
   reasonable alternatives whose differences materially affect the result.
2. **Consequence:** an action crosses a material boundary or introduces an
   unconsidered material consequence, even if there is no reasonable
   alternative.
3. **Drift:** new information invalidates an accepted assumption, expands the
   approved milestone, reveals material risk, or makes the approved direction
   unreasonable.

Material effects include user-visible behaviour, public contracts, data,
architecture, security, privacy, integrity, performance, cost, maintainability,
dependencies, integrations, external effects, reversibility, and meaningful
scope.

The existence of multiple technical possibilities is not sufficient by itself.
Their differences must matter to the result or the user.

### Consequences

Inspection, diagnosis, mechanical implementation within an accepted direction,
standard validation, formatting, and documentation do not require artificial
checkpoints. Work specified precisely by the user can proceed when it contains
no unresolved material decision or unconsidered consequence.

Related decisions for one milestone should be grouped into one checkpoint.
Execution must start a new checkpoint when it encounters Choice, Consequence,
or Drift outside the approved scope.

## D-011 — Make checkpoints decision-ready and interpret responses by intent

- **Date:** 2026-07-19
- **Status:** Accepted

### Context

A checkpoint needs enough structure to support an informed decision without
becoming a rigid form. The agent also needs predictable rules for distinguishing
approval from questions, revisions, rejection, and broad authorization.

### Decision

Every checkpoint communicates the decision needed, what is proposed, why the
change is needed, how it works, why the recommended approach is preferred,
material tradeoffs and alternatives, the approval scope, and an explicit
approval question. It includes a journey-based explanation when that would
materially improve understanding.

These are semantic requirements rather than mandatory headings. The amount and
format of explanation should be proportional to the significance and
complexity of the decision.

Interpret the user's response by communicative intent:

- Unambiguous agreement or an instruction to execute is approval.
- A material requested change is revision and requires an updated proposal.
- Rejection does not authorize execution.
- A question remains part of the checkpoint and does not authorize execution.
- Ambiguity requires concise clarification rather than assumed approval.

Broad approval such as “do the rest” authorizes the remaining milestones
already presented for the current task. It does not authorize later tasks or
undisclosed material decisions and consequences. The agent acknowledges the
interpreted batch scope and starts another checkpoint only for a new Choice,
Consequence, or Drift outside that scope.

Asking the agent to stop requesting approval for the rest of the conversation
is treated as explicitly disabling Deliberation because checkpoints are
constitutive of the mode.

### Consequences

Checkpoint prompts must state what approval covers and excludes. The skill must
not rely on magic phrases, treat praise or a question as consent, or repeat the
same approval request after receiving clear batch authorization.

## D-012 — Track state lightly and distinguish progress from checkpoints

- **Date:** 2026-07-19
- **Status:** Accepted

### Context

The user needs enough state visibility to understand where the work stands
without receiving a repetitive process ledger after every message. Progress
updates must also remain distinct from checkpoints so that information does not
create unnecessary approval requests.

Projects differ in how they preserve decisions. Automatically adding
Deliberation-specific state files to every repository would be intrusive.

### Decision

Maintain a lightweight conversational model of the active mode, objective,
roadmap, current milestone, approval scope, accepted and changed decisions,
open questions, and next checkpoint. Surface updates when decisions or the
roadmap change, milestones finish, Drift appears, or the user requests status.

Never replace an accepted decision silently. Explain what changed and which
earlier assumption or decision no longer applies.

Create or update durable state only when the project already has an appropriate
convention, the user requests it, cross-conversation continuity requires it, or
durable tracking is part of an approved milestone.

Provide concise informational updates when starting a milestone, after a
material discovery, before lengthy validation, and at milestone completion.
These updates are not checkpoints.

After execution, provide a result walkthrough covering the outcome, important
changes, useful actual journey, verification, deviations, roadmap impact, and
the next milestone or task completion.

At task completion, report whether the objective was achieved, what was
produced, important accepted decisions, verification, and remaining risks or
questions. State explicitly when nothing remains. If the objective is unmet,
report the exact blocker and what is needed to continue instead of claiming
completion.

### Consequences

Deliberation remains conversational by default and does not impose new files on
unrelated repositories. Completion of one task leaves the mode active for the
current conversation.

## D-013 — Support Codex, Claude Code, and OpenCode from one core

- **Date:** 2026-07-19
- **Status:** Accepted

### Context

Deliberation is a work mode rather than a capability tied to one coding agent.
Codex, Claude Code, and OpenCode support Agent Skills-compatible instructions
but differ in explicit invocation, metadata, packaging, and distribution.

Because activation persists for the whole conversation, implicit invocation
could surprise a user who intended only a one-task explanation or plan.

### Decision

Use **Deliberation** as the product name and `deliberation` as the primary skill
name. Require explicit activation in the first version.

Support three environments:

1. Codex, invoked through `$deliberation` or its plugin interface.
2. Claude Code, invoked through `/deliberation` as a standalone skill or the
   corresponding namespaced command when packaged as a plugin.
3. OpenCode, invoked through a `/deliberation` custom command that loads the
   shared behavioural contract.

Maintain one Agent Skills-compatible behavioural core and thin,
environment-specific adapters. Adapters may differ in invocation, metadata,
package layout, installation, and continuity mechanics, but not in product
semantics.

### Consequences

The shared behavioural scenario suite must pass in all three environments
before the first version is considered complete.

Validate Codex first in the desktop app and then in CLI and IDE. Validate Claude
Code first as a local skill and then as a plugin. Validate OpenCode with its
custom command and skill content. Public distribution follows local validation.

Codex and Claude Code may use their native plugin marketplaces. OpenCode first
uses a locally or globally installed command and skill bundle. Do not add a
JavaScript or TypeScript OpenCode plugin in the first version unless later
evidence shows material installation or runtime value.

Current platform references:

- [Agent Skills specification](https://agentskills.io/specification)
- [Codex skills](https://learn.chatgpt.com/docs/build-skills)
- [Claude Code skills](https://code.claude.com/docs/en/slash-commands)
- [Claude Code plugins](https://code.claude.com/docs/en/plugins)
- [OpenCode skills](https://opencode.ai/docs/skills)
- [OpenCode commands](https://opencode.ai/docs/commands)

## D-014 — Use shared behavioural scenarios and close product definition

- **Date:** 2026-07-19
- **Status:** Accepted

### Context

The behavioural contract needs observable acceptance criteria that can detect
correct final output produced through the wrong interaction model. The project
also needs an explicit terminal condition for its product-definition and
interaction-design phase.

### Decision

Use `docs/BEHAVIORAL_SCENARIOS.md` as the acceptance contract for observable
Deliberation behaviour.

The suite contains:

- Platform-neutral core scenarios.
- Cross-task-type coverage.
- Adapter-specific scenarios for Codex, Claude Code, and OpenCode.
- Critical failure cases.
- Traceability from accepted decisions to acceptance evidence.

Evaluate scenarios through representative transcripts first. Do not add a test
framework or runtime dependency during product definition.

Mark product definition and interaction design complete once every accepted
decision is covered, no product-contract questions remain, and the durable
documents are internally consistent.

### Consequences

Documentation completion closes the current phase but does not constitute
runtime validation. The first implemented release remains incomplete until all
core and applicable adapter scenarios pass in all three environments without a
critical failure.

The next phase is cross-environment skill and adapter design. It requires a
separate approved architecture milestone before scaffolding production
packages.

## D-015 — Generate three adapters from one canonical skill core

- **Date:** 2026-07-19
- **Status:** Accepted

### Context

Codex, Claude Code, and OpenCode all support Agent Skills-compatible
instructions, but their explicit invocation and distribution contracts differ.
Codex uses companion `agents/openai.yaml` policy, Claude Code uses skill
frontmatter and namespaced plugins, and OpenCode exposes discovered skills to
the model without an equivalent per-skill implicit-invocation switch.

Git-hosted marketplaces also require installable plugin contents to exist in
the cloned repository. Installed plugins are copied into host caches and cannot
reliably reference a shared source file outside their package.

Maintaining three hand-edited behavioural copies would make semantic drift
likely. Symlinks would be fragile across plugin caches and Windows.

### Decision

Maintain one Agent Skills-compatible canonical core at
`core/deliberation/SKILL.md`.

Generate thin host variants and self-contained publication packages:

1. Codex adds `agents/openai.yaml` with implicit invocation disabled and is
   packaged under `plugins/deliberation/`.
2. Claude Code adds `disable-model-invocation: true`, produces standalone and
   namespaced plugin variants, and is packaged under
   `claude-plugins/deliberation/`.
3. OpenCode generates an explicit `/deliberation` command with the normalized
   core behaviour embedded. The canonical skill is bundled outside OpenCode
   skill discovery paths.

Commit generated publication packages so Git-hosted marketplaces can install
them directly. Keep temporary build output untracked. Use deterministic
integrity checks to prove that adapter payloads match the canonical core after
removing declared host metadata and wrapper syntax.

Use one product SemVer from a top-level `VERSION` file across the core,
adapters, packages, and release validation evidence.

Use a repository-local Python 3 standard-library assembler. Add no end-user
runtime dependency, third-party build dependency, hook, MCP server, connector,
or OpenCode npm plugin in the first version.

Use structural validation, semantic-integrity checks, and shared
transcript-based fixtures with environment-specific adapter cases. Do not add
an LLM-as-judge or test-framework dependency in the first version.

The detailed accepted topology and adapter contracts are recorded in
`docs/ARCHITECTURE.md`.

### Consequences

The shared behaviour has one hand-authored source of truth while each
environment receives a native, self-contained package.

Generated marketplace packages are version-controlled artifacts, not
independent sources. Validation must fail when regeneration produces a diff or
when a host adapter changes normalized product semantics.

The repository may eventually contain both Codex and Claude Code marketplace
catalogs. Their public marketplace names, publisher metadata, and actual
entries require later distribution approval.

The next milestone may scaffold the canonical core, adapter templates,
assembler, and validation skeleton, but production scaffolding begins only
after a separate checkpoint approves that bounded implementation.

## D-016 — Scaffold the canonical core before committing publication packages

- **Date:** 2026-07-19
- **Status:** Accepted

### Context

The accepted architecture requires one canonical behavioural source,
host-specific overlays, deterministic assembly, and semantic-integrity
validation. Implementing that pipeline and committing installable publication
packages in one step would make it harder to review the behavioural contract
separately from distribution surfaces.

### Decision

Implement the first production scaffold with:

1. A canonical `core/deliberation/SKILL.md`.
2. `0.1.0-dev.0` as the shared development SemVer.
3. Codex, Claude Code, and OpenCode adapter templates.
4. A Python 3 standard-library assembler that generates complete standalone
   and publication previews under ignored `build/` output.
5. Deterministic structural and semantic-integrity checks.
6. A fixture assertion schema, one representative core fixture, and one
   explicit-activation fixture for each host.

Do not yet commit generated packages under `plugins/`, `claude-plugins/`, or
`opencode-bundles/`. Do not add marketplace catalogs, public publisher
metadata, host installation, release automation, or a new dependency.

### Consequences

The behavioural source and transformation rules can be reviewed and validated
before publication surfaces become version-controlled artifacts. The next
milestone can promote the reviewed generated packages and make validation fail
when committed output is stale, without reopening the accepted behavioural
architecture.
