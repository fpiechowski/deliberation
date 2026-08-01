param(
  [ValidateSet("Global", "Project")]
  [string]$Scope = "Global",

  [string]$ProjectPath = (Get-Location).Path
)

$ErrorActionPreference = "Stop"

$sourceRoot = $PSScriptRoot
$profileRoot = [Environment]::GetFolderPath("UserProfile")

if ($Scope -eq "Global") {
  $configRoot = Join-Path $profileRoot ".config\opencode"
} else {
  $resolvedProject = (Resolve-Path -LiteralPath $ProjectPath).Path
  $configRoot = Join-Path $resolvedProject ".opencode"
}

$commandsRoot = Join-Path $configRoot "commands"
$pluginsRoot = Join-Path $configRoot "plugins"

New-Item -ItemType Directory -Path $commandsRoot -Force | Out-Null
New-Item -ItemType Directory -Path $pluginsRoot -Force | Out-Null

Copy-Item `
  -LiteralPath (Join-Path $sourceRoot ".opencode\commands\deliberation.md") `
  -Destination (Join-Path $commandsRoot "deliberation.md") `
  -Force

Copy-Item `
  -LiteralPath (Join-Path $sourceRoot ".opencode\commands\explain.md") `
  -Destination (Join-Path $commandsRoot "explain.md") `
  -Force

Copy-Item `
  -LiteralPath (Join-Path $sourceRoot ".opencode\plugins\deliberation.js") `
  -Destination (Join-Path $pluginsRoot "deliberation.js") `
  -Force

Write-Host "Installed Deliberation 0.1.0-dev.14 for OpenCode at $configRoot"
Write-Host "Start OpenCode and invoke /deliberation or /explain."
