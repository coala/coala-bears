from bears.shell.BashateBear import BashateBear
from coalib.testing.LocalBearTestHelper import verify_local_bear


# E002: indents can only be spaces
E002_bad = """
\techo "E002: Has a tab"
"""

# E003: indents should be multiples of 4
E003_bad = """
   indent is not multiple of 4
"""

# E006: too long lines
E006_bad = 'a = "{}"\n'.format('a' * 100)


BashateBearTest = verify_local_bear(
    BashateBear,
    valid_files=(),
    invalid_files=(E006_bad,
                   E002_bad,
                   E003_bad,),
    tempfile_kwargs={'suffix': '.sh'})

BashateBearTestIgnoreMultipleErrors = verify_local_bear(
    BashateBear,
    valid_files=(E002_bad,
                 E003_bad,
                 E006_bad,),
    invalid_files=(),
    tempfile_kwargs={'suffix': '.sh'},
    settings={'bashate_ignore': 'E002, E003, E006'})

BashateBearTestIgnoreLineLength = verify_local_bear(
    BashateBear,
    valid_files=(E006_bad,),
    invalid_files=(E002_bad,
                   E003_bad,),
    tempfile_kwargs={'suffix': '.sh'},
    settings={'bashate_ignore': 'E006'})
