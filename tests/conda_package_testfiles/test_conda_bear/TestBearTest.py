from tests.LocalBearTestHelper import verify_local_bear


good_file = """def good_name
  test if something
end
""".splitlines(keepends=True)


bad_file = """def badName
  test if something
end
""".splitlines(keepends=True)

TestBearTest = verify_local_bear(
    TestBear,
    valid_files=(good_file,),
    invalid_files=(bad_file),)
