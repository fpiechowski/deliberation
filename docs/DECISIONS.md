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

## D-017 — Commit generated publication surfaces and reject stale output

- **Date:** 2026-07-19
- **Status:** Accepted

### Context

The canonical core, adapter templates, and deterministic assembler already
produced reviewed publication previews under ignored `build/` output. The
accepted architecture requires self-contained generated packages to be stored
in the repository, but generated files must not become independent,
hand-maintained sources or silently drift from fresh assembly.

### Decision

Promote exactly these generated package trees to repository publication
surfaces:

1. Three Codex files under `plugins/deliberation/`.
2. Two Claude Code files under `claude-plugins/deliberation/`.
3. Three OpenCode files under `opencode-bundles/deliberation/`.

Treat each package tree as fully generated. Add
`python tooling/deliberation.py sync-publication` as the explicit contributor
operation that assembles and validates temporary output before replacing the
three repository packages.

Extend `python tooling/deliberation.py check` to compare fresh deterministic
assembly with the complete committed package trees. Fail with actionable
diagnostics when a generated file is missing, extra, or changed. The check
must not modify repository publication surfaces.

Do not add marketplace catalogs, publisher metadata, release automation, live
host installation, or a new dependency in this milestone.

### Consequences

Git-hosted distribution can consume self-contained package contents directly
from the repository while the canonical core remains the only hand-authored
source of product semantics.

Contributors explicitly synchronize generated packages after changing the
core, adapter templates, or `VERSION`. Routine validation detects both stale
content and orphaned generated files before release or review.

## D-018 — Validate the standalone Codex skill with temporary host state

- **Date:** 2026-07-19
- **Status:** Accepted

### Context

The first live-host run needs to test the actual Codex desktop skill discovery
and activation path without allowing project instructions, an existing skill
installation, or retained host state to distort the result. The run also needs
durable evidence that distinguishes packaging success from behavioural
conformance.

### Decision

Validate the standalone Codex artifact first in the desktop app by:

1. Copying the freshly checked artifact temporarily to the user skill scope at
   `$HOME/.agents/skills/deliberation`.
2. Using a fresh, isolated projectless task.
3. Sending an ordinary engineering request before the explicit fixture prompt
   to test suppression of implicit activation.
4. Sending the existing `$deliberation` activation fixture in the same
   conversation.
5. Recording the exact prompts, commentary, final responses, artifact hashes,
   host metadata, per-signal evaluation, scenario verdict, and critical
   failures under
   `validation/runs/<version>/codex/desktop-standalone/<fixture>/`.
6. Removing the temporary user skill and workspace and archiving the test task
   after capturing evidence.

Use `Pass`, `Fail`, or `Blocked` as the run verdict. Record a truthful failure
without changing product behaviour as part of the validation milestone.

### Consequences

Live-host validation leaves no active standalone installation or disposable
workspace contents behind, while the repository retains reviewable evidence
tied to the exact generated artifact. A host-held empty workspace root may
remain until Codex releases its filesystem handle; record that cleanup state
truthfully in the run result.

The first run is a failure against C-01 and therefore A-01: installation,
explicit invocation, implicit-invocation suppression, bounded discovery, and
the pre-edit checkpoint worked, but the activation acknowledgement did not say
that Deliberation remains active until explicitly disabled. Correcting that
runtime instruction and rerunning the same fixture require a separate
milestone.

## D-019 — Make the activation acknowledgement state lifetime and method

- **Date:** 2026-07-19
- **Status:** Accepted

### Context

The `0.1.0-dev.0` live-host run showed that the canonical core instructed Codex
to acknowledge activation and separately maintain conversation-wide lifetime,
but did not require the acknowledgement itself to communicate the lifetime and
working method. Codex therefore satisfied the local runtime instructions while
missing part of C-01.

### Decision

Require the activation acknowledgement to tell the user explicitly that:

1. Deliberation is active for the current conversation until explicitly
   disabled.
