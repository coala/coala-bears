from Constants import classifiers, imports, encoding, requirements
from Constants import setup_constants
from coalib.bears.requirements.PythonRequirement import PythonRequirement
import shutil
import os
import glob
import re

if not os.path.exists('upload/'):
    os.mkdir('upload/')

#Reqrs = MockBear.REQUIREMENTS

# for req in Reqrs:
#    if type(req) == PythonRequirement:
#        if req.version:
#            reqs.write(req.package + '==' + req.version + '\n')
#        else:
#            reqs.write(req.package + '\n')

bears = glob.glob('**/*Bear.py')

for bear in bears:
    file = bear
    bear = re.match(r'.+/(.*)\.py', bear).group(1)
    if not os.path.exists('upload/' + bear):
        os.mkdir('upload/' + bear)
        if not os.path.exists('upload' + bear + '/' + bear):
            os.mkdir('upload/' + bear + '/' + bear)
    if not os.path.exists('upload/' + bear + '/' + bear + '/__init__.py'):
        init = open('upload/' + bear + '/' + bear + '/__init__.py', 'w')
        init.write(' ')
        init.close()
    shutil.copyfile(file, 'upload/' + bear + '/' + bear + '/' + bear + '.py')

    setup = open('upload/' + bear + '/setup.py', "w")
    reqs = open('upload/' + bear + '/requirements.txt', "w")

    # set env
    setup.write('#!/usr/bin/env python3\n\n')

    # write imports
    setup.write(imports + '\n\n')

    # encoding UTF-8
    setup.write(encoding + '\n\n')

    # requirements
    setup.write(requirements + '\n\n')

    # setuptools
    setup.write('if __name__== "__main__":\n')
    setup.write("\tsetup(name=" + "'" + bear + "',\n")
    setup.write('\t\t  version="0.1.30",\n')
    setup.write("\t\t  description='The " + bear + " bear for coala (Code")
    setup.write(" Analysis Application)',\n")
    setup.write('\t\t  ' + setup_constants + ',\n')
    setup.write('\t\t  classifiers=' + classifiers + ')')

    # close the files
    setup.close()
    reqs.close()
    # upload everything

    os.chdir('upload/' + bear)
    os.system('python setup.py register -r pypitest')
    os.system('python setup.py sdist upload -r pypitest')
    os.chdir('../../')
