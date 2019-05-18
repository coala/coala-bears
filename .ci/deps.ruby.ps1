Set-StrictMode -Version latest

function Install-Bundler {
    gem install bundler
}

function Complete-Install {
    Install-Bundler
}

Export-ModuleMember -Function Complete-Install
