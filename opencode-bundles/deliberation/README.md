# Deliberation for OpenCode

Version: `0.1.0-dev.11`

This is the experimental OpenCode distribution of Deliberation.

It installs:

- `.opencode/commands/deliberation.md` — the self-contained `/deliberation`
  command with the complete shared behavioural contract embedded.
- `.opencode/plugins/deliberation.js` — a minimal OpenCode plugin marker that
  confirms the Deliberation distribution has been loaded.
- `core/deliberation/` — the canonical Agent Skills-compatible source for
  audit and parity checks; it is intentionally outside OpenCode skill discovery.

## Install globally

From this directory:

```powershell
.\install.ps1
```

or:

```sh
sh ./install.sh
```

This installs into the global OpenCode config directory.

## Install for one project

From this directory:

```powershell
.\install.ps1 -Scope Project -ProjectPath C:\path\to\project
```

or:

```sh
sh ./install.sh project /path/to/project
```

Then start OpenCode and invoke:

```text
/deliberation
```

OpenCode remains an experimental adapter for this release. The command and
plugin layout are validated structurally, but retained live-host behavioural
evidence is still limited to Codex Desktop.
