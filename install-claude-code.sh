#!/usr/bin/env sh
set -eu

marketplace_name="deliberation"
marketplace_source="fpiechowski/deliberation"
plugin_id="deliberation@deliberation"

if ! command -v claude >/dev/null 2>&1; then
  echo "Claude Code CLI was not found on PATH. Install Claude Code, then run this script again." >&2
  exit 1
fi

marketplaces="$(claude plugin marketplace list --json)"
if printf '%s\n' "$marketplaces" | grep -Eq '"name"[[:space:]]*:[[:space:]]*"deliberation"'; then
  echo "Refreshing the Deliberation marketplace..."
  claude plugin marketplace update "$marketplace_name"
else
  echo "Adding the Deliberation marketplace from GitHub..."
  claude plugin marketplace add --scope user "$marketplace_source"
fi

plugins="$(claude plugin list --json)"
if printf '%s\n' "$plugins" | grep -Eq '"id"[[:space:]]*:[[:space:]]*"deliberation@deliberation"'; then
  echo "Updating Deliberation..."
  claude plugin update --scope user "$plugin_id"
else
  echo "Installing Deliberation..."
  claude plugin install --scope user "$plugin_id"
fi

echo "Deliberation is installed. Restart Claude Code or run /reload-plugins, then invoke /deliberation:deliberation."
