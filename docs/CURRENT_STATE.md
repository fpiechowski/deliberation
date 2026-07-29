# Current State

**Last updated:** 2026-07-29

## Phase

OpenCode distribution packaging — **`0.1.0-dev.10` adds an installable
OpenCode command-and-plugin bundle while preserving explicit `/deliberation`
activation and experimental adapter status**.

## Completed

- Selected **Deliberation** as the working product and plugin name.
- Defined the product as a cross-cutting work mode rather than a task-specific
  coding skill.
- Captured the product vision and high-level behavioural principles in
  `DELIBERATION_MANIFEST.md`.
- Distilled the original design conversation into durable project context and
  decisions.
- Prepared the repository for continuity across Codex sessions.
- Defined the mode lifetime: activation applies to the current conversation
  until the user explicitly disables it.
- Added journey-based explanation as a conditional technique for explaining
  dynamic code, design, and system behaviour.
- Defined milestones as bounded units of verifiable progress and checkpoints as
  decision-ready deliberation that ends with approval.
- Distinguished explanation before approval from the walkthrough and
  verification of the implemented result.
- Defined milestone planning as a provisional roadmap with detailed
  deliberation and default approval limited to the next milestone.
- Defined checkpoint triggers through Choice, Consequence, and Drift tests, and
  required related decisions to be grouped to limit approval fatigue.
- Defined the semantic content of checkpoints, intent-based response handling,
  bounded broad approval, and explicit mode exit when checkpoints are waived.
- Defined lightweight conversational state, conditional durable tracking,
  progress updates, result walkthroughs, and honest completion reporting.
- Selected `deliberation` as the primary skill name with explicit activation.
- Expanded the product to one shared behavioural core with distribution
  adapters for Codex, Claude Code, and OpenCode.
- Defined platform-neutral, cross-task-type, and adapter-specific behavioural
  scenarios with critical failure cases and decision traceability.
- Closed the product-definition and interaction-design phase.
- Approved the cross-environment package architecture.
- Selected one canonical Agent Skills-compatible core with deterministically
  generated Codex, Claude Code, and OpenCode adapters.
- Defined self-contained, committed publication packages for Git-hosted
  marketplaces and untracked temporary build output.
- Defined shared SemVer, structural validation, semantic-integrity checks, and
  transcript-based cross-environment fixtures.
- Implemented the canonical Agent Skills-compatible core at
  `core/deliberation/SKILL.md`.
- Added Codex, Claude Code, and OpenCode adapter templates.
- Added a deterministic Python 3 standard-library assembler and integrity
  validator.
- Added fixture metadata schema plus one core and three activation fixture
  skeletons.
- Established `0.1.0-dev.0` as the shared development version.
- Promoted the generated Codex, Claude Code, and OpenCode packages to the
  repository publication surfaces.
- Added explicit publication synchronization and exact stale-generation
  validation for missing, extra, and changed generated files.
- Defined a temporary user-scope installation, transcript evidence, structured
  verdict, and cleanup boundary for standalone Codex desktop validation.
- Executed the Codex explicit-activation fixture in the desktop app and recorded
  the first live-host transcript and result.
- Clarified the canonical activation acknowledgement, incremented the shared
  version to `0.1.0-dev.1`, regenerated every adapter, and preserved the failed
  `0.1.0-dev.0` run.
- Reran the standalone Codex desktop activation fixture successfully against
  C-01 and A-01.
- Executed the core checkpoint fixture successfully in standalone Codex
  desktop against C-03, C-04, C-06, and C-07.
- Added and passed a two-conversation Codex Desktop fixture for
  conversation-wide lifetime and explicit exit against C-02 and C-15.
- Added and passed a multi-turn Codex Desktop fixture for response intent and
  bounded broad approval against C-10 and C-11.
- Added and passed a staged Codex Desktop fixture for Drift during execution
  and routine-work boundaries against C-08 and C-09.
- Added and passed a real-file Codex Desktop execution fixture for progress
  updates, result walkthrough, and achieved/unmet completion against C-12,
  C-13, and C-14.
- Added and passed a specification fixture for journey-based explanation,
  conditional durable state, and real archive-and-resume continuity against
  C-05, C-16, and A-04.
