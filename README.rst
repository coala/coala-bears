.. image:: https://cloud.githubusercontent.com/assets/7521600/15992701/ef245fd4-30ef-11e6-992d-275c5ca7c3a0.jpg

coala-bears
-----------

coala-bears is a Python package containing all the bears that are officially
supported by coala. It features more than **78 bears** covering
**54 languages**. Here is a `generated list <https://github.com/coala/bear-docs/>`_
that contains information about each bear, such as the languages it supports and
what fixes it can apply to your code.

-----

.. contents::
    :local:
    :depth: 1
    :backlinks: none

-----

============
Installation
============

To install the **latest stable version** run:

.. code-block:: bash

    $ pip3 install coala-bears

|Stable|

To install the latest development version run:

.. code-block:: bash

    $ pip3 install coala-bears --pre

The latest code from the master branch is automatically deployed as the
development version in PyPI.

To also install all bears for coala at once run:

.. code-block:: bash

    $ pip3 install coala-bears

You can also use ``cib`` (coala Installs Bears), which is an experimental bear
manager that lets you install, upgrade, uninstall, check dependencies, etc.
for bears. To install it, run:

.. code-block:: bash

    $ pip3 install cib

For usage instructions, consult
`this link <http://coala.readthedocs.io/en/latest/Developers/Bear_Installation_Tool.html>`__.

Be sure to use the latest version of pip, the default pip from Debian doesn't
support our dependency version number specifiers. You will have to `use a
virtualenv <https://github.com/coala/coala/wiki/FAQ#installation-is-failing-help>`__
in this case.

|PyPI| |Windows| |Linux|

-----

===================
Languages Supported
===================

To see what coala can do for your language, run:

.. code-block:: bash

    $ coala --show-bears --filter-by-language Python

+----------------------------+----------------------------+----------------------------+
|                        Languages coala provides algorithms for                       |
+============================+============================+============================+
| C                          | Latex                      | SQL                        |
+----------------------------+----------------------------+----------------------------+
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

The number of bears grows every day! If you want to see any particular
functionality be sure to submit an issue, but please read the `Getting Involved`_
section before doing so.

You can read more at our `documentation <http://coala.readthedocs.io/en/latest/Developers/Writing_Bears.html>`__.
There you can learn how to easily write bears yourself! Be sure to let us know
if you do so, so we'll be able to include it here and spread the word about it.

-----

=====
Usage
=====

For more information about how to do basic analysis, check out the
`coala README <https://github.com/coala/coala#usage>`__.

-----

=======
Authors
=======

coala-bears is maintained by a growing community. Please take a look at the
meta information in `setup.py <setup.py>`__ for current maintainers.

-----

================
Getting Involved
================

If you would like to be a part of the coala community, you can check out our
`Getting In Touch <http://coala.readthedocs.io/en/latest/Help/Getting_In_Touch.html>`__
page or ask us at our active Gitter channel, where we have maintainers from
all over the world. We appreciate any help!

We also have a
`newcomer guide <http://coala.readthedocs.io/en/latest/Developers/Newcomers_Guide.html>`__
to help you get started by fixing an issue yourself! If you get stuck anywhere
or need some help, feel free to contact us on Gitter or drop a mail at our
`newcomer mailing list <https://groups.google.com/d/forum/coala-newcomers>`__.

|gitter|

-----

=======
Support
=======

Feel free to contact us at our `Gitter channel <https://gitter.im/coala/coala>`__, we'd be happy to help!

If you are interested in commercial support, please contact us on the Gitter
channel as well.

You can also drop an email at our
`mailing list <https://github.com/coala/coala/wiki/Mailing-Lists>`__.

-----

=======
Authors
=======

coala is maintained by a growing community. Please take a look at the
meta information in `setup.py <setup.py>`__ for the current maintainers.

-----

=======
License
=======

|AGPL|


.. |Stable| image:: https://img.shields.io/badge/latest%20stable-0.8.0-green.svg
.. |PyPI| image:: https://img.shields.io/pypi/v/coala-bears.svg
   :target: https://pypi.python.org/pypi/coala-bears
.. |Linux| image:: https://img.shields.io/circleci/project/coala/coala-bears/master.svg?label=linux%20build
   :target: https://circleci.com/gh/coala/coala-bears
.. |Windows| image:: https://img.shields.io/appveyor/ci/coala/coala-bears/master.svg?label=windows%20build
   :target: https://ci.appveyor.com/project/coala/coala-bears/branch/master
.. |Documentation Status| image:: https://readthedocs.org/projects/coala/badge/?version=latest
   :target: http://coala.rtfd.org/
.. |codecov.io| image:: https://img.shields.io/codecov/c/github/coala/coala-bears/master.svg?label=branch%20coverage
   :target: https://codecov.io/github/coala/coala-bears
.. |gitter| image:: https://img.shields.io/badge/gitter-join%20chat%20%E2%86%92-brightgreen.svg
   :target: https://gitter.im/coala/coala
.. |AGPL| image:: https://img.shields.io/github/license/coala/coala-bears.svg
   :target: https://www.gnu.org/licenses/agpl-3.0.html
