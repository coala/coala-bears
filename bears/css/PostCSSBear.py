from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear
from coalib.settings.Setting import typed_list


class PostCSSBear(Lint, LocalBear):
    executable = "postcss"
    gives_corrected = True

    def run(self, filename, file, postcss_plugins: typed_list(str)=[]):
        '''
        This bear adds ``PostCSS`` utilities to analyze CSS code.

        :param postcss_plugins: List of PostCSS plugins to use with
                                this bear which can be defined in
                                .coafile.
        '''
        if not postcss_plugins:
            self.err("Please specify at least one plugin name.")
            return []

        for plugin in postcss_plugins:
            self.arguments += " --use " + plugin
            self.arguments += " {filename}"
            self.diff_message = "PostCSS plugin {} is analyzing.".format(
                plugin)
        return self.lint(filename, file)
