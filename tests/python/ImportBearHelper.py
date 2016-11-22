import collections
import queue
import unittest
from contextlib import contextmanager

import pytest

from tests.BearTestHelper import generate_skip_decorator
from coalib.bears.LocalBear import LocalBear
from coalib.misc.ContextManagers import prepare_file
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


@contextmanager
def execute_bear(bear, *args, **kwargs):
    try:
        bear_output_generator = bear.execute(*args, **kwargs)
        assert bear_output_generator is not None, \
            "Bear returned None on execution\n"
        yield bear_output_generator
    except Exception as err:
        msg = []
        while not bear.message_queue.empty():
            msg.append(bear.message_queue.get().message)
        raise AssertionError(str(err) + " \n" + "\n".join(msg))
    return list(bear_output_generator)


class ImportBearHelper(unittest.TestCase):  # pragma: no cover
    """
    This is a helper class for simplification of testing of local bears.

    Please note that all abstraction will prepare the lines so you don't need
    to do that if you use them.

    If you miss some methods, get in contact with us, we'll be happy to help!
    """

    def check_results(self,
                      local_bear,
                      lines,
                      results,
                      filename=None,
                      check_order=False,
                      force_linebreaks=True,
                      create_tempfile=True,
                      tempfile_kwargs={}):
        """
        Asserts that a check of the given lines with the given local bear does
        yield exactly the given results.

        :param local_bear:       The local bear to check with.
        :param lines:            The lines to check. (List of strings)
        :param results:          The expected list of results.
        :param filename:         The filename, if it matters.
        :param force_linebreaks: Whether to append newlines at each line
                                 if needed. (Bears expect a \\n for every line)
        :param create_tempfile:  Whether to save lines in tempfile if needed.
        :param tempfile_kwargs:  Kwargs passed to tempfile.mkstemp().
        """
        assert isinstance(self, unittest.TestCase)
        self.assertIsInstance(local_bear,
                              LocalBear,
                              msg="The given bear is not a local bear.")
        self.assertIsInstance(lines,
                              (list, tuple),
                              msg="The given lines are not a list.")
        self.assertIsInstance(results,
                              list,
                              msg="The given results are not a list.")

        with prepare_file(lines, filename,
                          force_linebreaks=force_linebreaks,
                          create_tempfile=create_tempfile,
                          tempfile_kwargs=tempfile_kwargs) as (file, fname), \
                execute_bear(local_bear, fname, file) as bear_output:
            msg = ("The local bear '{}' doesn't yield the right results. Or "
                   "the order may be wrong."
                   .format(local_bear.__class__.__name__))
            if not check_order:
                self.assertEqual(bear_output[0].message, results[0], msg=msg)
            else:
                self.assertEqual(bear_output[0].message, results[0], msg=msg)
