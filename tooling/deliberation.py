#!/usr/bin/env python3
"""Assemble and validate Deliberation host artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SEMVER = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
FRONTMATTER_LINE = re.compile(r"^([a-z][a-z0-9-]*):\s*(.+)$")
SKILL_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
OPEN_CODE_PREFIX = (
    "Activate Deliberation for the current conversation. Acknowledge activation,\n"
    "then follow this behavioural contract:\n\n"
)
PUBLICATION_SURFACES = (
    Path(".agents"),
    Path(".claude-plugin"),
    Path("plugins/deliberation"),
    Path("claude-plugins/deliberation"),
    Path("opencode-bundles/deliberation"),
)


class ValidationError(RuntimeError):
    """Raised when an assembled artifact violates the accepted contract."""


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    normalized = content.replace("\r\n", "\n").rstrip("\n") + "\n"
    path.write_text(normalized, encoding="utf-8", newline="\n")


def write_json(path: Path, value: Any) -> None:
    write_text(path, json.dumps(value, indent=2, sort_keys=True))


def parse_frontmatter(content: str, source: Path) -> tuple[dict[str, str], str]:
    normalized = content.replace("\r\n", "\n")
    if not normalized.startswith("---\n"):
        raise ValidationError(f"{source}: missing opening YAML frontmatter")
    end = normalized.find("\n---\n", 4)
    if end < 0:
        raise ValidationError(f"{source}: missing closing YAML frontmatter")

    metadata: dict[str, str] = {}
    for line in normalized[4:end].splitlines():
        match = FRONTMATTER_LINE.fullmatch(line)
        if not match:
            raise ValidationError(
                f"{source}: unsupported frontmatter line {line!r}; "
                "only scalar key/value fields are allowed"
            )
        key, value = match.groups()
        if key in metadata:
            raise ValidationError(f"{source}: duplicate frontmatter field {key!r}")
        metadata[key] = value.strip().strip('"').strip("'")

    body = normalized[end + 5 :].lstrip("\n").rstrip("\n") + "\n"
    return metadata, body


def canonical() -> tuple[str, dict[str, str], str]:
    skill_path = ROOT / "core" / "deliberation" / "SKILL.md"
    skill = read_text(skill_path)
    metadata, body = parse_frontmatter(skill, skill_path)
    if set(metadata) != {"name", "description"}:
        raise ValidationError(
            f"{skill_path}: canonical frontmatter must contain only name and description"
        )
    if metadata["name"] != "deliberation":
        raise ValidationError(f"{skill_path}: name must be deliberation")
    if not SKILL_NAME.fullmatch(metadata["name"]):
        raise ValidationError(f"{skill_path}: name is not Agent Skills-compatible")
    if skill_path.parent.name != metadata["name"]:
        raise ValidationError(f"{skill_path}: name must match its parent directory")
    if not 1 <= len(metadata["description"]) <= 1024:
        raise ValidationError(f"{skill_path}: description must be 1-1024 characters")
    return skill.rstrip("\n") + "\n", metadata, body


def product_version() -> str:
    version = read_text(ROOT / "VERSION").strip()
    if not SEMVER.fullmatch(version):
        raise ValidationError(f"VERSION is not valid SemVer: {version!r}")
    return version


def render_template(relative_path: str, **values: str) -> str:
    content = read_text(ROOT / relative_path)
    for key, value in values.items():
        content = content.replace("{{" + key + "}}", value.rstrip("\n"))
    unresolved = re.findall(r"\{\{[A-Z0-9_]+\}\}", content)
    if unresolved:
        raise ValidationError(
            f"{relative_path}: unresolved template tokens {sorted(set(unresolved))}"
        )
    return content


def claude_skill(canonical_skill: str) -> str:
    marker = "\n---\n"
    closing = canonical_skill.find(marker, 4)
    if closing < 0:
        raise ValidationError("canonical skill has invalid frontmatter")
    return (
        canonical_skill[:closing]
        + "\ndisable-model-invocation: true"
        + canonical_skill[closing:]
    )


def sha256(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def prepare_output(output: Path) -> None:
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)


def assemble(output: Path) -> None:
    version = product_version()
    canonical_skill, _, core_body = canonical()
    codex_metadata = render_template("adapters/codex/openai.yaml.tmpl")
    codex_manifest = render_template(
        "adapters/codex/plugin.json.tmpl", VERSION=version
    )
    codex_marketplace = render_template("adapters/codex/marketplace.json.tmpl")
    claude_variant = claude_skill(canonical_skill)
    claude_manifest = render_template(
        "adapters/claude-code/plugin.json.tmpl", VERSION=version
    )
    claude_marketplace = render_template(
        "adapters/claude-code/marketplace.json.tmpl", VERSION=version
    )
    opencode_command = render_template(
        "adapters/opencode/deliberation.md.tmpl", CORE_BODY=core_body
    )

    prepare_output(output)

    write_text(
        output / "publication/.agents/plugins/marketplace.json",
        codex_marketplace,
    )

    write_text(
        output / "publication/.claude-plugin/marketplace.json",
        claude_marketplace,
    )

    write_text(
        output / "standalone/codex/deliberation/SKILL.md", canonical_skill
    )
    write_text(
        output / "standalone/codex/deliberation/agents/openai.yaml",
        codex_metadata,
    )
    write_text(
        output / "standalone/claude-code/deliberation/SKILL.md",
        claude_variant,
    )

    codex_plugin = output / "publication/plugins/deliberation"
    write_text(codex_plugin / ".codex-plugin/plugin.json", codex_manifest)
    write_text(
        codex_plugin / "skills/deliberation/SKILL.md", canonical_skill
    )
    write_text(
        codex_plugin / "skills/deliberation/agents/openai.yaml",
        codex_metadata,
    )

    claude_plugin = output / "publication/claude-plugins/deliberation"
    write_text(claude_plugin / ".claude-plugin/plugin.json", claude_manifest)
    write_text(
        claude_plugin / "skills/deliberation/SKILL.md", claude_variant
    )

    opencode_bundle = output / "publication/opencode-bundles/deliberation"
    write_text(
        opencode_bundle / ".opencode/commands/deliberation.md",
        opencode_command,
    )
    write_text(
        opencode_bundle / "core/deliberation/SKILL.md", canonical_skill
    )
    write_text(opencode_bundle / "VERSION", version)

    write_json(
        output / "integrity.json",
        {
            "canonical_body_sha256": sha256(core_body),
            "product_version": version,
            "runtime_payloads": {
                "claude-code": sha256(core_body),
                "codex": sha256(core_body),
                "opencode": sha256(core_body),
            },
        },
    )


def require_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(read_text(path))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValidationError(f"{path}: invalid JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ValidationError(f"{path}: expected a JSON object")
    return value


def validate_skill(
    path: Path,
    expected_body: str,
    *,
    claude: bool = False,
) -> None:
    metadata, body = parse_frontmatter(read_text(path), path)
    expected_keys = {"name", "description"}
    if claude:
        expected_keys.add("disable-model-invocation")
    if set(metadata) != expected_keys:
        raise ValidationError(
            f"{path}: expected frontmatter fields {sorted(expected_keys)}"
        )
    if metadata["name"] != "deliberation":
        raise ValidationError(f"{path}: invalid skill name")
    if claude and metadata["disable-model-invocation"] != "true":
        raise ValidationError(f"{path}: model invocation must be disabled")
    if body != expected_body:
        raise ValidationError(f"{path}: behavioural payload drifted from core")


def validate_fixtures() -> None:
    schema_path = ROOT / "validation" / "schemas" / "assertions.schema.json"
    schema = require_json(schema_path)
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        raise ValidationError(f"{schema_path}: unexpected JSON Schema dialect")

    fixture_root = ROOT / "validation" / "fixtures"
    assertions_files = sorted(fixture_root.glob("**/assertions.json"))
    if not assertions_files:
        raise ValidationError("no validation fixtures found")
    required = {
        "id",
        "scenarios",
        "required_signals",
        "forbidden_signals",
        "human_evaluation",
    }
    for path in assertions_files:
        value = require_json(path)
        if set(value) != required:
            raise ValidationError(
                f"{path}: expected fields {sorted(required)}"
            )
        if not isinstance(value["id"], str) or not value["id"]:
            raise ValidationError(f"{path}: id must be a non-empty string")
        for key in ("scenarios", "required_signals", "forbidden_signals"):
            if (
                not isinstance(value[key], list)
                or not value[key]
                or not all(isinstance(item, str) and item for item in value[key])
            ):
                raise ValidationError(
                    f"{path}: {key} must be a non-empty string array"
                )
        if not isinstance(value["human_evaluation"], bool):
            raise ValidationError(f"{path}: human_evaluation must be boolean")
        if not path.with_name("prompt.md").is_file():
            raise ValidationError(f"{path}: prompt.md is missing")


def validate_assembly(output: Path) -> None:
    version = product_version()
    canonical_skill, _, core_body = canonical()

    validate_skill(
        output / "standalone/codex/deliberation/SKILL.md", core_body
    )
    validate_skill(
        output
        / "publication/plugins/deliberation/skills/deliberation/SKILL.md",
        core_body,
    )
    validate_skill(
        output / "standalone/claude-code/deliberation/SKILL.md",
        core_body,
        claude=True,
    )
    validate_skill(
        output
        / "publication/claude-plugins/deliberation/skills/deliberation/SKILL.md",
        core_body,
        claude=True,
    )

    for path in (
        output / "standalone/codex/deliberation/agents/openai.yaml",
        output
        / "publication/plugins/deliberation/skills/deliberation/agents/openai.yaml",
    ):
        metadata = read_text(path)
        if "allow_implicit_invocation: false" not in metadata:
            raise ValidationError(f"{path}: implicit invocation is not disabled")
        if "allow_implicit_invocation: true" in metadata:
            raise ValidationError(f"{path}: implicit invocation is enabled")

    for relative, manifest_type in (
        ("publication/plugins/deliberation/.codex-plugin/plugin.json", "codex"),
        (
            "publication/claude-plugins/deliberation/.claude-plugin/plugin.json",
            "claude",
        ),
    ):
        path = output / relative
        manifest = require_json(path)
        if manifest.get("name") != "deliberation":
            raise ValidationError(f"{path}: invalid plugin name")
        if manifest.get("version") != version:
            raise ValidationError(f"{path}: version differs from VERSION")
        if manifest_type == "codex" and manifest.get("skills") != "./skills/":
            raise ValidationError(f"{path}: invalid Codex skills path")

    codex_marketplace_path = output / "publication/.agents/plugins/marketplace.json"
    codex_marketplace = require_json(codex_marketplace_path)
    expected_codex_marketplace = {
        "name": "deliberation",
        "interface": {"displayName": "Deliberation"},
        "plugins": [
            {
                "name": "deliberation",
                "source": {"source": "local", "path": "./plugins/deliberation"},
                "policy": {
                    "installation": "AVAILABLE",
                    "authentication": "ON_INSTALL",
                },
                "category": "Productivity",
            }
        ],
    }
    if codex_marketplace != expected_codex_marketplace:
        raise ValidationError(
            f"{codex_marketplace_path}: does not match the Deliberation Codex marketplace contract"
        )

    marketplace_path = output / "publication/.claude-plugin/marketplace.json"
    marketplace = require_json(marketplace_path)
    expected_marketplace = {
        "$schema": "https://json.schemastore.org/claude-code-marketplace.json",
        "name": "deliberation",
        "version": version,
        "description": "Deliberation plugin marketplace for Claude Code.",
        "owner": {"name": "Filip Piechowski"},
        "plugins": [
            {
                "name": "deliberation",
                "description": (
                    "Collaborative engineering through shared decisions and "
                    "bounded milestones."
                ),
                "source": "./claude-plugins/deliberation",
            }
        ],
    }
    if marketplace != expected_marketplace:
        raise ValidationError(
            f"{marketplace_path}: does not match the Deliberation marketplace contract"
        )

    opencode_path = (
        output
        / "publication/opencode-bundles/deliberation/.opencode/commands/deliberation.md"
    )
    command_metadata, command_body = parse_frontmatter(
        read_text(opencode_path), opencode_path
    )
    if set(command_metadata) != {"description"}:
        raise ValidationError(f"{opencode_path}: unexpected command metadata")
    if not command_body.startswith(OPEN_CODE_PREFIX):
        raise ValidationError(f"{opencode_path}: invalid command wrapper")
    if command_body[len(OPEN_CODE_PREFIX) :] != core_body:
        raise ValidationError(
            f"{opencode_path}: behavioural payload drifted from core"
        )

    audit_copy = (
        output
        / "publication/opencode-bundles/deliberation/core/deliberation/SKILL.md"
    )
    if read_text(audit_copy) != canonical_skill:
        raise ValidationError(f"{audit_copy}: audit copy differs from core")
    if (
        read_text(
            output / "publication/opencode-bundles/deliberation/VERSION"
        ).strip()
        != version
    ):
        raise ValidationError("OpenCode bundle version differs from VERSION")

    publication_root = output / "publication"
    for path in publication_root.rglob("*"):
        if path.is_file():
            content = read_text(path)
            if "../" in content or "..\\" in content:
                raise ValidationError(
                    f"{path}: published artifact references an external path"
                )

    integrity = require_json(output / "integrity.json")
    expected_digest = sha256(core_body)
    if integrity.get("product_version") != version:
        raise ValidationError("integrity metadata version differs from VERSION")
    if integrity.get("canonical_body_sha256") != expected_digest:
        raise ValidationError("integrity metadata has an invalid core digest")
    if integrity.get("runtime_payloads") != {
        "claude-code": expected_digest,
        "codex": expected_digest,
        "opencode": expected_digest,
    }:
        raise ValidationError("runtime payload digests are inconsistent")

    validate_fixtures()
    validate_installers()


def validate_installers() -> None:
    required_fragments = {
        ROOT / "install.ps1": (
            "fpiechowski/deliberation",
            '"master"',
            '"plugin", "marketplace", "upgrade"',
            '"plugin", "marketplace", "add"',
            '"plugin", "remove"',
            '"plugin", "add"',
            "ConvertFrom-Json",
        ),
        ROOT / "install.sh": (
            "#!/usr/bin/env sh",
            "fpiechowski/deliberation",
            'marketplace_ref="master"',
            "plugin marketplace upgrade",
            "plugin marketplace add",
            "plugin remove",
            "plugin add",
        ),
    }
    for path, fragments in required_fragments.items():
        content = read_text(path)
        for fragment in fragments:
            if fragment not in content:
                raise ValidationError(f"{path}: missing installer contract {fragment!r}")


def tree_snapshot(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def publication_differences(output: Path) -> list[str]:
    differences: list[str] = []
    publication_root = output / "publication"
    for relative in PUBLICATION_SURFACES:
        expected = tree_snapshot(publication_root / relative)
        committed = tree_snapshot(ROOT / relative)
        expected_paths = set(expected)
        committed_paths = set(committed)
        for path in sorted(expected_paths - committed_paths):
            differences.append(f"missing: {(relative / path).as_posix()}")
        for path in sorted(committed_paths - expected_paths):
            differences.append(f"extra: {(relative / path).as_posix()}")
        for path in sorted(expected_paths & committed_paths):
            if expected[path] != committed[path]:
                differences.append(f"changed: {(relative / path).as_posix()}")
    return differences


def validate_committed_publication(output: Path) -> None:
    differences = publication_differences(output)
    if differences:
        details = "\n".join(f"  - {difference}" for difference in differences)
        raise ValidationError(
            "committed publication surfaces are stale:\n"
            f"{details}\n"
            "run `python tooling/deliberation.py sync-publication`"
        )


def sync_publication(output: Path) -> None:
    publication_root = output / "publication"
    for relative in PUBLICATION_SURFACES:
        source = publication_root / relative
        destination = ROOT / relative
        if destination.exists():
            shutil.rmtree(destination)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, destination)


def checked_output(raw_path: str) -> Path:
    output = (ROOT / raw_path).resolve()
    try:
        relative = output.relative_to(ROOT)
    except ValueError as exc:
        raise ValidationError("assembly output must stay inside the repository") from exc
    if relative == Path("."):
        raise ValidationError("assembly output cannot be the repository root")
    return output


def command_assemble(args: argparse.Namespace) -> None:
    output = checked_output(args.output)
    assemble(output)
    validate_assembly(output)
    print(f"Assembled and validated {output.relative_to(ROOT)}")


def command_check(_: argparse.Namespace) -> None:
    with tempfile.TemporaryDirectory(prefix="deliberation-check-") as first:
        with tempfile.TemporaryDirectory(prefix="deliberation-check-") as second:
            first_path = Path(first)
            second_path = Path(second)
            assemble(first_path)
            assemble(second_path)
            validate_assembly(first_path)
            validate_assembly(second_path)
            if tree_snapshot(first_path) != tree_snapshot(second_path):
                raise ValidationError("assembly is not deterministic")
            validate_committed_publication(first_path)
    print(
        "Deliberation source, adapters, fixtures, assembly, and committed "
        "publication surfaces are valid"
    )


def command_sync_publication(_: argparse.Namespace) -> None:
    with tempfile.TemporaryDirectory(prefix="deliberation-publication-") as temporary:
        output = Path(temporary)
        assemble(output)
        validate_assembly(output)
        sync_publication(output)
        validate_committed_publication(output)
    print("Synchronized and validated committed publication surfaces")


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        description="Assemble and validate Deliberation host artifacts."
    )
    subcommands = result.add_subparsers(dest="command", required=True)

    assemble_parser = subcommands.add_parser(
        "assemble", help="generate local host artifacts"
    )
    assemble_parser.add_argument(
        "--output",
        default="build",
        help="repository-relative output directory (default: build)",
    )
    assemble_parser.set_defaults(handler=command_assemble)

    check_parser = subcommands.add_parser(
        "check",
        help="validate sources, deterministic assembly, and committed publication",
    )
    check_parser.set_defaults(handler=command_check)

    sync_parser = subcommands.add_parser(
        "sync-publication",
        help="regenerate committed publication surfaces",
    )
    sync_parser.set_defaults(handler=command_sync_publication)
    return result


def main() -> int:
    args = parser().parse_args()
    try:
        args.handler(args)
    except ValidationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
