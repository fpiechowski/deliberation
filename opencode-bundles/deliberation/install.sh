#!/usr/bin/env sh
set -eu

scope="${1:-global}"
project_path="${2:-$(pwd)}"
source_root="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"

case "$scope" in
  global)
    config_root="${HOME:?HOME is required}/.config/opencode"
    ;;
  project)
    config_root="$(CDPATH= cd -- "$project_path" && pwd)/.opencode"
    ;;
  *)
    echo "usage: sh ./install.sh [global|project] [project-path]" >&2
    exit 2
    ;;
esac

commands_root="$config_root/commands"
plugins_root="$config_root/plugins"

mkdir -p "$commands_root" "$plugins_root"
cp "$source_root/.opencode/commands/deliberation.md" "$commands_root/deliberation.md"
cp "$source_root/.opencode/commands/explain.md" "$commands_root/explain.md"
cp "$source_root/.opencode/plugins/deliberation.js" "$plugins_root/deliberation.js"

echo "Installed Deliberation 0.1.0-dev.13 for OpenCode at $config_root"
echo "Start OpenCode and invoke /deliberation or /explain."