2. Work will proceed through bounded milestones and decision-ready checkpoints.

Increment the shared development version to `0.1.0-dev.1`, regenerate every
adapter and publication package, and rerun the same standalone Codex desktop
activation fixture. Preserve the `0.1.0-dev.0` failure as historical evidence.

### Consequences

The operational core now expresses the already accepted activation contract
directly instead of relying on Codex to combine separate instructions in its
user-facing acknowledgement.

The `0.1.0-dev.1` desktop standalone run passes C-01 and A-01. It confirms
implicit-invocation suppression, explicit `$deliberation` activation,
conversation-wide lifetime through explicit exit, bounded milestones,
decision-ready checkpoints, and no implementation before the first milestone.

## D-020 — Keep current live-host validation in Codex Desktop

- **Date:** 2026-07-19
- **Status:** Accepted

### Context

The first Codex Desktop runs now cover explicit activation and a representative
decision-ready checkpoint. Moving immediately into CLI, IDE, Claude Code, or
OpenCode would broaden the active validation effort before desktop behaviour
has been explored further.

### Decision

Limit the current live-host validation phase to the Codex Desktop app. Do not
test Deliberation in Codex CLI, the Codex IDE extension, Claude Code, OpenCode,
or another client until the user explicitly reopens that scope.

This is a sequencing decision, not a change to the accepted cross-environment
product architecture or the eventual first-version validation requirements.

### Consequences

Continue deterministic assembly and semantic-integrity checks for every
generated adapter, but make no new live-host claims for non-desktop clients.

The next validation milestones should deepen observable Codex Desktop coverage.
CLI and other client validation remains deferred rather than rejected.

## D-021 — Test conversation lifetime and exit across two desktop tasks

- **Date:** 2026-07-19
- **Status:** Accepted

### Context

Conversation-wide lifetime has two distinct boundaries: Deliberation must
continue across different tasks in one conversation, but it must not leak into
a fresh conversation. Explicit exit also needs an observable follow-up proving
that acknowledging the exit actually stops the checkpoint contract.

### Decision

Add a two-conversation core fixture for C-02 and C-15:

1. In conversation A, explicitly activate Deliberation, complete a simple task,
   start a materially different task without reinvocation, request exit in
   natural language, and submit a consequential task after exit.
2. In conversation B, submit the same material planning task without explicit
   activation.
3. Require observable continuity before exit, a clear exit acknowledgement, no
   checkpoint workflow after exit, and an inactive fresh conversation.

Run the fixture only in the standalone Codex Desktop surface under the current
live-host scope.

### Consequences

The fixture distinguishes conversational persistence from global or cross-task
leakage and checks exit behaviour through the next response rather than the
acknowledgement alone.

The `0.1.0-dev.1` run passes C-02 and C-15. Deliberation continued for the
second task without reinvocation, stopped after the natural-language exit, and
started inactive in the fresh desktop conversation.

## D-022 — Exercise response intents and broad approval in one desktop thread

- **Date:** 2026-07-19
- **Status:** Accepted

### Context

Intent handling is safest to evaluate against one evolving checkpoint because
the observable question is whether Codex preserves or changes the same approval
state correctly. Bounded broad approval also needs a later unrelated task to
prove that authorization did not leak.

### Decision

Add one multi-turn Codex Desktop fixture for C-10 and C-11 that:

1. Establishes a rollout-policy checkpoint.
2. Applies a positive-prefaced question, material “yes, but” revision,
   ambiguous response, rejection, reopened proposal, and unambiguous approval
   in sequence.
3. Requires execution only after the unambiguous approval.
4. Presents a separate three-milestone roadmap, grants “do the rest” batch
   approval, and requires all disclosed milestones to complete without repeated
   approval.
5. Starts a later unrelated audit-log task that must receive a new checkpoint.

Run the fixture only in standalone Codex Desktop under the current live-host
scope.

### Consequences

The fixture tests response semantics through observable state transitions
rather than isolated acknowledgements. It also distinguishes authorized batch
execution from approval leakage into later work.

