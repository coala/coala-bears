
from coalib.bearlib.abstractions.ExternalBearWrap import external_bear_wrap


@external_bear_wrap(executable='the_test',
                    settings={})
class TestBear:
    """
    Just testing
    """
    LANGUAGES = {'TestLang'}
    REQUIREMENTS = {'test1', 'test2'}
    AUTHORS = {'TheTester'}
    AUTHORS_EMAILS = {'testing@test.com'}
    LICENSE = 'MIT'

    @staticmethod
    def create_arguments():
        return ()
