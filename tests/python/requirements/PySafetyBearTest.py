from queue import Queue
from unittest import mock

from safety.safety import Vulnerability

from bears.python.requirements.PySafetyBear import (
    PySafetyBear,
    Package,
    cve_key_checker
)
from coalib.settings.Section import Section
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper


class PySafetyBearTest(LocalBearTestHelper):

    def setUp(self):
        self.uut = PySafetyBear(Section('name'), Queue())

    def test_cve_key_checker(self):
        # avoid pragma: no cover
        assert cve_key_checker(mock.Mock(data={'cve': None})) is None
        assert cve_key_checker(mock.Mock(data={'cve': True}))
        assert cve_key_checker(mock.Mock(data={})) is None

    def test_without_vulnerability(self):
        with mock.patch(
            'bears.python.requirements.PySafetyBear.safety.check',
            return_value=[],
        ) as check:
            self.check_validity(self.uut, ['# whee', 'foo==1.0', '# whee'])
            check.assert_called_once_with([Package('foo', '1.0')], key=None,
                                          db_mirror=self.uut.db_path,
                                          cached=False, ignore_ids=[])

    def test_with_vulnerability(self):
        with mock.patch(
            'bears.python.requirements.PySafetyBear.safety.check',
            return_value=[Vulnerability('bar', '<0.2', '0.1', 'foo', '123')],
        ) as check:
            self.check_invalidity(self.uut, ['foo<2', 'bar==0.1', '**bar'])
            check.assert_called_once_with([Package('bar', '0.1')], key=None,
                                          db_mirror=self.uut.db_path,
                                          cached=False, ignore_ids=[])

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
