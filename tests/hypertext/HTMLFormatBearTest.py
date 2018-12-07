from queue import Queue

from bears.hypertext.HTMLFormatBear import HTMLFormatBear
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


good_file_1 = """<!doctype html>
<html>
  <head>
    <title>Hello!</title>
    <meta charset="utf8">
  </head>
  <body>
    <section>
      <p>hi there</p>
    </section>
  </body>
</html>""".splitlines(True)


good_file_2 = """
<!doctype html>
<html>
  <head>
    <title>Foo</title>
  </head>

  <body>
    <main>
      <p>Bar</p>
    </main>
  </body>
</html>""".splitlines(True)


good_file_3 = """<!doctype html>
<html>
   <head></head>
   <body>
      <p>
         Foo
         <strong>bar</strong>
      </p>
   </body>
</html>""".splitlines(True)


good_file_4 = """<!doctype html>
<html>
    <head></head>
    <body>
        <p>
            Foo
            <strong>bar</strong>
        </p>
    </body>
</html>""".splitlines(True)


good_file_5 = """<!doctype html>
<html>
<head>
  <title>Foo</title>
</head>
<body>
  <p>Bar</p>
</body>
</html>""".splitlines(True)


bad_file_1 = """<!doCTYPE HTML><html>
 <head>
    <title>Hello!</title>
<meta charset=utf8>
      </head>
  <body><section>    <p>hi there</p>
     </section>
 </body>
</html>""".splitlines(True)


bad_file_2 = """<!doctype html>
<html>
<head>
<title>
Foo
</title>
</head>
<body>
<main>
<p>Bar</p>
</main>
</body>
</html>""".splitlines(True)


bad_file_3 = """<!doctype html><p>Foo
<strong>bar</strong></p>""".splitlines(True)


class HTMLFormatBearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section('name')
        self.uut = HTMLFormatBear(self.section, Queue())

    def test_default(self):
        self.check_validity(self.uut, good_file_1)
        self.check_invalidity(self.uut, bad_file_1)

    def test_blanks_head_body_main(self):
        self.section.append(Setting('blanks', ['head', 'body', 'main']))
        self.check_validity(self.uut, good_file_2)

    def test_indent_char(self):
        self.section.append(Setting('indent', '   '))
        self.check_validity(self.uut, good_file_3)

    def test_indent_num(self):
        self.section.append(Setting('indent', 4))
        self.check_validity(self.uut, good_file_4)

    def test_initial_false(self):
        self.section.append(Setting('indentInitial', False))
        self.check_validity(self.uut, good_file_5)
