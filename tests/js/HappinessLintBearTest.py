from bears.js.HappinessLintBear import HappinessLintBear
from tests.LocalBearTestHelper import verify_local_bear


good_file = """
var x = 2;
console.log(x);
var message = 'hello, ' + 'world' + '!';
console.log(message);
var list = [1, 2, 3, 4];
console.log(list);
if (6 > 7 !== true) console.log('done');
window.alert('hi');
""".splitlines(keepends=True)

bad_file = """
function hello (name) {
 console.log('hi', name)
}
if (options.quiet !== true)
  console.log('done')
var x=2
var message = 'hello, '+name+'!'
""".splitlines(keepends=True)

HappinessLintBear = verify_local_bear(HappinessLintBear,
                                      valid_files=(good_file,),
                                      invalid_files=(bad_file,))
