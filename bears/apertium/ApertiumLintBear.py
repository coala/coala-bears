import json

from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.PipRequirement import PipRequirement
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


@linter(executable='apertium_lint',
        output_format='regex',
        output_regex=r'(?P<severity>\w+) : (?P<message>[^:\n]+: '
                     r'(?P<origin>[^\n]+))\n[^:\n]+: (?P<line>\d+)',
        config_suffix='.json',
        severity_map={'Warning': RESULT_SEVERITY.MAJOR})
class ApertiumLintBear:
    """
    `Apertium lint` is a python module that lints out irregular yet
    acceptable constructs that may creep into files involved in the
    transfer process. The lint is designed specifically to handle
    4 file types dictionaries, transfer, modes and tagger.

    https://github.com/coala/coala-bears/issues/1697 needs to be closed
    for extending Windows support for this bear.

    Lints the file using
    `apertium_lint <https://pypi.python.org/pypi/apertium_lint>`.
    """
    LANGUAGES = {'Apertium'}
    REQUIREMENTS = {PipRequirement('apertium-lint', '0.29'),
                    PipRequirement('lxml', '>=1.0')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Redundancy', 'Syntax', 'Formatting', 'Unused Code',
                  'Duplication', 'Undefined Element'}
    SEE_MORE = 'https://pypi.python.org/pypi/apertium_lint'

    @staticmethod
    def create_arguments(filename, file, config_file,
                         apertiumlint_config: str = '',
                         ):
        """
        :param apertiumlint_config: Path to a custom configuration file.
        """
        if apertiumlint_config:
            args = (filename, '--config', apertiumlint_config)
        else:
            args = (filename, '--config', config_file)
        return args

    @staticmethod
    def generate_config(filename, file,
                        redundant_pardef: bool = False,
                        paradigm_names: bool = True,
                        r_tag_data: bool = False,
                        repeated_attributes_pardef: bool = False,
                        repeated_entries_pardef: bool = False,
                        repeated_entries_main_section: bool = False,
                        repeated_tag_entries: bool = False,
                        monodix_transfer_direction: bool = False,
                        unused_paradigms: bool = False,
                        blank_space_detection: bool = False,
                        partially_in_lemma: bool = False,
                        unwanted_tag: bool = False,
                        bidix_transfer_direction: bool = False,
                        unwanted_white_space: bool = False,
                        compare_sdefs: bool = False,
                        verify_invariable_part: bool = False,
                        repeated_entries: bool = False,
                        repeated_entries_cat_item: bool = False,
                        repeated_entries_attr_item: bool = False,
                        unused_def_cats: bool = False,
                        check_valid_part_clip: bool = True,
                        check_valid_equal_tag: bool = True,
                        conflicting_cat_item: bool = False,
                        check_valid_position: bool = False,
                        enforce_break_tag: bool = False,
                        xsd_validation: bool = True,
                        enforce_side: bool = False,
                        macro_names: bool = False,
                        def_label_closed: bool = False,
                        validate_label_sequence: bool = False,
                        repeated_def_label: bool = True,
                        install_bool: bool = False,
                        repeated_program: bool = False,
                        validate_program: bool = False,
                        locate_file: bool = False,
                        empty_program: bool = False,
                        enforce_rules: bool = True,
                        install_switch_no: bool = True,
                        ):
        """
        :param redundant_pardef:
            This issue is responsible for detecting redundant paradigms in
            monodix files.
        :param paradigm_names:
            This issue is responsible for enforcing certain rules associated
            with naming paradigms in monodix files.
        :param r_tag_data:
            This issue is responsible for detecting any inconsistency in the
            data present in the `<r>` tag in the parameter definition entries
            in monodix files.
        :param repeated_attributes_pardef:
            This issue is responsible for checking any repeated entries in
            the attributes associated with an entry in the parameter
            definition in monodix files.
        :param repeated_entries_pardef:
            This issue is responsible for detecting repeated entries in the
            parameter definition entries for a given paradigm in monodix files.
        :param repeated_entries_main_section:
            This issue is responsible for detecting repeated entries in main
            section in monodix files.
        :param repeated_tag_entries:
            Same as `repeated_attributes_pardef`, but include repeated entries
            in the `<s>` and `<par>` tags in the Main Section.
        :param monodix_transfer_direction:
            This is issue is responsible for making sure that a valid transfer
            direction is supplied in monodix files.
        :param unused_paradigms:
            This issue is used for detecting unused paradigms in the parameter
            definitions section in monodix files.
        :param blank_space_detection:
            This issue detects 'extra' blank spaces that might be present in
            the entries in monodix files.
        :param partially_in_lemma:
            This issue is responsible for detecting if the parameter
            definitions that are part of lemma are written twice in monodix
            files.
        :param unwanted_tag:
            This issue detects extra/unwanted `<b/>` tags that might creep into
            entries in monodix files.
        :param bidix_transfer_direction:
            This issue is responsible for detecting and reporting incorrect
            transfer directions in bidix files.
        :param unwanted_white_space:
            This issue detects and reports white spaces that may creep into
            the entries in bidix files.
        :param compare_sdefs:
            This issue is responsible for detecting and reporting the sdefs
            that may be present in the bidix but are absent in the monodixes.
        :param verify_invariable_part:
            This issue is responsible for detecting homogeneity in definition
            of the invariable part across the monodix and the bidix.
        :param repeated_entries:
            Checks and reports repeated entries in the bidix.
        :param repeated_entries_cat_item:
            Simple check which iterates over all the `<cat-item>`s in a
            `<def­-cat>` and detects repeated `<cat-items>`
        :param repeated_entries_attr_item:
            Again another simple issue that checks for repeated `<attr-item>`s
            in `<def-attr>`.
        :param unused_def_cats:
            The lint can now detect and report redundant `<def-cat>`s that
            maybe present in the transfer rules definition but are never
            actually used.
        :param check_valid_part_clip:
            Check that the attribute listed in part='xyz' is defined
            using a `<def-attr>`. The valid parts are defined in `<def-attr>`s
            section of the transfer file.
        :param check_valid_equal_tag:
            Another common error in transfer files is trying to compare
            an attribute to a value it cannot take.
        :param conflicting_cat_item:
            This detects and reports if the same `<cat-item>` has been used in
            two or more `<def-cat>`s.
        :param check_valid_position:
            Every mention of pos='xyz' is checked to make sure that xyz
            is less than or equal to the number of elements in pattern item.
        :param enforce_break_tag:
            This function reports the if the `<b/>` tags are absent between
            two consecutive `<lu>` tags.
        :param xsd_validation:
            XSD Validation for transfer files, takes care of issues such as
            Repeated `<def-cat>`, `<def-attrs>`, and `<def-list>`.
            Valid side : `sl` or `tl` and repeated `<def-macro>`.
        :param enforce_side:
            In `<out>` the side attribute can either take the value of 'sl' or
            'tl'. With the lint in place, the user can enforce the side
            attribute to be 'tl' in all the `<out>` tags.
        :param macro_names:
            This issue detects multiple def-macro names in transfer files.
        :param def_label_closed:
            This function lints and reports if any other value has been used
            instead of the two valid ones: [true, false] in the closed
            attribute in `<def-label>` .
        :param validate_label_sequence:
            This function lints and detects and labels in <forbid> that are
            absent in `<tagset>`.
        :param repeated_def_label:
            This function detects and reports repeated def-labels in tagger
            files.
        :param install_bool:
            In modes files, the install attribute can only take one of two
            binary values, 'yes' or 'no'. This function is responsible for
            making sure that no other value is used for the same.
        :param repeated_program:
            Every modes file consists of various programs and there is always a
            chance that a certain program may unintentionally get repeated.
        :param validate_program:
            This function validates every program mentioned in the modes file.
        :param locate_file:
            This function checks and prompts incase a file defined in a
            "program" is missing in the `PWD`.
        :param empty_program:
            Not so much a risk, but this function prompts if a given "program"
            does not have any file associated with it.
        :param enforce_rules:
            This function is responsible for enforcing certain rules specific
            to given programs.
        :param install_switch_no:
            If in the definition of a certain mode, the attribute
            `install="no"`, the name should have an appropriate suffix like
            ­morph, interchunk, etc.
        """
        monodix = {'redundantPardef': {'message': 'Warning : Redundant pardef '
                                       'entry present for :',
                                       'enable': redundant_pardef},
                   'paradigmNames': {'message': 'Warning : Improper paradigm '
                                     'name found :',
                                     'enable': paradigm_names},
                   'rTagData': {'message': 'Warning : inconsistency in <r> '
                                'text for pardef :',
                                'enable': r_tag_data},
                   'repeatedAttributesPardef': {'message': 'Warning : Repeated'
                                                ' attributes found in <s> tag '
                                                'of pardef :',
                                                'enable':
                                                repeated_attributes_pardef},
                   'repeatedEntriesPardef': {'message': 'Warning : Repeated '
                                             'entries found in pardef :',
                                             'enable':
                                             repeated_entries_pardef},
                   'repeatedEntriesMainSection': {'message': 'Warning : '
                                                  'Repeated entries found in '
                                                  'main section entry :',
                                                  'enable':
                                                  repeated_entries_main_section
                                                  },
                   'repeatedTagEntries': {'message': 'Warning : Repeated tag '
                                          'entries for <s> or <par> found in '
                                          'main section entry :',
                                          'enable': repeated_tag_entries},
                   'transferDirection': {'message': 'Warning : Invalid '
                                         'transfer direction %s found for '
                                         'entry :',
                                         'enable': monodix_transfer_direction},
                   'unusedParadigms': {'message': 'Warning : Unused paradigm'
                                       '(s) found. List of unused '
                                       'paradigm(s) :',
                                       'enable': unused_paradigms},
                   'blankSpaceDetection': {'message': 'Warning : Unused '
                                           'paradigm(s) found. List of unused '
                                           'paradigm(s) :',
                                           'enable': blank_space_detection},
                   'partiallyInLemma': {'message': 'Warning : Issue regarding '
                                        'the lemma and the paradigm associated'
                                        ' with it for the entry :',
                                        'enable': partially_in_lemma},
                   'unwantedTag': {'message': 'Warning : Unwanted <b/> tag '
                                   'found for the entry :',
                                   'enable': unwanted_tag}
                   }

        bidix = {'transferDirection': {'message': 'Warning : Invalid transfer '
                                       'direction found for entry :',
                                       'enable': bidix_transfer_direction},
                 'unwantedWhiteSpace': {'message': 'Warning : Unwanted White '
                                        'space found in the entry :',
                                        'enable': unwanted_white_space},
                 'compareSdefs': {'message': 'Warning : Certain Sdefs present '
                                  'in the bidix are absent in the monodix :',
                                  'enable': compare_sdefs},
                 'verifyInvariablePart': {'message': 'Warning : Issue '
                                          'regarding usage of <g> tag found '
                                          'for entry : ',
                                          'enable': verify_invariable_part},
                 'repeatedEntries': {'message': 'Warning : Repeated entries '
                                     'found for entry : ',
                                     'enable': repeated_entries}
                 }

        transfer = {'repeatedEntriesCatItem': {'message': 'Warning : Repeated'
                                               ' cat-item found : ',
                                               'enable':
                                               repeated_entries_cat_item},
                    'repeatedEntriesAttrItem': {'message': 'Warning : Repeated'
                                                ' attr-item found : ',
                                                'enable':
                                                repeated_entries_attr_item},
                    'unusedDefCats': {'message': 'Warning : Following def-cats'
                                      ' have not been used : ',
                                      'enable': unused_def_cats},
                    'checkValidPartClip': {'message': 'Warning : Invalid part'
                                           "='%s', found for entry : %s",
                                           'enable': check_valid_part_clip},
                    'checkValidEqualTag': {'message': "Warning : The 'part' "
                                           'does not correspond with the lit'
                                           '-tag : ',
                                           'enable': check_valid_equal_tag},
                    'conflictingCatItem': {'message': 'Warning : Repeated '
                                           'cat-item entry found for two '
                                           'def-cats : ',
                                           'enable': conflicting_cat_item},
                    'checkValidPosition': {'message': 'Warning : The position '
                                           'mentioned for a tag in the entry '
                                           'is invalid : ',
                                           'enable': check_valid_position},
                    'enforceBreakTag': {'message': 'Warning : <b/> missing '
                                        'between consecutive <lu> elements '
                                        'for element : %s, on line number'
                                        ' : %s ',
                                        'enable': enforce_break_tag},
                    'xsdValidation': {'message': 'Warning : The position '
                                      'mentioned for a tag in the entry is '
                                      'invalid : ',
                                      'enable': xsd_validation},
                    'enforceSide': {'message': 'Warning : Are you sure you '
                                    "want to specify side='sl' in the %s tag"
                                    ' on line %s',
                                    'enable': enforce_side},
                    'macroNames': {'message': 'Warning : Are you sure you '
                                   "want to ''specify multiple def-macros "
                                   "with the same n='' and npar='' values : ",
                                   'enable': macro_names}
                    }

        tagger = {'defLabelClosed': {'message': 'Warning : Invalid value for '
                                     "closed' attribute used in def-label : ",
                                     'enable': def_label_closed},
                  'validateLabelSequence': {'message': 'Warning : Invalid '
                                            'label %s used in label '
                                            'sequence. ',
                                            'enable': validate_label_sequence},
                  'repeatedDefLabel': {'message': 'Warning : Repeated def-'
                                       'label : ',
                                       'enable': repeated_def_label}
                  }

        modes = {'installBool': {'message': 'Warning : Invalid install '
                                 'attrib : %s for <mode name=\"%s\">',
                                 'enable': install_bool},
                 'repeatedProgram': {'message': 'Warning : Repeated program '
                                     'definitions in : %s',
                                     'enable': repeated_program},
                 'validateProgram': {'message': 'Warning : Invalid program '
                                     ': %s',
                                     'enable': validate_program},
                 'locateFile': {'message': 'Warning : File not found : %s',
                                'enable': locate_file},
                 'emptyProgram': {'message': 'Warning : Are you sure you '
                                  'want to keep the program %s in the '
                                  'mode %s empty?',
                                  'enable': empty_program},
                 'enforceRules': {'message': 'Warning : Certain rules not '
                                  'followed in the modes file',
                                  'enable': enforce_rules},
                 'installSwitchNo': {'message': 'Warning : Improper mode '
                                     'name %s associated with attribute'
                                     " install = 'no'",
                                     'enable': install_switch_no}
                 }

        config = {'monodix': monodix, 'bidix': bidix,
                  'transfer': transfer, 'tagger': tagger, 'modes': modes}
        return json.dumps(config, indent=2)
