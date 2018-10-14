import json
from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.NpmRequirement import NpmRequirement
from coalib.results.Result import Result

_setting_map = {True: 'on',
                False: 'off'}


@linter(executable='gherkin-lint',
        use_stderr=True,
        use_stdout=False,
        global_bear=True)
class GherkinLintBear:
    """
    Use Gherkin to run linting on feature files
    """

    LANGUAGES = {'Gherkin'}
    REQUIREMENTS = {NpmRequirement('gherkin-lint', '2')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala_devel@googlegroups.com'}
    LICENSE = 'AGPL_3.0'
    CAN_DETECT = {'Formatting', 'Syntax'}

    def process_output(self, output, filename, file):
        stderr = json.loads(output)
        for fileErr in stderr:
            filePath = fileErr['filePath']
            for err in fileErr['errors']:
                yield Result.from_values(
                    origin='{} ({})'.format(
                        self.__class__.__name__,
                        err['rule']),
                    message=err['message'],
                    line=int(err['line']),
                    file=filePath)

    @staticmethod
    def generate_config(filename, file,
                        allow_trailing_whitespace: bool = True,
                        allow_dupe_feature_names: bool = True,
                        allow_dupe_scenario_names: bool = True,
                        allow_duplicate_tags: bool = True,
                        allow_empty_file: bool = True,
                        allow_files_without_scenarios: bool = True,
                        allow_homogenous_tags: bool = True,
                        allow_multiple_empty_lines: bool = True,
                        allow_scenario_outlines_without_examples: bool = True,
                        allow_superfluous_tags: bool = True,
                        allow_unnamed_features: bool = True,
                        allow_unnamed_scenarios: bool = True,
                        one_space_between_tags: bool = False,
                        use_and: bool = False):
        """
        :param allow_trailing_whitespace:
            Allow trailing spaces
        :param allow_dupe_feature_names:
            Disallows duplicate Feature names
        :param allow_dupe_scenario_names:
            Disallows duplicate Scenario names
        :param allow_duplicate_tags:
            Disallows duplicate tags on the same Feature or Scenario
        :param allow_empty_file:
            Disllows empty file
        :param allow_files_without_scenarios:
            Disallows files with no scenarios
        :param allow_homogenous_tags:
            Disallows tags present on every Scenario in a Feature,
            rather than on the Feature itself
        :param allow_multiple_empty_lines:
            Disallows/enforces new line at EOF
        :param allow_scenario_outlines_without_examples:
            Disallows scenario outlines without examples
        :param allow_superfluous_tags:
            Disallows tags present on a Feature and a Scenario in
            that Feature
        :param allow_unnamed_features:
            Disallows empty Feature name
        :param allow_unnamed_scenarios:
            Disallows empty Scenario name
        :param one_space_between_tags:
            Tags on the same time must be separated by a single space
        :param use_and:
            Disallows repeated step names requiring use of And instead
        """
        options = {'no-trailing-spaces':
                   _setting_map[not allow_trailing_whitespace],
                   'no-dupe-feature-names':
                   _setting_map[not allow_dupe_feature_names],
                   'no-dupe-scenario-names':
                   _setting_map[not allow_dupe_scenario_names],
                   'no-duplicate-tags': _setting_map[not allow_duplicate_tags],
                   'no-empty-file': _setting_map[not allow_empty_file],
                   'no-files-without-scenarios':
                   _setting_map[not allow_files_without_scenarios],
                   'no-homogenous-tags':
                   _setting_map[not allow_homogenous_tags],
                   'no-multiple-empty-lines':
                   _setting_map[not allow_multiple_empty_lines],
                   'no-scenario-outlines-without-examples':
                   _setting_map[not allow_scenario_outlines_without_examples],
                   'no-superfluous-tags':
                   _setting_map[not allow_superfluous_tags],
                   'no-unnamed-features':
                   _setting_map[not allow_unnamed_features],
                   'no-unnamed-scenarios':
                   _setting_map[not allow_unnamed_scenarios],
                   'one-space-between-tags':
                   _setting_map[one_space_between_tags],
                   'use-and': _setting_map[use_and]}
        return json.dumps(options)

    @staticmethod
    def create_arguments(config_file, gherkin_config: str = ''):
        args = ('-f', 'json', '--config',)
        if gherkin_config:
            args += (gherkin_config,)
        else:
            args += (config_file,)
        return args
