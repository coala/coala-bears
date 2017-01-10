from glob import glob
import os
import yaml
import shutil

from coalib.bears.GlobalBear import GlobalBear
from coalib.results.Result import Result
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from dependency_management.requirements.GemRequirement import GemRequirement
from dependency_management.requirements.PipRequirement import PipRequirement
from sarge import run, Capture


def check_path(image_file):
    if (glob(str(image_file)) == []):
        raise ValueError('Provide a correct path for image')
    else:
        return os.path.join('..', str(image_file))


def check_width(width):
    if (int(width) <= 0):
        raise ValueError('Width has to be greater than 0')

    else:
        return int(width)


def check_height(height):
    if (int(height) <= 0):
        raise ValueError('Height has to be greater than 0')
    else:
        return int(height)


class ImageDimensionBear(GlobalBear):
    """
    Checks the dimension of an image us a gem.

    More information is available at <github.com/Abhi2424shek/img_checker>
    """

    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    REQUIREMENTS = {GemRequirement('img_checker'),
                    PipRequirement('pyyaml', '3.12')}
    LICENSE = 'AGPL-3.0'
    CAN_FIX = {'Image Dimension'}

    @classmethod
    def check_prerequisites(cls):
        if shutil.which('img_checker') is None:
            return 'img_checker is not installed.'
        return True

    def run(self,
            image_file: check_path,
            width: check_width,
            height: check_height):
        """
        This bear ensures that images used in your project are
        within a fixed dimension.

        WARNING: If your repository has an existing img_config.yml
        file, please change it since this bear creates a file
        with that name and removes it in the end.

        :param image_file: The file/directory that bear
                           will look for images
        :param width:      The maximum width value allowed
                           for images
        :param height:     The maximum height value allowed
                           for images
        """
        # self.warn(warning_message)
        os.mkdir('temp_dir_for_img_config_file')
        os.chdir('temp_dir_for_img_config_file')
        with open('img_config.yml', 'w') as yaml_file:
            config = [{'directory': image_file,
                       'width': width,
                       'height': height}]
            yaml.dump(config, yaml_file, default_flow_style=False)
        self.debug(glob(image_file))
        cmd = 'img_checker'
        output = run(cmd, stdout=Capture(), stderr=Capture())
        os.remove('img_config.yml')
        os.chdir('..')
        os.rmdir('temp_dir_for_img_config_file')
        if (output.returncode):
            lines = output.stdout.text.split('\n')[1:-2]
            for line in lines:
                line = line[0:line.index('image')+6] + \
                                line[line.index('image')+9:]
                yield Result(origin=self,
                             message=line,
                             severity=RESULT_SEVERITY.MAJOR)
