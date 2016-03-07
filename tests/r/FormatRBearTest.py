from bears.r.FormatRBear import FormatRBear
from tests.LocalBearTestHelper import verify_local_bear

good_file = """
1 + 1
if (TRUE) {
    x = 1  # inline comments
} else {
    x = 2
    print("Oh no... ask the right bracket to go away!")
}""".splitlines(keepends=True)


bad_file = """1+1
if(TRUE){
x=1  # inline comments
}else{
x=2;print('Oh no... ask the right bracket to go away!')}
""".splitlines(keepends=True)


FormatRBearTest = verify_local_bear(FormatRBear,
                                    valid_files=(good_file,),
                                    invalid_files=(bad_file,))
