from coalib.testing.LocalBearTestHelper import verify_local_bear
from bears.php.PhanBear import PhanBear

bad_file_closure = '''<?php
$closure = function() {
    return 42;
};
class A {
    private $a = 42;
    public function f() {
        $b = 2;
        $closure = function(int $p) use (&$b, $c) {
            return ($p + $this->a + $b);
        };
        return $closure(3);
    }
}
'''

PhanBearTest = verify_local_bear(
    PhanBear,
    valid_files=(),
    invalid_files=(bad_file_closure,))