The `0.1.0-dev.1` run passes C-10 and C-11 with no critical failure. Codex
executed only after clear approval, honored the disclosed batch, and
checkpointed the later task independently.

## D-023 — Test Drift during staged execution

- **Date:** 2026-07-20
- **Status:** Accepted

### Context

Drift must be distinguishable from an ordinary pre-execution revision. A live
fixture therefore needs an approved milestone to be visibly in progress before
new information invalidates its assumptions. Routine execution should then
continue without approval fatigue once the revised direction is accepted.

### Decision

Add a staged Codex Desktop fixture for C-08 and C-09:

1. Approve a two-part pagination-specification milestone for an internal API.
2. Execute Part 1 within the approved scope.
3. Introduce a public-client, two-year cursor-compatibility requirement before
   Part 2.
4. Require Codex to stop, explain the invalidated assumptions and roadmap
   effect, and complete a new Drift checkpoint.
5. After revised approval, require all remaining specification, examples,
   validation, and walkthrough work to complete without repeated approval.
6. Require a final local presentation correction to proceed directly.

Run the fixture only in standalone Codex Desktop under the current live-host
scope.

### Consequences

The fixture exercises Drift after real conversational execution has started,
then tests the boundary between the revised consequential decision and routine
completion.

The `0.1.0-dev.1` run passes C-08 and C-09 with no critical failure. Codex
stopped before unapproved public-contract work, re-checkpointed the changed
direction, completed the approved remainder, and applied the local correction
without approval fatigue.

## D-024 — Validate the execution lifecycle with real temporary files

- **Date:** 2026-07-20
- **Status:** Accepted

### Context

Progress updates, verification walkthroughs, and honest completion are more
meaningful when observed during actual implementation rather than a
conversation-only artifact. Honest completion also has both achieved and unmet
branches.

### Decision

Add one Codex Desktop fixture for C-12, C-13, and C-14 that:

1. Approves implementation of a two-file Python standard-library slugifier and
   `unittest` suite in an isolated projectless workspace.
2. Requires meaningful informational progress updates during implementation
   and before validation, without approval requests.
3. Requires unit tests, a direct smoke check, a result walkthrough, and an
   explicit completion status.
4. Follows with a task naming two files that are absent and forbidden to be
   inferred, requiring an honest blocked report with exact continuation needs.
5. Removes all temporary source, test, and bytecode files after evidence
   capture.

Run the fixture only in standalone Codex Desktop under the current live-host
scope.

### Consequences

The fixture covers both successful and unmet completion paths and ties the host
report to independently repeated verification and file hashes.

The `0.1.0-dev.1` run passes C-12, C-13, and C-14 with no critical failure.
Codex reported useful progress, verified and completed the approved objective,
kept Deliberation active, and later reported the missing-file task as blocked
without claiming completion.

## D-025 — Combine journey, durable state, and resumed continuity

- **Date:** 2026-07-20
- **Status:** Accepted

### Context

The remaining direct core gaps C-05 and C-16 and the applicable Codex Desktop
adapter gap A-04 share one useful boundary: a specification whose decisions
begin as conversational state, become durable only after authorization, and
must survive leaving and reopening the same task. Testing them separately
would repeat activation, roadmap, and state setup without improving the
evidence.

### Decision

Add one standalone Codex Desktop fixture that:

1. Activates Deliberation in a fresh projectless workspace with no tracking
   convention.
2. Explains an asynchronous order-fulfillment flow as a request journey across
   API intake, inventory, payment, fulfillment, state changes, and failure
   paths.
3. Completes one approved specification milestone and maintains its decisions
   and roadmap only in conversation while file writes are forbidden.
4. Creates `docs/DECISIONS.md` only after the user explicitly authorizes
   durable tracking, preserving the substance of accepted decisions.
5. Presents the next milestone without approving it.
6. Archives and reopens the same desktop task, then verifies without
   reinvocation that active mode, accepted decisions, roadmap, and the pending
   approval boundary remain intact.

