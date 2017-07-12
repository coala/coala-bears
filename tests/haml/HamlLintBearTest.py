from bears.haml.HamlLintBear import HamlLintBear
from coalib.testing.LocalBearTestHelper import verify_local_bear

good_file = """
#content
  .left.column
    %h2 Welcome to our site!
    %p= print_information
  .right.column
    = render partial: 'sidebar'
 """

bad_file = """
 #content
  .left.column
    %h2 Welcome to our site!
    %p= print_information
  .right.column
    = render :partial =>'sidebar'
 """


HamlLintBearTest = verify_local_bear(HamlLintBear,
                                     valid_files=(good_file,),
                                     invalid_files=(bad_file,))
