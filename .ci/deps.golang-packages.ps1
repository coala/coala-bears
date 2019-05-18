function Install-GoMetalinter-Linters {
    gometalinter.v2.exe '--install'
}

function Invoke-ExtraInstallation {
    Install-GoMetalinter-Linters

    go get -u github.com/BurntSushi/toml/cmd/tomlv
    go get -u sourcegraph.com/sqs/goreturns
}
