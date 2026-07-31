$ErrorActionPreference = "Stop"

$marketplaceName = "deliberation"
$marketplaceSource = "fpiechowski/deliberation"
$marketplaceRef = "v0.1.0-dev.14"
$pluginId = "deliberation@deliberation"

function Invoke-CodexCommand {
    param([string[]]$CommandArguments)

    & codex @CommandArguments
    if ($LASTEXITCODE -ne 0) {
        throw "codex $($CommandArguments -join ' ') failed with exit code $LASTEXITCODE."
    }
}

function Get-CodexJson {
    param([string[]]$CommandArguments)

    $output = & codex @CommandArguments
    if ($LASTEXITCODE -ne 0) {
        throw "codex $($CommandArguments -join ' ') failed with exit code $LASTEXITCODE."
    }
    return ($output | ConvertFrom-Json)
}

if (-not (Get-Command codex -ErrorAction SilentlyContinue)) {
    throw "Codex CLI was not found on PATH. Install Codex, then run this script again."
}

$marketplaces = (Get-CodexJson @("plugin", "marketplace", "list", "--json")).marketplaces
if ($marketplaces.name -contains $marketplaceName) {
    Write-Host "Refreshing the Deliberation marketplace..."
    Invoke-CodexCommand @("plugin", "marketplace", "upgrade", $marketplaceName)
}
else {
    Write-Host "Adding the Deliberation marketplace..."
    Invoke-CodexCommand @("plugin", "marketplace", "add", $marketplaceSource, "--ref", $marketplaceRef)
}

$installed = (Get-CodexJson @("plugin", "list", "--json")).installed
if ($installed.pluginId -contains $pluginId) {
    Write-Host "Updating Deliberation..."
    Invoke-CodexCommand @("plugin", "remove", $pluginId)
}

try {
    Invoke-CodexCommand @("plugin", "add", $pluginId)
}
catch {
    Write-Error "Deliberation was removed but could not be reinstalled. After fixing the error, run: codex plugin add $pluginId"
    throw
}

Write-Host "Deliberation is installed. Start a new Codex conversation (or restart Codex Desktop), then invoke `$deliberation."
