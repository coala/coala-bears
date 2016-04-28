from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear


class CSSAutoPrefixBear(Lint, LocalBear):
    executable = "postcss"
    arguments = "--use autoprefixer {filename}"
    prerequisite_command = ['postcss', '--use', 'autoprefixer']
    prerequisite_fail_msg = "Autoprefixer is not installed."
    diff_message = "Add vendor prefixes to CSS rules."
    gives_corrected = True
    LANGUAGES = "CSS"

    def run(self, filename, file):
        '''
        This bear adds vendor prefixes to CSS rules using ``autoprefixer``
        utility.
        '''
        return self.lint(filename, file)
