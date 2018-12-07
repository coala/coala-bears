import yaml

from coalib.bearlib.abstractions.Linter import linter
from coalib.settings.Setting import typed_list
from dependency_management.requirements.GemRequirement import GemRequirement


@linter(executable='haml-lint',
        normalize_line_numbers=True,
        output_format='regex',
        output_regex=r'(?P<line>\d+) \[(?P<severity>W|E)\] '
                     r'(?P<message>.*)')
class HAMLLintBear:
    """
    Uses ``haml-lint`` to perform HAML-specific style and lint checks to ensure
    clean and readable HAML code.
    """
    LANGUAGES = {'Haml'}
    REQUIREMENTS = {GemRequirement('haml_lint', '0.27.0')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Formatting', 'Syntax'}
    SEE_MORE = 'https://github.com/brigade/haml-lint'

    DEFAULT_IGNORED_COPS = (
      'Lint/BlockAlignment',
      'Lint/EndAlignment',
      'Lint/Void',
      'Layout/AlignParameters',
      'Layout/ElseAlignment',
      'Layout/EndOfLine',
      'Layout/IndentationWidth',
      'Layout/TrailingBlankLines',
      'Layout/TrailingWhitespace',
      'Metrics/BlockLength',
      'Metrics/BlockNesting',
      'Metrics/LineLength',
      'Naming/FileName',
      'Style/FrozenStringLiteralComment',
      'Style/IfUnlessModifier',
      'Style/Next',
      'Style/WhileUntilModifier',
      )

    @staticmethod
    def generate_config(filename, file,
                        alignment_tabs: bool = True,
                        alt_text: bool = True,
                        class_attribute_with_static_value: bool = True,
                        classes_before_ids: bool = True,
                        consecutive_comments: bool = True,
                        max_consecutive_comments: int = 1,
                        consecutive_silent_scripts: bool = True,
                        max_consecutive_silent_scripts: int = 2,
                        empty_object_reference: bool = True,
                        empty_script: bool = True,
                        final_newline: bool = True,
                        final_newline_present: bool = True,
                        html_attributes: bool = True,
                        id_names: bool = True,
                        id_names_style: str = 'lisp_case',
                        implicit_div: bool = True,
                        indentation: bool = True,
                        indentation_character: str = 'space',
                        indentation_width: int = 2,
                        inline_styles: bool = True,
                        instance_variables: bool = True,
                        instance_variables_file_types: str = 'partials',
                        instance_variables_matchers_all: str = r'.*',
                        instance_variables_matchers_partials:
                            str = r'\A_.*\.haml\z',
                        leading_comment_space: bool = True,
                        line_length: bool = True,
                        max_line_length: int = 80,
                        multiline_pipe: bool = True,
                        multiline_script: bool = True,
                        object_reference_attributes: bool = True,
                        repeat_id: bool = True,
                        repeat_id_severity: str = 'error',
                        rubo_cop: bool = True,
                        rubo_cop_ignored_cops:
                            typed_list(str) = DEFAULT_IGNORED_COPS,
                        ruby_comments: bool = True,
                        space_before_script: bool = True,
                        space_inside_hash_attributes: bool = True,
                        space_inside_hash_attributes_style: str = 'space',
                        tag_name: bool = True,
                        trailing_whitespace: bool = True,
                        unnecessary_interpolation: bool = True,
                        unnecessary_string_output: bool = True,
                        view_length: bool = True,
                        max_view_length: int = 100,
                        hamllint_config: str = '',
                        ):
        """
        :param alignment_tabs:
            Check if tabs are used within a tag for alignment or not.
        :param alt_text:
            Check if alternate text is specified within img tags or not. Using
            alt attributes is important to make the site more accessible.
        :param class_attribute_with_static_value:
            Check if static class attributes are preferred over hash
            attributes with static values or not. Unless a dynamic value is
            being assigned to the class attribute, it is terser to use the
            inline tag to specify the class or classes to which an element
            should be assigned.
        :param classes_before_ids:
            Check whether classes or ID attributes should be listed first in
            the tags. Attributes should be listed in the order of specificity.
            Thus, the order should be classes followed by IDs.
        :param consecutive_comments:
            Check if consective comments are allowed or not. Consecutive
            comments should be condensed into a single multiline comment.
        :param max_consecutive_comments:
            Set the maximum number of consecutive comments allowed before
            warning.
        :param consecutive_silent_scripts:
            Check if there are multiple lines of Ruby using silent script
            markers (-). Large blocks of Ruby code in HAML templates are
            generally a smell and this rule can be used to warn against that.
        :param max_consecutive_silent_scripts:
            Set the maximum number of consective scripts before yielding a
            warning.
        :param empty_object_reference:
            Check if empty object references should be removed or not. These
            are no-ops and are usually left behind by mistake and can be
            removed safely.
        :param empty_script:
            Check if empty scripts should be removed or not. Empty scripts
            serve no purpose and are usually left behind by mistake.
        :param final_newline:
            Check if the file should have a final newline or not. Files should
            always have a final newline to ensure better diffs when adding
            lines to it.
        :param final_newline_present:
            Customize whether or not a final newline exists, with this
            parameter. Final newline should be present by default.
        :param html_attributes:
            Check if HTML-style attributes syntax is being used to define the
            attributes for an element or not. HTML-style attributes syntax can
            be terser, but it also introduces additional complexity to the
            templates, since there are now two different ways to define
            attributes. Using one style makes it easier to add greater
            cognitive load to writing templates. By default, HTML-style
            attributes syntax is not used.
        :param id_names:
            Check if the naming convention of the id attributes are conforming
            to one of the possible preferred styles.
        :param id_names_style:
            Specify the style with which the id attributes must conform.
            The preferred styles are:
            lisp-case,
            camelCase,
            PascalCase,
            snake_case.
            The default style is lisp-case.
        :param implicit_div:
            Check if %div can be converted into an implicit div. Implicit divs
            make HAML templates more concise.
        :param indentation:
            Check if spaces are used for indentation instead of hard tabs.
        :param indentation_character:
            Set the character used for indentation, spaces or tabs.
        :param indentation_width:
            Set the number of spaces for space indentation. This is ignored
            when indentation_character is set to tab.
        :param inline_styles:
            Check if the tags contain inline styles or not. In general, tags
            should not contain inline styles. Dynamic content and email
            templates are possible exceptions.
        :param instance_variables:
            Check if instance variables are not used in the specified type of
            files.
        :param instance_variables_file_types:
            Specify the class of files to lint. By default, this linter only
            runs on Rails-style partial views.
        :param instance_variables_matchers_all:
            Check all file names against.
        :param instance_variables_matchers_partials:
            Specify the regular expression to check file names against.
        :param leading_comment_space:
            Check if comments are separated from the leading # by a space or
            not. The comments should be space separated for more readability.
        :param line_length:
            Check whether maximum line length linter is enabled or not.
        :param max_line_length:
            Specify the maximum number of characters for a line, the newline
            character being excluded.
        :param multiline_pipe:
            Check if multiple lines are spanned using multiline pipe (|)
            syntax or not.
        :param multiline_script:
            Check if Ruby scripts are spanned over multiple lines using
            operators or not.
        :param object_reference_attributes:
            Check if object reference syntax is used to set the class/id of an
            element or not. This syntax should not be used since it makes it
            difficult to find where a particular class attribute is defined in
            the code. It also creates an unnecessary coupling by directly
            associating class names to the objects passed to it, making
            refactoring models affect the views.
        :param repeat_id:
            Check whether IDs are unique or not. Repeating an ID is an error
            in the HTML specification.
        :param repeat_id_severity:
            Set the severity level of the linter in checking whether the IDs
            are unique or not.
        :param rubo_cop:
            Use this rule to enable the linter to run RuboCop over the Ruby
            code in the templates.
        :param rubo_cop_ignored_cops:
            Specify cops which are to be ignored while running RuboCop over
            the Ruby code in the templates.
        :param ruby_comments:
            Check if HAML's built-in comments are preferred over ad hoc Ruby
            comments.
        :param space_before_script:
            Check if Ruby script indicators are separated from code with a
            single space or not.
        :param space_inside_hash_attributes:
            Check if the style of hash attributes is one of the two possible
            preferred styles or not.
        :param space_inside_hash_attributes_style:
            Set the preferred style of hash attributes.
        :param tag_name:
            Check if the tag names contain uppercase letters or not. Tag names
            should not contain uppercase letters.
        :param trailing_whitespace:
            Check whether trailing whitespace linter is enabled or not.
        :param unnecessary_interpolation:
            Check if there is unnecessary interpolation for inline tag content
            or not. Unnecessary interpolation must be avoided.
        :param unnecessary_string_output:
            Check if string expressions are being outputted in Ruby, when
            static text will suffice. HAML gracefully handles string
            interpolation in static text, so Ruby strings are not required in
            order to use interpolation.
        :param view_length:
            Check if large views are split into separate partials.
        :param max_view_length:
            Set maximum length of template views.
        """
        if hamllint_config:
            return None
        else:
            hamllint_config = {
                'linters': {
                    'AlignmentTabs': {
                        'enabled': alignment_tabs,
                    },
                    'AltText': {
                        'enabled': alt_text,
                    },
                    'ClassAttributeWithStaticValue': {
                        'enabled': class_attribute_with_static_value,
                    },
                    'ClassesBeforeIds': {
                        'enabled': classes_before_ids,
                    },
                    'ConsecutiveComments': {
                        'enabled': consecutive_comments,
                        'max_consecutive': max_consecutive_comments,
                    },
                    'ConsecutiveSilentScripts': {
                        'enabled': consecutive_silent_scripts,
                        'max_consecutive': max_consecutive_silent_scripts,
                    },
                    'EmptyObjectReference': {
                        'enabled': empty_object_reference,
                    },
                    'EmptyScript': {
                        'enabled': empty_script,
                    },
                    'FinalNewline': {
                        'enabled': final_newline,
                        'present': final_newline_present,
                    },
                    'HtmlAttributes': {
                        'enabled': html_attributes,
                    },
                    'IdNames': {
                        'enabled': id_names,
                        'style': id_names_style,
                    },
                    'ImplicitDiv': {
                        'enabled': implicit_div,
                    },
                    'Indentation': {
                        'enabled': indentation,
                        'character': indentation_character,
                        'width': indentation_width,
                    },
                    'InlineStyles': {
                        'enabled': inline_styles,
                    },
                    'InstanceVariables': {
                        'enabled': instance_variables,
                        'file_types': instance_variables_file_types,
                        'matchers': {
                            'all': instance_variables_matchers_all,
                            'partials': instance_variables_matchers_partials,
                        },
                    },
                    'LeadingCommentSpace': {
                        'enabled': leading_comment_space,
                    },
                    'LineLength': {
                        'enabled': line_length,
                        'max': max_line_length,
                    },
                    'MultilinePipe': {
                        'enabled': multiline_pipe,
                    },
                    'MultilineScript': {
                        'enabled': multiline_script,
                    },
                    'ObjectReferenceAttributes': {
                        'enabled': object_reference_attributes,
                    },
                    'RepeatedId': {
                        'enabled': repeat_id,
                        'severity': repeat_id_severity,
                    },
                    'RuboCop': {
                        'enabled': rubo_cop,
                        'ignored_cops': rubo_cop_ignored_cops,
                    },
                    'RubyComments': {
                        'enabled': ruby_comments,
                    },
                    'SpaceBeforeScript': {
                        'enabled': space_before_script,
                    },
                    'SpaceInsideHashAttributes': {
                        'enabled': space_inside_hash_attributes,
                        'style': space_inside_hash_attributes_style,
                    },
                    'TagName': {
                        'enabled': tag_name,
                    },
                    'TrailingWhitespace': {
                        'enabled': trailing_whitespace,
                    },
                    'UnnecessaryInterpolation': {
                        'enabled': unnecessary_interpolation,
                    },
                    'UnnecessaryStringOutput': {
                        'enabled': unnecessary_string_output,
                    },
                    'ViewLength': {
                        'enabled': view_length,
                        'max': max_view_length,
                    },
                },
            }

            return yaml.dump(hamllint_config, default_flow_style=False)

    @staticmethod
    def create_arguments(filename, file, config_file,
                         hamllint_config: str = '',
                         ):
        """
        :param hamllint_config:
            Path to a custom configuration file.
        """
        return ('--no-summary', filename, '--config',
                hamllint_config if hamllint_config else config_file)
