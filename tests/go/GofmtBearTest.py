from bears.go.GofmtBear import GofmtBear
from tests.LocalBearTestHelper import verify_local_bear

GofmtBear = verify_local_bear(
    GofmtBear,
    ('package main\n\nfunc main() {\n\treturn 1\n}',),
    ('package main\nfunc main() {\n\treturn 1\n}',))
