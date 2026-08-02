#!/usr/bin/env python3
"""Assemble and validate Deliberation host artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SHARED_REFERENCE_SOURCES = {
    "../shared/explain-model.md": Path("core/shared/explain-model.md"),
}
MATERIALIZED_REFERENCE_PATHS = {
    "../shared/explain-model.md": "references/explain-model.md",
}
SEMVER = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
FRONTMATTER_LINE = re.compile(r"^([a-z][a-z0-9-]*):\s*(.+)$")
SKILL_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REFERENCE_LINK = re.compile(
    r"\]\(((?:references/[a-z0-9-]+|\.\./shared/[a-z0-9-]+)\.md)\)"
)
OPEN_CODE_PREFIXES = {
    "deliberation": (
        "Activate Deliberation for the task in this request by default; use the current\n"
        "conversation only when the user explicitly requests that broader scope.\n"
        "Acknowledge the scope, then follow this behavioural contract:\n\n"
    ),
    "explain": (
        "Explain the user's named topic as a standalone answer. Do not activate "
        "Deliberation, open a checkpoint, seek approval, or modify files unless "
        "the user separately asks:\n\n"
    ),
}
SKILL_INTERFACE = {
    "deliberation": {
        "display_name": "Deliberation",
        "short_description": "Collaborative engineering with shared decisions",
        "default_prompt": (
            "Use $deliberation to work through this engineering task collaboratively."
        ),
        "command_description": (
            "Activate Deliberation for collaborative engineering with shared decisions"
        ),
    },
    "explain": {
        "display_name": "Explain",
        "short_description": "Explain a technical topic clearly",
        "default_prompt": "Use $explain to explain this technical topic clearly.",
        "command_description": "Explain a technical topic without activating Deliberation",
    },
}
PUBLICATION_SURFACES = (
    Path(".agents"),
    Path(".claude-plugin"),
    Path("dist/codex"),
    Path("dist/claude-code"),
    Path("dist/opencode"),
)
PROTECTED_OUTPUT_ROOTS = (
    Path(".agents"),
    Path(".claude-plugin"),
    Path("dist"),
)


class ValidationError(RuntimeError):
    """Raised when an assembled artifact violates the accepted contract."""


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def shell_path(path: Path) -> str:
    """Return a path usable by POSIX shells, including WSL on Windows."""
    normalized = path.as_posix()
    if os.name == "nt" and re.match(r"^[A-Za-z]:/", normalized):
        return f"/mnt/{normalized[0].lower()}{normalized[2:]}"
    return normalized


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


def canonical_references(skill_body: str, skill_path: Path) -> dict[str, str]:
    """Read the complete, explicitly linked canonical skill reference set."""
    reference_root = skill_path.parent / "references"
    linked_paths = set(REFERENCE_LINK.findall(skill_body))
    if not linked_paths:
        raise ValidationError(f"{skill_path}: must link at least one reference module")
    if not reference_root.is_dir() and not linked_paths.issubset(
        SHARED_REFERENCE_SOURCES
    ):
        raise ValidationError(f"{skill_path}: references directory is missing")

    actual_paths = {
        path.relative_to(skill_path.parent).as_posix()
        for path in reference_root.rglob("*.md")
        if path.is_file()
    } if reference_root.is_dir() else set()
    materialized_paths = {
        MATERIALIZED_REFERENCE_PATHS.get(relative, relative)
        for relative in linked_paths
    }
    for relative, shared_source in SHARED_REFERENCE_SOURCES.items():
        materialized = MATERIALIZED_REFERENCE_PATHS[relative]
        local_path = skill_path.parent / materialized
        shared_path = ROOT / shared_source
        if relative in linked_paths:
            if local_path.exists():
                raise ValidationError(
                    f"{local_path}: shared reference must not be duplicated locally"
                )
            if not shared_path.is_file():
                raise ValidationError(
                    f"{skill_path}: shared reference source is missing: {shared_source}"
                )
            actual_paths.add(materialized)
    if materialized_paths != actual_paths:
        missing = sorted(materialized_paths - actual_paths)
        unlinked = sorted(actual_paths - materialized_paths)
        details = []
        if missing:
            details.append(f"missing linked modules {missing}")
        if unlinked:
            details.append(f"unlinked modules {unlinked}")
        raise ValidationError(f"{skill_path}: " + "; ".join(details))

    references: dict[str, str] = {}
    for relative in sorted(materialized_paths):
        source = skill_path.parent / relative
        shared_link = next(
            (
                link
                for link, materialized in MATERIALIZED_REFERENCE_PATHS.items()
                if materialized == relative
            ),
            None,
        )
        if not source.is_file() and shared_link in SHARED_REFERENCE_SOURCES:
            source = ROOT / SHARED_REFERENCE_SOURCES[shared_link]
        references[relative] = read_text(source).rstrip("\n") + "\n"
    return references


def canonical(skill_name: str = "deliberation") -> tuple[str, dict[str, str], str, dict[str, str]]:
    skill_path = ROOT / "core" / skill_name / "SKILL.md"
    skill = read_text(skill_path)
    metadata, body = parse_frontmatter(skill, skill_path)
    if set(metadata) != {"name", "description"}:
        raise ValidationError(
            f"{skill_path}: canonical frontmatter must contain only name and description"
        )
    if metadata["name"] != skill_name:
        raise ValidationError(f"{skill_path}: name must be {skill_name}")
    if not SKILL_NAME.fullmatch(metadata["name"]):
        raise ValidationError(f"{skill_path}: name is not Agent Skills-compatible")
    if skill_path.parent.name != metadata["name"]:
        raise ValidationError(f"{skill_path}: name must match its parent directory")
    if not 1 <= len(metadata["description"]) <= 1024:
        raise ValidationError(f"{skill_path}: description must be 1-1024 characters")
    references = canonical_references(body, skill_path)
    return skill.rstrip("\n") + "\n", metadata, body, references


def canonical_core_digest(canonical_skill: str, references: dict[str, str]) -> str:
    payload = canonical_skill + "".join(
        f"\0{relative}\0{content}" for relative, content in references.items()
    )
    return sha256(payload)


def materialize_reference_links(content: str) -> str:
    """Rewrite source-only shared links to package-local reference links."""
    for source_link, runtime_link in MATERIALIZED_REFERENCE_PATHS.items():
        content = content.replace(f"]({source_link})", f"]({runtime_link})")
    return content


def validate_checkpoint_semantics(references: dict[str, str]) -> None:
    """Protect the accepted intent-based checkpoint interaction contract."""
    checkpoints = references.get("references/checkpoints.md", "")
    alternative = references.get("references/alternative.md", "")
    required_fragments = {
        "references/checkpoints.md": (
            "localized heading equivalent to\n**Suggested next step**",
            "**You can choose a suggestion or reply in your own\nwords.**",
            "Request a change or propose another next step",
            "Only a suggestion that explicitly says **Accept** can authorize work",
        ),
        "references/alternative.md": (
            "same visible, localized heading equivalent to\n**Suggested next step**",
            "**You can choose a suggestion or reply in\nyour own words.**",
            "Choose an alternative or propose another next step",
            "Only an explicit acceptance\nof the named current recommendation authorizes work",
        ),
    }
    for relative, fragments in required_fragments.items():
        content = checkpoints if relative.endswith("checkpoints.md") else alternative
        for fragment in fragments:
            if fragment not in content:
                raise ValidationError(
                    f"{relative}: missing checkpoint interaction contract {fragment!r}"
                )


def write_core(
    destination: Path,
    canonical_skill: str,
    references: dict[str, str],
    *,
    claude: bool = False,
) -> None:
    runtime_skill = materialize_reference_links(canonical_skill)
    write_text(
        destination / "SKILL.md",
        claude_skill(runtime_skill) if claude else runtime_skill,
    )
    for relative, content in references.items():
        write_text(destination / relative, content)


def opencode_contract(
    core_body: str, references: dict[str, str], skill_name: str
) -> str:
    """Inline canonical modules because an OpenCode command has no skill loader."""
    modules = "\n\n".join(
        f"## Loaded module: {relative}\n\n{content.rstrip()}"
        for relative, content in references.items()
    )
    return f"{core_body.rstrip()}\n\n# Loaded {skill_name} modules\n\n{modules}\n"


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


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def release_tag(version: str) -> str:
    return f"v{version}"


def release_asset_name(version: str) -> str:
    return f"opencode-deliberation-{version}.zip"


def write_release_archive(source: Path, archive_path: Path) -> None:
    files = sorted(path for path in source.rglob("*") if path.is_file())
    if not files:
        raise ValidationError(f"{source}: cannot package an empty release bundle")

    with zipfile.ZipFile(
        archive_path,
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as archive:
        for path in files:
            relative = path.relative_to(source).as_posix()
            info = zipfile.ZipInfo(relative, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = (0o755 if path.suffix == ".sh" else 0o644) << 16
            archive.writestr(info, path.read_bytes())


def package_release(output: Path) -> tuple[Path, Path]:
    version = product_version()
    with tempfile.TemporaryDirectory(prefix="deliberation-release-") as temporary:
        assembled = Path(temporary)
        assemble(assembled)
        validate_assembly(assembled)
        validate_committed_publication(assembled)

        bundle = assembled / "publication/dist/opencode"
        prepare_output(output)
        archive_path = output / release_asset_name(version)
        write_release_archive(bundle, archive_path)
        checksum_path = output / f"{archive_path.name}.sha256"
        checksum = sha256_bytes(archive_path.read_bytes())
        write_text(checksum_path, f"{checksum}  {archive_path.name}")

    return archive_path, checksum_path


def prepare_output(output: Path) -> None:
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)


def assemble(output: Path) -> None:
    version = product_version()
    canonical_skill, _, core_body, references = canonical()
    explain_skill, _, explain_body, explain_references = canonical("explain")
    runtime_skill = materialize_reference_links(canonical_skill)
    runtime_core_body = materialize_reference_links(core_body)
    runtime_explain_skill = materialize_reference_links(explain_skill)
    runtime_explain_body = materialize_reference_links(explain_body)
    codex_metadata = render_template(
        "adapters/codex/openai.yaml.tmpl",
        DISPLAY_NAME=SKILL_INTERFACE["deliberation"]["display_name"],
        SHORT_DESCRIPTION=SKILL_INTERFACE["deliberation"]["short_description"],
        DEFAULT_PROMPT=SKILL_INTERFACE["deliberation"]["default_prompt"],
    )
    explain_codex_metadata = render_template(
        "adapters/codex/openai.yaml.tmpl",
        DISPLAY_NAME=SKILL_INTERFACE["explain"]["display_name"],
        SHORT_DESCRIPTION=SKILL_INTERFACE["explain"]["short_description"],
        DEFAULT_PROMPT=SKILL_INTERFACE["explain"]["default_prompt"],
    )
    codex_manifest = render_template(
        "adapters/codex/plugin.json.tmpl", VERSION=version
    )
    codex_marketplace = render_template("adapters/codex/marketplace.json.tmpl")
    claude_manifest = render_template(
        "adapters/claude-code/plugin.json.tmpl", VERSION=version
    )
    claude_marketplace = render_template(
        "adapters/claude-code/marketplace.json.tmpl", VERSION=version
    )
    opencode_command = render_template(
        "adapters/opencode/deliberation.md.tmpl",
        COMMAND_DESCRIPTION=SKILL_INTERFACE["deliberation"]["command_description"],
        COMMAND_PREFIX=OPEN_CODE_PREFIXES["deliberation"],
        CORE_BODY=opencode_contract(
            runtime_core_body, references, "deliberation"
        ),
    )
    opencode_explain_command = render_template(
        "adapters/opencode/deliberation.md.tmpl",
        COMMAND_DESCRIPTION=SKILL_INTERFACE["explain"]["command_description"],
        COMMAND_PREFIX=OPEN_CODE_PREFIXES["explain"],
        CORE_BODY=opencode_contract(
            runtime_explain_body, explain_references, "explain"
        ),
    )
    opencode_plugin = render_template(
        "adapters/opencode/deliberation.js.tmpl",
        VERSION=version,
    )
    opencode_package = render_template(
        "adapters/opencode/package.json.tmpl",
        VERSION=version,
    )
    opencode_readme = render_template(
        "adapters/opencode/README.md.tmpl",
        VERSION=version,
    )
    opencode_install_ps1 = render_template(
        "adapters/opencode/install.ps1.tmpl",
        VERSION=version,
    )
    opencode_install_sh = render_template(
        "adapters/opencode/install.sh.tmpl",
        VERSION=version,
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

    write_core(output / "standalone/codex/deliberation", canonical_skill, references)
    write_text(
        output / "standalone/codex/deliberation/agents/openai.yaml",
        codex_metadata,
    )
    write_core(output / "standalone/codex/explain", explain_skill, explain_references)
    write_text(
        output / "standalone/codex/explain/agents/openai.yaml",
        explain_codex_metadata,
    )
    write_core(
        output / "standalone/claude-code/deliberation",
        canonical_skill,
        references,
        claude=True,
    )
    write_core(
        output / "standalone/claude-code/explain",
        explain_skill,
        explain_references,
        claude=True,
    )

    codex_plugin = output / "publication/dist/codex"
    write_text(codex_plugin / ".codex-plugin/plugin.json", codex_manifest)
    codex_icon = ROOT / "adapters/codex/assets/deliberation-icon.svg"
    if not codex_icon.is_file():
        raise ValidationError(f"{codex_icon}: Codex plugin icon is missing")
    (codex_plugin / "assets").mkdir(parents=True, exist_ok=True)
    shutil.copy2(codex_icon, codex_plugin / "assets/deliberation-icon.svg")
    write_core(codex_plugin / "skills/deliberation", canonical_skill, references)
    write_text(
        codex_plugin / "skills/deliberation/agents/openai.yaml",
        codex_metadata,
    )
    write_core(codex_plugin / "skills/explain", explain_skill, explain_references)
    write_text(
        codex_plugin / "skills/explain/agents/openai.yaml",
        explain_codex_metadata,
    )

    claude_plugin = output / "publication/dist/claude-code"
    write_text(claude_plugin / ".claude-plugin/plugin.json", claude_manifest)
    write_core(
        claude_plugin / "skills/deliberation",
        canonical_skill,
        references,
        claude=True,
    )
    write_core(
        claude_plugin / "skills/explain",
        explain_skill,
        explain_references,
        claude=True,
    )

    opencode_bundle = output / "publication/dist/opencode"
    write_text(
        opencode_bundle / ".opencode/commands/deliberation.md",
        opencode_command,
    )
    write_text(
        opencode_bundle / ".opencode/commands/explain.md",
        opencode_explain_command,
    )
    write_text(
        opencode_bundle / ".opencode/plugins/deliberation.js",
        opencode_plugin,
    )
    write_core(opencode_bundle / "core/deliberation", canonical_skill, references)
    write_core(opencode_bundle / "core/explain", explain_skill, explain_references)
    write_text(opencode_bundle / "package.json", opencode_package)
    write_text(opencode_bundle / "README.md", opencode_readme)
    write_text(opencode_bundle / "install.ps1", opencode_install_ps1)
    write_text(opencode_bundle / "install.sh", opencode_install_sh)
    write_text(opencode_bundle / "VERSION", version)

    write_json(
        output / "integrity.json",
        {
            "canonical_core_sha256": canonical_core_digest(
                runtime_skill, references
            ),
            "canonical_explain_sha256": canonical_core_digest(
                runtime_explain_skill, explain_references
            ),
            "product_version": version,
            "runtime_payloads": {
                "claude-code": canonical_core_digest(runtime_skill, references),
                "codex": canonical_core_digest(runtime_skill, references),
                "opencode": canonical_core_digest(runtime_skill, references),
            },
            "explain_runtime_payloads": {
                "claude-code": canonical_core_digest(
                    runtime_explain_skill, explain_references
                ),
                "codex": canonical_core_digest(
                    runtime_explain_skill, explain_references
                ),
                "opencode": canonical_core_digest(
                    runtime_explain_skill, explain_references
                ),
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
    skill_name: str = "deliberation",
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
    if metadata["name"] != skill_name:
        raise ValidationError(f"{path}: invalid skill name")
    if claude and metadata["disable-model-invocation"] != "true":
        raise ValidationError(f"{path}: model invocation must be disabled")
    if body != expected_body:
        raise ValidationError(f"{path}: behavioural payload drifted from core")


def validate_core_references(root: Path, expected: dict[str, str]) -> None:
    actual = {
        path.relative_to(root).as_posix(): read_text(path).rstrip("\n") + "\n"
        for path in root.joinpath("references").rglob("*.md")
        if path.is_file()
    } if root.joinpath("references").is_dir() else {}
    if actual != expected:
        raise ValidationError(f"{root}: reference modules drifted from core")


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
    canonical_skill, _, core_body, references = canonical()
    explain_skill, _, explain_body, explain_references = canonical("explain")
    runtime_skill = materialize_reference_links(canonical_skill)
    runtime_core_body = materialize_reference_links(core_body)
    runtime_explain_skill = materialize_reference_links(explain_skill)
    runtime_explain_body = materialize_reference_links(explain_body)
    validate_checkpoint_semantics(references)

    validate_skill(
        output / "standalone/codex/deliberation/SKILL.md", runtime_core_body
    )
    validate_skill(
        output / "standalone/codex/explain/SKILL.md",
        runtime_explain_body,
        skill_name="explain",
    )

    for root in (
        output / "standalone/codex/deliberation",
        output / "publication/dist/codex/skills/deliberation",
        output / "standalone/claude-code/deliberation",
        output / "publication/dist/claude-code/skills/deliberation",
        output / "publication/dist/opencode/core/deliberation",
    ):
        validate_core_references(root, references)
    for root in (
        output / "standalone/codex/explain",
        output / "publication/dist/codex/skills/explain",
        output / "standalone/claude-code/explain",
        output / "publication/dist/claude-code/skills/explain",
        output / "publication/dist/opencode/core/explain",
    ):
        validate_core_references(root, explain_references)
    validate_skill(
        output
        / "publication/dist/codex/skills/deliberation/SKILL.md",
        runtime_core_body,
    )
    validate_skill(
        output / "standalone/claude-code/deliberation/SKILL.md",
        runtime_core_body,
        claude=True,
    )
    validate_skill(
        output
        / "publication/dist/claude-code/skills/deliberation/SKILL.md",
        runtime_core_body,
        claude=True,
    )
    validate_skill(
        output / "publication/dist/codex/skills/explain/SKILL.md",
        runtime_explain_body,
        skill_name="explain",
    )
    validate_skill(
        output / "standalone/claude-code/explain/SKILL.md",
        runtime_explain_body,
        skill_name="explain",
        claude=True,
    )
    validate_skill(
        output / "publication/dist/claude-code/skills/explain/SKILL.md",
        runtime_explain_body,
        skill_name="explain",
        claude=True,
    )

    for path in (
        output / "standalone/codex/deliberation/agents/openai.yaml",
        output
        / "publication/dist/codex/skills/deliberation/agents/openai.yaml",
        output / "standalone/codex/explain/agents/openai.yaml",
        output / "publication/dist/codex/skills/explain/agents/openai.yaml",
    ):
        metadata = read_text(path)
        if "allow_implicit_invocation: false" not in metadata:
            raise ValidationError(f"{path}: implicit invocation is not disabled")
        if "allow_implicit_invocation: true" in metadata:
            raise ValidationError(f"{path}: implicit invocation is enabled")

    for relative, manifest_type in (
        ("publication/dist/codex/.codex-plugin/plugin.json", "codex"),
        (
            "publication/dist/claude-code/.claude-plugin/plugin.json",
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

    codex_icon_path = output / "publication/dist/codex/assets/deliberation-icon.svg"
    if not codex_icon_path.is_file():
        raise ValidationError(f"{codex_icon_path}: generated Codex icon is missing")

    codex_marketplace_path = output / "publication/.agents/plugins/marketplace.json"
    codex_marketplace = require_json(codex_marketplace_path)
    expected_codex_marketplace = {
        "name": "deliberation",
        "interface": {"displayName": "Deliberation"},
        "plugins": [
            {
                "name": "deliberation",
                "source": {"source": "local", "path": "./dist/codex"},
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
                "source": "./dist/claude-code",
            }
        ],
    }
    if marketplace != expected_marketplace:
        raise ValidationError(
            f"{marketplace_path}: does not match the Deliberation marketplace contract"
        )

    for skill_name, expected_body, expected_references in (
        ("deliberation", core_body, references),
        ("explain", explain_body, explain_references),
    ):
        opencode_path = (
            output
            / "publication/dist/opencode/.opencode/commands"
            / f"{skill_name}.md"
        )
        command_metadata, command_body = parse_frontmatter(
            read_text(opencode_path), opencode_path
        )
        if set(command_metadata) != {"description"}:
            raise ValidationError(f"{opencode_path}: unexpected command metadata")
        prefix = OPEN_CODE_PREFIXES[skill_name]
        if not command_body.startswith(prefix):
            raise ValidationError(f"{opencode_path}: invalid command wrapper")
        if command_body[len(prefix) :] != opencode_contract(
            materialize_reference_links(expected_body),
            expected_references,
            skill_name,
        ):
            raise ValidationError(
                f"{opencode_path}: behavioural payload drifted from core"
            )

    audit_copy = (
        output
        / "publication/dist/opencode/core/deliberation/SKILL.md"
    )
    if read_text(audit_copy) != runtime_skill:
        raise ValidationError(f"{audit_copy}: audit copy differs from core")
    explain_audit_copy = (
        output / "publication/dist/opencode/core/explain/SKILL.md"
    )
    if read_text(explain_audit_copy) != runtime_explain_skill:
        raise ValidationError(f"{explain_audit_copy}: audit copy differs from core")
    if (
        read_text(
            output / "publication/dist/opencode/VERSION"
        ).strip()
        != version
    ):
        raise ValidationError("OpenCode bundle version differs from VERSION")

    opencode_plugin_path = (
        output
        / "publication/dist/opencode/.opencode/plugins/deliberation.js"
    )
    opencode_plugin = read_text(opencode_plugin_path)
    for fragment in (
        "export const DeliberationPlugin",
        "export default DeliberationPlugin",
        version,
        "/deliberation",
        "/explain",
    ):
        if fragment not in opencode_plugin:
            raise ValidationError(
                f"{opencode_plugin_path}: missing plugin contract {fragment!r}"
            )

    opencode_package_path = (
        output / "publication/dist/opencode/package.json"
    )
    opencode_package = require_json(opencode_package_path)
    if opencode_package.get("name") != "opencode-deliberation":
        raise ValidationError(f"{opencode_package_path}: invalid package name")
    if opencode_package.get("version") != version:
        raise ValidationError(f"{opencode_package_path}: version differs from VERSION")
    if opencode_package.get("exports") != "./.opencode/plugins/deliberation.js":
        raise ValidationError(f"{opencode_package_path}: invalid plugin export")
    expected_files = [
        ".opencode/commands/deliberation.md",
        ".opencode/commands/explain.md",
        ".opencode/plugins/deliberation.js",
        "core/deliberation",
        "core/explain",
        "install.ps1",
        "install.sh",
        "README.md",
        "VERSION",
    ]
    if opencode_package.get("files") != expected_files:
        raise ValidationError(f"{opencode_package_path}: invalid packaged files")

    for relative, fragments in {
        "README.md": (
            version,
            "/deliberation",
            "/explain",
            ".opencode/plugins/deliberation.js",
        ),
        "install.ps1": (
            version,
            ".config\\opencode",
            ".opencode",
            "Copy-Item",
            "deliberation.md",
            "explain.md",
            "deliberation.js",
        ),
        "install.sh": (
            version,
            ".config/opencode",
            ".opencode",
            "cp ",
            "deliberation.md",
            "explain.md",
            "deliberation.js",
        ),
    }.items():
        path = output / "publication/dist/opencode" / relative
        content = read_text(path)
        for fragment in fragments:
            if fragment not in content:
                raise ValidationError(
                    f"{path}: missing OpenCode installer contract {fragment!r}"
                )

    publication_root = output / "publication"
    for path in publication_root.rglob("*"):
        if path.is_file():
            content = read_text(path)
            if "../" in content or "..\\" in content:
                raise ValidationError(
                    f"{path}: published artifact references an external path"
                )

    integrity = require_json(output / "integrity.json")
    expected_digest = canonical_core_digest(runtime_skill, references)
    expected_explain_digest = canonical_core_digest(
        runtime_explain_skill, explain_references
    )
    if integrity.get("product_version") != version:
        raise ValidationError("integrity metadata version differs from VERSION")
    if integrity.get("canonical_core_sha256") != expected_digest:
        raise ValidationError("integrity metadata has an invalid core digest")
    if integrity.get("canonical_explain_sha256") != expected_explain_digest:
        raise ValidationError("integrity metadata has an invalid explain digest")
    if integrity.get("runtime_payloads") != {
        "claude-code": expected_digest,
        "codex": expected_digest,
        "opencode": expected_digest,
    }:
        raise ValidationError("runtime payload digests are inconsistent")
    if integrity.get("explain_runtime_payloads") != {
        "claude-code": expected_explain_digest,
        "codex": expected_explain_digest,
        "opencode": expected_explain_digest,
    }:
        raise ValidationError("explain runtime payload digests are inconsistent")

    validate_fixtures()
    validate_installers()


def validate_installers() -> None:
    version = product_version()
    tag = release_tag(version)
    asset_name = release_asset_name(version)
    required_fragments = {
        ROOT / "install.ps1": (
            "fpiechowski/deliberation",
            f'"{tag}"',
            '"plugin", "marketplace", "upgrade"',
            '"plugin", "marketplace", "add"',
            '"plugin", "remove"',
            '"plugin", "add"',
            "ConvertFrom-Json",
        ),
        ROOT / "install.sh": (
            "#!/usr/bin/env sh",
            "fpiechowski/deliberation",
            f'marketplace_ref="{tag}"',
            "plugin marketplace upgrade",
            "plugin marketplace add",
            "plugin remove",
            "plugin add",
        ),
        ROOT / "install-claude-code.sh": (
            "#!/usr/bin/env sh",
            "fpiechowski/deliberation",
            "claude plugin marketplace list --json",
            "claude plugin marketplace update",
            "claude plugin marketplace add",
            "claude plugin list --json",
            "has_user_scope_plugin",
            '"scope"',
            "awk",
            "claude plugin update",
            "claude plugin install",
            "--scope user",
        ),
        ROOT / "install-opencode.ps1": (
            tag,
            asset_name,
            "Invoke-WebRequest",
            "Expand-Archive",
            "install.ps1",
            "System.IO.Directory",
        ),
        ROOT / "install-opencode.sh": (
            "#!/usr/bin/env sh",
            tag,
            asset_name,
            "curl",
            "unzip",
            "install.sh",
        ),
    }
    for path, fragments in required_fragments.items():
        content = read_text(path)
        for fragment in fragments:
            if fragment not in content:
                raise ValidationError(f"{path}: missing installer contract {fragment!r}")

    for path in (
        ROOT / "install.ps1",
        ROOT / "install.sh",
        ROOT / "install-claude-code.sh",
    ):
        content = read_text(path).lower()
        for fragment in ("invoke-webrequest", "expand-archive", "curl ", "wget "):
            if fragment in content:
                raise ValidationError(
                    f"{path}: Git-marketplace installer contains legacy download marker {fragment!r}"
                )

    validate_claude_installer_scope_selection()


def validate_claude_installer_scope_selection() -> None:
    """Exercise the Claude installer against each supported plugin scope."""
    shell = shutil.which("bash") or shutil.which("sh")
    if shell is None:
        return

    installer = ROOT / "install-claude-code.sh"
    with tempfile.TemporaryDirectory(prefix="deliberation-claude-installer-") as temporary:
        temporary_root = Path(temporary)
        harness = temporary_root / "claude-harness.sh"
        log = temporary_root / "calls.log"

        scenarios = {
            "project": "plugin install --scope user deliberation@deliberation",
            "local": "plugin install --scope user deliberation@deliberation",
            "user": "plugin update --scope user deliberation@deliberation",
        }
        for scope, expected_call in scenarios.items():
            log.write_text("", encoding="utf-8", newline="\n")
            plugins_json = json.dumps(
                [{"id": "deliberation@deliberation", "scope": scope}], indent=2
            )
            write_text(
                harness,
                f"""#!/usr/bin/env sh