- Added and passed a real-file Implementation fixture for pre-edit planning,
  checkpoint communication, mid-execution Drift, routine completion, and
  result walkthrough against C-03, C-04, C-08, C-09, and C-13.
- Added and passed a seeded real-file Debugging fixture for diagnosis before
  editing, a material Choice, incompatible-contract Drift, routine correction,
  and honest achieved and blocked completion against C-06, C-08, C-09, and
  C-14.
- Added and passed a seeded real-file Refactoring fixture for a complete
  pre-edit checkpoint, a public compatibility Choice and Consequence, preserved
  behavior, result walkthrough, and a routine local correction against C-04,
  C-06, C-07, and C-13.
- Added and passed a seeded real-file Review fixture for a request journey,
  consequential release-recommendation checkpoint, question and revision
  intent handling, bounded artifact creation, and final walkthrough against
  C-04, C-05, C-10, and C-13.
- Executed an additional Polish-language specification fixture whose first
  message combines `$deliberation` and a short task without roadmap or
  checkpoint instructions. The run passes autonomous planning and bounded
  execution in C-03, but fails C-01 and C-04 because the activation
  acknowledgement omits the explicit-until-disabled boundary and the initial
  checkpoint omits response alternatives and a complete negative approval
  boundary.
- Prioritized and added a generated root Claude Code marketplace catalog that
  references the committed Claude Code plugin and is checked for freshness,
  structure, version, and source integrity.
- Approved the focused Codex Desktop correction for the Polish combined
  invocation-and-task fixture.
- Passed the rerun of the Polish combined invocation-and-task fixture against
  C-01, C-03, C-04, and A-01 with `0.1.0-dev.2`.
- Added localized main-phase visibility and a natural-language, conversation
  scoped detailed-loop trace to the canonical contract.
- Added transcript fixture skeletons for normal loop visibility and detailed
  trace transitions, including trace-only exit and checkpoint response intent.
- Regenerated every publication package at `0.1.0-dev.4` and passed the
  deterministic assembly, semantic-integrity, fixture, and stale-output check.
- Strengthened the roadmap contract so every new objective shows a visible,
  ordered provisional roadmap after Gather and before its first checkpoint or
  consequential execution, distinct from the approval scope.
- Strengthened the journey contract so every checkpoint visibly considers
  journey-based explanation, offers it when omitted, and provides it before
  approval when requested.
- Added a core fixture skeleton for the explicit optional journey offer on a
  small mechanical change.
- Added Polish regression coverage that does not request a roadmap or detailed
  trace and fails responses that move from inspection directly to a checkpoint
  or reveal the roadmap only outside the substantive response.
- Regenerated every publication package at `0.1.0-dev.5` and passed the
  deterministic assembly, semantic-integrity, fixture, and stale-output check.
- Added a generated Codex Git marketplace and public PowerShell and POSIX
  installers with `0.1.0-dev.3`.
- Passed the live PowerShell Git-marketplace installation and repeated-run
  update fixture without a manual clone or local plugin source.
- Implemented the approved modular core and `0.1.0-dev.7` checkpoint contract:
  explicit reference modules, light brief and initial proposal, inspectable
  pre-approval artefacts, A–D controls, and Explain-on-A validation fixtures.
- Added a dedicated C — Alternative module that compares the proposed solution
  with meaningful alternatives using concise assessments and a pros/cons table.
- Executed the isolated `0.1.0-dev.8` C — Alternative Codex Desktop fixture;
  the comparison content passed, but the host relabeled the canonical A–D menu
  and the retained run is a truthful `Fail` against C-04 and C-18.
- Replaced the fixed A–D contract with contextual suggestions: ordinary
  proposals offer explanation, changes, alternative exploration, and accepting
  the named proposal; alternative views offer explaining or choosing a named
  alternative, further exploration, and accepting the named recommendation.
- Attempted the isolated `0.1.0-dev.9` contextual-suggestion fixture, but the
  fresh task reported `$deliberation` unavailable; the retained result is
  `Blocked` and does not evaluate the new behavior.
