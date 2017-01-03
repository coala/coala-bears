coala-bears 0.9.2
=================

- A dependency problem in `RadonBear` causing install failure has been fixed
  `Issue #1228 <https://github.com/coala/coala-bears/issues/1228>`_
- coala dependency has been fixed to only allow coala versions 0.9.x with
  0.9 series bears
  `Pull #1243 <https://github.com/coala/coala-bears/pull/1243>`_
- `InvalidLinkBear` default timeout has been increased to 15 seconds from 2
  because it was creating false positives
  `Issue #1219 <https://github.com/coala/coala-bears/issues/1219>`_

coala-bears 0.9.1
=================

This bugfix release fixes the following issues:

- `TailorBear` was not distributed correctly.
  (https://github.com/coala/coala-bears/issues/1048)

coala-bears 0.9.0
=================

This release, we had 40 different contributors, pushing almost 200 commits.

To get a quick overview over the current state of all bears, check out
https://coala.io/languages. We added a number of asciinemas so you can see
them in action right away.

Here are the important changes and additions, of course coala was upgraded to
0.9 so you can enjoy all it's new features and bugfixes:

**New Bears:**

Language Independent:

- `QuotesBear` - Checks and corrects your quoting style for any language!
- `SpellCheckBear` - Checks for english spelling mistakes in any source code.

Python:

- `MypyBear` - Checks Python code for typing using Mypy!
- `BanditBear` - Checks Python code for security issues.
- `PEP8NotebookBear` - Autocorrects formatting for Python code in Jupyter
  Notebooks.
- `PySafetyBear` - Checks for known security vulnerabilities of your Python
  requirements.
- `PinRequirementsBear` - Checks if Python requirements are pinned precisely.
- `PycodestyleBear` - Checks Python coding style with better error messages
  and reliability than `PEP8Bear`, however without automatic correction.

Others:

- `PHPCodeSnifferBear` - Ensures that your PHP, JavaScript or CSS code remains
  clean and consistent.
- `Jinja2Bear` - Detects and fixes formatting issues in Jinja2 templates.
- `RSTcheckBear` - Checks reStructuredText for formatting and syntax.
- `PuppetLintBear` - Checks and autocorrects puppet configuration files.
- `CSVLintBear` - Checks syntax of CSV files.

**Bears with New Settings:**

You can look up the new settings at https://coala.io/languages.

- `InvalidLinkBear`
- `GitCommitBear`
- `YapfBear`
- `SCSSLintBear`

**Deleted Settings:**

- `CSecurityBear` does not accept a `neverignore` setting anymore. Those kinds
  of issues are and should be consistently handled by coala.

**Deprecated Settings:**

- The `ignore_regex` setting from `InvalidLinkBear` was deprecated in favour of
  `link_ignore_regex` for more clarity in coafiles.
- `KeywordBear` accepts only one `keywords` argument. The `ci_keywords` and
  `cs_keywords` arguments have been deprecated.
- `JSHintBear` provides an `es_version` argument that implies the
  `use_es6_syntax` argument. The latter has been deprecated in favour of the
  former.
- `JSHintBear` provides a more flexible `javascript_strictness` argument
  instead of the `allow_global_strict` which has been deprecated.
- `RuboCopBear` uses `naming_convention` instead of `name_case` now.

**Other Bear Enhancements:**

- The `coala-bears` package does no longer require Java upon installation.
- `VultureBear` picks up global dependencies.
- `ESLintBear` shows errors as `WARNING` in coala. This simplifies debugging
  bad ESLint configurations.
- `KeywordBear` can now automatically remove TODO comments for any language
  coala has `Language` definitions for.
- `FilenameBear` supports the `spacecase` convention.
- `KeywordBear` checks for `todo` and `fixme` by default.
- `GitCommitBear` has improved result messages.
- `YAMLLintBear` does not check for `document-start` by default. This was not
  a commonly chosen setting.
- `YapfBear` will pass files in-memory to save precious IO time.

**Major API Changes:**

- The bears testing modules were moved to the coalib and are deprecated.

**Bug Fixes:**

- `AnnotationBear` yields a `HiddenResult` with an error message instead of
  raising an exception, when the desired language is not available.
- `AnnotationBear` yields correct results for escaped strings.
  (https://github.com/coala/coala-bears/issues/993)
- `AnnotationBear` yields correct results for rare corner cases of multiline
  strings. (https://github.com/coala/coala-bears/issues/1006)
- An issue where `LatexLintBear` crashed has been resolved.
  (https://github.com/coala/coala-bears/issues/317)
- `InvalidLinkBear` parses links within backticks properly. It also ignores
  links with placeholders like `%s` and others.
- `InvalidLinkBear` ignores FTP links.
  (https://github.com/coala/coala-bears/issues/906)
- `DartLintBear` emits an error when it cannot satisfy given settings.
  (https://github.com/coala/coala-bears/issues/897)
- `CheckstyleBear` emits an error when it cannot satisfy given settings.
  (https://github.com/coala/coala-bears/issues/898)
- `CheckstyleBear`: preset configurations `google` and `sun` are no longer
  downloaded. (https://github.com/coala/coala-bears/issues/1034)
- `YAMLLintBear` picks up the configuration properly.
  (https://github.com/coala/coala-bears/issues/979)
- `JavaPMDBear` works correctly on Mac now.
  (https://github.com/coala/coala-bears/issues/998)
- The dependencies of the following bears were bumped due to upstream
  bugfixes:

    - `AlexBear`
    - `CPPCleanBear`
    - `ESLintBear`
    - `MarkdownBear`
    - `ProseLintBear`
    - `YapfBear`

**Internal Changes:**

- All bears use the new `linter` API now.

coala-bears 0.8.4
=================

This bugfix release fixes the following issues:

- ESLintBear was unable to resolve relative imports correctly.
  (https://github.com/coala/coala-bears/issues/741)
- CPDBear was not showing the context of results correctly.
  (https://github.com/coala/coala-bears/issues/810)

coala-bears 0.8.3
=================

This bugfix release fixes the following issues:

- coala updated from 0.8.0 to 0.8.1.
- YapfBear handles files with syntax errors gracefully.
  (https://github.com/coala/coala-bears/issues/750)
- ESLintBear doesn't fail with an unrelated error when eslint fails anymore,
  it rather shows the errors from eslint as a warning.
  (https://github.com/coala/coala-bears/issues/727 and
  https://github.com/coala/coala-bears/issues/730)

coala-bears 0.8.2
=================

This bugfix release fixes the following issues:

- YapfBear handles empty files correctly now.
  (https://github.com/coala/coala-bears/issues/739)
- JSComplexityBear shows errors on invalid syntax correctly
  (https://github.com/coala/coala-bears/issues/729)
- Cases where RadonBear failed to raise an issue have been solved
  (https://github.com/coala/coala-bears/issues/609)

coala-bears 0.8.1
=================

This bugfix release fixes two issues:

- A dependency issue due to a newly released version of one of coala's
  dependencies.
- YapfBear's unstable syntax verification has been disabled.
  (https://github.com/coala/coala-bears/issues/738)

coala-bears 0.8.0
=================

For this release, we have had 19 contributors from around the world
contributing 176 commits to just coala-bears in the past 9 weeks.

Here are the important changes and additions:

**New Bears**

- ``CSecurityBear`` - Lints C/C++ files and identifies possible security
  issues.
  `[CSecurityBear documentation] <https://github.com/coala/bear-docs/blob/master/docs/CSecurityBear.rst>`__

- ``HappinessLintBear`` - Checks JavaScript files for semantic and syntax
  errors using ``happiness``.
  `[HappinessLintBear documentation] <https://github.com/coala/bear-docs/blob/master/docs/HappinessLintBear.rst>`__

- ``WriteGoodLintBear`` - Lints the text files using ``write-good`` to
  improve proses.
  `[WriteGoodLintBear documentation] <https://github.com/coala/bear-docs/blob/master/docs/WriteGoodLintBear.rst>`__

- ``coalaBear`` - Checks for the correct spelling and casing of ``coala``
  in the text files.
  `[coalaBear documentation] <https://github.com/coala/bear-docs/blob/master/docs/coalaBear.rst>`__

- ``VultureBear`` - Checks Python code for unused variables and functions
  using ``vulture``.
  `[VultureBear documentation] <https://github.com/coala/bear-docs/blob/master/docs/VultureBear.rst>`__

- ``YapfBear`` - Checks and corrects the formatting of Python code using
  ``yapf`` utility.
  `[YapfBear documentation] <https://github.com/coala/bear-docs/blob/master/docs/YapfBear.rst>`__

**Major API Changes**

- Settings unification - most bears have seen API changes. Settings' names
  are now consistent across bears. This supports backwards
  compatibility, however (but with a deprecation notice). You can find the
  whole list `here <http://dpaste.com/3EP5GCV>`_.

**New Features**

- Bear upload tool - this is a part of the complete decentralization of
  bears. With this tool, bears are uploaded as individual packages to PyPI
  and just the necessary bears (and their dependencies) can be installed.

- Also as a part of the decentralization process, several bears now have
  the ``REQUIREMENTS`` attribute. This is one of the requirement objects
  supporting various package managers such as ``apt-get``, ``dnf``,
  ``yum``, ``pip``, ``npm``, ``gem``, and so on. To learn more, please
  see the ``coala`` `0.8.0 release changelog <https://github.com/coala/coala/blob/master/RELEASE_NOTES.rst>`__.

- Several bears now support the ``ASCIINEMA_URL`` attribute. This contains
  an URL to an asciinema video displaying the bear's working.

**Bug Fixes**

- An issue in ``FilenameBear`` involving files with fully capitalized names
  has been resolved. `Pull #687 <https://github.com/coala/coala-bears/pull/687>`_

- Various corner cases with ``InvalidLinkBear`` involving some false positives
  and false negatives have been fixed.
  `Issue #691 <https://github.com/coala/coala-bears/issues/691>`_

**Documentation**

- A complete overhaul of the README page with a special emphasis on design
  and user-friendliness.

**Regressions**

- Python 3.3 support was dropped.

coala-bears 0.7.0
=================

For this release, 17 contributors have contributed about 200 commits to
coala-bears only.

We are bumping the version number to 0.7.0 to keep it in sync with the coala
releases.

New bears:

- ``VerilogLintBear`` (Lints verilog code)
- ``AnnotationBear`` (Annotates source code language independent for further
  processing)
- ``TailorBear`` (Checks Swift code for style compliance)
- ``CPPCheckBear`` (Checks C/C++ code for security issues)
- ``RAMLLintBear`` (Checks style of RAML documents)
- ``GoErrCheckBear`` (Finds unchecked Go function calls)
- ``RubySmellBear`` (Finds code smells in Ruby)
- ``FilenameBear`` (Checks and corrects file naming conventions)
- ``IndentationBear`` (An experimental indentation checker and fixer with a
  language independent algorithm.)

New features:

- Numerous documentation improvements.
- GitCommitBear:
    - The WIP check yields a ``Normal`` Result now.
- InvalidLinkBear:
    - Numerous false positive fixes.
    - An ignore regex can now be passed.
- RuboCopBear:
    - About 30 new configuration options were added.
- GNUIndentBear:
    - 15 new configuration options were added.
- FormatRBear:
    - 6 new configuration options were added.

Bugfixes:

- CPDBear:
    - A case where results with an invalid line reference were yielded was
      fixed.
- CheckstyleBear:
    - In some cases results were not correctly parsed. This was fixed.

Internal changes:

- Almost all bears use the new ``linter`` now instead of ``Lint``.

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
   (https://github.com/coala/coala-bears/issues/332)
-  ``GitCommitBear`` now checks for imperative tense in your commit message
   shortlog. (https://github.com/coala/coala-bears/issues/243)
-  ``GitCommitBear`` checks for WIP in commit message.
-  ``ClangCodeDetectionBear`` now supports for switch/case statements.
   (https://github.com/coala/coala-bears/issues/39)
-  Some configs have been added for ``PyDocStyleBear``.
   (https://github.com/coala/coala-bears/issues/261)
-  More configs have been added to ``PyImportSortBear``.
   (https://github.com/coala/coala-bears/issues/26)
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
   (https://github.com/coala/coala-bears/issues/222)
-  ``XMLBear`` now processes errors correctly for both ``stdout`` and
   ``stderr``.
   (https://github.com/coala/coala-bears/issues/251)

coala-bears 0.1.0 beta
=======================

coala-bears is a Python package containing all the bears that are used by coala.
It has been split from `coala <https://github.com/coala/coala>`_.
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
