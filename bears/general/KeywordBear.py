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
        results = list()

        for i in range(len(keywords)):
            keywords[i] = keywords[i].lower()

        for line_number, line in enumerate(file):
            for keyword in keywords:
                results += self.check_line_for_keyword(line.lower(),
                                                       filename,
                                                       line_number,
                                                       keyword)

        return results

    def check_line_for_keyword(self, line, filename, line_number, keyword):
        pos = line.find(keyword)
        if pos != -1:
            return [Result.from_values(
                origin=self,
                message="The line contains the keyword `{}`."
                        .format(keyword),
                file=filename,
                line=line_number+1,
                column=pos+1,
                end_line=line_number+1,
                end_column=pos+len(keyword)+1,
                severity=RESULT_SEVERITY.INFO)]

        return []