- Added an installable OpenCode distribution bundle at
  `opencode-bundles/deliberation` with `.opencode/commands/deliberation.md`,
  `.opencode/plugins/deliberation.js`, `package.json`, `README.md`, and
  PowerShell/POSIX installers for global or project installation.
- Verified the OpenCode bundle against the local `opencode` CLI by resolving a
  temporary config directory: `/deliberation` is discovered as a command and the
  local plugin file is resolved by the host configuration.

## Current implementation

The canonical core, adapter templates, repository-local assembly tooling, and
three generated publication packages are implemented.
`python tooling/deliberation.py assemble` generates and validates standalone
and publication previews under ignored `build/` output.
`python tooling/deliberation.py sync-publication` replaces the three
repository publication packages with freshly validated assembly.
`python tooling/deliberation.py check` independently assembles twice, proves
deterministic output, validates host structure and explicit-only activation,
compares every normalized runtime payload with the canonical core, and fails
when any committed generated file is missing, extra, or changed.

Retained live-host evidence under `validation/runs/` includes the
`0.1.0-dev.0` failure and the corrective `0.1.0-dev.1` pass for the standalone
Codex desktop activation fixture. The passing run proves standalone discovery,
suppression of implicit activation, explicit `$deliberation` invocation,
conversation-wide lifetime through explicit exit, bounded milestones, and a
pre-edit checkpoint.

The standalone desktop checkpoint run also proves provisional roadmap
presentation, next-milestone detail, material Choice and Consequence handling,
explicit approval scope, and a pause before implementation.

The standalone desktop lifetime-and-exit run proves continuity across different
tasks without reinvocation, inactive state in a fresh conversation,
natural-language exit acknowledgement, and removal of the checkpoint contract
from the following response.

The standalone desktop response-intent run proves question, revision,
ambiguity, rejection, and approval handling against one evolving checkpoint.
It also proves bounded batch authorization without repeated approval or leakage
into a later task.

The standalone desktop Drift run proves that new public-contract requirements
stop an approved milestone already in progress, reopen a decision-ready
checkpoint, and allow the revised routine remainder and local corrections to
finish without approval fatigue.

The standalone desktop execution-lifecycle run proves meaningful progress
updates, independently repeated unit and smoke verification, a complete success
report, continued mode state, and an exact blocked report for an impossible
follow-up.

The standalone desktop journey-and-state run proves a trigger-to-outcome
explanation of dynamic behaviour, conversational state without unauthorized
files, explicitly authorized durable tracking, and preservation of active mode,
accepted decisions, roadmap, and approval scope after the same task is archived
and reopened.

Taken together, the retained standalone runs now provide direct passing
evidence for every core scenario C-01–C-16, Codex activation A-01, and
desktop resumed-conversation continuity A-04. The Specification row of the
cross-task-type acceptance matrix is complete.

The representative desktop Implementation run proves that the same behavioural
loop applies during real code changes: no files appeared before approval, the
approved first part completed and verified independently, a newly disclosed
public persisted-data contract reopened a Drift checkpoint before further
edits, and the revised implementation, smoke check, walkthrough, and final
local test cleanup completed without approval fatigue.

The representative desktop Debugging run proves that Codex can diagnose from
evidence without prematurely editing, surface unresolved product semantics,
implement only an approved focused fix, and stop again when compatibility
evidence invalidates that fix. It then completes the revised repair and routine
validation without approval fatigue, reports the achieved task completely, and
honestly blocks a separate task when its required production trace is absent.

The representative desktop Refactoring run proves that Codex checkpoints a
material refactoring boundary before editing, recommends a compatibility-safe
internal model over a breaking public migration, preserves the public function
and observable behavior, explains and verifies the resulting structure, and
applies a later private test cleanup without an artificial checkpoint.

The representative desktop Review run proves that Codex can explain reviewed
behavior as a request journey, distinguish observed behavior from a
consequential release recommendation, keep a positive-prefaced question inside
the checkpoint, revise the recommendation when the user adds a material
migration condition, and create only the approved review artifact before
walking through the result.

All five cross-task-type acceptance rows — Specification, Implementation,
Debugging, Refactoring, and Review — have passing standalone Codex Desktop
evidence. Together with direct C-01–C-16 coverage and passing A-01 and A-04,
this completes the currently approved desktop-only live-host slice.

