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
By default, invoking Deliberation applies it only to the task in that prompt;
users can explicitly request that it remain active for the conversation.
For every new objective, it shows a provisional roadmap in the main
conversation content after gathering and before a checkpoint or consequential
execution; the roadmap remains distinct from the scope being approved.

## Project status

Product definition, interaction design, and the cross-environment package
architecture are complete. The canonical skill core, host adapter templates,
deterministic standard-library assembler, semantic-integrity checks, and
validation-fixture skeleton are implemented. Generated publication packages
are present under `dist/codex/`, `dist/claude-code/`, and `dist/opencode/`.

The assembler writes complete local previews under ignored `build/` output;
release archives and checksums are written under ignored `build/release/`.
Repository publication surfaces are synchronized explicitly and validated
against fresh deterministic assembly. A generated Claude Code marketplace
catalog is present at `.claude-plugin/marketplace.json`; a generated Codex
marketplace catalog is present at `.agents/plugins/marketplace.json`. Tag-based
release automation validates the repository, builds the OpenCode release asset
and checksum, and creates a draft GitHub Release.

Standalone Codex desktop activation evidence is recorded under
`validation/runs/`. The retained `0.1.0-dev.0` failure led to an activation
acknowledgement clarification; the `0.1.0-dev.1` rerun passes C-01 and A-01.
The standalone desktop checkpoint fixture also passes C-03, C-04, C-06, and
C-07.
The retained desktop lifetime-and-exit fixture passed the former
conversation-wide contract. The current task-scoped and explicit
persistent-scope replacement requires fresh desktop evidence.
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

Version `0.1.0-dev.11` makes every checkpoint a visible design preview: it
contains a light milestone brief, an initial proposal, representative code or
design artefacts before approval, and contextual suggestions for the next user
message under a localized “Suggested next step” heading. Each block explicitly
invites a suggestion or free-text reply. The A–D labels remain optional
shortcuts, including a broad B for a change or another next step; only a clearly
named Accept action authorizes work. In the alternative view, the same framing
applies to explaining or choosing a named alternative, another next step,
finding more alternatives, and accepting the marked current recommendation.
The canonical skill entry point explicitly loads its modular runtime contract from
`core/deliberation/references/`. The OpenCode adapter now includes an
installable local command-and-plugin bundle under `dist/opencode/`.

Version `0.1.0-dev.13` adds `explain`, a separate explicit skill for explaining
a technical topic without activating Deliberation, creating files, or opening a
checkpoint. It uses the same concise four-question model and an appropriate
journey for dynamic subjects. Its cross-environment fixture skeletons and
deterministic package validation are included; live-host validation is a later
optional milestone.

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

Build the release assets locally with:

```text
python tooling/deliberation.py package-release
```

Regenerate the repository publication surfaces after changing the canonical
core, an adapter template, or `VERSION` with:

```text
python tooling/deliberation.py sync-publication
```

## Codex installation

The following commands add or refresh the Deliberation marketplace from the
immutable `v0.1.0-dev.14` tag, then install or update the plugin. They do not
require a manual clone or local plugin source; Codex stores its own marketplace
snapshot.

PowerShell (Windows):

```powershell
irm https://raw.githubusercontent.com/fpiechowski/deliberation/v0.1.0-dev.14/install.ps1 | iex
```

POSIX shell (macOS, Linux, Git Bash, or WSL):

```sh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/fpiechowski/deliberation/v0.1.0-dev.14/install.sh)"
```

Both commands execute scripts from the immutable release tag. Review the
linked scripts before running them if you do not want to trust remote code.
After installation or update, start a new Codex conversation or restart Codex
Desktop, then activate the mode with `$deliberation`.
For a standalone explanation, invoke `$explain <topic>`.

The PowerShell path was verified against the GitHub marketplace with
`0.1.0-dev.3`, including a repeated-run update.

These Codex installers add the repository as a Git marketplace; they do not
download an archive or copy a local plugin directory. The archive/copy
installer is retained only for OpenCode below.

## Experimental Claude Code installation

Claude Code is an experimental adapter and is not live-host validated or
release-gating. The marketplace is available for early adopters.

Add this GitHub repository as a marketplace, then install the plugin:

```text
/plugin marketplace add fpiechowski/deliberation
/plugin install deliberation@deliberation
```

The same Git-marketplace installation is available as a one-line POSIX shell
command:

```sh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/fpiechowski/deliberation/v0.1.0-dev.14/install-claude-code.sh)"
```

The script adds or updates the GitHub marketplace and installs or updates the
user-scope plugin. It does not download an archive or copy files locally.
If the plugin exists only at project or local scope, the script installs a
separate user-scope copy instead of attempting a user-scope update.

After installation, activate the mode with:

```text
/deliberation:deliberation
```

For a standalone explanation, invoke the corresponding `/explain` skill.

## Experimental OpenCode installation

OpenCode is an experimental adapter and is not live-host behaviour validated.
The ready dist is generated under `dist/opencode`.

PowerShell one-line install from the current release asset:

```powershell
irm https://raw.githubusercontent.com/fpiechowski/deliberation/v0.1.0-dev.14/install-opencode.ps1 | iex
```

POSIX shell one-line install from the current release asset:

```sh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/fpiechowski/deliberation/v0.1.0-dev.14/install-opencode.sh)"
```

For one project instead of global OpenCode config:

```powershell
iex "& { $(irm https://raw.githubusercontent.com/fpiechowski/deliberation/v0.1.0-dev.14/install-opencode.ps1) } -Scope Project -ProjectPath 'C:\path\to\project'"
```

or:

```sh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/fpiechowski/deliberation/v0.1.0-dev.14/install-opencode.sh)" sh project /path/to/project
```

Both commands execute the versioned wrapper script. The wrapper downloads the
published `v0.1.0-dev.14` OpenCode zip from GitHub Releases, extracts it to a
temporary directory, runs the bundled installer, and removes the temporary
files. The draft release must be published before this channel is usable.

Install globally from that directory:

```powershell
.\install.ps1
```

or:

```sh
sh ./install.sh
```

Install into one project:

```powershell
.\install.ps1 -Scope Project -ProjectPath C:\path\to\project
```

or:

```sh
sh ./install.sh project /path/to/project
```

After installation, activate the mode with:

```text
/deliberation
```

For a standalone explanation, invoke `/explain <topic>`.

## Repository guide

- [`AGENTS.md`](AGENTS.md) — instructions for Codex sessions working on this
  repository.
- [`docs/MANIFEST.md`](docs/MANIFEST.md) — product vision, context, and behavioural
  principles.
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — accepted shared-core,
  adapter, distribution, versioning, and validation architecture.
- [`docs/ACCEPTANCE.md`](docs/ACCEPTANCE.md) — observable
  acceptance scenarios and critical failure cases.
- [`docs/TODO.md`](docs/TODO.md) — current next steps and open questions.
- [`core/deliberation/SKILL.md`](core/deliberation/SKILL.md) — canonical
  behavioural entry point and links to the modular runtime source for all
  environments.
- [`core/explain/SKILL.md`](core/explain/SKILL.md) — canonical standalone
  explanation skill for all environments.
- [`tooling/deliberation.py`](tooling/deliberation.py) — deterministic
  assembler, publication synchronizer, and integrity validator.
