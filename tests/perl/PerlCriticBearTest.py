import os

from bears.perl.PerlCriticBear import PerlCriticBear
from coalib.testing.LocalBearTestHelper import verify_local_bear


good_file = """
#!/usr/bin/perl

# $Id$
# $Revision$
# $Date$

use strict;
use warnings;
use vars qw/ $VERSION /;

$VERSION = '1.00';

exit 1 if !print "Hello, world!\n";
"""


bad_file = """
#!/usr/bin/perl

print "Hello World\n";
"""


conf_file = os.path.abspath(os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'testfiles', '.perlcriticrc'))

PerlCriticBearTest = verify_local_bear(PerlCriticBear,
                                       valid_files=(good_file,),
                                       invalid_files=(bad_file,))

PerlCriticBearConfigTest = verify_local_bear(
    PerlCriticBear,
    valid_files=(good_file, bad_file),
    invalid_files=(),
    settings={'perlcritic_profile': conf_file})
