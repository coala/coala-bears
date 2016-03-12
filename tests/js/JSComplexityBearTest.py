from bears.js.JSComplexityBear import JSComplexityBear
from tests.LocalBearTestHelper import verify_local_bear

complexity_12 = """(function () {
  var foo = 1 && 1 || 0;
  if (foo) {
    if (1) {
    } else {
      if (5*2/10) {
        if (0 || 1) {
          if (foo) {
          if (1) {
          } else {
            if (5*2/10) {
              if (0 || 1) {
                return;
              }
              return;
            }
          }
        }
          return;
        }
        return;
      }
    }
  }
})()
""".splitlines(True)

complexity_4 = """(function () {
  var foo = 1 && 1 || 0;
  if (0 || 1) {
    return;
  }
})()
""".splitlines(True)

JSComplexityBearTest = verify_local_bear(JSComplexityBear,
                                         valid_files=(complexity_4,),
                                         invalid_files=(complexity_12,),
                                         tempfile_kwargs={"suffix": ".js"})

JSComplexityBearThresholdTest = verify_local_bear(JSComplexityBear,
                                                  valid_files=(),
                                                  invalid_files=(complexity_4,
                                                                 complexity_12),
                                                  settings={"cc_threshold": 2},
                                                  tempfile_kwargs={"suffix":
                                                                   ".js"})

# No output for non-js files
JSComplexityBearInvalidFileTest = verify_local_bear(JSComplexityBear,
                                                    valid_files=(complexity_4,
                                                                 complexity_12),
                                                    invalid_files=())
