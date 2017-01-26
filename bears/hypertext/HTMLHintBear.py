from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.NpmRequirement import NpmRequirement


@linter(
    executable='htmlhint',
    output_format='regex',
    output_regex=r'(?P<filename>.+):(?P<line>\d+):(?P<column>\d+):\s*'
                 r'(?P<message>.+)\s*(\d+)(\sproblems)\s*',
    config_suffix='.conf')
class HTMLHintBear:
    LANGUAGES = {'HTML'}
    REQUIREMENTS = {NpmRequirement('htmlhint', '0.9.13')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Syntax', 'Formatting', 'Duplication', 'Code Simplification'}

    @staticmethod
    def create_arguments(filename, file, config_file):
        return (filename, '--config', config_file, '-f', 'unix')

    @staticmethod
    def generate_config(filename, file,
                        enforce_lowercase_tagname: bool=True,
                        enforce_lowercase_attribute: bool=True,
                        allow_attribute_value_in_single_quote: bool=False,
                        prohibit_empty_attribute: bool=False,
                        prohibit_attribute_duplication: bool=True,
                        use_doctype_first: bool=True,
                        enforce_tag_pair: bool=True,
                        enforce_self_close_empty_tag: bool=True,
                        allow_unescaped_special_character: bool=False,
                        allow_duplicate_attribute_id: bool=False,
                        require_title_tag: bool=True,
                        allow_script_head_tag: bool=False):
        """
        :param enforce_lowercase_tagname:
            Require that tagnames are written in lowercase.
        :param enforce_lowercase_attribute:
            Require that attributes names are written in lowercase.
        :param allow_attribute_value_in_single_quote:
            Allow attributes value to be enclosed in single quotes.
        :param prohibit_empty_attribute:
            Require that attributes value are set.
        :param prohibit_attribute_duplication:
            Require that the same attribute is not defined more that once in
            a tag.
        :param use_doctype_first:
            Require that Doctype is first.
        :param enforce_tag_pair:
            Require that tags are paired.
        :param enforce_self_close_empty_tag:
            Require that empty must closed by self.
        :param allow_unescaped_special_character:
            Allow unescaped special characters.
        :param allow_duplicate_attribute_id:
            Allow duplicating attributes ids.
        :param require_title_tag:
            Require that ``<title>`` is present in ``<head>`` tag.
        :param allow_script_head_tag:
            Allow the use of the ``<script>`` tag in the ``<head>`` tag.
        """
        configs = """{opening_brace}
"tagname-lowercase": {enforce_lowercase_tagname},
"attr-lowercase": {enforce_lowercase_attribute},
"attr-value-double-quotes": {allow_attribute_value_in_single_quote},
"attr-value-not_empty: {prohibit_empty_attribute},
"attr-no-duplication: {prohibit_attribute_duplication},
"doctype-first": {use_doctype_first},
"tag-pair": {enforce_tag_pair},
"spec-char-escape": {enforce_self_close_empty_tag},
"id-unique": {allow_duplicate_attribute_id},
"src-not-empty": true,
"title-require": {require_title_tag}
{closing_brace}
""".format(opening_brace='{',
           closing_brace='}',
           enforce_lowercase_tagname=convert_bool_to_str(
               enforce_lowercase_tagname),
           enforce_lowercase_attribute=convert_bool_to_str(
               enforce_lowercase_attribute),
           allow_attribute_value_in_single_quote=convert_bool_to_str(
                not allow_attribute_value_in_single_quote),
           prohibit_empty_attribute=convert_bool_to_str(
               prohibit_empty_attribute),
           prohibit_attribute_duplication=convert_bool_to_str(
               prohibit_attribute_duplication),
           use_doctype_first=convert_bool_to_str(use_doctype_first),
           enforce_tag_pair=convert_bool_to_str(enforce_tag_pair),
           enforce_self_close_empty_tag=convert_bool_to_str(
               enforce_self_close_empty_tag),
           allow_duplicate_attribute_id=convert_bool_to_str(
               not allow_duplicate_attribute_id),
           require_title_tag=convert_bool_to_str(require_title_tag))
        return configs


def convert_bool_to_str(boolean):
    result = 'true' if boolean else 'false'
