Set-StrictMode -Version latest

function Install-PPM-cpanm {
    ppm install App-cpanminus
}

function Complete-Install {
    Install-PPM-cpanm
}

Export-ModuleMember -Function Install-PPM-cpanm, Complete-Install
