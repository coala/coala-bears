Set-StrictMode -Version latest

function Add-EnvPythonVersion {
    if ($env:TRAVIS -and $env:TRAVIS_PYTHON_VERSION) {
        $env:PYTHON_VERSION = $env:TRAVIS_PYTHON_VERSION
    }
    else {
        $env:PYTHON_VERSION = python -c 'import sys; print(sys.version[0:3])'
    }
}

function Add-EnvPythonMinorDotless {
    if (!($env:PYTHON_MINOR_NODOTS)) {
        $python_minor = $env:PYTHON_VERSION.Substring(0, 3)

        $env:PYTHON_MINOR_NODOTS = $python_minor -replace '.', ''
    }
}

function Add-PATHPythonRoaming {
    $roaming_home = (
        $env:APPDATA + '/Python/Python' + $env:PYTHON_MINOR_NODOTS)

    Install-ChocolateyPath -PathToInstall $roaming_home
    Install-ChocolateyPath -PathToInstall ($roaming_home + '/Scripts')
}

function Add-EnvPipNonEagerUpgradeStrategy {
    $env:PIP_UPGRADE_STRATEGY = 'only-if-needed'

    Set-ItemProperty -Path 'HKCU:\Environment' -Name 'PIP_UPGRADE_STRATEGY' -Value $env:PIP_UPGRADE_STRATEGY
}

function Complete-Install {
    Add-EnvPythonVersion

    Add-EnvPythonMinorDotless

    Add-EnvPipNonEagerUpgradeStrategy

    Add-PATHPythonRoaming
}

Export-ModuleMember -Function Complete-Install
