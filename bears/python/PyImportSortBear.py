from isort import SortImports

from coalib.bearlib import deprecate_settings
from coalib.bearlib.spacing.SpacingHelper import SpacingHelper
from coalib.bears.LocalBear import LocalBear
from dependency_management.requirements.PipRequirement import PipRequirement
from coalib.results.Diff import Diff
from coalib.results.Result import Result
from coalib.settings.Setting import typed_list


class PyImportSortBear(LocalBear):

    LANGUAGES = {'Python', 'Python 3', 'Python 2'}
    REQUIREMENTS = {PipRequirement('isort', '4.2')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_FIX = {'Formatting'}

    @staticmethod
    def _seperate_imports(file):
        import_stmts = []
        tmp = []
        paren = False
        for lineno, lines in enumerate(file, start=1):
            if 'import' in lines.split() or paren:
                # To ensure that
                # from x import ( y,
                #                 z) type of imports are not treated as
                # different sections
                if '(' in lines and ')' not in lines:
                    paren = True
                if ')' in lines:
                    paren = False
                tmp.append((lineno, lines))
            else:
                if tmp:
                    import_stmts.append(tmp)
                tmp = []
        # To ensure that if the last line of a file is an import statement
        # it doesn't get ignored
        if tmp:
            import_stmts.append(tmp)
            tmp = []
        return import_stmts

    def _get_diff(self):
        if self.treat_seperated_imports_independently:
            import_stmts = PyImportSortBear._seperate_imports(self.file)
            sorted_imps = []
            for units in import_stmts:
                sort_imports = SortImports(file_contents=''.
                                           join([x[1] for x in units]),
                                           **self.isort_settings)
                sort_imports = sort_imports.output.splitlines(True)
                sorted_imps.append((units, sort_imports))

            diff = Diff(self.file)
            for old, new in sorted_imps:
                start = old[0][0]
                end = start + len(old) - 1
                diff.delete_lines(start, end)
                assert isinstance(new, list)
                diff.add_lines(start, list(new))

            if diff.modified != diff._file:
                return diff
        else:
            sort_imports = SortImports(file_contents=''.join(self.file),
                                       **self.isort_settings)

            new_file = tuple(sort_imports.output.splitlines(True))
            if new_file != tuple(self.file):
                diff = Diff.from_string_arrays(self.file, new_file)
                return diff
        return None

    @deprecate_settings(indent_size='tab_width')
    def run(self, filename, file,
            use_parentheses_in_import: bool=True,
            force_alphabetical_sort_in_import: bool=False,
            force_sort_within_import_sections: bool=True,
            from_first_in_import: bool=False,
            include_trailing_comma_in_import: bool=False,
            combine_star_imports: bool=True,
            combine_as_imports: bool=True,
            lines_after_imports: int=-1,
            order_imports_by_type: bool=False,
            balanced_wrapping_in_imports: bool=False,
            import_heading_localfolder: str='',
            import_heading_firstparty: str='',
            import_heading_thirdparty: str='',
            import_heading_stdlib: str='',
            import_heading_future: str='',
            default_import_section: str='FIRSTPARTY',
            force_grid_wrap_imports: bool=False,
            force_single_line_imports: bool=True,
            sort_imports_by_length: bool=False,
            use_spaces: bool=True,
            indent_size: int=SpacingHelper.DEFAULT_TAB_WIDTH,
            forced_separate_imports: typed_list(str)=(),
            isort_multi_line_output: int=4,
            known_first_party_imports: typed_list(str)=(),
            known_third_party_imports: typed_list(str)=(),
            known_standard_library_imports: typed_list(str)=None,
            max_line_length: int=79,
            imports_forced_to_top: typed_list(str)=(),
            treat_seperated_imports_independently: bool=False):
        """
        Raise issues related to sorting imports, segregating imports into
        various sections, and also adding comments on top of each import
        section based on the configurations provided.

        You can read more about ``isort`` at
        <https://isort.readthedocs.org/en/latest/>.

        :param use_parentheses_in_import:
            True if parenthesis are to be used in import statements.
        :param force_alphabetical_sort_in_import:
            If set, forces all imports to be sorted as a single section,
            instead of within other groups (such as straight vs from).
        :param force_sort_within_import_sections:
            If set, imports will be sorted within there section independent
            to the import_type.
        :param from_first_in_import:
            If set, imports using "from" will be displayed above normal
            (straight) imports.
        :param include_trailing_comma_in_import:
            If set, will automatically add a trailing comma to the end of
            "from" imports. Example: ``from abc import (a, b, c,)``
        :param combine_star_imports:
            If set to true - ensures that if a star import is present,
            nothing else is imported from that namespace.
        :param combine_as_imports:
            If set to true - isort will combine as imports on the same line
            within for import statements.
        :param lines_after_imports:
            Forces a certain number of lines after the imports and before the
            first line of functional code. By default this is set to -1 which
            uses 2 lines if the first line of code is a class or function and
            1 line if it's anything else.
        :param order_imports_by_type:
            If set to true - isort will create separate sections within "from"
            imports for CONSTANTS, Classes, and modules/functions.
        :param balanced_wrapping_in_imports:
            If set to true - for each multi-line import statement isort will
            dynamically change the import length to the one that produces
            the most balanced grid, while staying below the maximum import
            length defined.
        :param import_heading_localfolder:
            A comment to consistently place directly above imports that
            start with '.'.
        :param import_heading_firstparty:
            A comment to consistently place directly above imports from
            the current project.
        :param import_heading_thirdparty:
            A comment to consistently place directly above thirdparty imports.
        :param import_heading_stdlib:
            A comment to consistently place directly above imports from
            the standard library.
        :param import_heading_future:
            A comment to consistently place directly above future imports.
        :param default_import_section:
            The default section to place imports in, if their section can
            not be automatically determined.
        :param force_grid_wrap_imports:
             Force "from" imports to be grid wrapped regardless of line length.
        :param force_single_line_imports:
            If set to true - instead of wrapping multi-line from style imports,
            each import will be forced to display on its own line.
        :param sort_imports_by_length:
            Set to true to sort imports by length instead of alphabetically.
        :param use_spaces:
            True if spaces are to be used instead of tabs.
        :param indent_size:
            Number of spaces per indentation level.
        :param forced_separate_imports:
            A list of modules that you want to appear in their own separate
            section.
        :param isort_multi_line_output:
            An integer that represents how you want imports to be displayed
            by ``isort`` if they're long enough to span multiple lines.
            This value is passed to isort as the ``multi_line_output`` setting.
            Possible values are (0-grid, 1-vertical, 2-hanging, 3-vert-hanging,
            4-vert-grid, 5-vert-grid-grouped)
            A full definition of all possible modes can be found at
            <https://github.com/timothycrosley/isort#multi-line-output-modes>.
        :param known_first_party_imports:
            A list of imports that will be forced to display within the
            standard library category of imports.
        :param known_third_party_imports:
            A list of imports that will be forced to display within the
            third party category of imports.
        :param known_standard_library_imports:
            A list of imports that will be forced to display within the
            first party category of imports.
        :param import_wrap_length:
            An integer that represents the longest line-length you want when
            wrapping. If not set will default to line_length.
        :param imports_forced_to_top:
            Forces a list of imports to the top of their respective section.
            This works well for handling the unfortunate cases of import
            dependencies that occur in many projects.
        :param max_line_length:
            Maximum number of characters for a line.
        :param treat_seperated_imports_independently:
            Treat import statements seperated by one or more blank line or any
            statement other than an import statement as an independent bunch.
        """
        isort_settings = dict(
            use_parentheses=use_parentheses_in_import,
            force_alphabetical_sort=force_alphabetical_sort_in_import,
            force_sort_within_sections=force_sort_within_import_sections,
            from_first=from_first_in_import,
            include_trailing_comma=include_trailing_comma_in_import,
            combine_star=combine_star_imports,
            lines_after_imports=lines_after_imports,
            order_by_type=order_imports_by_type,
            balanced_wrapping=balanced_wrapping_in_imports,
            import_heading_localfolder=import_heading_localfolder,
            import_heading_firstparty=import_heading_firstparty,
            import_heading_thirdparty=import_heading_thirdparty,
            import_heading_stdlib=import_heading_stdlib,
            import_heading_future=import_heading_future,
            default_section=default_import_section,
            force_grid_wrap=force_grid_wrap_imports,
            force_single_line=force_single_line_imports,
            length_sort=sort_imports_by_length,
            indent='Tab' if not use_spaces else indent_size,
            forced_separate=forced_separate_imports,
            multi_line_output=isort_multi_line_output,
            known_first_party=known_first_party_imports,
            known_third_party=known_third_party_imports,
            line_length=max_line_length,
            force_to_top=imports_forced_to_top)

        if known_standard_library_imports is not None:
            isort_settings['known_standard_library'] = (
                known_standard_library_imports)

        self.isort_settings = isort_settings
        self.file = file
        self.filename = filename
        self.treat_seperated_imports_independently = \
            treat_seperated_imports_independently

        diff = self._get_diff()

        if diff:
            yield Result(self,
                         'Imports can be sorted.',
                         affected_code=diff.affected_code(filename),
                         diffs={filename: diff})
