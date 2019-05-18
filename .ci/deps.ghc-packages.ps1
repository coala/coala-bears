function Install-Cabal-Deps {
    cabal install --only-dependencies --avoid-reinstalls
}

function Invoke-ExtraInstallation {
    Install-Cabal-Deps
}
