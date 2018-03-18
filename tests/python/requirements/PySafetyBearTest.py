from queue import Queue
from unittest import mock
import unittest

from safety.safety import Vulnerability

from bears.python.requirements.PySafetyBear import (
    PySafetyBear,
    Package,
    cve_key_checker
)
from coalib.settings.Section import Section
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper

Vuln1 = Vulnerability(name='bottle', spec='<0.12.10',
                      version='0.10.1',
                      data={'cve': 'CVE-2016-9964',
                            'id': 'pyup.io-25642',
                            'advisory': 'redirect() in '
                            'bottle.py in '
                            'bottle 0.12.10 doesn\'t filter '
                            'a "\\r\\n" sequence, which leads '
                            'to a CRLF attack, as demonstrated '
                            'by a redirect("233\\r\\nSet-Cookie: name=salt") '
                            'call.',
                            'v': '<0.12.10',
                            'specs': ['<0.12.10']})

Vuln2 = Vulnerability(name='locustio', spec='<0.7',
                      version='0.5.1',
                      data={'cve': None, 'id': 'pyup.io-25878',
                            'advisory': 'locustio before 0.7 uses pickle.',
                            'v': '<0.7',
                            'specs': ['<0.7']})

Vuln3 = Vulnerability(name='locustio', spec='<0.7',
                      version='0.5.1',
                      data={'id': 'pyup.io-25878',
                            'advisory': 'locustio before 0.7 uses pickle.',
                            'v': '<0.7',
                            'specs': ['<0.7']})


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
            'advisory': 'foo',
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
            'advisory': 'foo',
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


class cveKeyCheckerFunctionTest(unittest.TestCase):
    def test_cve_key_with_value(self):
        myresult = cve_key_checker(Vuln1)
        self.assertEqual(myresult, True)

    def test_cve_key_without_value(self):
        myresult = cve_key_checker(Vuln2)
        self.assertEqual(myresult, None)

    def test_without_cve_key(self):
        myresult = cve_key_checker(Vuln3)
        self.assertEqual(myresult, None)
