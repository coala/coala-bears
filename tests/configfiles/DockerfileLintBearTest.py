from bears.configfiles.DockerfileLintBear import DockerfileLintBear
from coalib.testing.LocalBearTestHelper import verify_local_bear

good_file = """
FROM ubuntu:14.04
MAINTAINER coala
LABEL Name coala-docker
LABEL Version 0.1

# Install basic tools
RUN apt-get -y -qq update
RUN apt-get -y -qq upgrade
EXPOSE 5432
CMD ["/bin/bash", "coala"]
"""


bad_file = """
FROM ubuntu:14.04

# Install basic tools
apt-get -y -qq update
apt-get -y -qq upgrade
"""


DockerfileLintBearTest = verify_local_bear(DockerfileLintBear,
                                           valid_files=(good_file,),
                                           invalid_files=(bad_file,))
