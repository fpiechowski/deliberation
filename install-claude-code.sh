#!/usr/bin/env sh
set -eu

marketplace_name="deliberation"
marketplace_source="fpiechowski/deliberation"
plugin_id="deliberation@deliberation"

has_user_scope_plugin() {
  printf '%s\n' "$1" | awk '
    /^  [{]$/ { in_plugin = 1; has_id = 0; has_user_scope = 0 }
    in_plugin && /"id"[[:space:]]*:[[:space:]]*"deliberation@deliberation"/ {
      has_id = 1
    }
    in_plugin && /"scope"[[:space:]]*:[[:space:]]*"user"/ {
      has_user_scope = 1
    }
    in_plugin && /^  [}][,]?$/ {
      if (has_id && has_user_scope) {
        found = 1
      }
      in_plugin = 0
    }
    END { exit found ? 0 : 1 }
  '
}

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
if has_user_scope_plugin "$plugins"; then
  echo "Updating Deliberation..."
  claude plugin update --scope user "$plugin_id"
else
  echo "Installing Deliberation..."
  claude plugin install --scope user "$plugin_id"
fi

echo "Deliberation is installed. Restart Claude Code or run /reload-plugins, then invoke /deliberation:deliberation."
