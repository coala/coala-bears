from bears.elm.ElmLintBear import ElmLintBear
from tests.LocalBearTestHelper import verify_local_bear

ElmLintBearTest = verify_local_bear(ElmLintBear,
                                    ('test',),
                                    ('\t',))
