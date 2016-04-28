coala-bears 0.2.0
=================

In this release, coala-bears has been revamped with new bears and more configs
are added for existing bears.

New bears:
-  ``AutoPrefixBear`` (Add vendor prefixes automatically in CSS)
-  ``ClangComplexityBear`` (Calculates cyclomatic complexity of each function
    for C, C++ and other Clang supported languages.)
-  ``GoTypeBear`` (Static analysis for Go code)
-  ``PMDBear`` (Static analysis for Java code)
-  ``CPDBear`` (Checks for code duplication in a file/multiple files)
-  ``VHDLLintBear`` (Lints for VHDL code)

New features:

-  Additional info is added and documentation is improved for some bears.
   (https://github.com/coala-analyzer/coala-bears/issues/332)
-  ``GitCommitBear`` now checks for imperative tense in your commit message
   shortlog. (https://github.com/coala-analyzer/coala-bears/issues/243)
-  ``GitCommitBear`` checks for WIP in commit message.
-  ``ClangCodeDetectionBear`` now supports for switch/case statements.
   (https://github.com/coala-analyzer/coala-bears/issues/39)
-  Some configs have been added for ``PyDocStyleBear``.
   (https://github.com/coala-analyzer/coala-bears/issues/261)
-  More configs have been added to ``PyImportSortBear``.
   (https://github.com/coala-analyzer/coala-bears/issues/26)
-  ``LineCountBear`` can now warn on files containing lines more than the
    limit.
-  ``CheckStyleBear`` now implements for more settings like checking your
   code against Sun's and Geosoft's code style.
-  Lot of improvements made to LuaLintBear to show error codes and use
   standard input for file passing.

For developers:

-  All existing bears have been updated to use the new ``linter`` decorator.
-  The ``LANGUAGES`` attribute is now set for each bear listing the
   languages it can support.


Bugfixes:

-  ``JuliaLintBear`` is now skipped if the ``Lint`` package is not found.
   (https://github.com/coala-analyzer/coala-bears/issues/222)
-  ``XMLBear`` now processes errors correctly for both ``stdout`` and
   ``stderr``.
   (https://github.com/coala-analyzer/coala-bears/issues/251)

coala-bears 0.1.0 beta
=======================

coala-bears is a Python package containing all the bears that are used by coala.
It has been split from `coala <https://github.com/coala-analyzer/coala>`_.
With the initial release, it features 56 bears covering 32 languages.
You can see all of them `here <https://gist.github.com/Adrianzatreanu/cf2d0c8b2ecd542a4860>`_
with a brief description each.

coala-bears has bears for famous languages, such as:

- C++
- C#
- CMake
- CoffeeScript
- CSS
- Dart
- Go
- Haskell
- HTML
- Java
- JavaScript
- Julia
- Latex
- Lua
- Markdown
- Matlab/Octave
- Natural Language (English)
- Perl
- PHP
- Python 2
- Python 3
- R
- RST
- Ruby
- Scala
- SCSS
- sh & bash scripts
- SQL
- TypeScript
- Vimscript
- XML
- YAML
