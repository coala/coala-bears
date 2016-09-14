from itertools import chain

from coalib.bearlib.abstractions.Linter import linter
from coalib.settings.Setting import typed_list


@linter(executable='postcss',
        output_format='corrected')
class PostCSSBear:
    """
    This bear adds ``PostCSS`` utilities to analyze CSS code.
    """

    def create_arguments(self, filename, file,
                         postcss_plugins: typed_list(str)):
        """
        :param postcss_plugins:
            List of PostCSS `plugins
            <https://github.com/postcss/postcss/blob/master/docs/plugins.md>`_
            to use with this bear.
        """
        # TODO List some available plugins
        if not postcss_plugins:
            # TODO Check this inside __init__ / Bear needs an interface
            # TODO   function allowing to check stuff like this.
            self.err("Please specify at least one plugin name.")
            return

        return chain.from_iterable(('--use', plugin, filename)
                                   for plugin in postcss_plugins)
