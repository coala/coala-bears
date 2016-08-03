import sys
import unittest
from unittest.mock import patch

from bears.installation_tool import (
    create_installation_parser, get_all_bears_names_from_PyPI, get_output,
    install_pip_package, install_requirements)


class install_pip_packageTest(unittest.TestCase):

    @patch('subprocess.call')
    def test_install_pip_package(self, call_mock):
        install_pip_package('pip')
        call_mock.assert_called_with(['sudo', sys.executable, '-m',
                                      'pip', 'install', 'pip', '--upgrade'])


class create_installation_parserTest(unittest.TestCase):

    def test_parser(self):
        self.assertTrue(
            create_installation_parser().parse_args(['--install']).install)


class install_requirementsTest(unittest.TestCase):

    def test_requirements_succeeded(self):
        install_pip_package('PEP8Bear')
        self.assertEqual(install_requirements('PEP8Bear'), [])
