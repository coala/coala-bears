set -x
set -e

source .ci/env_variables.sh

bash <(curl -s https://codecov.io/bash)
