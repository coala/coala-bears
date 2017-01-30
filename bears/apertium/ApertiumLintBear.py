import os
import json
import lxml

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
    Apertium lint is a python module that lints out irregular yet
    acceptable constructs that may creep into files involved in the
    transfer process. The lint is designed specifically to handle
    4 file types dictionaries, transfer, modes and tagger.

    Lints the file using
    `apertium_lint <https://gitlab.com/jpsinghgoud/apertium-lint>`.
    """
    LANGUAGES = {'Apertium'}
    REQUIREMENTS = {PipRequirement('apertium-lint', '0.24')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Repitition', 'Unused Items', 'Missing Files'}

    @staticmethod
    def create_arguments(filename, file, config_file,
                         apertiumlint_config: str=''):
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
                        redundantPardef: bool=False,
                        paradigmNames: bool=True,
                        rTagData: bool=False,
                        repeatedAttributesPardef: bool=False,
                        repeatedEntriesPardef: bool=False,
                        repeatedEntriesMainSection: bool=False,
                        repeatedTagEntries: bool=False,
                        monodix_transferDirection: bool=False,
                        unusedParadigms: bool=False,
                        blankSpaceDetection: bool=False,
                        partiallyInLemma: bool=False,
                        unwantedTag: bool=False,
                        bidix_transferDirection: bool=False,
                        unwantedWhiteSpace: bool=False,
                        compareSdefs: bool=False,
                        verifyInvariablePart: bool=False,
                        repeatedEntries: bool=False,
                        repeatedEntriesCatItem: bool=False,
                        repeatedEntriesAttrItem: bool=False,
                        unusedDefCats: bool=False,
                        checkValidPartClip: bool=True,
                        checkValidEqualTag: bool=True,
                        conflictingCatItem: bool=False,
                        checkValidPosition: bool=False,
                        enforceBreakTag: bool=False,
                        xsdValidation: bool=True,
                        enforceSide: bool=False,
                        macroNames: bool=False,
                        defLabelClosed: bool=False,
                        validateLabelSequence: bool=False,
                        repeatedDefLabel: bool=True,
                        installBool: bool=False,
                        repeatedProgram: bool=False,
                        validateProgram: bool=False,
                        locateFile: bool=False,
                        emptyProgram: bool=False,
                        enforceRules: bool=True,
                        installSwitchNo: bool=True
                        ):
        """
        :param redundantPardef:
            This issue is responsible for detecting redundant paradigms in
            monodix files.
        :param paradigmNames:
            This issue is responsible for enforcing certain rules associated
            with naming paradigms in monodix files.
        :param rTagData:
            This issue is responsible for detecting any inconsistency in the
            data present in the <r> tag in the pardef entries in monodix files.
        :param repeatedAttributesPardef:
            This issue is responsible for checking any repeated entries in
            the attributes associated with an entry in the pardef section
            n monodix files.
        :param repeatedEntriesPardef:
            This issue is responsible for detecting repeated entries in the
            pardef entries for a given paradigm in monodix files.
        :param repeatedEntriesMainSection:
            This issue is responsible for detecting repeated entries in main
            section in monodix files.
        :param repeatedTagEntries:
            Same as repeatedAttributesPardef, but include repeated entries in
            the <s> and <par> tags in the Main Section.
        :param monodix_transferDirection:
            This is issue is responsible for making sure that a valid transfer
            direction is supplied in monodix files.
        :param unusedParadigms:
            This issue is used for detecting unused paradigms in the pardefs
            section in monodix files.
        :param blankSpaceDetection:
            This issue detects “extra” blank spaces that might be present in
            the entries in monodix files.
        :param partiallyInLemma:
            This issue is responsible for detecting if the pardefs that are
            part of lemma are written twice in monodix files.
        :param unwantedTag:
            This issue detects extra/unwanted <b/> tags that might creep into
            entries in monodix files.
        :param bidix_transferDirection:
            This issue is responsible for detecting and reporting incorrect
            transfer directions in bidix files.
        :param unwantedWhiteSpace:
            This issue detects and reports white spaces that may creep into
            the entries in bidix files.
        :param compareSdefs:
            This issue is responsible for detecting and reporting the sdefs
            that may be present in the bidix but are absent in the monodixes.
        :param verifyInvariablePart:
            This issue is responsible for detecting homogeneity in definition
            of the invariable part across the monodix and the bidix.
        :param repeatedEntries:
            Checks and reports repeated entries in the bidix.
        :param repeatedEntriesCatItem:
            Simple check which iterates over all the <cat­item>s in a
            <def­cat> and detects repeated <cat­items>
        :param repeatedEntriesAttrItem:
            Again another simple issue that checks for repeated attr­items
            in def­attr.
        :param unusedDefCats:
            The lint can now detect and report redundant def­cats that
            maybe present in the transfer rules definition but are never
            actually used.
        :param checkValidPartClip:
            Check that the attribute listed in part="xyz" is defined
            using a <def­attr>. The valid parts are defined in def­attrs
            section of the transfer file.
        :param checkValidEqualTag:
            Another common error in transfer files is trying to compare
            an attribute to a value it cannot take.
        :param conflictingCatItem:
            This detects and reports if the same cat­item has been used in
            two or more def­cats.
        :param checkValidPosition:
            Every mention of pos="xyz" is checked to make sure that xyz
            is less than or equal to the number of elements in pattern ­item.
        :param enforceBreakTag:
            This function reports the if the <b/> tags are absent between
            two consecutive <lu> tags.
        :param xsdValidation:
            XSD Validation for transfer files, takes care of issues such as
            Repeated def­cats, Repeated def­attrs, Repeted def­list,
            Valid side : ‘sl’ or ‘tl’ and Repeated def­macro
        :param enforceSide:
            In <out> the side attribute can either take the value of "sl" or
            "tl". With the lint in place, the user can enforce the side
            attribute to be "tl" in all the <out> tags.
        :param macroNames:
            This issue detects multiple def-macro names in transfer files.
        :param defLabelClosed:
            This function lints and reports if any other value has been used
            instead of the two valid ones: [true, false] in the closed
            attribute in <def­label> .
        :param validateLabelSequence:
            This function lints and detects and labels in <forbid> that are
            absent in <tagset>.
        :param repeatedDefLabel:
            This function detects and reports repeated def-labels in tagger
            files.
        :param installBool:
            In modes files, the install attribute can only take one of two
            binary values, ‘yes’ or ‘no’. This function is responsible for
            making sure that no other value is used for the same.
        :param repeatedProgram:
            Every modes file consits of various programs and there is always a
            chance that a certain program may unintentionally get repeated.
        :param validateProgram:
            This function validates every program mentioned in the modes file.
        :param locateFile:
            This function checks and prompts incase a file defined in a
            “program” is missing in the PWD.
        :param emptyProgram:
            Not so much a risk, but this function prompts if a given program
            does not have any file associated with it.
        :param enforceRules:
            This function is responsible for enforcing certain rules specific
            to given programs.
        :param installSwitchNo:
            If in the definition of a certain mode, the attribute install=”no”,
            the name should have an appropriate suffix like ­morph,
            interchunk, etc.
        """
        monodix = {'redundantPardef': {'message': 'Warning : Redundant pardef '
                                       'entry present for :',
                                       'enable': redundantPardef},
                   'paradigmNames': {'message': 'Warning : Improper paradigm '
                                     'name found :',
                                     'enable': paradigmNames},
                   'rTagData': {'message': 'Warning : Inconsitency in <r> '
                                'text for pardef :',
                                'enable': rTagData},
                   'repeatedAttributesPardef': {'message': 'Warning : Repeated'
                                                ' attributes found in <s> tag '
                                                'of pardef :',
                                                'enable':
                                                repeatedAttributesPardef},
                   'repeatedEntriesPardef': {'message': 'Warning : Repeated '
                                             'entries found in pardef :',
                                             'enable': repeatedEntriesPardef},
                   'repeatedEntriesMainSection': {'message': 'Warning : '
                                                  'Repeated entries found in '
                                                  'main section entry :',
                                                  'enable':
                                                  repeatedEntriesMainSection},
                   'repeatedTagEntries': {'message': 'Warning : Repeated tag '
                                          'entries for <s> or <par> found in '
                                          'main section entry :',
                                          'enable': repeatedTagEntries},
                   'transferDirection': {'message': 'Warning : Invalid '
                                         'transfer direction %s found for '
                                         'entry :',
                                         'enable': monodix_transferDirection},
                   'unusedParadigms': {'message': 'Warning : Unused paradigm'
                                       '(s) found. List of unused '
                                       'paradigm(s) :',
                                       'enable': unusedParadigms},
                   'blankSpaceDetection': {'message': 'Warning : Unused '
                                           'paradigm(s) found. List of unused '
                                           'paradigm(s) :',
                                           'enable': blankSpaceDetection},
                   'partiallyInLemma': {'message': 'Warning : Issue regarding '
                                        'the lemma and the paradigm associated'
                                        ' with it for the entry :',
                                        'enable': partiallyInLemma},
                   'unwantedTag': {'message': 'Warning : Unwanted <b/> tag '
                                   'found for the entry :',
                                   'enable': unwantedTag}
                   }

        bidix = {'transferDirection': {'message': 'Warning : Invalid transfer '
                                       'direction found for entry :',
                                       'enable': bidix_transferDirection},
                 'unwantedWhiteSpace': {'message': 'Warning : Unwanted White '
                                        'space found in the entry :',
                                        'enable': unwantedWhiteSpace},
                 'compareSdefs': {'message': 'Warning : Certain Sdefs present '
                                  'in the bidix are absent in the monodix :',
                                  'enable': compareSdefs},
                 'verifyInvariablePart': {'message': 'Warning : Issue '
                                          'regarding usage of <g> tag found '
                                          'for entry : ',
                                          'enable': verifyInvariablePart},
                 'repeatedEntries': {'message': 'Warning : Repeated entries '
                                     'found for entry : ',
                                     'enable': repeatedEntries}
                 }

        transfer = {'repeatedEntriesCatItem': {'message': 'Warning : Repeated'
                                               ' cat-item found : ',
                                               'enable':
                                               repeatedEntriesCatItem},
                    'repeatedEntriesAttrItem': {'message': 'Warning : Repeated'
                                                ' attr-item found : ',
                                                'enable':
                                                repeatedEntriesAttrItem},
                    'unusedDefCats': {'message': 'Warning : Following def-cats'
                                      ' have not been used : ',
                                      'enable': unusedDefCats},
                    'checkValidPartClip': {'message': 'Warning : Invalid part'
                                           "='%s', found for entry : %s",
                                           'enable': checkValidPartClip},
                    'checkValidEqualTag': {'message': "Warning : The 'part' "
                                           'does not correspond with the lit'
                                           '-tag : ',
                                           'enable': checkValidEqualTag},
                    'conflictingCatItem': {'message': 'Warning : Repeated '
                                           'cat-item entry found for two '
                                           'def-cats : ',
                                           'enable': conflictingCatItem},
                    'checkValidPosition': {'message': 'Warning : The position '
                                           'mentioned for a tag in the entry '
                                           'is invalid : ',
                                           'enable': checkValidPosition},
                    'enforceBreakTag': {'message': 'Warning : <b/> missing '
                                        'between consecutive <lu> elements '
                                        'for element : %s, on line number'
                                        ' : %s ',
                                        'enable': enforceBreakTag},
                    'xsdValidation': {'message': 'Warning : The position '
                                      'mentioned for a tag in the entry is '
                                      'invalid : ',
                                      'enable': xsdValidation},
                    'enforceSide': {'message': 'Warning : Are you sure you '
                                    "want to specify side='sl' in the %s tag"
                                    ' on line %s',
                                    'enable': enforceSide},
                    'macroNames': {'message': 'Warning : Are you sure you '
                                   "want to ''specify multiple def-macros "
                                   "with the same n='' and npar='' values : ",
                                   'enable': macroNames}
                    }

        tagger = {'defLabelClosed': {'message': 'Warning : Invalid value for '
                                     "closed' attribute used in def-label : ",
                                     'enable': defLabelClosed},
                  'validateLabelSequence': {'message': 'Warning : Invalid '
                                            'label %s used in label '
                                            'sequence. ',
                                            'enable': validateLabelSequence},
                  'repeatedDefLabel': {'message': 'Warning : Repeated def-'
                                       'label : ',
                                       'enable': repeatedDefLabel}
                  }

        modes = {'installBool': {'message': 'Warning : Invalid install '
                                 'attrib : %s for <mode name=\"%s\">',
                                 'enable': installBool},
                 'repeatedProgram': {'message': 'Warning : Repeated program '
                                     'definitions in : %s',
                                     'enable': repeatedProgram},
                 'validateProgram': {'message': 'Warning : Invalid program '
                                     ': %s',
                                     'enable': validateProgram},
                 'locateFile': {'message': 'Warning : File not found : %s',
                                'enable': locateFile},
                 'emptyProgram': {'message': 'Warning : Are you sure you '
                                  'want to keep the program %s in the '
                                  'mode %s empty?',
                                  'enable': emptyProgram},
                 'enforceRules': {'message': 'Warning : Certain rules not '
                                  'followed in the modes file',
                                  'enable': enforceRules},
                 'installSwitchNo': {'message': 'Warning : Improper mode '
                                     'name %s associated with attribute'
                                     " install = 'no'",
                                     'enable': installSwitchNo}
                 }

        config = {'monodix': monodix, 'bidix': bidix,
                  'transfer': transfer, 'tagger': tagger, 'modes': modes}
        return json.dumps(config, indent=2)
