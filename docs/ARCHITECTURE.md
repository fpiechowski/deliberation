# Cross-Environment Architecture

**Status:** Accepted  
**Accepted:** 2026-07-19

## Purpose

Deliberation is implemented from one canonical behavioural core and distributed
through thin adapters for Codex, Claude Code, and OpenCode.

The architecture must preserve one product contract while accommodating
host-specific invocation, metadata, packaging, installation, and validation.
It must also prevent implicit activation in the explicit-only first release.

## Architectural principles

1. The shared core is the only hand-authored source of Deliberation semantics.
2. Adapters may change invocation and packaging, but not milestones,
   checkpoints, approval, continuation, exit, or completion semantics.
3. Published packages are self-contained because installed plugins cannot rely
   on files outside their package directory.
4. Published packages are generated rather than edited by hand.
5. Generated marketplace packages are committed so a Git-hosted marketplace
   can install them directly from the repository.
6. Deterministic validation detects semantic drift between the core and every
   generated adapter.
7. The first version introduces no runtime service, MCP server, or third-party
   build dependency. The OpenCode local plugin marker is allowed only as
   installable distribution plumbing and does not change product semantics.

## Repository topology

The intended source and publication layout is:

```text
core/
├── shared/
│   └── explain-model.md          # shared Explain source
├── deliberation/
    ├── SKILL.md                   # entry point and explicit module links
    └── references/                # hand-authored runtime modules
└── explain/
    ├── SKILL.md                   # standalone explanation entry point
    └── references/                # hand-authored explanation model

adapters/
├── codex/
├── claude-code/
└── opencode/

plugins/
└── deliberation/                    # generated Codex plugin

claude-plugins/
└── deliberation/                    # generated Claude Code plugin

opencode-bundles/
└── deliberation/                    # generated OpenCode command-and-plugin bundle

validation/
├── fixtures/
│   ├── core/
│   └── adapters/
├── schemas/
└── runs/

tooling/

.agents/plugins/marketplace.json      # generated Codex marketplace catalog
.claude-plugin/marketplace.json       # generated Claude Code marketplace catalog
install.ps1                            # Codex Git-marketplace installer
install.sh                             # Codex POSIX Git-marketplace installer
install-claude-code.sh                 # Claude Code POSIX Git-marketplace installer
install-opencode.ps1                   # OpenCode release-asset wrapper
install-opencode.sh                    # OpenCode POSIX release-asset wrapper
VERSION
```

This is the target topology. The Codex and Claude Code marketplace catalogs and
production packages are committed generated publication surfaces.

The asymmetric publication paths are intentional. Codex's repository
marketplace convention uses `plugins/<plugin-name>`, while a Claude Code
marketplace may reference any in-repository plugin directory through a
relative `source`. Keeping the packages separate prevents host-specific
metadata from contaminating the other adapter.

## Shared behavioural core

`core/deliberation/SKILL.md` is an Agent Skills-compatible skill named
`deliberation`. It is the canonical entry point and explicitly links every
runtime module under `core/deliberation/references/`, instructing the skill to
read the relevant module before acting in that phase. The modules divide
activation/state, the Deliberation Loop, checkpoints, the Explain model, and
execution/results. Together they contain:

- Portable `name` and `description` frontmatter.
- The complete operational behaviour required on every activation.
- The Deliberation loop, task-scoped default lifetime, and explicit
  conversation-wide opt-in.
- Milestone and checkpoint semantics.
- Choice, Consequence, and Drift tests.
- Approval and response-intent handling.
- Progress, result walkthrough, completion, and explicit exit behaviour.

The core is concise and imperative. It does not duplicate the complete product
history, decision log, or scenario suite. Behaviour needed on every turn stays
in the entry point and its explicitly linked runtime modules; validation details
remain outside the runtime skill.

The first core is instruction-only. It has no scripts, assets, external tools,
or runtime dependencies.

`core/explain/SKILL.md` is a second, independent Agent Skills-compatible core
named `explain`. It provides the Explain step for a named topic without
activating Deliberation or its conversation-wide state, checkpoint, approval,
or execution semantics. It uses the same four-question and conditional-journey
teaching model from `core/shared/explain-model.md`, but it is not a delegation
target for an open Deliberation checkpoint: that checkpoint must retain its own
state and approval boundary.

The canonical source skills link the shared source as
`../shared/explain-model.md`. The assembler materializes that one source as
`references/explain-model.md` in each self-contained package, so published
adapters contain no external path while source maintenance has no duplicated
Explain contract.

## Adapter contracts

### Codex

The Codex adapter copies the canonical skill without semantic changes and adds
`agents/openai.yaml` with:

```yaml
policy:
  allow_implicit_invocation: false
```

