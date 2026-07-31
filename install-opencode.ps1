param(
    [ValidateSet("Global", "Project")]
    [string]$Scope = "Global",

    [string]$ProjectPath = (Get-Location).Path
)

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

$releaseTag = "v0.1.0-dev.14"
$assetName = "opencode-deliberation-0.1.0-dev.14.zip"
$downloadUrl = "https://github.com/fpiechowski/deliberation/releases/download/$releaseTag/$assetName"
$temporaryRoot = Join-Path ([System.IO.Path]::GetTempPath()) "deliberation-opencode-$([System.Guid]::NewGuid().ToString('N'))"
$zipPath = Join-Path $temporaryRoot $assetName
$extractPath = Join-Path $temporaryRoot "dist"

try {
    New-Item -ItemType Directory -Path $temporaryRoot | Out-Null

    Write-Host "Downloading Deliberation OpenCode $releaseTag..."
    Invoke-WebRequest -Uri $downloadUrl -OutFile $zipPath -UseBasicParsing

    Write-Host "Extracting Deliberation OpenCode dist..."
    Expand-Archive -LiteralPath $zipPath -DestinationPath $extractPath -Force

    $installer = Join-Path $extractPath "install.ps1"
    if (-not (Test-Path -LiteralPath $installer)) {
        throw "Downloaded OpenCode dist does not contain install.ps1."
    }

    & $installer -Scope $Scope -ProjectPath $ProjectPath
}
finally {
    if (Test-Path -LiteralPath $temporaryRoot) {
        [System.IO.Directory]::Delete($temporaryRoot, $true)
    }
}
