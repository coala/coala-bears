function Install-Perl-Modules {
    cpanm --quiet --installdeps --with-develop --notest .

    Remove-Item -Force MYMETA.yml -ErrorAction Ignore
}

function Invoke-ExtraInstallation {
    Install-Perl-Modules
}
