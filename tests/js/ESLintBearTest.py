import os
from pathlib import Path
from queue import Queue
from unittest import mock

from bears.js.ESLintBear import ESLintBear

from coalib.results.Result import RESULT_SEVERITY, Result
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting
from coalib.bearlib.languages import Language
from coalib.testing.BearTestHelper import generate_skip_decorator
from coalib.testing.LocalBearTestHelper import (
    verify_local_bear,
    LocalBearTestHelper,
    get_results,
)


test_good = """function addOne(i) {
    if (!isNaN(i)) {
        return i+1;
    }
    return i;
}

addOne(3);
"""

test_bad = """function addOne(i) {
    if (i != NaN) {
        return i ++
    }
    else {
        return
    }
};
"""

test_import_good = """
import test from "./test";

test();
"""

test_import_bad = """
import test from "../test";

test();
"""

test_file_global_vars = """
(function(a,b,c) {
    return [a, b, c];
})(x,y,z)
"""

test_file_eslint_env = """
(function(a) {
    return a;
})(suiteSetup)

"""

test_file_markdown = """
# H1
## H2
```js
// This gets linted
var answer = 6 * 7;
(function(a) {
    return a;
})(answer)
```
"""

test_file_markdown_bad = """
# H1
## H2
```js
var answer = 6 * 7;
```
"""

test_file_HTML = """
<head></head>
<body>
<script>
var foo = 1;
(function(a) {
    return a;
})(foo)
</script>
</body>
"""

test_file_HTML_bad = """
<head></head>
<body>
<script>
var foo = 1
</script>
</body>
"""

test_file_typescript = """
function greeter (person: string) {
  return 'Hello, ' + person
}
greeter('Bob')
"""

test_syntax_error = '{<!@3@^ yeah!/\n'

test_dir = os.path.join(os.path.dirname(__file__), 'test_files')

ESLintBearWithConfigTest = verify_local_bear(
    ESLintBear,
    valid_files=('',),
    invalid_files=(test_bad, test_good),
    settings={'eslint_config': os.path.join(test_dir, 'eslintconfig.json')})

ESLintBearWithoutConfigTest = verify_local_bear(
    ESLintBear,
    valid_files=(test_good, ''),
    invalid_files=(test_syntax_error, test_bad))

# If there is an invalid config file, the results cannot be found. So, no
# file gives a result.
ESLintBearWithUnloadablePluginTest = verify_local_bear(
    ESLintBear,
    valid_files=(test_bad, test_good),
    invalid_files=(),
    settings={'eslint_config': os.path.join(test_dir,
                                            'eslintconfig_badplugin.json')})
ESLintBearImportTest = verify_local_bear(
    ESLintBear,
    valid_files=(test_import_good, ),
    invalid_files=(test_import_bad, ),
    filename=os.path.join(test_dir, 'test.js'),
    create_tempfile=False,
    settings={'eslint_config': os.path.join(test_dir,
                                            'eslintconfig_import.json')})

ESLintBearGlobalVarsTest = verify_local_bear(
    ESLintBear,
    invalid_files=(),
    valid_files=(test_file_global_vars,),
    settings={'global_vars': 'x,y,z'})

ESLintBearEslintEnvTest = verify_local_bear(
    ESLintBear,
    invalid_files=(),
    valid_files=(test_file_eslint_env,),
    settings={'eslint_env': 'mocha'})


@generate_skip_decorator(ESLintBear)
class ESLintBearIgnoredFileTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section('')
        self.uut = ESLintBear(self.section, Queue())

    def test_lint_config_file(self):

        self.maxDiff = None
        config_filename = os.path.join(test_dir, '.eslintrc.js')

        self.section.append(Setting('eslint_config', config_filename))

        expected = Result.from_values(
            'ESLintBear',
            'File ignored by default.  Use a negated ignore pattern '
            '(like "--ignore-pattern \'!<relative/path/to/filename>\'") '
            'to override.',
            severity=RESULT_SEVERITY.NORMAL,
            file=config_filename,
            )

        Path(config_filename).touch()

        self.check_results(
            self.uut, ['{}'],
            [expected],
            create_tempfile=False,
            filename=config_filename,
        )


@generate_skip_decorator(ESLintBear)
class ESLintBearLanguageTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section('name')
        self.queue = Queue()
        self.uut = ESLintBear(self.section, self.queue)

    def test_markdown(self):
        good_file = [line + '\n' for line in test_file_markdown.splitlines()]
        bad_file = [line + '\n' for line in
                    test_file_markdown_bad.splitlines()]
        self.section.language = Language['Markdown']
        self.check_validity(self.uut, good_file,
                            tempfile_kwargs={'suffix': '.md'})
        self.check_invalidity(self.uut, bad_file,
                              tempfile_kwargs={'suffix': '.md'})

    def test_HTML(self):
        good_file = [line + '\n' for line in test_file_HTML.splitlines()]
        bad_file = [line + '\n' for line in test_file_HTML_bad.splitlines()]
        self.section.language = Language['html']
        self.check_validity(self.uut, good_file,
                            tempfile_kwargs={'suffix': '.html'})
        self.check_invalidity(self.uut, bad_file,
                              tempfile_kwargs={'suffix': '.html'})

    def test_typscript(self):
        good_file = [line + '\n' for line in test_file_typescript.splitlines()]
        self.section.language = Language['Typescript']
        self.check_validity(self.uut, good_file)

    def test_bad_language(self):
        test_file = [line + '\n' for line in test_good.splitlines()]
        self.section.language = Language['Python']
        self.check_validity(self.uut, test_file)
        while not self.queue.empty():
            message = self.queue.get()
            msg = ('Language needs to be either Markdown, HTML, TypeScript'
                   ' or JavaScript. Assuming JavaScript.')
            if message.message == msg:
                break
        else:
            assert False, 'Message not found'


@generate_skip_decorator(ESLintBear)
class ESLintBearLegacyErrorTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section('name')
        self.queue = Queue()
        self.uut = ESLintBear(self.section, self.queue)

    @mock.patch('coalib.misc.Shell.Popen')
    def test_eslint2_error(self, mock_popen):
        error = 'foo'
        mock_popen.return_value.communicate.return_value = ('output', error)

        get_results(self.uut, '',
                    filename=None,
                    force_linebreaks=True,
                    create_tempfile=True,
                    tempfile_kwargs={},
                    settings={},
                    aspects=None,
                    )

        self.assertIn(error, (msg.message for msg in self.queue.queue))
