import os
import sys

# Allow import to fail to avoid annoying developers
try:
    from pytest_reqs import check_requirements
except ImportError:
    check_requirements = None


if check_requirements:
    def pytest_collection_modifyitems(config, session, items):
        check_requirements(config, session, items)

_tests_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(_tests_dir, '..', '.ci'))
