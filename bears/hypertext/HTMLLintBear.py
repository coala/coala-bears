from shutil import which
import sys

from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.PipRequirement import PipRequirement
from coalib.settings.Setting import typed_list


@linter(executable=sys.executable,
        output_format='regex',
        output_regex=r'(?P<line>\d+):(?P<column>\d+): '
                     r'(?P<severity>Error|Warning|Info): (?P<message>.+)')
class HTMLLintBear:
    """
    Check HTML source code for invalid or misformatted code.

    See also <https://pypi.python.org/pypi/html-linter>.
    """

    _html_lint = which('html_lint.py')

    LANGUAGES = {'HTML', 'Jinja2', 'PHP'}
    REQUIREMENTS = {PipRequirement('html-linter', '0.3.0')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Syntax', 'Formatting'}

    @staticmethod
    def create_arguments(filename, file, config_file,
                         enable_doctype: bool=True,
                         enable_entities: bool=True,
                         enable_trailing_whitespace: bool=True,
                         enable_tabs: bool=True,
                         enable_charset: bool=True,
                         enable_void_element: bool=True,
                         enable_optional_tag: bool=True,
                         enable_type_attribute: bool=True,
                         enable_concerns_separation: bool=True,
                         enable_protocol: bool=True,
                         enable_names: bool=True,
                         enable_capitalization: bool=True,
                         enable_quotation: bool=True,
                         enable_indentation: bool=True,
                         enable_formatting: bool=True,
                         enable_boolean_attribute: bool=True,
                         enable_invalid_attribute: bool=True,
                         enable_void_zero: bool=True,
                         enable_invalid_handler: bool=True,
                         enable_http_equiv: bool=True,
                         enable_extra_whitespace: bool=True,
                         htmllint_ignore: typed_list(str)=()):
        """
        :param enable_doctype:
            Enable or disable doctype checker.
        :param enable_entities:
            Enable or disable unicode entity checker.
        :param enable_trailing_whitespace:
            Enable or disable checker for trailing whitespace.
        :param enable_tabs:
            Enable or disable check for tabs.
        :param enable_charset:
            Enable or disable utf-8 checking.
        :param enable_void_element:
            Enable or disable checker for void tags.
        :param enable_optional_tag:
            Enable or disable checker for optional tags.
        :param enable_type_attribute:
            Enable or disable checker for default types.
        :param enable_concerns_separation:
            Enable or disable checker for seperation of concern.
        :param enable_protocol:
            Enable or disable checker for protocol specification.
        :param enable_names:
            Enable or disable checker for id or class name delimiters.
        :param enable_capitalization:
            Enable or disable checker for capitalization
            of tags and attributes.
        :param enable_quotation:
            Enable or disable checker for quotation marks.
        :param enable_indentation:
            Enable or disable checker for indentation using spaces.
        :param enable_formatting:
            Enable or disable checker for general formatting.
        :param enable_boolean_attribute:
            Enable or disable checker for boolean attributes.
        :param enable_invalid_attribute:
             Enable or disable checker for invalid attributes.
        :param enable_void_zero:
           Enable or disable checker for javascript void(0).
        :param enable_invalid_handler:
           Enable or disable checker for Javascript links.
        :param enable_http_equiv:
           Enable or disable checker for http-equiv.
        :param enable_extra_whitespace:
           Enable or disable checker for extra whitespace.
        :param htmllint_ignore:
           List of checkers to ignore.
        """
        param_dict = {
            'doctype': enable_doctype,
            'entities': enable_entities,
            'trailing_whitespace': enable_trailing_whitespace,
            'tabs': enable_tabs,
            'charset': enable_charset,
            'void_element': enable_void_element,
            'optional_tag': enable_optional_tag,
            'type_attribute': enable_type_attribute,
            'concerns_separation': enable_concerns_separation,
            'protocol': enable_protocol,
            'names': enable_names,
            'capitalization': enable_capitalization,
            'quotation': enable_quotation,
            'indentation': enable_indentation,
            'formatting': enable_formatting,
            'boolean_attribute': enable_boolean_attribute,
            'invalid_attribute': enable_invalid_attribute,
            'void_zero': enable_void_zero,
            'invalid_handler': enable_invalid_handler,
            'http_equiv': enable_http_equiv,
            'extra_whitespace': enable_extra_whitespace,
        }

        ignore = ','.join(part.strip() for part in htmllint_ignore)
        for param, use in param_dict.items():
            if not use and param not in htmllint_ignore:
                ignore += ',{}'.format(param)
        return HTMLLintBear._html_lint, '--disable=' + ignore, filename
