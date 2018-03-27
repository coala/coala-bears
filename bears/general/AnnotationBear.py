import re

from pygments.lexers import get_lexer_by_name
from pygments.token import Token
from pygments.util import ClassNotFound

from coalib.bearlib.languages.LanguageDefinition import LanguageDefinition
from coalib.bears.LocalBear import LocalBear
from coalib.results.HiddenResult import HiddenResult
from coalib.results.Result import Result, RESULT_SEVERITY
from coalib.results.SourceRange import SourceRange
from coalib.results.AbsolutePosition import AbsolutePosition
from coala_utils.string_processing.Core import unescaped_search_for


#: All variants of Pygments root token types for all different categories of
#  syntax ranges the AnnotationBear should extract from a source file, in the
#  order in which the file's token stream should be checked
TOKEN_TYPES = [
    ('comments', 'multiline_comments', (
        Token.Comment.Multiline,
        Token.Comment.Multi,
    )),
    ('comments', 'singleline_comments', (
        Token.Comment,
    )),
    ('strings', 'multiline_strings', (
        Token.String.Doc,
        Token.String.Heredoc,
        Token.String.Multiline,
        Token.String.Multi,
    )),
    ('strings', 'singleline_strings', (
        Token.String,
    )),
]


class AnnotationBear(LocalBear):
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'

    def run(self, filename, file, language: str, coalang_dir: str = None):
        """
        Finds out all the positions of strings and comments in a file.
        The Bear searches for valid comments and strings and yields their
        ranges as SourceRange objects in HiddenResults.

        :param language:
            The programming language of the source code.
        :param coalang_dir:
            External directory for coalang file.
        :return:
            One HiddenResult containing a dictionary with keys being 'strings'
            or 'comments' and values being a tuple of SourceRanges pointing to
            the strings and a tuple of SourceRanges pointing to all comments
            respectively. The ranges do include string quotes or the comment
            starting separator but not anything before (e.g. when using
            ``u"string"``, the ``u`` will not be in the source range).
        """
        try:
            # ignore whitespace on pygments lexer name lookup
            pygment = get_lexer_by_name(re.sub(r'\s+', '', language))
        except ClassNotFound:
            content = ('coalang specification for ' + language +
                       ' not found.')
            yield HiddenResult(self, content)
            return

        # the HiddenResult's contents dict of SourceRange objects
        contents = {key: () for *keys, _ in TOKEN_TYPES for key in keys}
        try:
            # first get the token iterator, so it can be additionally consumed
            # in nested loops below
            itokens = pygment.get_tokens(''.join(file))
            start = end = 0
            for token, text in itokens:
                for *keys, token_type_choices in TOKEN_TYPES:
                    for token_type in token_type_choices:
                        # if token type is found at current token stream
                        # position then combine all consecutive tokens of that
                        # token type to a single range, because pygments might
                        # split the token type region into sub-tokens, like
                        # delimiters and escapes in case of strings...
                        while token in token_type:
                            end += len(text)
                            token, text = next(itokens, (None, ''))
                        if not end > start:
                            continue

                        source_range = SourceRange.from_absolute_position(
                            filename,
                            AbsolutePosition(file, start),
                            AbsolutePosition(file, end - 1))
                        for key in keys:
                            contents[key] += (source_range, )
                        start = end
                end += len(text)
                start = end
        except NoCloseError as e:
            yield Result(self, str(e), severity=RESULT_SEVERITY.MAJOR,
                         affected_code=(e.code,))

        yield HiddenResult(self, contents)


class NoCloseError(Exception):

    def __init__(self, annotation, code):
        Exception.__init__(self, annotation + ' has no closure')
        self.code = code
