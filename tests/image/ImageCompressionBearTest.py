import os
import unittest

from bears.image.ImageCompressionBear import ImageCompressionBear
from coalib.settings.Section import Section
from coalib.testing.BearTestHelper import generate_skip_decorator
from queue import Queue


def get_absolute_path(filename):
    return os.path.join(os.path.dirname(__file__),
                        'test_files',
                        filename)


@generate_skip_decorator(ImageCompressionBear)
class ImageCompressionBearTest(unittest.TestCase):
    """
    Tests for ImageCompressionBear
    """

    MESSAGE_RE = ('This Image can be losslessly compressed to .* bytes '
                  '\(savings: .* .*%\)')

    def setUp(self):
        self.section = Section('')
        self.queue = Queue()
        self.icb = ImageCompressionBear(self.section, self.queue)

    def _run_and_get_results(self, filename):
        return list(self.icb.run(get_absolute_path(filename), None))

    def _test_known_invalid(self, filename):
        results = self._run_and_get_results(filename)
        self.assertNotEqual([], results)
        self.assertRegex(results[0].message, self.MESSAGE_RE)

    def _test_known_valid(self, filename):
        results = self._run_and_get_results(filename)
        self.assertEqual([], results)

    def test_clean_jpeg(self):
        self._test_known_valid('gradient_clean.jpg')

    def test_clean_png(self):
        self._test_known_valid('gradient_clean.png')

    def test_bloat_jpeg(self):
        self._test_known_invalid('gradient_bloat.jpg')

    def test_bloat_png(self):
        self._test_known_invalid('gradient_bloat.png')

    def test_bloat_and_metadata_jpeg(self):
        self._test_known_invalid('gradient_bloat_and_metadata.jpg')

    def test_bloat_and_metadata_png(self):
        self._test_known_invalid('gradient_bloat_and_metadata.png')

    def test_metadata_jpeg(self):
        self._test_known_invalid('gradient_metadata.jpg')

    def test_metadata_png(self):
        self._test_known_invalid('gradient_metadata.png')
