import os

from bears.scss.SASSLintBear import SASSLintBear
from coalib.testing.LocalBearTestHelper import verify_local_bear

# Test examples from http://sass-lang.com/guide
good_sass_file = '''
nav
  ul
    list-style: none
    margin: 0
    padding: 0

  li
    display: inline-block

  a
    display: block
    padding: 6px 12px
    text-decoration: none
'''

bad_sass_file = '''
nav
  ul
    margin: 0
    padding: 0 !important
    err-style: none

  li
    display: inline-block

  a
    display: block
    padding: 6px 12px
    text-decoration: none
'''

good_sass_file_with_config = '''
nav
  ul
    margin: 0
    padding: 0 !important

  li
    display: inline-block
'''

good_scss_file = """
nav {
  ul {
    list-style: none;
    margin: 0;
    padding: 0;
  }

  li { display: inline-block; }

  a {
    display: block;
    padding: 6px 12px;
    text-decoration: none;
  }
}
"""

bad_scss_file = """
nav {
  ul {
    margin: 0
    padding: 0
    list-style: none
  }

  li { display: inline-block; }

  a {
    display: block;
    padding: 6px 12px;
    text-decoration: none;
}
"""

test_dir = os.path.join(os.path.dirname(__file__), 'test_files')

SASSLintBearTest = verify_local_bear(
    SASSLintBear,
    valid_files=(good_sass_file,),
    invalid_files=(bad_sass_file,),
    tempfile_kwargs={'suffix': '.sass'})

SASSLintBearSCSSTest = verify_local_bear(
    SASSLintBear,
    valid_files=(good_scss_file,),
    invalid_files=(bad_scss_file,),
    tempfile_kwargs={'suffix': '.scss'})

SASSLintBearConfigTest = verify_local_bear(
    SASSLintBear,
    valid_files=(good_sass_file_with_config,),
    invalid_files=(bad_sass_file,),
    tempfile_kwargs={'suffix': '.sass'},
    settings={'sasslint_config': os.path.join(test_dir, 'sass-lint.yml')})

SASSLintBearEmptyFileTest = verify_local_bear(
    SASSLintBear,
    valid_files=('',),
    invalid_files=tuple(),
    filename=os.path.join(test_dir, 'test.scss'),
    tempfile_kwargs={'suffix': '.scss'},
    create_tempfile=False)
