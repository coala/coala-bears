import logging
import unittest

import bears
import coalib


class coalaBearTest(unittest.TestCase):

    def test_check_coala_version(self):
        bears.__version__ = coalib.__version__ = '1.0.0.dev999999999'
        logger = logging.getLogger()
        with self.assertLogs(logger, 'WARNING') as cm:
            bears.check_coala_version()
            self.assertEqual(0, len(cm.output))

            bears.__version__ = '1.1.0.dev999999999'
            bears.check_coala_version()
            self.assertEqual(0, len(cm.output))

            bears.__version__ = '1.0.0.dev999999999'
            coalib.__version__ = '1.1.0.dev999999999'
            bears.check_coala_version()
            self.assertIn('Version mismatch between coala',
                          cm.output[0])
