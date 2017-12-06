from bears.php.PHPCodeSnifferBear import PHPCodeSnifferBear
from coalib.testing.LocalBearTestHelper import verify_local_bear


good_file = """<?php
/**
 * PHP_CodeSniffer tokenizes PHP code and detects violations of a
 * defined set of coding standards.
 *
 * PHP version 5
 *
 * @category PHP
 * @package  Your_Package
 * @author   John Snow <johnsnow@link.net>
 * @license  https://licence.txt LICENSE
 * @link     http://somelink
 */
$var = false;
$var = true;
>
"""


bad_file = """<?php
/**
 * PHP_CodeSniffer tokenizes PHP code and detects violations of a
 * defined set of coding standards.
 *
 * PHP version 5
 *
 * @category PHP
 * @package  Your_Package
 * @author   John Snow <johnsnow@link.net>
 * @license  https://licence.txt LICENSE
 * @link     http://somelink
 */
$var = TRUE;
$var = FALSE;
"""

long_length_test_file = """<?php
/**
 * PHP_CodeSniffer tokenizes PHP code and detects violations of a defined set \
of coding.This is to test that the absoluteLineLength is violated or not.

 * PHP version 5
 *
 * @category PHP
 * @package  Your_Package
 * @author   John Snow <johnsnow@link.net>
 * @license  https://licence.txt LICENSE
 * @link     http://somelink
 */
>
"""


PHPCodeSnifferBearTest = verify_local_bear(
    PHPCodeSnifferBear,
    valid_files=(good_file,),
    invalid_files=(bad_file,),
    tempfile_kwargs={'suffix': '.php'})


PHPCodeSnifferBearLineLengthTest = verify_local_bear(
    PHPCodeSnifferBear,
    valid_files=(long_length_test_file,),
    invalid_files=(),
    settings={'max_line_length': '160'},
    tempfile_kwargs={'suffix': '.php'})
