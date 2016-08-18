import os
import shutil
import sys
import unittest
from unittest.mock import patch
from coalib.parsing.Globbing import glob
from bears.generate_package import (touch, create_file_from_template,
                                    create_file_structure_for_packages,
                                    perform_register, perform_upload, main,
                                    create_upload_parser, get_bear_glob,
                                    fetch_url)


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

    INIT_FILE_PATH = os.path.join('folder', 'Test', 'Test', '__init__.py')

    def test_structure(self):
        touch('TestFile.py')
        create_file_structure_for_packages('folder', 'TestFile.py',
                                           'Test', 'pypi')
        self.assertTrue(os.path.exists(self.INIT_FILE_PATH))

    def tearDown(self):
        shutil.rmtree('folder')
        os.remove('TestFile.py')


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


class get_bear_globTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        bear_path = os.path.join('tests', 'conda_package_testfiles',
                                 'test_conda_bear')
        shutil.copytree(os.path.join(bear_path, 'git'),
                        os.path.join(bear_path, '.git'))

    def test_single_bear(self):
        bear_path = os.path.join('tests', 'conda_package_testfiles',
                                 'test_conda_bear')
        result = get_bear_glob(bear_path)
        self.assertEqual(result, [os.path.join(bear_path, 'TestBear.py')])

    def test_all_bears(self):
        bear_path = os.path.join('tests', 'conda_package_testfiles',
                                 'test_conda_bear')
        result = get_bear_glob("")
        expected = sorted(set(glob('bears/**/*Bear.py')))
        self.assertEqual(result, expected)

    @classmethod
    def tearDownClass(cls):
        bear_path = os.path.join('tests', 'conda_package_testfiles',
                                 'test_conda_bear')
        shutil.rmtree(os.path.join(bear_path, '.git'))


class fetch_urlTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        bear_path = os.path.join('tests', 'conda_package_testfiles',
                                 'test_conda_bear')
        shutil.copytree(os.path.join(bear_path, 'git'),
                        os.path.join(bear_path, '.git'))

    def test_existing_url(self):
        result = fetch_url(os.path.join('tests', 'conda_package_testfiles',
                                        'test_conda_bear'))
        self.assertEqual(result, '../test_conda_bear_remote/')

    def test_non_existing_url(self):
        result = fetch_url(os.path.join('tests', 'conda_package_testfiles',
                                        'test_conda_beare'))
        self.assertEqual(result, None)

    @classmethod
    def tearDownClass(cls):
        bear_path = os.path.join('tests', 'conda_package_testfiles',
                                 'test_conda_bear')
        shutil.rmtree(os.path.join(bear_path, '.git'))


class mainTest(unittest.TestCase):

    CSS_BEAR_SETUP_PATH = os.path.join(
        'bears', 'upload', 'CSSLintBear', 'setup.py')
    NO_BEAR_PATH = os.path.join('bears', 'BadBear', 'NoBearHere.py')

    @classmethod
    def setUpClass(cls):
        bear_path = os.path.join('tests', 'conda_package_testfiles',
                                 'test_conda_bear')
        shutil.copytree(os.path.join(bear_path, 'git'),
                        os.path.join(bear_path, '.git'))

    def setUp(self):
        self.argv = ["generate_package.py"]
        argv_patcher = patch.object(sys, 'argv', self.argv)
        self.addCleanup(argv_patcher.stop)
        self.argv_mock = argv_patcher.start()

    def test_main(self):
        main()
        self.assertTrue(os.path.exists(os.path.join('bears', 'upload')))
        with open(self.CSS_BEAR_SETUP_PATH) as fl:
            setup_py = fl.read()
        self.assertIn("Check code for syntactical or semantical", setup_py)

    @patch('bears.generate_package.perform_upload')
    def test_upload(self, call_mock):
        self.argv.append("--upload")
        main()
        for call_object in call_mock.call_args_list:
            self.assertRegex(call_object[0][0], r".+Bear")

    @patch('bears.generate_package.perform_register')
    def test_register(self, call_mock):
        self.argv.append("--register")
        main()
        for call_object in call_mock.call_args_list:
            self.assertRegex(call_object[0][0], r".+Bear")

    def test_conda(self):
        package_path = os.path.join('tests', 'conda_package_testfiles',
                                    'test_conda_bear')
        template_path = os.path.join('bears', 'templates')
        sys.argv = ["generate_package.py", "--conda", package_path]
        main()
        self.assertTrue(os.path.exists(os.path.join(package_path, 'build.sh')))
        self.assertTrue(os.path.exists(os.path.join(package_path, 'bld.bat')))
        self.assertTrue(os.path.exists(
            os.path.join(package_path, 'meta.yaml')))
        self.assertTrue(os.path.exists(os.path.join(package_path, 'setup.py')))

    def test_no_bear_object(self):
        if not os.path.exists(self.NO_BEAR_PATH):
            os.makedirs(os.path.join('bears', 'BadBear'))
            touch(self.NO_BEAR_PATH)
        main()
        self.assertFalse(os.path.exists(os.path.join(
            'bears', 'upload', 'BadBear')))
        shutil.rmtree(os.path.join('bears', 'BadBear'))

    def tearDown(self):
        shutil.rmtree(os.path.join('bears', 'upload'))

    @classmethod
    def tearDownClass(cls):
        package_path = os.path.join('tests', 'conda_package_testfiles',
                                    'test_conda_bear')
        shutil.rmtree(os.path.join(package_path, '.git'))
        shutil.rmtree(os.path.join(package_path, 'TestBear'))
        os.remove(os.path.join(package_path, 'setup.py'))
        os.remove(os.path.join(package_path, 'build.sh'))
        os.remove(os.path.join(package_path, 'bld.bat'))
        os.remove(os.path.join(package_path, 'meta.yaml'))
