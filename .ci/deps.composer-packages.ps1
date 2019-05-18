function Install-Composer-DependList {
    $composer_phar = "C:\ProgramData\ComposerSetup\bin\composer.phar"

    php.exe $composer_phar install
}

function Invoke-ExtraInstallation {
    Install-Composer-DependList
}