The later `core-polish-single-message-specification` run intentionally adds a
stricter natural-use shape beyond those baseline fixtures. The retained
`0.1.0-dev.1` run fails C-01 and C-04 for omissions in the activation
acknowledgement and checkpoint. The focused `0.1.0-dev.2` clarification makes
both obligations explicit for a combined first message; its rerun passes C-01,
C-03, C-04, and A-01 in Polish, pauses before execution, and completes only
the approved first milestone.

Codex Desktop is the sole live-host-validated and supported environment. Claude
Code and OpenCode remain experimental distribution adapters: they are generated
from the same canonical core and may be published, but do not require live-host
validation or determine release completion. Codex CLI, the IDE extension, and
other clients are outside the current support scope.

The repository now contains a generated root Claude Code marketplace catalog
that exposes the generated `claude-plugins/deliberation` package. It uses the
marketplace and plugin name `deliberation` and the owner name Filip Piechowski.
The repository now also contains a generated Codex marketplace catalog at
`.agents/plugins/marketplace.json` and PowerShell and POSIX installation
scripts. The retained `0.1.0-dev.3` PowerShell run proves that the public raw
GitHub installer adds the Git marketplace, installs the plugin without a manual
clone or local source path, and updates it successfully on a repeated run.
Release automation is not included. The Claude Code marketplace has been
confirmed working externally, but no retained live-host transcript is required
under the experimental-adapter policy.

The generated OpenCode bundle is now installable as a local command-and-plugin
package. Its command remains the only activation surface and embeds the full
canonical contract. Its plugin is a minimal local OpenCode plugin marker rather
than an npm-published runtime extension. OpenCode remains experimental: the
local CLI discovery check proves packaging, not behavioural scenario support.

The shared core now also has an observable-loop contract. Ordinary
Deliberation signals main phase boundaries without constraining response
format. A user can request a detailed trace for the conversation, which makes
actual transitions through the loop visible while preserving the distinction
between a label and evidence of behaviour. The trace is disabled separately
from Deliberation and is preserved when the same conversation resumes.

Every new objective now receives a visible, provisional roadmap in the main
substantive response after planning information is gathered and before any
checkpoint or consequential execution. It covers the foreseeable objective
scope, current milestone, and known later uncertainty without turning the
roadmap into approval; it is revised before a later checkpoint when material
new information changes it. A phase marker or detailed trace cannot be the
only roadmap.

The canonical core is now organized as an Agent Skills-compatible `SKILL.md`
entry point with explicitly linked modules for activation/state, the
Deliberation Loop, checkpoints, Explain, and execution/results. Generated
Codex and Claude packages retain the same reference tree; the self-contained
OpenCode command embeds the entry point and all modules.

At every checkpoint, Deliberation shows a light brief, initial proposal,
representative code or equivalent design artefacts, and contextual suggestions
for the next user message. They are optional shortcuts; a user may always reply
in free text. Only a plainly labeled Accept action or equally unambiguous
free-text instruction authorizes the exact named proposal and scope.

When alternatives are requested, the `alternative.md` module compares the
current proposal with two to four meaningful approaches. It requires a short
explanation and assessment of each, a compact advantages/disadvantages table,
and a named recommendation with the decisive tradeoff. Its contextual
suggestions let the user explain or choose a named alternative, find more, or
accept that recommendation.

The retained live-host run at
`validation/runs/0.1.0-dev.8/codex/desktop-standalone/core-checkpoint-alternative-comparison/`
shows that the comparison itself works but that fixed letter meanings are not a
reliable host-level contract. It motivated the contextual-suggestion model.


## Recommended next milestone

Restore standalone skill discovery in Codex Desktop, then rerun the structured
checkpoint and alternative-comparison fixtures against `0.1.0-dev.10`. This does
not reopen validation for experimental adapters.

## Open questions

No unresolved product-contract or architecture questions are currently known.

Release automation and a stable tag-based installation channel remain later
decisions.

## Repository hygiene

The `.idea/` directory is currently untracked and is treated as user-owned IDE
state. Do not add, modify, or remove it unless the user explicitly asks.
