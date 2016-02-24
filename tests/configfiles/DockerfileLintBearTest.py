from bears.configfiles.DockerfileLintBear import DockerfileLintBear
from tests.LocalBearTestHelper import verify_local_bear

good_file = """
FROM ubuntu:14.04

# Install basic tools
RUN apt-get -y -qq update
RUN apt-get -y -qq upgrade
""".splitlines(keepends=True)


bad_file = """
FROM ubuntu:14.04

# Install basic tools
apt-get -y -qq update
apt-get -y -qq upgrade
""".splitlines(keepends=True)


DockerfileLintBearTest = verify_local_bear(DockerfileLintBear,
                                           valid_files=(good_file,),
                                           invalid_files=(bad_file,))
