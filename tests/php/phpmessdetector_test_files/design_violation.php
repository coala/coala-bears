<?
class Foo {
    public function bar($param)  {
        if ($param === 42) {
            exit(23);
        }
    }
}
class Bar {
    public function foo($param)  {
        if ($param === 42) {
            eval('$param = 23;');
        }
    }
}
?>
