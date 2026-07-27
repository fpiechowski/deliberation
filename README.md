# Deliberation

Deliberation is a coding-agent work mode, validated in Codex Desktop, that turns
an autonomous workflow into an incremental, consultative collaboration.

Instead of completing a large task in one opaque run, the agent decomposes it
into meaningful steps. At each consequential checkpoint it proposes a
direction, explains the reasoning and realistic alternatives, reaches a
decision with the user, waits for approval, and then executes the approved
step.

The mode is intended to work across:

- Specification and planning.
- Implementation and refactoring.
- Debugging.
- Code and pull-request review.

The first version uses one shared Agent Skills-compatible behavioural core and
thin environment-specific adapters. Codex Desktop is supported and live-host
validated; Claude Code and OpenCode are experimental adapters.

Knowledge transfer and shared understanding are first-class outcomes alongside
the quality of the completed work.

Deliberation also makes its main loop boundaries visible. A user can ask in
natural language to show a detailed stage trace for the current conversation;
this aids review and validation without imposing a fixed response template.
For every new objective, it shows a provisional roadmap in the main
conversation content after gathering and before a checkpoint or consequential
execution; the roadmap remains distinct from the scope being approved.

## Project status

Product definition, interaction design, and the cross-environment package
architecture are complete. The canonical skill core, host adapter templates,
deterministic standard-library assembler, semantic-integrity checks, and
validation-fixture skeleton are implemented. Generated publication packages
are present under `plugins/`, `claude-plugins/`, and `opencode-bundles/`.

The assembler writes complete local previews under ignored `build/` output.
Repository publication surfaces are synchronized explicitly and validated
against fresh deterministic assembly. A generated Claude Code marketplace
catalog is present at `.claude-plugin/marketplace.json`; a generated Codex
marketplace catalog is present at `.agents/plugins/marketplace.json`. Release
automation is not present yet.

Standalone Codex desktop activation evidence is recorded under
`validation/runs/`. The retained `0.1.0-dev.0` failure led to an activation
acknowledgement clarification; the `0.1.0-dev.1` rerun passes C-01 and A-01.
The standalone desktop checkpoint fixture also passes C-03, C-04, C-06, and
C-07.
The desktop lifetime-and-exit fixture passes C-02 and C-15 across two fresh
conversations.
The desktop response-intent and broad-approval fixture passes C-10 and C-11.
The staged desktop Drift and routine-execution fixture passes C-08 and C-09.
The real-file desktop execution-lifecycle fixture passes C-12, C-13, and C-14.
The desktop journey, durable-state, and resumed-conversation fixture passes
C-05, C-16, and A-04. Together, the retained desktop runs cover every core
scenario C-01–C-16 and complete the Specification row of cross-task-type
acceptance.
The real-file desktop Implementation fixture passes C-03, C-04, C-08, C-09,
and C-13 in an implementation context.
The seeded real-file desktop Debugging fixture passes C-06, C-08, C-09, and
C-14 in a debugging context.
The seeded real-file desktop Refactoring fixture passes C-04, C-06, C-07, and
C-13 in a refactoring context.
The seeded real-file desktop Review fixture passes C-04, C-05, C-10, and C-13
in a review context.

All five cross-task-type rows now pass in standalone Codex Desktop. Together
with direct C-01–C-16, A-01, and A-04 evidence, the current desktop-only
live-host validation scope is complete.

The additional Polish natural-use fixture now passes with `0.1.0-dev.2` after
the combined invocation-and-task acknowledgement and checkpoint contract was
made explicit.

Version `0.1.0-dev.9` makes every checkpoint a visible design preview: it
contains a light milestone brief, an initial proposal, representative code or
design artefacts before approval, and contextual suggestions for the next user
message. They are not a rigid letter protocol: users may respond freely, while
only a clearly named Accept action authorizes work. In the alternative view,
the suggestions cover explaining or choosing a named alternative, finding more
alternatives, and accepting the marked current recommendation. The canonical
skill entry point explicitly loads its modular runtime contract from
`core/deliberation/references/`.

Codex Desktop is the only live-host-validated and supported environment. CLI,
IDE, and other Codex clients are out of scope. Claude Code and OpenCode are
experimental adapters and are not release-gating.

Run the implementation checks with:

```text
python tooling/deliberation.py check
```

Generate and validate local host artifacts with:

```text
python tooling/deliberation.py assemble
```

Regenerate the repository publication surfaces after changing the canonical
core, an adapter template, or `VERSION` with:

```text
python tooling/deliberation.py sync-publication
```

## Codex installation

The following commands add or refresh the Deliberation marketplace from the
current `master` branch, then install or update the plugin. They do not require
a manual clone or local plugin source; Codex stores its own marketplace snapshot.

PowerShell (Windows):

```powershell
irm https://raw.githubusercontent.com/fpiechowski/deliberation/master/install.ps1 | iex
```

POSIX shell (macOS, Linux, Git Bash, or WSL):

```sh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/fpiechowski/deliberation/master/install.sh)"
```

Both commands execute the current scripts from `master`. Review the linked
scripts before running them if you do not want to trust mutable remote code.
After installation or update, start a new Codex conversation or restart Codex
Desktop, then activate the mode with `$deliberation`.

The PowerShell path was verified against the GitHub marketplace with
`0.1.0-dev.3`, including a repeated-run update.

## Experimental Claude Code installation

Claude Code is an experimental adapter and is not live-host validated or
release-gating. The marketplace is available for early adopters.

Add this GitHub repository as a marketplace, then install the plugin:

```text
/plugin marketplace add fpiechowski/deliberation
/plugin install deliberation@deliberation
```

After installation, activate the mode with:

```text
/deliberation:deliberation
```

## Repository guide

- [`AGENTS.md`](AGENTS.md) — instructions for Codex sessions working on this
  repository.
- [`DELIBERATION_MANIFEST.md`](DELIBERATION_MANIFEST.md) — product vision and
  behavioural principles.
- [`docs/PROJECT_CONTEXT.md`](docs/PROJECT_CONTEXT.md) — the reasoning and
  background that led to the current direction.
- [`docs/DECISIONS.md`](docs/DECISIONS.md) — durable decision log.
- [`docs/BEHAVIORAL_SCENARIOS.md`](docs/BEHAVIORAL_SCENARIOS.md) — observable
  acceptance scenarios and critical failure cases.
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — accepted shared-core,
  adapter, distribution, versioning, and validation architecture.
- [`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md) — current phase, open
  questions, and the recommended next milestone.
- [`core/deliberation/SKILL.md`](core/deliberation/SKILL.md) — canonical
  behavioural entry point and links to the modular runtime source for all
  environments.
- [`tooling/deliberation.py`](tooling/deliberation.py) — deterministic
  assembler, publication synchronizer, and integrity validator.