set -eu
claude() {{
printf '%s\\n' \"$*\" >> '{shell_path(log)}'
case \"$*\" in
  \"plugin marketplace list --json\") printf '%s\\n' '[]' ;;
  \"plugin marketplace add --scope user fpiechowski/deliberation\") ;;
  \"plugin marketplace update deliberation\") ;;
  \"plugin list --json\") printf '%s\\n' '{plugins_json}' ;;
  \"plugin update --scope user deliberation@deliberation\") ;;
  \"plugin install --scope user deliberation@deliberation\") ;;
  *) exit 99 ;;
esac
}}
. '{shell_path(installer)}'
""",
            )
            result = subprocess.run(
                [shell, shell_path(harness)],
                capture_output=True,
                check=False,
                text=True,
            )
            if result.returncode != 0:
                raise ValidationError(
                    "Claude installer scope fixture failed for "
                    f"{scope!r}: {result.stderr.strip() or result.stdout.strip()}"
                )
            calls = log.read_text(encoding="utf-8").splitlines()
            if expected_call not in calls:
                raise ValidationError(
                    f"Claude installer did not select {expected_call!r} for {scope!r} scope"
                )


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
        raise ValidationError("output path must stay inside the repository") from exc
    if relative == Path("."):
        raise ValidationError("output path cannot be the repository root")
    for protected_root in PROTECTED_OUTPUT_ROOTS:
        if relative == protected_root or protected_root in relative.parents:
            raise ValidationError(
                f"output path cannot overlap protected publication root {protected_root}"
            )
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


def command_package_release(args: argparse.Namespace) -> None:
    output = checked_output(args.output)
    archive_path, checksum_path = package_release(output)
    print(
        "Packaged release assets: "
        f"{archive_path.relative_to(ROOT)}, {checksum_path.relative_to(ROOT)}"
    )


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

    package_parser = subcommands.add_parser(
        "package-release",
        help="build deterministic release assets from the validated OpenCode bundle",
    )
    package_parser.add_argument(
        "--output",
        default="build/release",
        help="repository-relative asset directory (default: build/release)",
    )
    package_parser.set_defaults(handler=command_package_release)
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