The local validation artifact can be installed as a standalone skill and
invoked as `$deliberation`.

The published package is generated under `plugins/deliberation/` and contains:

```text
plugins/deliberation/
├── .codex-plugin/
│   └── plugin.json
└── skills/
    └── deliberation/
        ├── SKILL.md
        ├── references/
        └── agents/
            └── openai.yaml
    └── explain/
        ├── SKILL.md
        ├── references/
        └── agents/
            └── openai.yaml
```

The package is listed by `.agents/plugins/marketplace.json`. It does not add
hooks, apps, MCP servers, or connectors in the first version.

### Claude Code

Claude Code controls explicit-only invocation with frontmatter in `SKILL.md`.
The adapter adds:

```yaml
disable-model-invocation: true
```

to the generated copy while leaving the normalized behavioural body unchanged.

Two artifacts are produced:

1. A standalone skill for early local validation, invoked as `/deliberation`.
2. A plugin under `claude-plugins/deliberation/`, invoked through the
   environment's plugin namespace, initially
   `/deliberation:deliberation`.

The published plugin contains:

```text
claude-plugins/deliberation/
├── .claude-plugin/
│   └── plugin.json
    └── skills/
        └── deliberation/
            ├── SKILL.md
            └── references/
        └── explain/
            ├── SKILL.md
            └── references/
```

The eventual root `.claude-plugin/marketplace.json` references it with a
relative source:

```json
{
  "name": "deliberation",
  "source": "./claude-plugins/deliberation"
}
```

The marketplace catalog is named `deliberation`, identifies Filip Piechowski as
its owner, uses the shared product version, and references the generated plugin
with `./claude-plugins/deliberation`. It is generated from the Claude adapter
template and validated with the rest of the publication surfaces.

The generated Claude package is committed. This is required for users who add
the repository itself as a Git marketplace because Claude Code resolves
relative plugin sources against its cloned marketplace checkout. The installed
plugin is self-contained and never references `../../core`.

Codex and Claude Code are installed by adding this repository as a Git
marketplace and then installing the named plugin from that marketplace. Their
root installers do not download archives or copy plugin files. OpenCode is the
only adapter that retains a download-and-copy installer because its published
distribution is a release asset rather than a native Git marketplace.

### OpenCode

OpenCode exposes installed skills to the model through its native `skill` tool
but does not provide a per-skill equivalent of Codex
`allow_implicit_invocation` or Claude Code `disable-model-invocation`.

The first release therefore does not install Deliberation into an OpenCode
skill discovery directory. Instead, the adapter generates an explicit custom
command:

```text
.opencode/commands/deliberation.md
```

The command embeds the normalized behavioural content of the canonical entry
point and all linked modules. Invoking `/deliberation` injects that complete
contract into the current conversation.
Ordinary engineering prompts do not expose Deliberation as an automatically
loadable OpenCode skill.

The same bundle also includes `.opencode/commands/explain.md`. Invoking
`/explain` injects the self-contained standalone explanation contract; it does
not activate Deliberation. Both canonical audit copies remain outside OpenCode
skill discovery paths.

The generated distribution bundle includes the canonical `SKILL.md` for audit
and portability, but stores it outside OpenCode's discovered skill paths. The
runtime command is self-contained so that both project and global installation
work without fragile absolute or project-relative file references.

The generated distribution bundle also includes:

```text
.opencode/plugins/deliberation.js
package.json
README.md
install.ps1
install.sh
```

The local plugin is a minimal OpenCode plugin marker. It confirms that the
bundle is loadable as an OpenCode plugin distribution and points users to the
explicit `/deliberation` command, but it does not add hooks, tools, implicit
activation, persistent state, or behavioural semantics. The PowerShell and
POSIX installers copy the command and plugin into either the global OpenCode
config directory or one project's `.opencode` directory.

An npm-published OpenCode plugin remains outside the first-release
architecture. It may be reconsidered only if it later provides material runtime
or installation value beyond the local command-and-plugin bundle.

## Assembly and publication

A small repository-local assembler produces every host artifact from the
canonical core and adapter templates.

The assembler:

1. Reads `VERSION`, both canonical skill entry points, and every explicitly
   linked reference module.
2. Applies only the declared host overlay.
3. Writes standalone validation artifacts and self-contained publication
   packages.
4. Injects the same product version into relevant plugin manifests.
5. Emits normalized content information used by integrity validation.

Python 3 with only its standard library is the intended contributor-side
implementation. It is not an end-user runtime requirement and introduces no
third-party package dependency.

Temporary build output remains untracked. The publication surfaces under
`plugins/`, `claude-plugins/`, and `opencode-bundles/` are generated and
committed. A validation command fails when regenerating them would produce a
diff, preventing stale marketplace contents.

## Versioning

