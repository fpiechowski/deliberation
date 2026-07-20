# Codex Git marketplace installation transcript

- **Executed:** 2026-07-20
- **Product version:** `0.1.0-dev.3`
- **Host:** Codex Desktop installation on Windows
- **Surface:** Git marketplace and installed plugin cache
- **Fixture:** `codex-git-marketplace-installation`

## First installation

The public command was executed without a repository clone or local plugin
source:

```powershell
irm https://raw.githubusercontent.com/fpiechowski/deliberation/master/install.ps1 | iex
```

Codex added marketplace `deliberation` from
`https://github.com/fpiechowski/deliberation.git#master`, using its own snapshot
under `.codex/.tmp/marketplaces/deliberation`. It then installed
`deliberation@deliberation` at version `0.1.0-dev.3` under the local plugin
cache. `codex plugin list --json` reported a Git marketplace source and an
enabled installed plugin.

## Repeated installation / update

The same public command was executed again. It refreshed marketplace
`deliberation`, removed the installed plugin, and reinstalled it successfully
from the refreshed Git snapshot. The resulting plugin remained enabled at
version `0.1.0-dev.3`.

## Scope note

This fixture validates marketplace discovery, installation, and the update
path. A new Codex Desktop conversation or restart is still required before an
installed plugin can be used by a newly created task; behavioural activation is
already covered by the retained standalone Codex Desktop fixtures.
