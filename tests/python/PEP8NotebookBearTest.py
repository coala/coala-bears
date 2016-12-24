from coalib.testing.LocalBearTestHelper import verify_local_bear
from bears.python.PEP8NotebookBear import PEP8NotebookBear


# metadata field deleted manually
good_file = r"""{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "x = 'good'"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "a markdown cell is not a code cell"
   ]
  }
 ],
 "metadata": {},
 "nbformat": 4,
 "nbformat_minor": 0
}
"""

# metadata field deleted manually
bad_file = r"""{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "x =    1  # <-- PEP8 Error"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "x =    1  # <-- PEP8 Error but we are in a Markdown cell"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {
    "collapsed": false
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "1\n"
     ]
    }
   ],
   "source": [
    "print(x)  # <-- here everything is fine\n"
   ]
  }
 ],
 "metadata": {},
 "nbformat": 4,
 "nbformat_minor": 0
}
"""

PEP8NotebookBearTest = \
    verify_local_bear(PEP8NotebookBear,
                      valid_files=(good_file,),
                      invalid_files=(bad_file,)
                      )

PEP8NotebookBearWithoutTrailingNewlineTest = \
    verify_local_bear(PEP8NotebookBear,
                      valid_files=(good_file[:-1],),
                      invalid_files=(bad_file[:-1],),
                      force_linebreaks=False,
                      )