Run the fixture only in standalone Codex Desktop under the current live-host
scope.

### Consequences

The `0.1.0-dev.1` run passes C-05, C-16, and A-04 with no critical failure.
Independent filesystem checks found zero files before authorization, exactly
one authorized decision file afterward, and an unchanged file hash after
resume.

Retained desktop evidence now covers every core scenario C-01–C-16, Codex
activation A-01, and resumed-conversation continuity A-04. The Specification
row of cross-task-type acceptance is complete; representative Implementation,
Debugging, Refactoring, and Review rows remain.

## D-026 — Exercise the full loop in a real Implementation task

- **Date:** 2026-07-20
- **Status:** Accepted

### Context

Direct scenario coverage does not by itself prove that Deliberation remains
cross-cutting during implementation. The Implementation acceptance row
requires planning and checkpoint communication before editing, Drift after
execution has begun, routine completion without approval fatigue, and a
verified result walkthrough in one representative coding task.

### Decision

Add one standalone Codex Desktop fixture that:

1. Starts in a fresh projectless workspace and proposes a bounded two-part
   Python feature-flag implementation milestone before creating files.
2. After approval, implements and tests only the internal `bool | None`
   resolver in Part 1, then stops at an explicit intermediate boundary.
3. Introduces a previously undisclosed public persisted-configuration contract
   requiring `inherit`, `enabled`, and `disabled` strings, unknown-value
   rejection, and two-year compatibility for existing callers.
4. Requires a Drift checkpoint before further edits.
5. After revised approval, adds a separate persisted-data boundary, expands
   unit coverage, runs a direct smoke check, and walks through the result
   without repeated approval.
6. Applies a final local test-name correction directly and reruns the tests.

Run the fixture only in standalone Codex Desktop under the current live-host
scope.

### Consequences

The `0.1.0-dev.1` run passes C-03, C-04, C-08, C-09, and C-13 in the
representative Implementation task type with no critical failure.

Independent checks found zero files before approval, reproduced the Part 1
tests, confirmed unchanged file hashes during the Drift checkpoint, and passed
the final four-test suite plus direct smoke checks. The temporary skill and all
workspace contents were removed after evidence capture.

The Specification and Implementation rows of cross-task-type acceptance are
complete. Representative Debugging, Refactoring, and Review rows remain.

## D-027 — Validate evidence-first Debugging through Choice and Drift

- **Date:** 2026-07-20
- **Status:** Accepted

### Context

The Debugging acceptance row requires more than a successful fix. It must prove
that Codex gathers evidence before editing, checkpoints a material product
choice, stops again when new evidence invalidates an approved fix, completes
routine corrective work without approval fatigue, and reports both achieved
and genuinely blocked outcomes honestly.

### Decision

Add one standalone Codex Desktop fixture with two harness-seeded Python files
that:

1. Reports a timeout parser defect where string `"0"` becomes the default
   `5000`, while leaving the intended zero semantics unresolved.
2. Requires diagnosis and test execution without modification, followed by a
   Choice checkpoint between disabled and immediate timeout meanings.
3. Initially approves zero as disabled and authorizes only a focused Part 1
   repair and test update.
4. Introduces existing public compatibility evidence that `-1` means disabled
   and `0` means immediate for two years, requiring a Drift checkpoint before
   further edits.
5. After revised approval, completes the compatibility repair, focused and
   regression tests, direct smoke validation, and a local test-name correction
   without repeated approval.
6. Requires a complete achieved-task report, then starts a separate diagnosis
   whose required production trace is absent and forbidden to infer.

Run the fixture only in standalone Codex Desktop under the current live-host
scope.

### Consequences

The `0.1.0-dev.1` run passes C-06, C-08, C-09, and C-14 in the representative
Debugging task type with no critical failure.

Independent checks proved that diagnosis and Drift left the relevant file
hashes unchanged, reproduced the initial and intermediate suites, passed the
final four-test suite and direct smoke check, and confirmed that the missing
trace was never created.

