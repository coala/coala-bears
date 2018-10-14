import os

from bears.configfiles.DockerfileLintBear import DockerfileLintBear
from coalib.testing.LocalBearTestHelper import verify_local_bear

good_file = """
FROM ubuntu:14.04
LABEL MAINTAINER coala
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


good_file2 = """
FROM ubuntu
LABEL MAINTAINER coala
LABEL Name coala-docker
LABEL Version 0.1

RUN apt-get -y -qq update
RUN apt-get -y -qq upgrade
RUN curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
EXPOSE 5432
CMD ["/usr/bin/node", "/var/www/app.js"]
"""


bad_file2 = """
FROM ubuntu

apt-get -y -qq update
apt-get -y -qq upgrade
curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
"""


good_file3 = """
FROM kali
LABEL MAINTAINER coala
LABEL Name coala-docker
LABEL Version 0.1
EXPOSE 5432
"""


bad_file3 = """
FROM kali
LABEL Name
LABEL Version
"""


def get_testfile_path(filename):
    return os.path.join(os.path.dirname(__file__),
                        'dockerfile_lint_test_files',
                        filename)


default_rule = get_testfile_path('default_rule.yaml')

sample_rule = get_testfile_path('sample_rule.yaml')


DockerfileLintBearTest = verify_local_bear(DockerfileLintBear,
                                           valid_files=(good_file,),
                                           invalid_files=(bad_file,))

DockerfileLintBearDefaultRuleTest = verify_local_bear(
    DockerfileLintBear,
    valid_files=(good_file2,),
    invalid_files=(bad_file2,),
    settings={'dockerfile_lint_rule_file':
              default_rule})

DockerfileLintBearCustomRuleTest = verify_local_bear(
    DockerfileLintBear,
    valid_files=(good_file3,),
    invalid_files=(bad_file3,),
    settings={'dockerfile_lint_rule_file':
              sample_rule})
