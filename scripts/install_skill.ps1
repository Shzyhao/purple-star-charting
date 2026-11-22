# 将 purple-star-charting 安装到 DSH skills 目录
# 用法：powershell -ExecutionPolicy Bypass -File scripts/install_skill.ps1 [-Target <skills目录>]
param(
    [string]$Target = "$env:USERPROFILE\.dsh\skills"
)
$ErrorActionPreference = "Stop"
$src = Join-Path $PSScriptRoot "..\skills\purple-star-charting"
if (-not (Test-Path $src)) { throw "找不到 skills/purple-star-charting" }
New-Item -ItemType Directory -Force -Path $Target | Out-Null
$dst = Join-Path $Target "purple-star-charting"
if (Test-Path $dst) { Remove-Item $dst -Recurse -Force }
Copy-Item $src $dst -Recurse
Write-Output "已安装到: $dst"
Write-Output "重新打开 DSH 会话后即可在 skill 目录看到 purple-star-charting"
