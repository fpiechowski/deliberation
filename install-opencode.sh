#!/usr/bin/env sh
set -eu

scope="${1:-global}"
project_path="${2:-$(pwd)}"
release_tag="v0.1.0-dev.10"
asset_name="opencode-deliberation-0.1.0-dev.10.zip"
download_url="https://github.com/fpiechowski/deliberation/releases/download/$release_tag/$asset_name"

if command -v mktemp >/dev/null 2>&1; then
  temporary_root="$(mktemp -d "${TMPDIR:-/tmp}/deliberation-opencode.XXXXXX")"
else
  temporary_root="${TMPDIR:-/tmp}/deliberation-opencode.$$"
  mkdir -p "$temporary_root"
fi

cleanup() {
  rm -rf "$temporary_root"
}
trap cleanup EXIT INT TERM

zip_path="$temporary_root/$asset_name"
extract_path="$temporary_root/dist"

if command -v curl >/dev/null 2>&1; then
  echo "Downloading Deliberation OpenCode $release_tag..."
  curl -fsSL "$download_url" -o "$zip_path"
elif command -v wget >/dev/null 2>&1; then
  echo "Downloading Deliberation OpenCode $release_tag..."
  wget -q "$download_url" -O "$zip_path"
else
  echo "curl or wget is required to download Deliberation OpenCode." >&2
  exit 1
fi

if ! command -v unzip >/dev/null 2>&1; then
  echo "unzip is required to extract Deliberation OpenCode." >&2
  exit 1
fi

mkdir -p "$extract_path"
unzip -q "$zip_path" -d "$extract_path"

if [ ! -f "$extract_path/install.sh" ]; then
  echo "Downloaded OpenCode dist does not contain install.sh." >&2
  exit 1
fi

sh "$extract_path/install.sh" "$scope" "$project_path"
