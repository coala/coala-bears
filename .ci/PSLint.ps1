Set-StrictMode -Version Latest

$ErrorActionPreference = 'Stop'

Import-Module -Name 'PsScriptAnalyzer' -Force
$base = $global:PSScriptRoot

$Utf8NoBomEncoding = New-Object System.Text.UTF8Encoding $False

function Test-Skip-File {
    param (
        [Parameter(Mandatory)]
        [string]
        $filename
    )

    # Ignore imported files
    # https://github.com/pypa/virtualenv/issues/1371
    # https://github.com/ogrisel/python-appveyor-demo/issues/55
    # https://github.com/MathieuBuisson/PowerShell-DevOps/issues/6
    return (
        $filename -eq 'Export-NUnitXml.psm1' -or
        $filename -eq 'Fudge.ps1' -or
        $filename -eq 'FudgeTools.psm1' -or
        $filename -eq 'install.ps1' -or
        $filename -eq 'activate.ps1' -or
        $filename.EndsWith('.jj2'))
}

$Utf8NoBomEncoding = New-Object System.Text.UTF8Encoding $False

$UNIXEOL = "`n"

function ReformatFile {
    param (
        [Parameter(Mandatory)]
        [string]
        $filename,

        [Parameter(Mandatory)]
        [string]
        $eol
    )
    $orig = Get-Content -Raw $filename
    $content = Invoke-Formatter -ScriptDefinition $orig -Settings $base\PSScriptAnalyzerSettings.psd1 -ErrorAction Stop

    if ($content) {
        $content = $content -split "`r?`n"
        if (!($content[-1])) {
            $content = $content[0..($content.length - 2)]
        }
        $content = (($content -join $eol) + $eol)
        [System.IO.File]::WriteAllText($filename, $content, $Utf8NoBomEncoding)
    }
}

[Microsoft.Windows.PowerShell.ScriptAnalyzer.Generic.DiagnosticRecord[]]$ScriptAnalyzerResult = $null

Get-ChildItem -Recurse -Force '*.ps*' | ForEach-Object {
    $path = $_.FullName

    if ( $path.Contains('.git') -or (Test-Skip-File($_.Name)) ) {
        Write-Output "Skipping $path"
    }
    else {
        $NewResult = Invoke-ScriptAnalyzer -IncludeDefaultRules -Setting $base\PSScriptAnalyzerSettings.psd1 -Path $path
        if ($ScriptAnalyzerResult) {
            $ScriptAnalyzerResult += $NewResult
        }
        else {
            $ScriptAnalyzerResult = $NewResult
        }

        ReformatFile $path $UNIXEOL
    }
}

if ($env:APPVEYOR) {
    Import-Module "$base\Export-NUnitXml.psm1"
    Export-NUnitXml -ScriptAnalyzerResult $ScriptAnalyzerResult -Path ".\ScriptAnalyzerResult.xml"
    (New-Object 'System.Net.WebClient').UploadFile(
        "https://ci.appveyor.com/api/testresults/nunit/$($env:APPVEYOR_JOB_ID)",
        (Resolve-Path .\ScriptAnalyzerResult.xml)
    )
}

git diff

if ($ScriptAnalyzerResult) {
    Write-Output $ScriptAnalyzerResult

    # Failing the build
    Throw 'Build failed because there was one or more PSScriptAnalyzer violation. See test results for more information.'
}
