from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.PipRequirement import PipRequirement


@linter(executable='futurize',
        output_format='unified-diff',
        result_message='The code could be futurized.',
        diff_distance=0,
        use_stdout=True,
        use_stderr=False)
class FutureBear:
    LANGUAGES = {'Python', 'Python 2'}
    REQUIREMENTS = {PipRequirement('future', '0.16.0')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}

    @staticmethod
    def create_arguments(filename, file, config_file,
                         futurize_stage: int = 0):
        """
        :param futurize_stage: The desired stage of futurization (0, 1, or 2).
                               Please refer to the futurize documentation for
                               more information on the meaning of the
                               different stages.
        """
        stage = '-0'
        if futurize_stage in (0, 1, 2):
            stage = '-{}'.format(futurize_stage)
        return (stage, filename)
