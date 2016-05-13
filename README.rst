.. Start ignoring LineLengthBear

::

                                                         .o88Oo._
                                                        d8P         .ooOO8bo._
                                                        88                  '*Y8bo.
                                          __            YA                      '*Y8b   __
                                        ,dPYb,           YA                        68o68**8Oo.
                                        IP'`Yb            "8D                       *"'    "Y8o
                                        I8  8I             Y8     'YB                       .8D
                                        I8  8P             '8               d8'             8D
                                        I8  8'              8       d8888b          d      AY
         ,gggo,    ,ggggo,    ,gggo,gg  I8 dP    ,gggo,gg   Y,     d888888         d'  _.oP"
        dP"  "Yb  dP"  "Y8go*8P"  "Y8I  I8dP    dP"  "Y8I    q.    Y8888P'        d8
       i8'       i8'    ,8P i8'    ,8I  I8P    i8'    ,8I     "q.  `Y88P'       d8"
      ,d8,_    _,d8,   ,d8' d8,   ,d8b,,d8b,_ ,d8,   ,d8b,       Y           ,o8P
    ooP""Y8888PP*"Y8888P"   "Y8888P"`Y88P'"Y88P"Y8888P"`Y8            oooo888P"

.. Stop ignoring LineLengthBear

About
-----

coala-bears is a Python package containing all the bears that are officially
supported by coala. It features more than **65 bears** covering **35 languages**.
You can see all of them `here <https://github.com/coala-analyzer/coala-bears/wiki/Available-bears>`_.

+----------------------------+----------------------------+----------------------------+
|                        Languages coala provides algorithms for                       |
+============================+============================+============================+
| C++                        | Lua                        | TypeScript                 |
+----------------------------+----------------------------+----------------------------+
| C#                         | Markdown                   | VHDL                       |
+----------------------------+----------------------------+----------------------------+
| CMake                      | Matlab/Octave              | Vimscript                  |
+----------------------------+----------------------------+----------------------------+
| CoffeeScript               | Natural Language (English) | XML                        |
+----------------------------+----------------------------+----------------------------+
| CSS                        | Perl                       | YAML                       |
+----------------------------+----------------------------+----------------------------+
| Dart                       | PHP                        |                            |
+----------------------------+----------------------------+----------------------------+
| Fortran                    | Python 2                   |                            |
+----------------------------+----------------------------+----------------------------+
| Go                         | Python 3                   |                            |
+----------------------------+----------------------------+----------------------------+
| Haskell                    | R                          |                            |
+----------------------------+----------------------------+----------------------------+
| HTML                       | reStructured Text          |                            |
+----------------------------+----------------------------+----------------------------+
| Java                       | Ruby                       |                            |
+----------------------------+----------------------------+----------------------------+
| JavaScript                 | Scala                      |                            |
+----------------------------+----------------------------+----------------------------+
| JSP                        | SCSS                       |                            |
+----------------------------+----------------------------+----------------------------+
| Julia                      | sh & bash scripts          |                            |
+----------------------------+----------------------------+----------------------------+
| Latex                      | SQL                        |                            |
+----------------------------+----------------------------+----------------------------+

The number of bears grows every day! If you want to see any particular
functionality be sure to submit an issue, but please read the `GETTING INVOLVED`_
section before doing so.

You can read more at our `documentation <http://coala.readthedocs.org/en/latest/Users/Tutorials/Writing_Bears.html#guide-to-write-a-bear>`__.
There you can learn how to easily write bears yourself! Be sure to let us know
if you do so, then we'll be able to include it here and spread the word about it.

Installation
-------------

coala-bears can be installed with ``pip3 install coala-bears``. If you need more
information about the installation and dependencies, take a look at our
`installation documentation
<http://coala.rtfd.org/en/latest/Users/Install.html>`__.

The latest code from master is automatically deployed to PyPI as a
development version. Get it with ``pip3 install coala-bears --pre``.

Be sure to use the latest pip, the default pip from Debian doesn't support our
dependency version number specifiers. You will have to use a
`virtualenv <https://github.com/coala-analyzer/coala/wiki/FAQ#installation-is-failing-help>`__
in this case.

|PyPI|

Usage
-----

Basic analysis:

::

    echo "print('Hi!') " >> hw.py
    coala --files hw.py --bears SpaceConsistencyBear

Finding out what analysis routines exist:

::

    coala -l JavaScript  # Shows bears for JS
    coala -A  # Shows all bears
    coala -B -b SpaceConsistencyBear  # Shows full bear documentation

If you want to learn more about **coala-bears**, its functionality and its usage,
please take a look at our
`tutorial <http://coala.readthedocs.org/en/latest/Users/Tutorials/Tutorial.html>`__.

Authors
-------

coala-bears is maintained by a growing community. Please take a look at the
meta information in `setup.py <setup.py>`__ for current maintainers.

Getting Involved
----------------

If you want to contribute to coala-bears, please take a look at the `Getting
Involved Information
<http://coala.readthedocs.org/en/latest/Getting_Involved/README.html>`__.

We appreciate any help! Join us on one of:

- `gitter <https://gitter.im/coala-analyzer/coala/>`
- `#coala at freenode <webchat.freenode.net/?channels=coala>`
- `Telegram <https://telegram.me/joinchat/AuL-lwKZ8JLFZiI6SbtQVw>`

(All channels are linked with gitter. Approach @sils1297 if the link doesn't
work properly.)

Project Status
--------------

|Linux Build Status| |Windows Build status| |OSX Build status|

|Documentation Status| |codecov.io|

License
--------

|AGPL|

This code falls under the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or (at
your option) any later version.

Please note that some files or content may be copied from other places.
Most of them are GPL compatible. There is a small portion of code in the
tests that falls under the Creative Commons license, see
https://creativecommons.org/licenses/by-sa/3.0/deed.de for more
information.

.. |PyPI| image:: https://img.shields.io/pypi/v/coala-bears.svg
   :target: https://pypi.python.org/pypi/coala-bears
.. |Linux Build Status| image:: https://img.shields.io/circleci/project/coala-analyzer/coala-bears/master.svg?label=linux%20build
   :target: https://circleci.com/gh/coala-analyzer/coala-bears
.. |Windows Build status| image:: https://img.shields.io/appveyor/ci/coala/coala-bears/master.svg?label=windows%20build
   :target: https://ci.appveyor.com/project/coala/coala-bears/branch/master
.. |Documentation Status| image:: https://readthedocs.org/projects/coala/badge/?version=latest
   :target: http://coala.rtfd.org/
.. |codecov.io| image:: https://img.shields.io/codecov/c/github/coala-analyzer/coala-bears/master.svg?label=branch%20coverage
   :target: https://codecov.io/github/coala-analyzer/coala-bears
.. |https://gitter.im/coala-analyzer/coala| image:: https://img.shields.io/badge/gitter-join%20chat%20%E2%86%92-brightgreen.svg
   :target: https://gitter.im/coala-analyzer/coala
.. |AGPL| image:: https://img.shields.io/github/license/coala-analyzer/coala-bears.svg
   :target: https://www.gnu.org/licenses/agpl-3.0.html
