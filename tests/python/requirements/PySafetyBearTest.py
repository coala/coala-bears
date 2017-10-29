from queue import Queue
from unittest import mock

from safety.safety import Vulnerability

from bears.python.requirements.PySafetyBear import PySafetyBear, Package
from coalib.settings.Section import Section
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper


class PySafetyBearTest(LocalBearTestHelper):

    def setUp(self):
        self.uut = PySafetyBear(Section('name'), Queue())

    def test_without_vulnerability(self):
        with mock.patch(
            'bears.python.requirements.PySafetyBear.safety.check',
            return_value=[],
        ) as check:
            self.check_validity(self.uut, ['# whee', 'foo==1.0', '# whee'])
            check.assert_called_once_with(packages=[Package('foo', '1.0')])

    def test_with_vulnerability(self):
        vuln_data = {
            'description': 'foo',
            'changelog': 'bar',
        }
        with mock.patch(
            'bears.python.requirements.PySafetyBear.safety.check',
            return_value=[Vulnerability('bar', '<0.2', '0.1', vuln_data)],
        ) as check:
            self.check_invalidity(self.uut, ['foo<2', 'bar==0.1'])
            check.assert_called_once_with(packages=[Package('bar', '0.1')])

    def test_with_cve_vulnerability(self):
        vuln_data = {
            'description': 'foo',
            'cve': 'CVE-2016-9999',
        }
        with mock.patch(
            'bears.python.requirements.PySafetyBear.safety.check',
            return_value=[Vulnerability('baz', '<2.0', '1.10', vuln_data)],
        ) as check:
            self.check_invalidity(self.uut, ['baz==1.10', '-e .'])
            check.assert_called_once_with(packages=[Package('baz', '1.10')])

    def test_with_no_requirements(self):
        with mock.patch(
            'bears.python.requirements.PySafetyBear.safety.check',
            return_value=[],
        ) as check:
            self.check_validity(self.uut, [])
            assert not check.called

    def test_with_no_pinned_requirements(self):
        with mock.patch(
            'bears.python.requirements.PySafetyBear.safety.check',
            return_value=[],
        ) as check:
            self.check_validity(self.uut, ['foo', 'bar>2'])
            assert not check.called

    def test_with_no_description(self):
        vuln_data = {
            'cve': 'CVE-2016-9999',
        }
        with mock.patch(
            'bears.python.requirements.PySafetyBear.safety.check',
            return_value=[Vulnerability(
                'baz', '<0.12.10', '0.10.0', vuln_data)],
        ) as check:
            self.check_invalidity(self.uut, ['baz==0.10.0', '-e .'])
            check.assert_called_once_with(packages=[Package(
                'baz', '0.10.0')])