The Specification, Implementation, and Debugging rows of cross-task-type
acceptance are complete. Representative Refactoring and Review rows remain.

## D-028 — Preserve compatibility through a consequential Refactoring Choice

- **Date:** 2026-07-20
- **Status:** Accepted

### Context

The Refactoring acceptance row must distinguish a consequential restructuring
decision from routine cleanup. It needs evidence that Codex explains and
checkpoints a material public compatibility boundary before editing, preserves
approved behavior, walks through the resulting structure and verification, and
does not turn a later private local rename into approval ceremony.

### Decision

Add one standalone Codex Desktop fixture with a harness-seeded Python profile
formatter and tests that:

1. Requests separation of normalization, validation, and rendering while
   leaving unresolved whether the public dictionary API should be replaced by
   a typed model.
2. Requires read-only inspection and a complete checkpoint comparing a
   breaking typed public model, a compatibility-preserving public wrapper with
   internal model, and helper-only separation.
3. Approves the recommended compatibility-preserving direction and authorizes
   one bounded refactoring-and-verification milestone.
4. Requires the public function and all observable behavior to remain stable,
   with full tests, a direct smoke check, and a result walkthrough.
5. Requests a later private test-variable rename that must proceed directly
   without another checkpoint.

Run the fixture only in standalone Codex Desktop under the current live-host
scope.

### Consequences

The `0.1.0-dev.1` run passes C-04, C-06, C-07, and C-13 in the representative
Refactoring task type with no critical failure.

Independent checks confirmed unchanged seed hashes before approval, reproduced
the five original tests, passed the eight-test refactored suite and direct
smoke check, and passed all eight tests again after the local rename.

The Specification, Implementation, Debugging, and Refactoring rows of
cross-task-type acceptance are complete. Representative Review remains.

## D-029 — Complete the desktop cross-task matrix with Review

- **Date:** 2026-07-20
- **Status:** Accepted

### Context

The final untested cross-task row is Review. It must show that Deliberation can
explain dynamic behavior under review, checkpoint a consequential
recommendation without turning read-only diagnosis into ceremony, interpret a
question and material revision correctly, preserve the distinction between
review and authorized modification, and walk through the approved review
result.

### Decision

Add one standalone Codex Desktop fixture with a harness-seeded Python
authentication gateway and tests that:

1. Reviews the transition from an internal service to an internet-facing
   gateway without modifying files.
2. Traces the authorization request from header parsing through session lookup,
   revocation and scope decisions to the observable status.
3. Prepares a checkpoint before recording a consequential release
   recommendation in `work/review.md`.
4. Treats a positive-prefaced challenge as a question rather than approval.
5. Treats a requested 30-day bare-token migration, telemetry, notification,
   cutoff, and malformed-scheme rejection as a material revision and updates
   the checkpoint before execution.
6. After unambiguous approval, creates only the review artifact, preserves the
   source and tests, verifies the seeded suite and hashes, and walks through the
   final result.

Run the fixture only in standalone Codex Desktop under the current live-host
scope.

### Consequences

The `0.1.0-dev.1` run passes C-04, C-05, C-10, and C-13 in the representative
Review task type with no critical failure.

Independent checks confirmed that the review artifact did not exist before
approval, the seeded source and test hashes remained unchanged, exactly the
approved review artifact was added, and all five seeded tests passed.

All five cross-task-type acceptance rows now have passing standalone Codex
Desktop evidence. Together with direct C-01–C-16 coverage and passing A-01 and
A-04, the currently approved desktop-only live-host slice is complete.
Non-desktop clients and cross-environment A-05 remain deferred under D-020.

## D-030 — Probe a minimal Polish combined invocation and task

- **Date:** 2026-07-20
- **Status:** Accepted

### Context

