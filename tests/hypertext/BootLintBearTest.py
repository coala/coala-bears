from bears.hypertext.BootLintBear import BootLintBear
from tests.LocalBearTestHelper import verify_local_bear


good_file = """
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8" />
        <meta http-equiv="X-UA-Compatible" content="IE=edge" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Test</title>
        <!--[if lt IE 9]>
            <script src="https://oss.maxcdn.com/html5shiv/3.7.2/
            html5shiv.min.js">
            </script>
            <script src="https://oss.maxcdn.com/respond/1.4.2/
            respond.min.js">
            </script>
        <![endif]-->
        <script src="../../lib/jquery.min.js"></script>

        <link rel="stylesheet" href="../../lib/qunit.css">
        <script src="../../lib/qunit.js"></script>
        <script src="../../../dist/browser/bootlint.js"></script>
        <script src="../generic-qunit.js"></script>
    </head>
    <body>

        <button type="submit">Submit</button>
        <button type="reset">Reset</button>
        <button type="button">Button</button>

        <div id="qunit"></div>
        <ol id="bootlint"></ol>
    </body>
</html>
""".splitlines(keepends=True)

bad_file = """
<html lang="en">
    <head>
        <meta http-equiv="X-UA-Compatible" content="IE=edge" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Test</title>
        <!--[if lt IE 9]>
            <script src="https://oss.maxcdn.com/html5shiv/3.7.2/
            html5shiv.min.js"></script>
            <script src="https://oss.maxcdn.com/respond/1.4.2/
            respond.min.js"></script>
        <![endif]-->
        <script src="../../lib/jquery.min.js"></script>

        <link rel="stylesheet" href="../../lib/qunit.css">
        <script src="../../lib/qunit.js"></script>
        <script src="../../../dist/browser/bootlint.js"></script>
        <script src="../generic-qunit.js"></script>
    </head>
    <body>

        <button>No type set</button>
        <div>
          <div class="panel-body">
            <p>Something</p>
          </div>
        </div>

        <div id="qunit"></div>
        <ol id="bootlint">
          <li data-lint="Found one or more `<button>`s
           missing a `type` attribute."></li>
        </ol>
    </body>
</html>
""".splitlines(keepends=True)
# There's a missing type in <button> tag, missing DOCTYPE
# and panel has no body.

BootLintBearTest = verify_local_bear(BootLintBear,
                                     valid_files=(good_file,),
                                     invalid_files=(bad_file,))

BootLintBearDisableTest = verify_local_bear(
    BootLintBear,
    valid_files=(good_file, bad_file),
    invalid_files=(),
    settings={'bootlint_ignore': 'W001,W007,E001,E023'})
