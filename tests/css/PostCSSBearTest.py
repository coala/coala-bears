from bears.css.PostCSSBear import PostCSSBear
from tests.LocalBearTestHelper import verify_local_bear


good_file = """
.example {
    display: -webkit-box;
    display: -webkit-flex;
    display: -ms-flexbox;
    display: flex;
}
""".splitlines(keepends=True)

bad_file = """
.example {
    display: flex;
}
.foo {
  clear: fix;
}
""".splitlines(keepends=True)

PostCSSBearTest = verify_local_bear(PostCSSBear,
                                    valid_files=(good_file,),
                                    invalid_files=(bad_file,),
                                    settings={'postcss_plugins':
                                              'autoprefixer,cssgrace'})

PostCSSBearDefaultTest = verify_local_bear(PostCSSBear,
                                           valid_files=(good_file, bad_file,),
                                           invalid_files=())
