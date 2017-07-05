from coalib.testing.LocalBearTestHelper import verify_local_bear

from bears.js.JSStandardBear import JSStandardBear


good_file = """
var foo = {
  bar: 1,
  baz: 2
}
var { bar, baz } = foo
var x = 1
function hello (arg) { return arg }

if (baz === 2 && x !== 1) {
  window.alert('hi')
  bar = bar === 1
    ? bar
    : 1
  if ((x = 33)) {
    console.log(bar + "hello 'world'")
  }
} else {
  (function myFunction (err) {
    if (err) throw err
    console.log('nothing')
  })()
  if (hello(bar)) console.log('bar')
}
"""

bad_file_indent = """
(function () {
    console.log('hello world')
})()
"""

bad_file_quote = """
console.log("hello world")
"""

bad_file_semicolon = """
console.log('hello world');
"""

bad_file_infix = """
var a = 'world'
console.log('hello'+a)
"""

bad_file_undef = """
console.log(a)
"""

bad_file_ifelse = """
var a = 1
if (a) {
  console.log(a)
}
else {
  console.log(0)
}
"""

bad_file_func_name = """
function my_function (a) {
  return a
}
"""

JSStandardBearTest = verify_local_bear(JSStandardBear,
                                       valid_files=(good_file,),
                                       invalid_files=(bad_file_indent,
                                                      bad_file_quote,
                                                      bad_file_semicolon,
                                                      bad_file_infix,
                                                      bad_file_undef,
                                                      bad_file_ifelse,
                                                      bad_file_func_name,))
