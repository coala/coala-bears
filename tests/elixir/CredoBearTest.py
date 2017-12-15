import unittest

from queue import Queue

from bears.elixir.CredoBear import CredoBear
from coalib.testing.BearTestHelper import generate_skip_decorator
from coalib.settings.Section import Section
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.processes.BearRunning import run

bad_file_consistency = """
defmodule Consistency do
@moduledoc false
def myfun( p1 , p2 ) when is_list(p2) do
if p1 == p2 do
p1
else
p2 + p1
end
end
end
"""

bad_file_readability = """
defmodule Readability do end
"""

bad_file_design = """
defmodule Design do
@moduledoc false
alias Exzmq.{Socket, Tcp}
def just_an_example do
Socket.test1
Exzmq.Socket.test2
end
end
"""

bad_file_refactoring = """
defmodule Refactoring do
@moduledoc false
def some_fun do
cond do
false -> 0
true -> 1
end
end
end
"""

bad_file_warning = """
defmodule Warning do
@moduledoc false
def some_function(parameter1, parameter2) do
IO.inspect parameter1 + parameter2
end
end
"""


@generate_skip_decorator(CredoBear)
class CredoBearTest(unittest.TestCase):

def setUp(self):
self.section = Section('name')
self.queue = Queue()
self.uut = CredoBear(self.section, self.queue)

def test_readability(self):
suggestion = self.uut.run(bad_file_readability)
suggestion = next(suggestion)
self.assertEqual(suggestion.severity, RESULT_SEVERITY.NORMAL)
self.assertEqual(suggestion.message, 'Found readability issue.')

def test_consistency(self):
suggestion = self.uut.run(bad_file_consistency)
suggestion = next(suggestion)
self.assertEqual(suggestion.severity, RESULT_SEVERITY.MAJOR)
self.assertEqual(suggestion.message, 'Found consistency issue.')

def test_refactoring(self):
suggestion = self.uut.run(bad_file_refactoring)
suggestion = next(suggestion)
self.assertEqual(suggestion.severity, RESULT_SEVERITY.INFO)
self.assertEqual(suggestion.message, 'Found refactoring opportunity.')

def test_warning(self):
suggestion = self.uut.run(bad_file_warning)
suggestion = next(suggestion)
self.assertEqual(suggestion.severity, RESULT_SEVERITY.MAJOR)
self.assertEqual(suggestion.message,
                 'Found a warning please take a closer look.')

def test_design(self):
suggestion = self.uut.run(bad_file_design)
suggestion = next(suggestion)
self.assertEqual(suggestion.severity, RESULT_SEVERITY.INFO)
self.assertEqual(suggestion.message,
                 'Found software design issue.')

def tearDown(self):
pass
