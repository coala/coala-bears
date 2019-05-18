function Install-Node-Packages {
    npm config set loglevel warn

    # pnpm setting
    npm config set reporter silent

    cp -force package.json package.json.bak

    # elm-platform should be added to Fudgefile
    # https://github.com/coala/coala-bears/issues/2924
    sed -i '/elm/d' package.json

    # textlint-plugin-asciidoc-loose requires a compiler
    # and should be replaced with textlint-plugin-asciidoctor
    sed -i '/textlint-plugin-asciidoc-loose/d' package.json

    # If gyp fails, use npm config python to help locate Python 2.7

    $old_EAP = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'

    npm install

    $ErrorActionPreference = $old_EAP

    mv -force package.json.bak package.json

    npm config set reporter default
}

function Invoke-ExtraInstallation {
    Install-Node-Packages
}
