import os
import shutil
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from bears.generate_package import (VERSION, create_file_from_template,
                                    create_file_structure_for_packages,
                                    perform_register, perform_upload, main,
                                    create_upload_parser)


class TouchTest(unittest.TestCase):

    def setUp(self):
        if os.path.exists('TestFile.py'):
            os.remove('TestFile.py')

    def test_file_doesnt_exist(self):
        self.assertFalse(os.path.exists('TestFile.py'))
        Path('TestFile.py').touch()
        self.assertTrue(os.path.exists('TestFile.py'))

    def tearDown(self):
        os.remove('TestFile.py')


class CreateFileFromTemplateTest(unittest.TestCase):

    BASE_TEST_PATH = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        'generate_package_input_files'))

    SUBST_FILE = os.path.join(
        BASE_TEST_PATH, 'substituted_file.py')
    TEMPL_FILE = os.path.join(
        BASE_TEST_PATH, 'template_file.py.in')

    def test_output_file(self):
        data = {'who': 'George', 'sport': 'swimming'}
        create_file_from_template(self.TEMPL_FILE, self.SUBST_FILE, data)
        with open(self.SUBST_FILE) as fl:
            substituted_file = fl.read()
        self.assertEqual(substituted_file, 'George has gone swimming again.\n')

    def tearDown(self):
        os.remove(self.SUBST_FILE)


class CreateFileStructureForPackagesTest(unittest.TestCase):

    INIT_FILE_PATH = os.path.join('folder', 'Test', 'coalaTest', '__init__.py')
    BEAR_FILE_PATH = os.path.join('folder', 'Test', 'coalaTest', 'Test.py')

    def test_structure(self):
        Path('TestFile.py').touch()
        create_file_structure_for_packages('folder', 'TestFile.py', 'Test')
        self.assertTrue(os.path.exists(self.INIT_FILE_PATH))
        self.assertTrue(os.path.exists(self.BEAR_FILE_PATH))

    def tearDown(self):
        shutil.rmtree('folder')
        os.remove('TestFile.py')


class CreateUploadParserTest(unittest.TestCase):

    def test_parser(self):
        self.assertTrue(create_upload_parser().parse_args(['--upload']).upload)


class PerformRegisterTest(unittest.TestCase):

    @patch('subprocess.call')
    def test_command(self, call_mock):
        perform_register('.', 'MarkdownBear-0.8.0.dev20160623094115')
        call_mock.assert_called_with(
            ['twine', 'register', '-r', 'pypi', os.path.join(
                '.', 'dist',
                'MarkdownBear-0.8.0.dev20160623094115-py3-none-any.whl')])


class PerformUploadTest(unittest.TestCase):

    @patch('subprocess.call')
    def test_command(self, call_mock):
        perform_upload('.')
        call_mock.assert_called_with(['twine', 'upload', './dist/*'])


class MainTest(unittest.TestCase):

    BEARS_PATH = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '..', 'bears'))
    BEARS_UPLOAD_PATH = os.path.join(BEARS_PATH, 'upload')
    CSS_BEAR_SETUP_PATH = os.path.join(
        BEARS_UPLOAD_PATH, 'CSSLintBear', 'setup.py')
    NO_BEAR_PATH = os.path.join(BEARS_PATH,
                                'BadBear', 'InvalidBear.py')

    def setUp(self):
        self.orig_dir = os.getcwd()

        self.argv = ['generate_package.py']
        argv_patcher = patch.object(sys, 'argv', self.argv)
        self.addCleanup(argv_patcher.stop)
        self.argv_mock = argv_patcher.start()

    def test_main(self):
        main()
        self.assertTrue(os.path.exists(self.BEARS_UPLOAD_PATH))
        with open(self.CSS_BEAR_SETUP_PATH) as fl:
            setup_py = fl.read()
        self.assertIn('Check code for syntactical or semantical', setup_py)

    def test_main_bear_version_prod(self):
        fake_prod_version = '99.99.99'
        with patch('bears.generate_package.VERSION', fake_prod_version):
            main()
        with open(self.CSS_BEAR_SETUP_PATH) as fl:
            setup_py = fl.read()
        self.assertIn(fake_prod_version, setup_py)
        self.assertNotIn(VERSION, setup_py)

    def test_main_bear_version_dev(self):
        fake_dev_version = '13.37.0.dev133713371337'
        with patch('bears.generate_package.VERSION', fake_dev_version):
            main()
        with open(self.CSS_BEAR_SETUP_PATH) as fl:
            setup_py = fl.read()
        self.assertNotIn(fake_dev_version, setup_py)
        self.assertIn('13.37.0', setup_py)

    @patch('bears.generate_package.perform_upload')
    def test_upload(self, call_mock):
        self.argv.append('--upload')
        main()
        for call_object in call_mock.call_args_list:
            self.assertRegex(call_object[0][0], r'.+Bear')

    @patch('bears.generate_package.perform_register')
    def test_register(self, call_mock):
        self.argv.append('--register')
        main()
        for call_object in call_mock.call_args_list:
            self.assertRegex(call_object[0][0], r'.+Bear')

    def test_no_bear_object(self):
        if not os.path.exists(self.NO_BEAR_PATH):
            os.makedirs(os.path.join(self.BEARS_PATH, 'BadBear'))
            Path(self.NO_BEAR_PATH).touch()
        main()
        self.assertFalse(os.path.exists(os.path.join(
            self.BEARS_UPLOAD_PATH, 'BadBear')))
        shutil.rmtree(os.path.join(self.BEARS_PATH, 'BadBear'))

    def tearDown(self):
        shutil.rmtree(os.path.join(self.BEARS_UPLOAD_PATH))

        os.chdir(self.orig_dir)
