from bears.hypertext.HTMLHintBear import HTMLHintBear
from coalib.testing.LocalBearTestHelper import verify_local_bear

good_file = """
<!DOCTYPE HTML>
<html>
<head>
    <meta charset="UTF-8">
    <title>HTMLHint</title>
</head>
<body>
    <div>HTMLHint: help your html code better</div>
</body>
</html>
"""

bad_file = """
<!DOCTYPE HTML>
<html>
<head>
    <meta charset="UTF-8">
    <title>HTMLHint</title>
</head>
<body>
    <div>HTMLHint: help your html code better
</body>
</html>
"""

HTMLHintBearTest = verify_local_bear(HTMLHintBear,
                                     valid_files=(good_file,),
                                     invalid_files=(bad_file,))