The repository uses one product SemVer for:

- The shared core.
- All three adapter outputs.
- Codex and Claude Code plugin manifests.
- The OpenCode distribution bundle.
- Validation evidence for a release candidate.

`VERSION` is the single source of the product version. Host-specific local
cache-busting metadata may be added during development without changing the
product version.

A release regenerates the publication surfaces, validates them, records the
scenario results, commits the generated artifacts, and tags the repository.

The release-readiness workflow at `.github/workflows/release.yml` runs for
`v<SemVer>` tags. It verifies that the tag matches `VERSION`, runs the full
repository check, builds the deterministic OpenCode ZIP and SHA-256 checksum,
and creates a draft GitHub Release. Publishing the draft remains a human
controlled step. The root installers use the same immutable release tag rather
than the mutable default branch.

## Installation paths

Codex Desktop is the release-gating installation and behaviour-validation
surface. The following paths remain available for experimental-adapter work and
are not release-gating:

1. Codex CLI and IDE.
2. Codex plugin through a local repository marketplace.
3. Claude Code standalone skill and plugin through a local or Git-hosted
   marketplace.
4. OpenCode project or global command-and-plugin bundle.

Experimental public distribution does not make a live-host support claim.

## Validation architecture

Validation has three layers.

### Structural validation

Validate:

- Agent Skills frontmatter and naming.
- Codex skill metadata and plugin manifest.
- Claude Code skill frontmatter, plugin manifest, and marketplace catalog.
- OpenCode command format and installation paths.
- Product-version consistency.

Use native host validators where available and repository checks for shared
invariants.

### Semantic integrity

Normalize each generated runtime payload by removing declared host metadata and
wrapping syntax. Compare the remaining behavioural content and complete
reference-module tree with the canonical core.

Validation fails when an adapter:

- Omits or changes core behaviour.
- Adds host-specific product semantics.
- Enables implicit invocation.
- References source files outside its published package.
- Contains a version different from `VERSION`.

### Behavioural fixtures

Each fixture has:

```text
<scenario>/
├── prompt.md
├── context/               # optional synthetic repository context
└── assertions.json
```

`assertions.json` records applicable behavioural scenarios, required observable
signals, forbidden signals, and whether human evaluation is required.

Representative runs record:

```text
validation/runs/<version>/<environment>/<surface>/<scenario>/
├── transcript.md
└── result.json
```

Core fixtures are reused across environments. Adapter fixtures add only
activation, installation, namespace, and continuity conditions specific to a
host.

The first version does not add an LLM-as-judge or a test-framework dependency.
Deterministic checks validate packaging and clear transcript invariants;
decision quality and conversational meaning use the rubric in
`docs/ACCEPTANCE.md`.

Release evidence is retained for synthetic fixtures. Local exploratory runs
may remain untracked.

## Continuity and state

Adapters activate the mode but do not create a separate runtime state store.
The behavioural contract maintains lightweight state in the conversation:

- Active or inactive mode.
- Current objective and provisional roadmap.
- Approved milestone scope.
- Accepted decisions and open questions.
- Detailed-loop-trace preference, when the user enabled it.

Resuming the same conversation must preserve this context through the host's
normal conversation history. If an environment cannot satisfy the continuity
scenario, the result is Blocked and the architecture is revisited rather than
adding silent repository state or weakening the product contract.

## Explicit non-goals for the first release

- Separate behavioural cores per environment.
- Implicit activation.
- Runtime hooks with product semantics, MCP servers, connectors, or background
  services.
- An npm-published OpenCode plugin.
- Automatic persistent state files in user repositories.
- A third-party build or test framework.
- Publishing experimental adapters before their cross-environment scenario
  validation, provided their experimental status is stated plainly.

## Architecture acceptance criteria

The architecture is implemented correctly when:

1. One canonical core produces all runtime variants.
2. All published packages are self-contained.
3. Git-hosted Codex and Claude Code marketplaces can install their committed
   generated packages.
4. OpenCode activates only through its explicit command, even when installed
   through the local plugin bundle.
5. Integrity validation detects any semantic adapter drift.
6. Shared fixtures are available for execution and comparison across all three
   environments; only Codex Desktop evidence is required for release
   completion.

## Current platform references

- [Agent Skills specification](https://agentskills.io/specification)
- [Codex skills](https://learn.chatgpt.com/docs/build-skills)
- [Codex plugins](https://learn.chatgpt.com/docs/build-plugins)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Claude Code plugins](https://code.claude.com/docs/en/plugins)
- [Claude Code marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
- [OpenCode skills](https://opencode.ai/docs/skills)
- [OpenCode commands](https://opencode.ai/docs/commands)
- [OpenCode plugins](https://opencode.ai/docs/plugins)
