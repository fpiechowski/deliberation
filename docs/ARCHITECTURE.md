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
7. The first version introduces no runtime service, hook, MCP server, or
   third-party build dependency.

## Repository topology

The intended source and publication layout is:

```text
core/
└── deliberation/
    └── SKILL.md

adapters/
├── codex/
├── claude-code/
└── opencode/

plugins/
└── deliberation/                    # generated Codex plugin

claude-plugins/
└── deliberation/                    # generated Claude Code plugin

opencode-bundles/
└── deliberation/                    # generated OpenCode distribution bundle

validation/
├── fixtures/
│   ├── core/
│   └── adapters/
├── schemas/
└── runs/

tooling/

.agents/plugins/marketplace.json      # eventual Codex marketplace catalog
.claude-plugin/marketplace.json       # eventual Claude Code marketplace catalog
VERSION
```

This is the target topology, not scaffolding created by the architecture
milestone. Marketplace catalogs and production packages are added only in
later approved milestones.

The asymmetric publication paths are intentional. Codex's repository
marketplace convention uses `plugins/<plugin-name>`, while a Claude Code
marketplace may reference any in-repository plugin directory through a
relative `source`. Keeping the packages separate prevents host-specific
metadata from contaminating the other adapter.

## Shared behavioural core

`core/deliberation/SKILL.md` is an Agent Skills-compatible skill named
`deliberation`. It contains:

- Portable `name` and `description` frontmatter.
- The complete operational behaviour required on every activation.
- The Deliberation loop and conversation-wide lifetime.
- Milestone and checkpoint semantics.
- Choice, Consequence, and Drift tests.
- Approval and response-intent handling.
- Progress, result walkthrough, completion, and explicit exit behaviour.

The core is concise and imperative. It does not duplicate the complete product
history, decision log, or scenario suite. Behaviour needed on every turn stays
in `SKILL.md`; validation details remain outside the runtime skill.

The first core is instruction-only. It has no scripts, assets, external tools,
or runtime dependencies.

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
        └── agents/
            └── openai.yaml
```

The package may later be listed by
`.agents/plugins/marketplace.json`. It does not add hooks, apps, MCP servers, or
connectors in the first version.

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
        └── SKILL.md
```

The eventual root `.claude-plugin/marketplace.json` references it with a
relative source:

```json
{
  "name": "deliberation",
  "source": "./claude-plugins/deliberation"
}
```

The final marketplace name and publisher metadata remain distribution
decisions. The example above shows the plugin entry shape, not an accepted
marketplace identity.

The generated Claude package is committed. This is required for users who add
the repository itself as a Git marketplace because Claude Code resolves
relative plugin sources against its cloned marketplace checkout. The installed
plugin is self-contained and never references `../../core`.

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

The command embeds the normalized behavioural content of the canonical core.
Invoking `/deliberation` injects that contract into the current conversation.
Ordinary engineering prompts do not expose Deliberation as an automatically
loadable OpenCode skill.

The generated distribution bundle includes the canonical `SKILL.md` for audit
and portability, but stores it outside OpenCode's discovered skill paths. The
runtime command is self-contained so that both project and global installation
work without fragile absolute or project-relative file references.

An OpenCode JavaScript or TypeScript plugin is outside the first-release
architecture. It may be reconsidered only if it later provides material
runtime or installation value.

## Assembly and publication

A small repository-local assembler produces every host artifact from the
canonical core and adapter templates.

The assembler:

1. Reads `VERSION` and the canonical `SKILL.md`.
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

## Installation paths

The first implementation validates installation in this order:

1. Codex standalone skill in the desktop app, then the same skill in CLI and
   IDE.
2. Codex plugin through a local repository marketplace.
3. Claude Code standalone skill.
4. Claude Code plugin through a local marketplace, then through the Git-hosted
   repository marketplace.
5. OpenCode project command and global command bundle.

Public distribution follows successful local and Git-source validation.

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
wrapping syntax. Compare the remaining behavioural content with the canonical
core.

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
`docs/BEHAVIORAL_SCENARIOS.md`.

Release evidence is retained for synthetic fixtures. Local exploratory runs
may remain untracked.

## Continuity and state

Adapters activate the mode but do not create a separate runtime state store.
The behavioural contract maintains lightweight state in the conversation:

- Active or inactive mode.
- Current objective and provisional roadmap.
- Approved milestone scope.
- Accepted decisions and open questions.

Resuming the same conversation must preserve this context through the host's
normal conversation history. If an environment cannot satisfy the continuity
scenario, the result is Blocked and the architecture is revisited rather than
adding silent repository state or weakening the product contract.

## Explicit non-goals for the first release

- Separate behavioural cores per environment.
- Implicit activation.
- Runtime hooks, MCP servers, connectors, or background services.
- An OpenCode npm plugin.
- Automatic persistent state files in user repositories.
- A third-party build or test framework.
- Publication before cross-environment scenario validation.

## Architecture acceptance criteria

The architecture is implemented correctly when:

1. One canonical core produces all runtime variants.
2. All published packages are self-contained.
3. Git-hosted Codex and Claude Code marketplaces can install their committed
   generated packages.
4. OpenCode activates only through its explicit command.
5. Integrity validation detects any semantic adapter drift.
6. Shared fixtures can be executed and compared across all three environments.

## Current platform references

- [Agent Skills specification](https://agentskills.io/specification)
- [Codex skills](https://learn.chatgpt.com/docs/build-skills)
- [Codex plugins](https://learn.chatgpt.com/docs/build-plugins)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Claude Code plugins](https://code.claude.com/docs/en/plugins)
- [Claude Code marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
- [OpenCode skills](https://opencode.ai/docs/skills)
- [OpenCode commands](https://opencode.ai/docs/commands)
