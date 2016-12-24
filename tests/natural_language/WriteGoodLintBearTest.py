from bears.natural_language.WriteGoodLintBear import WriteGoodLintBear
from coalib.testing.LocalBearTestHelper import verify_local_bear

good_file = """The 70s era was awesome for music lovers.
"""

bad_file = """So the 70s era was awesome for music lovers.
"""

passive_file = """This analysis was provided by coala-bears.
"""

wordy_file = """It was a project which was very complex in structure and very
ambitious in nature."""

thereIs_file = """There are so many tools to check this, no right?
"""

cliche_file = 'A fine kettle of fish.'

adverb_file = 'It really is an extremely hot day.'

so_file = """So it was a bad day, wasn't it?"""

illusion_file = """Many readers are not aware that the the second the is
ignored."""

weasel_file = """Some people say that weasel words are great.
"""

WriteGoodLintBearTest = verify_local_bear(WriteGoodLintBear,
                                          valid_files=(good_file,),
                                          invalid_files=(bad_file,))

WriteGoodLintBearWithPassiveTest = verify_local_bear(WriteGoodLintBear,
                                                     valid_files=(good_file,
                                                                  weasel_file,
                                                                  bad_file,
                                                                  wordy_file,
                                                                  thereIs_file,
                                                                  cliche_file,
                                                                  adverb_file,
                                                                  so_file,),
                                                     invalid_files=(
                                                         passive_file,
                                                         illusion_file),
                                                     settings={
                                                         'allow_passive_voice':
                                                             False})

WriteGoodLintBearWithTooWordyTest = verify_local_bear(WriteGoodLintBear,
                                                      valid_files=(
                                                          good_file,
                                                          weasel_file,
                                                          bad_file,
                                                          passive_file,
                                                          thereIs_file,
                                                          cliche_file,
                                                          adverb_file,
                                                          illusion_file),
                                                      invalid_files=(
                                                          wordy_file,
                                                          so_file),
                                                      settings={
                                                          'allow_extra_words':
                                                              False})

WriteGoodLintBearWithThereIsTest = verify_local_bear(WriteGoodLintBear,
                                                     valid_files=(
                                                         good_file,
                                                         bad_file,
                                                         weasel_file,
                                                         wordy_file,
                                                         so_file,
                                                         passive_file,
                                                         cliche_file,
                                                         illusion_file,
                                                         adverb_file,),
                                                     invalid_files=(),
                                                     settings={
                                                         'allow_there_is':
                                                             False})

WriteGoodLintBearWithClicheTest = verify_local_bear(WriteGoodLintBear,
                                                    valid_files=(good_file,
                                                                 weasel_file,
                                                                 bad_file,
                                                                 wordy_file,
                                                                 so_file,
                                                                 passive_file,
                                                                 thereIs_file,
                                                                 illusion_file,
                                                                 adverb_file,),
                                                    invalid_files=(
                                                        cliche_file,),
                                                    settings={
                                                        'allow_cliche_phrases':
                                                            False})

WriteGoodLintBearWithAdverbTest = verify_local_bear(WriteGoodLintBear,
                                                    valid_files=(
                                                        good_file,
                                                        bad_file,
                                                        weasel_file,
                                                        cliche_file,
                                                        so_file,
                                                        passive_file,),
                                                    invalid_files=(
                                                        illusion_file,
                                                        thereIs_file,
                                                        wordy_file,
                                                        adverb_file),
                                                    settings={'allow_adverbs':
                                                              False})

WriteGoodLintBearWithSoTest = verify_local_bear(WriteGoodLintBear,
                                                valid_files=(good_file,
                                                             weasel_file,
                                                             wordy_file,
                                                             thereIs_file,
                                                             cliche_file,
                                                             adverb_file,
                                                             passive_file,
                                                             illusion_file,),
                                                invalid_files=(
                                                    bad_file, so_file,),
                                                settings={'allow_so_beginning':
                                                          False})

WriteGoodLintBearWithIllusionTest = verify_local_bear(WriteGoodLintBear,
                                                      valid_files=(
                                                          good_file,
                                                          weasel_file,
                                                          wordy_file,
                                                          thereIs_file,
                                                          cliche_file,
                                                          adverb_file,
                                                          passive_file,
                                                          bad_file,
                                                          so_file,),
                                                      invalid_files=(
                                                          illusion_file,),
                                                      settings={
                                                        'allow_repeated_words':
                                                            False})

WriteGoodLintBearWithWeaselTest = verify_local_bear(WriteGoodLintBear,
                                                    valid_files=(good_file,
                                                                 bad_file,
                                                                 weasel_file,
                                                                 cliche_file,
                                                                 so_file,
                                                                 passive_file,
                                                                 ),
                                                    invalid_files=(
                                                        illusion_file,
                                                        thereIs_file,
                                                        wordy_file,
                                                        adverb_file),
                                                    settings={
                                                      'allow_ambiguous_words':
                                                          False})
