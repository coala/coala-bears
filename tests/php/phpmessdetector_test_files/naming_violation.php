<?
class Something {
    private $q = 15; // VIOLATION - Field
    public static function main( array $as ) { // VIOLATION - Formal
        $r = 20 + $this->q; // VIOLATION - Local
        for (int $i = 0; $i < 10; $i++) { // Not a Violation (inside FOR)
            $r += $this->q;
        }
    }
}
?>
