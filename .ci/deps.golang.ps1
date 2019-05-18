Set-StrictMode -Version latest

function Install-GoPM {
    go.exe get -u github.com/gpmgo/gopm
    go.exe install github.com/gpmgo/gopm
}

function Install-GoMetaLinter {
    go.exe get -u gopkg.in/alecthomas/gometalinter.v2
}

function Complete-Install {
    Install-GoMetaLinter

    Install-GoPM
}

Export-ModuleMember -Function Install-GoPM, Install-GoMetaLinter, Complete-Install
