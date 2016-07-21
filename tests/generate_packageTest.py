import os
import shutil
import sys
import unittest
from unittest.mock import patch
from bears.generate_package import (touch, create_file_from_template,
                                    create_file_structure_for_packages,
                                    perform_register, perform_upload, main,
                                    create_upload_parser)


class touchTest(unittest.TestCase):

    def setUp(self):
        if os.path.exists('TestFile.py'):
            os.remove('TestFile.py')

    def test_file_doesnt_exist(self):
        self.assertFalse(os.path.exists('TestFile.py'))
        touch('TestFile.py')
        self.assertTrue(os.path.exists('TestFile.py'))

    def tearDown(self):
        os.remove('TestFile.py')


class create_file_from_templateTest(unittest.TestCase):

    SUBST_FILE = os.path.join(
        'tests', 'generate_package_input_files', 'substituted_file.py')
    TEMPL_FILE = os.path.join(
        'tests', 'generate_package_input_files', 'template_file.py.in')

    def test_output_file(self):
        data = {'who': 'George', 'sport': 'swimming'}
        create_file_from_template(self.TEMPL_FILE, self.SUBST_FILE, data)
        with open(self.SUBST_FILE) as fl:
            substituted_file = fl.read()
        self.assertEqual(substituted_file, 'George has gone swimming again.\n')

    def tearDown(self):
        os.remove(self.SUBST_FILE)


class create_file_structure_for_packagesTest(unittest.TestCase):

    TEST_FILE_PATH = os.path.join('folder', 'Test', 'Test', 'Test.py')
    INIT_FILE_PATH = os.path.join('folder', 'Test', 'Test', '__init__.py')

    def test_structure(self):
        touch('TestFile.py')
        create_file_structure_for_packages('folder', 'TestFile.py', 'Test')
        self.assertTrue(os.path.exists(self.TEST_FILE_PATH))
        self.assertTrue(os.path.exists(self.INIT_FILE_PATH))

    def tearDown(self):
        shutil.rmtree('folder')


class create_upload_parserTest(unittest.TestCase):

    def test_parser(self):
        self.assertTrue(create_upload_parser().parse_args(['--upload']).upload)


class perform_registerTest(unittest.TestCase):

    @patch('subprocess.call')
    def test_command(self, call_mock):
        perform_register('.', 'MarkdownBear-0.8.0.dev20160623094115')
        call_mock.assert_called_with(
            ['twine', 'register', '-r', 'pypi', os.path.join(
                '.', 'dist',
                'MarkdownBear-0.8.0.dev20160623094115-py3-none-any.whl')])


class perform_uploadTest(unittest.TestCase):

    @patch('subprocess.call')
    def test_command(self, call_mock):
        perform_upload('.')
        call_mock.assert_called_with(['twine', 'upload', './dist/*'])


class mainTest(unittest.TestCase):

    CSS_BEAR_SETUP_PATH = os.path.join(
        'bears', 'upload', 'CSSLintBear', 'setup.py')
    NO_BEAR_PATH = os.path.join('bears', 'BadBear', 'NoBearHere.py')

    def setUp(self):
        self.old_argv = sys.argv

    def test_main(self):
        sys.argv = ["generate_package.py"]
        main()
        self.assertTrue(os.path.exists(os.path.join('bears', 'upload')))
        with open(self.CSS_BEAR_SETUP_PATH) as fl:
            setup_py = fl.read()
        self.assertIn("Check code for syntactical or semantical", setup_py)

    @patch('bears.generate_package.perform_upload')
    def test_upload(self, call_mock):
        sys.argv = ["generate_package.py", "--upload"]
        main()
        for call_object in call_mock.call_args_list:
            self.assertRegex(call_object[0][0], r".+Bear")

    @patch('bears.generate_package.perform_register')
    def test_register(self, call_mock):
        sys.argv = ["generate_package.py", "--register"]
        main()
        for call_object in call_mock.call_args_list:
            self.assertRegex(call_object[0][0], r".+Bear")

    def test_no_bear_object(self):
        if not os.path.exists(self.NO_BEAR_PATH):
            os.makedirs(os.path.join('bears', 'BadBear'))
            touch(self.NO_BEAR_PATH)
        sys.argv = ["generate_package.py"]
        main()
        self.assertFalse(os.path.exists(os.path.join(
            'bears', 'upload', 'BadBear')))
        shutil.rmtree(os.path.join('bears', 'BadBear'))

    def tearDown(self):
        shutil.rmtree(os.path.join('bears', 'upload'))
        sys.argv = self.old_argv
