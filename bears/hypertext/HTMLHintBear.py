import json

from coalib.bearlib.abstractions.Linter import linter

from dependency_management.requirements.NpmRequirement import NpmRequirement


@linter(executable='htmlhint',
        output_format='regex',
        output_regex=r'(?P<filename>.+):(?P<line>\d+):(?P<column>\d+):\s*'
                     r'(?P<message>.+) \[(?P<severity>error|warning).+\]')
class HTMLHintBear:
    """
    Checks HTML code with ``htmlhint`` for possible problems. Attempts to catch
    little mistakes and enforces a code style guide on HTML files.
    """
    LANGUAGES = {'HTML'}
    REQUIREMENTS = {NpmRequirement('htmlhint', '0.9.13')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Syntax', 'Formatting', 'Duplication', 'Code Simplification'}
    SEE_MORE = 'https://github.com/yaniswang/HTMLHint'

    @staticmethod
    def generate_config(filename, file,
                        enforce_lowercase_tagname: bool=True,
                        enforce_lowercase_attribute: bool=True,
                        require_attribute_value_in_double_quotes: bool=False,
                        prohibit_empty_value_for_attribute: bool=False,
                        prohibit_attribute_duplication: bool=True,
                        require_doctype_at_beginning: bool=True,
                        enforce_tag_pair: bool=True,
                        enforce_self_close_empty_tag: bool=True,
                        require_escaped_special_characters: bool=False,
                        require_unique_attribute_id: bool=True,
                        require_title_tag: bool=True,
                        prohibit_script_in_head: bool=False,
                        require_alt_attribute: bool=True,
                        enforce_id_class_naming_convention: str=None,
                        prohibit_inline_style: bool=True,
                        require_relative_links_in_href: bool=None,
                        prohibit_unsafe_characters: bool=True,
                        prohibit_inline_script: bool=False,
                        prohibit_style_tag: bool=False,
                        htmlhint_config: str=''):
        """
        :param enforce_lowercase_tagname:
            Enforce the tagnames to be written in lowercase.
            For example: If set to ``True``, prefer ``<span><div>`` over
            ``<SPAN><BR>``.
        :param enforce_lowercase_attribute:
            Enforce the attribute names to be written in lowercase.
            For example: If set to ``True``, prefer
            ``<img src="test.png" alt="test">`` over
            ``<img SRC="test.png" ALT="test">``.
        :param require_attribute_value_in_double_quotes:
            Allow attribute values to be enclosed in double quotes.
            For example: If set to ``True``, prefer ``<a href="" title="abc">``
            over ``<a href='' title=abc>``.
        :param prohibit_empty_value_for_attribute:
            Disallow empty values for attributes.
            For example: If set to ``True``, prefer
            ``<input type="button" disabled="disabled">`` over
            ``<input type="button" disabled>``.
        :param prohibit_attribute_duplication:
            Disallow defining of the same attribute more than once in
            a tag. For example: If set to ``True``, prefer
            ``<img src="a.png" />`` over ``<img src="a.png" src="b.png" />``.
        :param require_doctype_at_beginning:
            Enforce the ``<!DOCTYPE>`` declaration at the beginning.
            For example: If set to ``True``, prefer ``<!DOCTYPE HTML><html>``
            over ``<!--comment--><!DOCTYPE HTML><html>``.
        :param enforce_tag_pair:
            Enforce the tags to be paired.
        :param enforce_self_close_empty_tag:
            Enforce the empty tag to be closed by self.
            For example: If set to ``True``, prefer ``<br />`` over ``<br>``.
        :param require_escaped_special_characters:
            Require the special characters to be escaped.
            For example: If set to ``True``, prefer
            ``<span>aaa&gt;bbb&lt;ccc</span>`` over
            ``<span>aaa>bbb<ccc</span>``.
        :param require_unique_attribute_id:
            Require the ID attributes to be unique in the document.
            For example: If set to ``True``, prefer
            ``<div id="id1"></div><div id="id2"></div>`` over
            ``<div id="id1"></div><div id="id1"></div>``.
        :param require_title_tag:
            Require the ``<title>`` to be present in the ``<head>`` tag.
        :param prohibit_script_in_head:
            Prohibit the use of the ``<script>`` tag in the ``<head>`` tag.
        :param require_alt_attribute:
            Require ``alt`` attribute when using images (``img`` tag) and links
            (``href`` tag).
            For example: If set to ``True``, prefer this::

                <img src="test.png" alt="test">
                <input type="image" alt="test">

            over this::

                <img src="test.png">
                <input type="image">

        :param enforce_id_class_naming_convention:
            Possible values are ``underline``, ``dash`` and ``hump``.
            Require the ``id`` and ``class`` values to be set according to
            the given rules.
            For example: If set to ``underline``, prefer
            ``<div id="aaa_bbb">``.
            For example: If set to ``dash``, prefer ``<div id="aaa-bbb">``.
        :param prohibit_inline_style:
            Disallow the use of inline ``style`` attribute.
            For example: If set to ``True``, ``<div style="color:red"></div>``
            will raise a warning.
        :param require_relative_links_in_href:
            If ``True``, enforce relative links in the ``href`` attribute and
            if ``False``, enforce absolute links.
        :param prohibit_unsafe_characters:
            Prohibit the use of unsafe characters in attribute values.
            For example: If set to ``True``,
            ``<li><a href="https://vimeo.com//56931059‎\u0009‎">2012</a></li>``
            will raise a warning.
        :param prohibit_inline_script:
            Disallow the use of inline scripts.
            For example: If set to ``True``, this will raise a warning::

                <img src="test.gif" onclick="alert(1);">
                <img src="javascript:alert(1)">
                <a href="javascript:alert(1)">test1</a>

        :param prohibit_style_tag:
            Prohibit the use of ``style`` tag.
            For example: If set to ``True``,
            ``<body><style type="text/css"></style></body>``
            will raise a warning.
        """
        if htmlhint_config:
            return None
        else:
            options = {
                'tagname-lowercase': enforce_lowercase_tagname,
                'attr-lowercase': enforce_lowercase_attribute,
                'attr-value-double-quotes':
                    require_attribute_value_in_double_quotes,
                'attr-value-not_empty': prohibit_empty_value_for_attribute,
                'attr-no-duplication': prohibit_attribute_duplication,
                'doctype-first': require_doctype_at_beginning,
                'tag-pair': enforce_tag_pair,
                'tag-self-close': enforce_self_close_empty_tag,
                'spec-char-escape': require_escaped_special_characters,
                'id-unique': require_unique_attribute_id,
                'title-require': require_title_tag,
                'head-script-disabled': prohibit_script_in_head,
                'alt-require': require_alt_attribute,
                'id-class-value': enforce_id_class_naming_convention,
                'inline-style-disabled': prohibit_inline_style,
                'attr-unsafe-chars': prohibit_unsafe_characters,
                'inline-script-disabled': prohibit_inline_script,
                'style-disabled': prohibit_style_tag,
                'href-abs-or-rel':
                    'false' if require_relative_links_in_href is None
                    else 'rel' if require_relative_links_in_href else 'abs'
            }

            return json.dumps(options)

    @staticmethod
    def create_arguments(filename, file, config_file, htmlhint_config: str=''):
        """
        :param htmlhint_config:
            The path to a custom ``.htmlhintrc`` config file.
        """
        return (filename, '--config',
                htmlhint_config if htmlhint_config else config_file,
                '--format', 'unix')
