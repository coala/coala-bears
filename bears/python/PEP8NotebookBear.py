import autopep8
import nbformat

from coalib.bearlib.spacing.SpacingHelper import SpacingHelper
from coalib.bears.LocalBear import LocalBear
from coalib.bears.requirements.PipRequirement import PipRequirement
from coalib.results.Diff import Diff
from coalib.results.Result import Result
from coalib.settings.Setting import typed_list

# Comments regarind Jupyter Notebooks:
# The `nbformat` module contains the reference implementation of the Jupyter
# Notebook format, and Python APIs for working with notebooks.
# On the file level, a notebook is a JSON file, i.e. dictionary with a few
# keys.
# The functions in `nbformat` work with `NotebookNode` objects, which are like
# dictionaries, but allow attribute access. The structure of these objects
# matches the notebook format specification.


def notebook_node_from_string_list(string_list):
    """
    Reads a notebook from a string list and returns the NotebookNode
    object.

    :param string_list: The notebook file contents as list of strings
                        (linewise).
    :return:            The notebook as NotebookNode.
    """
    return nbformat.reads(''.join(string_list), nbformat.NO_CONVERT)


def notebook_node_to_string_list(notebook_node):
    """
    Writes a NotebookNode to a list of strings.

    :param notebook_node: The notebook as NotebookNode to write.
    :return:              The notebook as list of strings (linewise).
    """
    return nbformat.writes(notebook_node, nbformat.NO_CONVERT).splitlines(True)


def autopep8_fix_code_cell(source, options=None, apply_config=None):
    """
    Applies autopep8.fix_code and takes care of newline characters.

    autopep8.fix_code automatically adds a final newline at the end,
    e.g. ``autopep8.fix_code('a=1')`` yields 'a = 1\\n'.
    Note that this is not related to the 'W292' flag, i.e.
    ``autopep8.fix_code('a=1', options=dict(ignore=('W292',)))`` gives
    the same result.
    For notebook code cells, this behaviour does not make sense, hence
    newline is removed if ``source`` does not end with one.
    """
    source_corrected = autopep8.fix_code(source,
                                         apply_config=apply_config,
                                         options=options)

    if not source.endswith('\n'):
        return source_corrected[:-1]

    return source_corrected


class PEP8NotebookBear(LocalBear):
    LANGUAGES = {'Python', 'Python 2', 'Python 3'}
    REQUIREMENTS = {PipRequirement('autopep8', '1.2'),
                    PipRequirement('nbformat', '4.1')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    ASCIINEMA_URL = 'https://asciinema.org/a/83333'
    CAN_FIX = {'Formatting'}

    def run(self, filename, file,
            max_line_length: int=79,
            indent_size: int=SpacingHelper.DEFAULT_TAB_WIDTH,
            pep_ignore: typed_list(str)=(),
            pep_select: typed_list(str)=(),
            local_pep8_config: bool=False):
        """
        Detects and fixes PEP8 incompliant code in Jupyter Notebooks. This bear
        will not change functionality of the code in any way.

        :param max_line_length:   Maximum number of characters for a line.
        :param indent_size:       Number of spaces per indent level.
        :param pep_ignore:        A list of errors/warnings to ignore.
        :param pep_select:        A list of errors/warnings to exclusively
                                  apply.
        :param local_pep8_config: Set to true if autopep8 should use a config
                                  file as if run normally from this directory.
        """
        options = {'ignore': pep_ignore,
                   'select': pep_select,
                   'max_line_length': max_line_length,
                   'indent_size': indent_size}
        notebook_node = notebook_node_from_string_list(file)
        cells = notebook_node['cells']

        for cell in cells:
            if cell['cell_type'] != 'code':
                continue
            cell['source'] = autopep8_fix_code_cell(cell['source'],
                                                    local_pep8_config,
                                                    options)

        corrected = notebook_node_to_string_list(notebook_node)

        # If newline at eof in `file` but not in `corrected`, add
        # final newline character to `corrected` to make sure this difference
        # does not pop up in `diffs`.
        if file[-1].endswith('\n') and not corrected[-1].endswith('\n'):
            corrected[-1] += '\n'

        diffs = Diff.from_string_arrays(file, corrected).split_diff()

        for diff in diffs:
            yield Result(self,
                         'The code does not comply to PEP8.',
                         affected_code=(diff.range(filename),),
                         diffs={filename: diff})