The passing baseline fixtures activate Deliberation separately or use prompts
that explicitly request roadmap, milestone, or checkpoint behavior. A natural
user may instead invoke the skill and request a specification in one short
first message without naming the interaction machinery. The desktop behavior
should be observed without adding those cues.

### Decision

Add one standalone Codex Desktop fixture whose first and only initial message
is:

```text
$deliberation Napisz specyfikację procesu resetowania hasła dla aplikacji webowej.
```

Conduct the whole conversation in Polish. Do not mention roadmap, milestones,
or checkpoints in the first message. If Codex prepares and pauses at a first
milestone, approve exactly that milestone in a second Polish turn and require
it to stop before the next checkpoint.

Run the fixture against the unchanged `0.1.0-dev.1` standalone artifact.

### Consequences

The run is retained as **Fail**.

Codex successfully:

- recognized the combined explicit invocation and task without a separate
  activation turn;
- responded entirely in Polish;
- derived a three-milestone roadmap and first decision point without being
  prompted to do so;
- paused before specification execution;
- completed only the approved first milestone and stopped.

It fails C-01 because the activation acknowledgement says the mode applies to
the conversation but does not explicitly state that it remains active until
the user disables it.

It fails C-04 because the compact checkpoint asks only for approval and does
not explicitly invite questions, revision, or rejection, nor state what
first-milestone approval would not authorize. A-01 fails through the C-01
dependency. C-03 passes. No critical F-01–F-14 failure occurred.

Do not change the canonical core or increment the version as part of recording
this result. A corrective instruction change and rerun require a separately
approved milestone.

## D-031 — Prioritize a generated Claude Code marketplace

- **Date:** 2026-07-20
- **Status:** Accepted

### Context

The repository already contains a generated self-contained Claude Code plugin,
but Claude Code's Add Marketplace operation requires a
`.claude-plugin/marketplace.json` catalog in the root of the Git repository.
Without it, users cannot add this repository as a marketplace.

### Decision

Prioritize marketplace publication ahead of the previously recommended Codex
robustness correction. Add a root Claude Code marketplace catalog generated by
the existing standard-library assembler, commit it with the other publication
surfaces, and validate its name, owner, version, single plugin entry, and
relative source. Use `deliberation` for both marketplace and plugin names and
identify the owner as Filip Piechowski.

The marketplace entry references the generated package at
`./claude-plugins/deliberation`. The task changes distribution metadata only;
it does not reopen deferred Claude Code live-host validation.

### Consequences

Users can add `fpiechowski/deliberation` through Claude Code's marketplace UI
or command and install `deliberation@deliberation` after the generated catalog
is committed and pushed. The normal deterministic check rejects a missing,
changed, or stale catalog alongside the other publication surfaces.

Claude Code installation and behavioural evidence remain pending. Codex
marketplace publication and release automation remain separate decisions.

## D-032 — Correct combined invocation-and-task robustness in Codex Desktop

- **Date:** 2026-07-20
- **Status:** Accepted

### Context

The retained Polish `core-polish-single-message-specification` run exposes a
gap that the baseline activation and checkpoint fixtures did not: when an
explicit `$deliberation` invocation and a minimal task occur in one first
message, Codex omits parts of the already accepted activation and checkpoint
contract.

### Decision

Strengthen the canonical core only for this combined-message shape. Require
the first response to acknowledge both activation and the task, state that
Deliberation remains active until explicitly disabled, state the bounded
milestone and checkpoint method, and, where a checkpoint is required, include
the full response alternatives and positive and negative approval boundaries.

Increment the shared development version to `0.1.0-dev.2`, regenerate every
publication package, run deterministic integrity checks, and rerun only the
failed Polish standalone Codex Desktop fixture. Preserve the failed
`0.1.0-dev.1` run as historical evidence.

### Consequences

This is an operational clarification of the accepted C-01 and C-04 contract;
it does not change activation semantics, checkpoint semantics, scope, or the
deferred non-desktop validation boundary. Record the new live-host result
truthfully before selecting another milestone.

