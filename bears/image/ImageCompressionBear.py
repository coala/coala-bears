import os
import optimage

from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import Result
from dependency_management.requirements.AnyOneOfRequirements import (
    AnyOneOfRequirements)
from dependency_management.requirements.DistributionRequirement import (
    DistributionRequirement)
from dependency_management.requirements.ExecutableRequirement import (
    ExecutableRequirement)
from dependency_management.requirements.PipRequirement import PipRequirement
from coala_utils.FileUtils import create_tempfile


class ImageCompressionBear(LocalBear):
    """
    Checks for possible optimizations for JPEGs and PNGs

    See https://github.com/sk-/optimage
    """
    LANGUAGES = {'Image'}
    REQUIREMENTS = {
        PipRequirement('optimage', '0.0.1'),
        AnyOneOfRequirements([
            DistributionRequirement(apt_get='jpegoptim',
                                    portage='jpegoptim',
                                    xbps='jpegoptim'),
            ExecutableRequirement('jpegoptim')
        ]),
        AnyOneOfRequirements([
            DistributionRequirement(apt_get='libjpeg-progs',
                                    portage='libjpeg-turbo',
                                    xbps='libjpeg-turbo-tools'),
            ExecutableRequirement('jpegtran')
        ]),
        AnyOneOfRequirements([
            DistributionRequirement(apt_get='pngcrush',
                                    portage='pngcrush',
                                    xbps='pngcrush'),
            ExecutableRequirement('pngcrush')
        ]),
        AnyOneOfRequirements([
            DistributionRequirement(apt_get='optipng',
                                    portage='pngcrush',
                                    xbps='pngcrush'),
            ExecutableRequirement('optipng')
        ]),
        AnyOneOfRequirements([
            DistributionRequirement(apt_get='zopfli',
                                    portage='zopfli',
                                    xbps='zopfli'),
            ExecutableRequirement('zopflipng')
        ])
    }
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'The coala developers'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Compression', 'Bloat'}
    USE_RAW_FILES = True

    def run(self, filename, file):
        """
        Check for how much the image file size can be optimized

        :param image_files: The image files that this bear will use
        """

        _, extension = os.path.splitext(filename)
        extension = extension.lower()
        compressor = optimage._EXTENSION_MAPPING.get(extension)

        if compressor is None:
            raise '{} extension is unsupported'.format(extension)

        output_filename = create_tempfile(suffix=extension)

        compressor(filename, output_filename)

        original_size = os.path.getsize(filename)
        new_size = os.path.getsize(output_filename)
        reduction = original_size - new_size
        reduction_percentage = reduction * 100 / original_size
        savings = 'savings: {} bytes = {:.2f}%'.format(
            reduction, reduction_percentage)

        if new_size < original_size:
            yield Result.from_values(origin=self,
                                     message=('This Image can be '
                                              'losslessly compressed '
                                              'to {} bytes ({})'
                                              .format(new_size,
                                                      savings)),
                                     file=filename)

        os.remove(output_filename)
