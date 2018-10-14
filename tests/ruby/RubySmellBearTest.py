from bears.ruby.RubySmellBear import RubySmellBear
from coalib.testing.LocalBearTestHelper import verify_local_bear


good_file = """# Does something
class Something;
end
"""

bad_file1 = 'class Something; end'

bad_file2 = """class Dirty
  # This method smells of :reek:NestedIterators but ignores them
  def awful(x, y, offset = 0, log = false)
    puts @screen.title
    @screen = widgets.map { |w| w.each { |key| key += 3 * x } }
    puts @screen.contents
  end
end
"""

RubySmellBearTest = verify_local_bear(RubySmellBear,
                                      valid_files=(good_file, ''),
                                      invalid_files=(bad_file1, bad_file2))

RubySmellBearConfigTest = verify_local_bear(
    RubySmellBear, valid_files=(good_file, bad_file1), invalid_files=(),
    settings={'missing_module_description': 'nope'})
