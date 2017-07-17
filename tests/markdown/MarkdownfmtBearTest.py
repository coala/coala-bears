from coalib.testing.LocalBearTestHelper import verify_local_bear

from bears.markdown.MarkdownfmtBear import MarkdownfmtBear


header_in_file1 = """
MarkdownBear
=====

"""

header_out_file1 = """
MarkdownBear
============

"""

spacing_in_file2 = """

This is   a test    file.

"""

spacing_out_file2 = """

This is a test file.

"""

MarkdownfmtBear = verify_local_bear(
    MarkdownfmtBear,
    valid_files=(header_in_file1, spacing_in_file2,),
    invalid_files=(header_out_file1, spacing_out_file2,))