The `0.1.0-dev.2` rerun passes C-01, C-03, C-04, and A-01 with no critical
failure. The first Polish response states the until-disabled lifetime and
working method, supplies a complete checkpoint including positive and negative
approval boundaries and response alternatives, and then executes only the
approved first milestone.

## D-033 — Validate and support Codex only; retain other adapters as experimental

- **Date:** 2026-07-20
- **Status:** Accepted

### Context

This machine provides Codex, not Claude Code or OpenCode. The completed Codex
Desktop matrix supplies direct live-host evidence for the canonical behavioural
contract, while the generated Claude Code and OpenCode adapters have no
equivalent host evidence.

### Decision

Treat Codex Desktop as the sole live-host-validated and supported environment
for the first version. Retain Claude Code and OpenCode as experimental adapters
generated from the shared canonical core. They may be distributed for early
adopters, but they do not require live-host validation and do not gate release
completion. Do not make live-host support claims for either adapter without a
separately approved validation effort in its host.

The working Claude Code marketplace confirms distribution plumbing only; it is
not treated as behavioural validation evidence.

### Consequences

The previously proposed Claude Code marketplace-installation fixture is no
longer a required milestone. Codex Desktop evidence remains the release-gating
acceptance basis. The shared core and deterministic generation checks continue
to protect experimental adapters against structural and semantic drift.

This decision supersedes the three-environment release-completion requirements
in D-013 and D-014, and the corresponding release-gating validation language
in `DELIBERATION_MANIFEST.md` and `docs/ARCHITECTURE.md`. It retains their
one-core, three-adapter architecture.

## D-034 — Publish Codex through a self-updating Git marketplace installer

- **Date:** 2026-07-20
- **Status:** Accepted

### Context

Codex Desktop is the supported environment, but the generated Codex plugin
still requires users to clone the repository or configure its marketplace
manually. Codex can add and refresh a Git marketplace by repository shorthand,
while the CLI exposes marketplace refresh but no separate plugin-upgrade
command.

### Decision

Generate a repository-root Codex marketplace at
`.agents/plugins/marketplace.json` that lists `plugins/deliberation`. Add
tracked `install.ps1` and `install.sh` entrypoints. Both install from
`fpiechowski/deliberation` at `master`; a repeated run refreshes the marketplace
and replaces the installed `deliberation@deliberation` plugin.

Use PowerShell as the supported Windows/Codex Desktop entrypoint and provide
the POSIX shell equivalent. Increment the shared development version to
`0.1.0-dev.3`. Do not add release automation, a package registry, a new
dependency, or a stable-tag channel in this milestone.

### Consequences

Users can install without a manual clone or local plugin source, although Codex
maintains its own Git marketplace snapshot. The installer intentionally follows
mutable `master`, so README must state that trust boundary and link to the
scripts. It must never remove an installed plugin before marketplace refresh
succeeds, and it must state recovery steps if reinstalling fails.

The retained `0.1.0-dev.3` Codex Desktop marketplace run passes. The raw
GitHub PowerShell command added the marketplace from the Git source, installed
the enabled `deliberation@deliberation` plugin at `0.1.0-dev.3`, and then
refreshed, removed, and reinstalled it successfully on a repeated run.

## D-035 — Make Deliberation Loop transitions observable without templating conversation

- **Date:** 2026-07-20
- **Status:** Accepted

### Context

The Deliberation Loop is observable today through transcript interpretation,
but a user cannot reliably see which part of the loop the agent considers
active. Requiring a fixed sequence of headings in every response would make
the mode bureaucratic and would let a declaration stand in for the underlying
behaviour.

### Decision

Signal concise, localized main phase boundaries in ordinary Deliberation:
understanding and gathering, planning, checkpoint, approved execution, and
result walkthrough with verification and roadmap update. The signal is a
process cue, not a mandatory response layout.

