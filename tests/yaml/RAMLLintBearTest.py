from bears.yaml.RAMLLintBear import RAMLLintBear
from coalib.testing.LocalBearTestHelper import verify_local_bear

good_file = """
#%RAML 0.8

title: World Music API
baseUri: http://example.api.com/{version}
version: v1
"""


bad_file = """#%RAML 0.8

title: Failing RAML
version: 1
baseUri: http://example.com

/resource:
  description: hello

  post:

"""


RAMLLintBearTest = verify_local_bear(RAMLLintBear,
                                     valid_files=(good_file,),
                                     invalid_files=(bad_file,),
                                     tempfile_kwargs={'suffix': '.raml'})
