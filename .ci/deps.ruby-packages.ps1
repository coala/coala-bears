function Install-Gemfile {
    cp -force Gemfile Gemfile.orig
    cp -force Gemfile Gemfile.win

    # Unbuildable on Windows
    sed -i '/sqlint/d' Gemfile.win
    # https://github.com/coala/coala-bears/issues/2909
    sed -i '/csvlint/d' Gemfile.win

    # pusher-client 0.4.0 doesnt depend on json, which requires
    # a compiler and the GMP library
    Write-Output 'gem "pusher-client", "~>0.4.0", require: false' |
        Out-File -FilePath Gemfile.win -Append -Encoding ascii

    cp -force Gemfile.win Gemfile

    # The build crawls if DevKit is included in the PATH
    $old_PATH = $env:PATH
    $env:PATH = ($env:ChocolateyToolsLocation + '\DevKit2\bin;' + $env:PATH)

    bundle install

    $env:PATH = $old_PATH

    mv -force Gemfile.orig Gemfile
}

function Invoke-ExtraInstallation {
    Install-Gemfile
}
