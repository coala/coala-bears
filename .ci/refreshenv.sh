# shellcheck disable=SC2059,SC2154
# as shellcheck believes the $ in the heredoc are shell variables

function refreshenv
{
  powershell -NonInteractive - <<\EOF
Import-Module "$env:ChocolateyInstall\helpers\chocolateyProfile.psm1"

Update-SessionEnvironment

# Round brackets in variable names cause problems with bash
Get-ChildItem env:* | %{
  if (!($_.Name.Contains('('))) {
    $value = $_.Value
    if ($_.Name -eq 'PATH') {
      $value = $value -replace ';',':'
    }
    Write-Output ("export " + $_.Name + "='" + $value + "'")
  }
} | Out-File -Encoding ascii $env:TEMP\refreshenv.sh

EOF

  # shellcheck disable=SC1090
  # as shellcheck can not follow this `source`
  source "$TEMP/refreshenv.sh"
}

alias RefreshEnv=refreshenv
