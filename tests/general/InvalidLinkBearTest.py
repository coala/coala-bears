from bears.general.InvalidLinkBear import InvalidLinkBear
from tests.LocalBearTestHelper import verify_local_bear

LinkRedirect = verify_local_bear(InvalidLinkBear,
                                 valid_files=(
                                    ["http://httpbin.org/status/200"],),
                                 invalid_files=(
                                    ["http://httpbin.org/status/301"],
                                    ["http://coala.rtfd.org"]),
                                 force_linebreaks=False)

InvalidLinkNotFound = verify_local_bear(InvalidLinkBear,
                                        valid_files=(
                                            ["http://httpbin.org/status/202"],),
                                        invalid_files=(
                                            ["http://httpbin.org/status/404"],
                                            ["http://httpbin.org/status/401"]),
                                        force_linebreaks=False)

InvalidLinkServerError = verify_local_bear(InvalidLinkBear,
                                           valid_files=(
                                            ["http://httpbin.org/status/202"],),
                                           invalid_files=(
                                            ["http://httpbin.org/status/500"],
                                            ["http://httpbin.org/status/503"]),
                                           force_linebreaks=False)

LinkDoesNotExist = verify_local_bear(InvalidLinkBear,
                                     valid_files=(
                                        ["http://coala-analyzer.org/\n"],
                                        ["http://coala-analyzer.org/"],
                                        ["http://not a link dot com"],
                                        ["<http://lwn.net/>"],
                                        ["'https://www.gnome.org/'"],
                                        ["http://coala-analyzer.org/..."]),
                                     invalid_files=(
                                        ["http://coalaisthebest.com"],),
                                     force_linebreaks=False)

MarkdownLinks = verify_local_bear(InvalidLinkBear,
                                  valid_files=(
                                        ["[coala](http://coala-analyzer.org/)"],
                                        ["https://en.wikipedia.org/wiki/"
                                         "Hello_(Adele_song)"]),
                                  invalid_files=(),
                                  force_linebreaks=False)

SphinxLinks = verify_local_bear(InvalidLinkBear,
                                valid_files=(
                                    ["|https://github.com/coala-analyzer/"
                                     "coala-bears|"],),
                                invalid_files=(),
                                force_linebreaks=False)