Allow a user in active Deliberation to enable a detailed loop trace through a
natural-language request. Keep it active for the current conversation until
the user asks to hide it or exits Deliberation. The detailed trace exposes each
actual canonical stage, including Propose, Explain, Alternatives, Discuss,
Decision, and Approval inside a checkpoint. It must distinguish a checkpoint
that is not required, questions, revisions, rejection, and explicit approval.
Hiding the trace does not exit Deliberation; exiting Deliberation hides it.

Keep canonical stage identifiers in English for documentation and validation,
but render user-facing labels in the language of the conversation. Preserve
this preference across tasks and resumption of the same conversation.

Increment the shared development version to `0.1.0-dev.4`, regenerate all
publication packages, add transcript fixtures and C-17, and validate the
changed contract first in Codex Desktop. Experimental adapters remain outside
the live-host validation scope.

### Consequences

Users can observe the method without adopting a prescribed writing style. Test
evidence must independently confirm the agent's actions; labels alone cannot
pass a scenario. The core and all generated adapters share the same contract,
while the host may choose its native progress or commentary surface for the
short signals.

## D-036 — Require a visible roadmap before the first checkpoint

- **Date:** 2026-07-20
- **Status:** Accepted

### Context

Two manual Codex Desktop trials reached a checkpoint after inspection without a
roadmap in the main response. In one shape the only plan-like signal was a
detailed trace. This makes the objective's foreseeable scope and the boundary
of the requested approval hard to observe, even though a Planning label may be
present.

### Decision

For every new objective, after gathering the information needed to plan,
Deliberation presents a visible provisional roadmap in the main substantive
conversation content before the first checkpoint or consequential execution.
The roadmap shows the currently foreseeable scope as ordered milestones,
identifies the milestone developed now, and names known later decisions or
uncertainties. A simple objective uses one concise milestone.

The roadmap remains provisional and is distinct from approval scope: by
default, approval covers only the current milestone. Before a later-milestone
checkpoint, show the current roadmap. When Choice, Consequence, or Drift
changes it, show the revision and its impact before that checkpoint. Do not
repeat it mechanically during questions or discussion within the same open
checkpoint.

A Planning marker, `[Plan]` detailed-trace entry, commentary, or progress
surface cannot be the sole roadmap. Preserve D-009 as the original roadmap and
bounded-approval decision; this decision strengthens its required visibility
and ordering.

Increment the shared development version to `0.1.0-dev.5`, regenerate all
publication surfaces, and add Polish regression coverage without detailed trace
or user-authored roadmap wording. The next live-host evidence run covers
ordinary visibility, detailed trace, and roadmap-before-checkpoint fixtures in
Codex Desktop.

### Consequences

Users see the scope of the whole objective before being asked to authorize its
current step. The contract does not impose a response template or multiply
milestones, but it makes ordering, provisionality, and approval boundaries
testable independently of trace rendering.

## D-037 — Make journey consideration explicit at every checkpoint

- **Date:** 2026-07-24
- **Status:** Accepted

### Context

The existing journey-based explanation rule names several dynamic subjects, but
does not make the agent's decision visible when a checkpoint does not need a
journey. This can make a valid omission look like the technique was forgotten,
and it gives the user no direct way to request the explanation when they prefer
it.

### Decision

At every checkpoint, require the agent to consider whether a journey-based
explanation would materially improve understanding of the decision or proposed
milestone. Include the appropriate user, request, data, or execution journey
when it would help. When it would not, briefly explain why it is being omitted
and explicitly offer it as an optional explanation. If the user requests it,
provide the journey before seeking approval. Do not force a journey when it adds
no clarity.

Increment the shared development version to `0.1.0-dev.6`, regenerate all
publication surfaces, add a fixture for the explicit optional-offer case, and
validate the changed contract in the supported Codex Desktop environment.

### Consequences

Journey use becomes more observable and user-controllable without turning it
into a mandatory response template. Every checkpoint communicates whether the
technique was considered; users can request it before approval even when the
agent initially recommends omitting it. The journey remains conditional in
content, so small mechanical changes do not acquire unnecessary ceremony.
