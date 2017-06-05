import unittest
from queue import Queue
from coalib.settings.Section import Section
from bears.jinja2.Jinja2Bear import Jinja2Bear
from coalib.testing.LocalBearTestHelper import verify_local_bear, execute_bear


Jinja2BearVariableSpacingTest = verify_local_bear(
    Jinja2Bear,
    valid_files=(r'foo {{ var }}',
                 r'foo {{ var1|filter }} bar {{ var2 }}'),
    invalid_files=(r'foo {{var }}',
                   r'foo {{ var}} bar',
                   r'{{  var }}',
                   r'{{ good_var }} foo {{bad_var }}'))

Jinja2BearCustomVariableSpacingTest = verify_local_bear(
    Jinja2Bear,
    valid_files=(r'foo {{var}}',
                 r'foo {{var1|filter}} bar {{var2}}'),
    invalid_files=(r'foo {{ var }}',
                   r'foo {{ var}} bar',
                   r'{{  var }}'),
    settings={'variable_spacing': '0'})


class Jinja2BearSpacingDiffTest(unittest.TestCase):

    def setUp(self):
        self.uut = Jinja2Bear(Section(''), Queue())

    def test_variable_spacing(self):
        content = (r'foo {{var }} bar',)
        with execute_bear(self.uut, 'F', content) as result:
            self.assertEqual(result[0].diffs['F'].unified_diff,
                             '--- \n'
                             '+++ \n'
                             '@@ -1 +1 @@\n'
                             '-foo {{var }} bar\n'
                             '+foo {{ var }} bar')

    def test_control_spacing(self):
        content = [
            '{% for x in y %}\n',
            'rendering stuff\n',
            '{% endfor%}{# for x in y #}\n'
        ]
        with execute_bear(self.uut, 'F', content) as result:
            self.assertEqual(result[0].diffs['F'].unified_diff,
                             '--- \n'
                             '+++ \n'
                             '@@ -1,3 +1,3 @@\n'
                             ' {% for x in y %}\n'
                             ' rendering stuff\n'
                             '-{% endfor%}{# for x in y #}\n'
                             '+{% endfor %}{# for x in y #}\n')


Jinja2BearControlSpacingTest = verify_local_bear(
    Jinja2Bear,
    valid_files=(r'foo {% if something %} bar {% endif %}',),
    invalid_files=(r'foo {% if var%} bar {% endif %}',
                   r'{% if something %} foo {%endif%}{# if something #}',
                   r'{%for a in var %} {% endfor %}'))

Jinja2BearCustomControlSpacingTest = verify_local_bear(
    Jinja2Bear,
    valid_files=(r'foo {%if something%} bar {%endif%}',),
    invalid_files=(r'foo {% if var%} bar {%endif%}',
                   r'foo {%if foo%} bar {% endif%}',
                   r'{%for a in var %} {%endfor%}'),
    settings={'control_spacing': '0'})


good_file1 = """
foo
{% for x in something %}
render stuff
{% endfor %}{# for x in something #}
"""

good_file2 = """
foo
{% if x == something %}
render stuff
{% endif %}{# if x == something #}
"""

good_file3 = '{% for x in y %} one liner needs no label {% endfor %}'

bad_file1 = """
foo
{% for x in something %}
render stuff
{% endfor %} more stuff
"""

bad_file2 = """
foo
{% if x == something %}
render stuff
{% endif %}{# some random comment #} more stuff
"""

Jinja2BearForLoopLabelTest = verify_local_bear(
    Jinja2Bear,
    valid_files=(good_file1, good_file2, good_file3),
    invalid_files=(bad_file1, bad_file2))


class Jinja2BearLabelDiffTest(unittest.TestCase):

    def setUp(self):
        self.section = Section('')
        self.uut = Jinja2Bear(self.section, Queue())

    def test_missing_label(self):
        content = [line + '\n' for line in bad_file1.splitlines()]
        with execute_bear(self.uut, 'F', content) as result:
            self.assertEqual(
                result[0].diffs['F'].unified_diff,
                '--- \n'
                '+++ \n'
                '@@ -2,4 +2,4 @@\n'
                ' foo\n'
                ' {% for x in something %}\n'
                ' render stuff\n'
                '-{% endfor %} more stuff\n'
                '+{% endfor %}{# for x in something #} more stuff\n')

    def test_wrong_label(self):
        content = [line + '\n' for line in bad_file2.splitlines()]
        with execute_bear(self.uut, 'F', content) as result:
            self.assertEqual(
                result[0].diffs['F'].unified_diff,
                '--- \n'
                '+++ \n'
                '@@ -2,4 +2,4 @@\n'
                ' foo\n'
                ' {% if x == something %}\n'
                ' render stuff\n'
                '-{% endif %}{# some random comment #} more stuff\n'
                '+{% endif %}{# if x == something #} more stuff\n')


Jinja2BearControlBlockTest = verify_local_bear(
    Jinja2Bear,
    valid_files=('foo {% for a in b %} bar {% endfor %}',),
    invalid_files=('This {% for a in b %} has no closing tag',
                   'This {% endif %} has no open tag'))
