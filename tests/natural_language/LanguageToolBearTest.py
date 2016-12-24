import shutil
import unittest
from unittest.case import SkipTest

from bears.natural_language.LanguageToolBear import LanguageToolBear
from tests.BearTestHelper import generate_skip_decorator
from coalib.testing.LocalBearTestHelper import verify_local_bear

try:
    import language_check
    import guess_language
    language_check
    guess_language
except ImportError as err:
    raise SkipTest(str(err))

LanguageToolBearTest = verify_local_bear(
    LanguageToolBear,
    valid_files=('A correct English sentence sounds nice to everyone.',
                 'Ein korrekter englischer Satz klingt für alle gut.'),
    invalid_files=('  ',
                   'asdgaasdfgahsadf',
                   '"quoted"'))


LanguageToolBearLanguageTest = verify_local_bear(
    LanguageToolBear,
    valid_files=('A correct English sentence sounds nice to everyone.',),
    invalid_files=('Ein korrekter englischer Satz klingt für alle gut.',),
    settings={'language': 'en-US'})


LanguageToolBearDisableRulesTest = verify_local_bear(
    LanguageToolBear,
    valid_files=('Line without unnecessary spaces at the start.',
                 'a line beginning with lowercase.',
                 'A line beginning with uppercase.'),
    invalid_files=('  Line with unnecessary spaces at the start.',),
    settings={'languagetool_disable_rules': 'UPPERCASE_SENTENCE_START'})


@generate_skip_decorator(LanguageToolBear)
class LanguageToolBearPrerequisitesTest(unittest.TestCase):

    def test_check_prerequisites(self):
        _shutil_which = shutil.which
        try:
            shutil.which = lambda *args, **kwargs: None
            self.assertEqual(LanguageToolBear.check_prerequisites(),
                             'java is not installed.')

            shutil.which = lambda *args, **kwargs: 'path/to/java'
            self.assertTrue(LanguageToolBear.check_prerequisites())
        finally:
            shutil.which = _shutil_which
