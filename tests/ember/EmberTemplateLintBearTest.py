import os

from bears.ember.EmberTemplateLintBear import EmberTemplateLintBear
from coalib.testing.LocalBearTestHelper import verify_local_bear

test_dir = os.path.join(os.path.dirname(__file__),
                        'template_lint_test_files')
good_file = os.path.join(test_dir, 'good_file.hbs')
bad_file = os.path.join(test_dir, 'bad_file.hbs')
good_file_with_config = os.path.join(test_dir,
                                     'good_file_with_config.hbs')
bad_file_with_config = os.path.join(test_dir,
                                    'bad_file_with_config.hbs')

EmberTemplateLintBearTest = verify_local_bear(EmberTemplateLintBear,
                                              valid_files=(good_file,),
                                              invalid_files=(bad_file,))

EmberTemplateLintBearConfigTest = verify_local_bear(
    EmberTemplateLintBear,
    valid_files=(good_file_with_config,),
    invalid_files=(bad_file_with_config,),
    settings={'custom_config': os.path.join(test_dir, '.template-lintrc.js')})
