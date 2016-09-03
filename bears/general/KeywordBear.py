import re

from coalib.bearlib import deprecate_settings
from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import RESULT_SEVERITY, Result


class KeywordBear(LocalBear):
    LANGUAGES = {"All"}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Documentation'}

    @deprecate_settings(keywords='ci_keywords')
    def run(self, filename, file, keywords: list):
        '''
        Checks the code files for given keywords.

        :param keywords:
            A list of keywords to search for (case insensitive).
            Usual examples are TODO and FIXME.
        '''
        keywords_regex = re.compile(
            '(' + '|'.join(re.escape(key) for key in keywords) + ')',
            re.IGNORECASE)

        for line_number, line in enumerate(file):
            for keyword in keywords_regex.finditer(line):
                yield Result.from_values(
                    origin=self,
                    message="The line contains the keyword '{}'."
                            .format(keyword.group()),
                    file=filename,
                    line=line_number + 1,
                    column=keyword.start() + 1,
                    end_line=line_number + 1,
                    end_column=keyword.end() + 1,
                    severity=RESULT_SEVERITY.INFO)
