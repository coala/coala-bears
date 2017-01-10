import unittest
from queue import Queue
import shutil

from bears.general.ImageDimensionBear import *
from coalib.settings.Section import Section
from coalib.testing.BearTestHelper import generate_skip_decorator


@generate_skip_decorator(ImageDimensionBear)
class ImageDimensionBearTest(unittest.TestCase):
    """
    Runs unittests for ImageDimensionBear
    """

    def setUp(self):
        self.section = Section('')
        self.queue = Queue()
        self.file_dict = {}
        self.idb = ImageDimensionBear(None, self.section, self.queue)

    def test_check_width(self):
        with self.assertRaisesRegexp(ValueError, 'Width'):
            check_width('-12')
        self.assertEqual(check_width('120'), 120)

    def test_check_height(self):
        with self.assertRaisesRegexp(ValueError, 'Height'):
            check_height('-12')
        self.assertEqual(check_height('120'), 120)

    def test_check_path(self):
        with self.assertRaisesRegexp(ValueError, 'Provide'):
            check_path('test-image/')
        self.assertEqual(check_path('test-img/'), '../test-img/')

    def test_check_prerequisites(self):
        _shutil_which = shutil.which
        try:
            shutil.which = lambda *args, **kwargs: None
            self.assertEqual(ImageDimensionBear.check_prerequisites(),
                             'img_checker is not installed.')

            shutil.which = lambda *args, **kwargs: 'path/to/bundle'
            self.assertTrue(ImageDimensionBear.check_prerequisites())
        finally:
            shutil.which = _shutil_which

    def test_run_with_png(self):
        path = os.path.join('..', 'test-img', '*.png')
        message = ('The image test-img/img.png is larger'
                   ' than 240px x 240px [w x h]')
        result = next(self.idb.run(
                       image_file=path,
                       width=240,
                       height=240))
        self.assertEqual(message,
                         result.message)

    def test_run_with_jpg(self):
        path = os.path.join('..', 'test-img', '*.jpg')
        self.assertEqual([],
                         list(self.idb.run(
                               image_file=path,
                               width=240,
                               height=240)))

    def test_run_with_jpg_fail(self):
        path = os.path.join('..', 'test-img', '*.jpg')
        message = ('The image test-img/images.jpg is larger'
                   ' than 50px x 50px [w x h]')
        result = next(self.idb.run(
                       image_file=path,
                       width=50,
                       height=50))
        self.assertEqual(message,
                         result.message)

    def test_run_with_both(self):
        path = os.path.join('..', 'test-img', '*.*')
        message = ('\w* \w+-\w+\/\w+\.\w+ is larger'
                   ' than 50px x 50px \[w x h]')
        output = str(list(self.idb.run(
                       image_file=path,
                       width=50,
                       height=50)))
        self.assertRegex(output,
                         message)
