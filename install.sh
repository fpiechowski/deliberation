#!/usr/bin/env sh
set -eu

marketplace_name="deliberation"
marketplace_source="fpiechowski/deliberation"
marketplace_ref="master"
plugin_id="deliberation@deliberation"

if ! command -v codex >/dev/null 2>&1; then
  echo "Codex CLI was not found on PATH. Install Codex, then run this script again." >&2
  exit 1
fi

marketplaces="$(codex plugin marketplace list --json)"
if printf '%s\n' "$marketplaces" | grep -Eq '"name"[[:space:]]*:[[:space:]]*"deliberation"'; then
  echo "Refreshing the Deliberation marketplace..."
  codex plugin marketplace upgrade "$marketplace_name"
else
  echo "Adding the Deliberation marketplace..."
  codex plugin marketplace add "$marketplace_source" --ref "$marketplace_ref"
fi

plugins="$(codex plugin list --json)"
if printf '%s\n' "$plugins" | grep -Eq '"pluginId"[[:space:]]*:[[:space:]]*"deliberation@deliberation"'; then
  echo "Updating Deliberation..."
  codex plugin remove "$plugin_id"
fi

if ! codex plugin add "$plugin_id"; then
  echo "Deliberation was removed but could not be reinstalled. After fixing the error, run: codex plugin add $plugin_id" >&2
  exit 1
fi

echo "Deliberation is installed. Start a new Codex conversation (or restart Codex Desktop), then invoke \$deliberation."
