from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.DistributionRequirement import (
    DistributionRequirement)


@linter(executable='astyle',
        output_format='corrected',
        use_stdin=True)
class ArtisticStyleBear:
    """
    Artistic Style is a source code indenter, formatter,
    and beautifier for the C, C++, C++/CLI, Objective-C,
    C# and Java programming languages.
    """

    LANGUAGES = {'C', 'CPP', 'Objective-C', 'C#', 'Java'}
    REQUIREMENTS = {
        DistributionRequirement(
            apt_get='astyle',
            dnf='astyle'
        )
    }
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_FIX = {'Formatting'}
    SEE_MORE = 'http://astyle.sourceforge.net/astyle.html'

    @staticmethod
    def create_arguments(filename, file, config_file,
                         bracket_style: str = '',
                         use_spaces: bool = None,
                         indent_size: int = 4,
                         require_braces_at_namespace: bool = True,
                         require_braces_at_class: bool = True,
                         require_braces_at_inline: bool = True,
                         require_braces_at_extern: bool = False,
                         allow_indent_classes: bool = True,
                         allow_indent_modifiers: bool = True,
                         allow_indent_switches: bool = True,
                         allow_indent_cases: bool = True,
                         allow_indent_namespaces: bool = False,
                         allow_indent_labels: bool = True,
                         allow_indent_preproc_block: bool = True,
                         allow_indent_preproc_definition: bool = True,
                         allow_indent_preproc_conditionals: bool = True,
                         allow_indent_column_one_comments: bool = True,
                         allow_pad_header_blocks: bool = True,
                         allow_pad_operators: bool = True,
                         allow_pad_parenthesis: bool = False,
                         allow_pad_parenthesis_out: bool = False,
                         allow_pad_parenthesis_in: bool = False,
                         prohibit_empty_lines_in_func: bool = False,
                         break_closing_braces: bool = False,
                         break_elseifs: bool = False,
                         break_one_line_headers: bool = False,
                         require_braces_at_one_line_conditionals: bool = False,
                         prohibit_braces_from_one_line_conditionals:
                             bool = False,
                         prohibit_comment_prefix: bool = True,
                         ):
        """
        :param bracket_style:
            Defines the brace style to use.
            Possible values are ``allman, java, kr, stroustrup, whitesmith,
            vtk, banner, gnu, linux, horstmann, google, mozilla, pico and
            lisp.``
            For example: Allman style uses braces that are broken from the
            previous block. If set to ``allman``, prefer::

                int Foo(bool isBar)
                {
                    if (isBar)
                    {
                        bar();
                        return 1;
                    }
                    else
                        return 0;
                }

            For example: Java style uses braces that are attached to the
            end of the last line of the previous block.
            If set to ``java``, prefer::

                int Foo(bool isBar) {
                    if (isBar) {
                        bar();
                        return 1;
                    } else
                        return 0;
                }

            For example: Kernighan & Ritchie style uses linux braces.
            Opening braces are broken from ``namespaces``, ``classes`` and
            ``function`` definitions. The braces are attached to everything
            else, including arrays, structs, enums, and statements within
            a function. If set to ``kr``, prefer::

                int Foo(bool isBar)
                {
                    if (isBar) {
                        bar();
                        return 1;
                    } else
                        return 0;
                }

            For example: Stroustrup style uses linux braces with closing
            headers broken from closing braces. Opening braces are broken from
            function definitions only. The opening braces are attached to
            everything else, including ``namespaces``, ``classes``, ``arrays``,
            ``structs``, enums, and statements within a function.
            If set to ``stroustrup``, prefer::

                int Foo(bool isBar)
                {
                    if (isBar) {
                        bar();
                        return 1;
                    }
                    else
                        return 0;
                }

            For example: Whitesmith style uses broken, indented braces.
            Switch blocks and class blocks are indented to prevent a
            'hanging indent' with the following case statements and C++ class
            modifiers (``public``, ``private``, ``protected``).
            If set to ``whitesmith``, prefer::

                int Foo(bool isBar)
                    {
                    if (isBar)
                        {
                        bar();
                        return 1;
                        }
                    else
                        return 0;
                    }

            For example: VTK (Visualization Toolkit) style uses broken,
            indented braces, except for the opening brace. Switch blocks are
            indented to prevent a 'hanging indent' with following case
            statements. If set to ``vtk``, prefer::

                int Foo(bool isBar)
                {
                    if (isBar)
                        {
                        bar();
                        return 1;
                        }
                    else
                        return 0;
                }

            For example: Banner style uses attached, indented braces.
            Switch blocks and class blocks are indented to prevent a
            'hanging indent' with following case statements and C++ class
            modifiers (``public``, ``private``, ``protected``).
            If set to ``banner``, prefer::

                int Foo(bool isBar) {
                    if (isBar) {
                        bar();
                        return 1;
                        }
                    else
                        return 0;
                    }

            For example: GNU style uses broken braces and indented blocks.
            Extra indentation is added to blocks within a function only. Other
            braces and blocks are broken, but NOT indented. This style
            frequently is used with an indent of 2 spaces. If set to ``gnu``,
            prefer::

                int Foo(bool isBar)
                {
                    if (isBar)
                        {
                            bar();
                            return 1;
                        }
                    else
                        return 0;
                }

            For example: Linux style uses linux braces. Opening braces are
            broken from namespace, class, and function definitions. The braces
            are attached to everything else, including ``arrays``, ``structs``,
            ``enums``, and statements within a function. The minimum
            conditional indent is one-half indent. If you want a different
            minimum conditional indent, use the K&R style instead. This style
            works best with a large indent. It frequently is used with an
            indent of 8 spaces. If set to ``linux``, prefer::

                int Foo(bool isBar)
                {
                        if (isFoo) {
                                bar();
                                return 1;
                        } else
                                return 0;
                }

            For example: Horstmann style uses broken braces and run-in
            statements. ``Switches`` are indented to allow a run-in to the
            opening ``switch`` block. This style frequently is used with an
            indent of 3 spaces. If set to ``horstmann``, prefer::

                int Foo(bool isBar)
                {   if (isBar)
                    {   bar();
                        return 1;
                    }
                    else
                        return 0;
                }

            For example: Google style uses attached braces and indented
            class access modifiers. This is not actually a unique brace
            style, but is Java style with a non-brace variation. This style
            frequently is used with an indent of 2 spaces. If set to
            ``google``, prefer::

                int Foo(bool isBar) {
                    if (isBar) {
                        bar();
                        return 1;
                    } else
                        return 0;
                }

            For example: Mozilla style uses linux braces. Opening braces
            are broken from ``classes``, ``structs``, ``enums``, and
            ``function`` definitions. The braces are attached to everything
            else, including ``namespaces``, ``arrays``, and ``statements``
            within a ``function``. This style frequently is used with an
            indent of 2 spaces. If set to ``mozilla``, prefer::

                int Foo(bool isBar)
                {
                    if (isBar) {
                        bar();
                        return 1;
                    } else
                        return 0;
                }

            For example: Pico style uses broken braces and run-in
            statements with attached closing braces. The closing brace is
            attached to the last line in the block. ``Switches`` are indented
            to allow a run-in to the opening ``switch`` block. This style
            frequently is used with an indent of 2 spaces.
            If set to ``pico``, prefer::

                int Foo(bool isBar)
                {   if (isBar)
                    {   bar();
                        return 1; }
                    else
                        return 0; }

            For example: Lisp style uses attached opening and closing
            braces. The closing brace is attached to the last line in the
            block. If set to ``lisp``,
            prefer::

                int Foo(bool isBar) {
                if (isBar) {
                    bar()
                    return 1; }
                else
                    return 0; }

        :param use_spaces:
            In the following examples, ``q`` space is indicated with a ``.``
            (dot), a tab is indicated by a > (greater than).
            For example: If ``None``, the default option of 4 spaces will be
            used as below::

                void Foo() {
                ....if (isBar1
                ............&& isBar2)
                ........bar();
                }

            For example: If set to ``True``, spaces will be used for
            indentation.
            For example: If set to ``False``, tabs will be used for
            indentation, and spaces for continuation line alignment as below::

                void Foo() {
                >   if (isBar1
                >   ........&& isBar2)
                >   >   bar();
                }

        :param indent_size:
            Number of spaces per indentation level.
            For example: If ``use_spaces`` is ``True`` and ``indent_size`` is
            ``3``, prefer::

                void Foo() {
                ...if (isBar1
                .........&& isBar2)
                ......bar();
                }

        :param require_braces_at_namespace:
            Attach braces to a namespace statement. This is done
            regardless of the brace style being used.
            For example: If set to ``True``, prefer::

                namespace FooName {
                ...
                }

        :param require_braces_at_class:
            Attach braces to a class statement. This is done regardless of the
            brace style being used.
            For example: If set to ``True``, prefer::

                class FooClass {
                ...
                };

        :param require_braces_at_inline:
            Attach braces to class and struct inline function definitions. This
            option has precedence for all styles except ``Horstmann`` and
            ``Pico`` (run-in styles). It is effective for C++ files only.
            For example: If set to ``True``, prefer::

                class FooClass
                {
                    void Foo() {
                    ...
                    }
                };

        :param require_braces_at_extern:
            Attach braces to a braced extern "C" statement. This is done
            regardless of the brace style being used. This option is effective
            for C++ files only.
            For example: If set to ``True``, prefer::

                #ifdef __cplusplus
                extern "C" {
                #endif

        :param allow_indent_classes:
            Indent ``class`` and ``struct`` blocks so that the entire block is
            indented. The ``struct`` blocks are indented only if an access
            modifier, ``public:``, ``protected:`` or ``private:``, is declared
            somewhere in the ``struct``. This option is effective for C++ files
            only. For example: If set to ``True``, prefer this::

                class Foo
                {
                    public:
                        Foo();
                        virtual ~Foo();
                };

            over this::

                class Foo
                {
                public:
                    Foo();
                    virtual ~Foo();
                };

        :param allow_indent_modifiers:
            Indent ``class`` and ``struct`` access modifiers, ``public:``,
            ``protected:`` and ``private:``, one half indent. The rest of the
            class is not indented. This option is effective for C++ files only.
            For example: If set to ``True``, prefer this::

                class Foo
                {
                  public:
                    Foo();
                    virtual ~Foo();
                };

            over this::

                class Foo
                {
                public:
                    Foo();
                    virtual ~Foo();
                };

        :param allow_indent_switches:
            Indent ``switch`` blocks so that the ``case X:`` statements are
            indented in the switch block. The entire case block is indented.
            For example: If set to ``True``, prefer this::

                switch (foo)
                {
                    case 1:
                        a += 1;
                        break;

                    case 2:
                    {
                        a += 2;
                        break;
                    }
                }

            over this::

                switch (foo)
                {
                case 1:
                    a += 1;
                    break;

                case 2:
                {
                    a += 2;
                    break;
                }
                }

        :param allow_indent_cases:
            Indent ``case X:`` blocks from the ``case X:`` headers. Case
            statements not enclosed in blocks are NOT indented.
            For example: If set to ``True``, prefer this::

                switch (foo)
                {
                    case 1:
                        a += 1;
                        break;

                    case 2:
                        {
                            a += 2;
                            break;
                        }
                }

            over this::

                switch (foo)
                {
                    case 1:
                        a += 1;
                        break;

                    case 2:
                    {
                        a += 2;
                        break;
                    }
                }

        :param allow_indent_namespaces:
            Add extra indentation to namespace blocks. This option has no
            effect on Java files.
            For example: If set to ``True``, prefer this::

                namespace foospace
                {
                    class Foo
                    {
                        public:
                            Foo();
                            virtual ~Foo();
                    };
                }

            over this::

                namespace foospace
                {
                class Foo
                {
                    public:
                        Foo();
                        virtual ~Foo();
                };
                }

        :param allow_indent_labels:
            Add extra indentation to labels so they appear 1 indent less than
            the current indentation, rather than being flushed to the
            left (the default).
            For example: If set to ``True``, prefer this::

                void Foo() {
                    while (isFoo) {
                        if (isFoo)
                            goto error;
                        ...
                    error:
                        ...
                        }
                }

            over this::

                void Foo() {
                    while (isFoo) {
                        if (isFoo)
                            goto error;
                        ...
                error:
                        ...
                        }
                }

        :param allow_indent_preproc_block:
            Indent preprocessor blocks at brace level zero and immediately
            within a namespace. There are restrictions on what will be
            indented. Blocks within methods, classes, arrays, etc., will not
            be indented. Blocks containing braces or multi-line define
            statements will not be indented. Without this option the
            preprocessor block is not indented.
            For example: If set to ``True``, prefer this::

                #ifdef _WIN32
                    #include <windows.h>
                    #ifndef NO_EXPORT
                        #define EXPORT
                    #endif
                #endif

            over this::

                #ifdef _WIN32
                #include <windows.h>
                #ifndef NO_EXPORT
                #define EXPORT
                #endif
                #endif

        :param allow_indent_preproc_definition:
            Indent multi-line preprocessor definitions ending with a backslash.
            Should be used with ``convert_tabs_to_spaces`` for proper results.
            Does a pretty good job, but cannot perform miracles in obfuscated
            preprocessor definitions. Without this option the preprocessor
            statements remain unchanged.
            For example: If set to ``True``, prefer this::

                #define Is_Bar(arg,a,b) \
                    (Is_Foo((arg), (a)) \
                     || Is_Foo((arg), (b)))

            over this::

                #define Is_Bar(arg,a,b) \
                (Is_Foo((arg), (a)) \
                || Is_Foo((arg), (b)))

        :param allow_indent_preproc_conditionals:
            Indent preprocessor conditional statements to the same level as the
            source code.
            For example: If set to ``True``, prefer this::

                        isFoo = true;
                        #ifdef UNICODE
                        text = wideBuff;
                        #else
                        text = buff;
                        #endif
            over this::

                        isFoo = true;
                #ifdef UNICODE
                        text = wideBuff;
                #else
                        text = buff;
                #endif

        :param allow_indent_column_one_comments:
            Indent C++ comments beginning in column one. By default C++
            comments beginning in column one are assumed to be commented-out
            code and not indented. This option will allow the comments to be
            indented with the code.
            For example: If set to ``True``, prefer this::

                void Foo()\n"
                {
                    // comment
                    if (isFoo)
                        bar();
                }

            over this::

                void Foo()\n"
                {
                // comment
                    if (isFoo)
                        bar();
                }

        :param allow_pad_header_blocks:
            Pad empty lines around header blocks
            (e.g. ``if``, ``for``, ``while``...).
            For example: If set to ``True``, prefer this::

                isFoo = true;

                if (isFoo) {
                    bar();
                } else {
                    anotherBar();
                }

                isBar = false;

            over this::

                isFoo = true;
                if (isFoo) {
                    bar();
                } else {
                    anotherBar();
                }
                isBar = false;

        :param allow_pad_operators:
            Insert space padding around operators. This will also pad commas.
            For example: If set to ``True``, prefer this::

                if (foo == 2)
                    a = bar((b - c) * a, d--);

            over this::

                if (foo==2)
                    a=bar((b-c)*a,d--);

        :param allow_pad_parenthesis:
            Insert space padding around parenthesis on both the outside and the
            inside.
            For example: If set to ``True``, prefer this::

                if ( isFoo ( ( a+2 ), b ) )
                    bar ( a, b );

            over this::

                if (isFoo((a+2), b))
                    bar(a, b);

        :param allow_pad_parenthesis_out:
            Insert space padding around parenthesis on the outside only.
            Parenthesis that are empty will not be padded.
            For example: If set to ``True``, prefer this::

                if (isFoo ( (a+2), b) )
                    bar (a, b);

            over this::

                if (isFoo((a+2), b))
                    bar(a, b);

        :param allow_pad_parenthesis_in:
            Insert space padding around parenthesis on the inside only.
            For example: If set to ``True``, prefer this::

                if ( isFoo( ( a+2 ), b ) )
                    bar( a, b );

            over this::

                if (isFoo((a+2), b))
                    bar(a, b);

        :param prohibit_empty_lines_in_func:
            Delete empty lines within a function or method. Empty lines outside
            of functions or methods are NOT deleted.
            For example: If set to ``True``, prefer this::

                void Foo()
                {
                    foo1 = 1;
                    foo2 = 2;
                }

            over this::

                void Foo()
                {

                    foo1 = 1;

                    foo2 = 2;

                }

        :param break_closing_braces:
            When used with some specific ``bracket_style``, this breaks closing
            headers (e.g. ``else``, ``catch``, ...) from their immediately
            preceding closing braces. Closing header braces are always broken
            with the other styles.
            For example: If set to ``True``, prefer this::

                void Foo(bool isFoo) {
                    if (isFoo) {
                        bar();
                    }
                    else {
                        anotherBar();
                    }
                }

            over this::

                void Foo(bool isFoo) {
                    if (isFoo) {
                        bar();
                    } else {
                        anotherBar();
                    }
                }

        :param break_elseifs:
            Break ``else if`` header combinations into separate lines.
            For example: If set to ``True``, prefer this::

                if (isFoo) {
                    bar();
                }
                else
                    if (isFoo1()) {
                        bar1();
                    }
                    else
                        if (isFoo2()) {
                            bar2();
                        }

            over this::

                if (isFoo) {
                    bar();
                }
                else if (isFoo1()) {
                    bar1();
                }
                else if (isFoo2()) {
                    bar2;
                }

        :param break_one_line_headers:
            Break one line headers (e.g. ``if``, ``while``, ``else``, ...) from
            a statement residing on the same line. If the statement is enclosed
            in braces, the braces will be formatted according to the requested
            brace style.
            For example: If set to ``True``, prefer this::

                void Foo(bool isFoo)
                {
                    if (isFoo1)
                        bar1();

                    if (isFoo2) {
                        bar2();
                    }
                }

            over this::

                void Foo(bool isFoo)
                {
                    if (isFoo1) bar1();

                    if (isFoo2) { bar2(); }
                }

        :param require_braces_at_one_line_conditionals:
            Add braces to unbraced one line conditional statements
            (e.g. ``if``, ``for``, ``while``...). The statement must be on a
            single line. The braces will be added according to the requested
            brace style.
            For example: If set to ``True``, prefer this::

                if (isFoo) {
                    isFoo = false;
                }

            over this::

                if (isFoo)
                    isFoo = false;

        :param prohibit_braces_from_one_line_conditionals:
            Remove braces from conditional statements
            (e.g. ``if``, ``for``, ``while``...). The statement must be a
            single statement on a single line.
            For example: If set to ``True``, prefer this::

                if (isFoo)
                    isFoo = false;

            over this::

                if (isFoo)
                {
                    isFoo = false;
                }

        :param prohibit_comment_prefix:
            Remove the preceding '*' in a multi-line comment that begins a
            line. A trailing '*', if present, is also removed. Text that is
            less than one indent is indented to one indent. Text greater than
            one indent is not changed. Multi-line comments that begin a line,
            but without the preceding '*', are indented to one indent for
            consistency. This can slightly modify the indentation of commented
            out blocks of code. Lines containing all '*' are left unchanged.
            Extra spacing is removed from the comment close '*/'.
            For example: If set to ``True``, prefer this::

                /*
                    comment line 1
                    comment line 2
                */

            over this::

                /*
                 * comment line 1
                 * comment line 2
                 */

        """
        rules_map = {
            '--attach-namespaces': require_braces_at_namespace,
            '--attach-classes': require_braces_at_class,
            '--attach-inlines': require_braces_at_inline,
            '--attach-extern-c': require_braces_at_extern,
            '--indent-classes': allow_indent_classes,
            '--indent-modifiers': allow_indent_modifiers,
            '--indent-switches': allow_indent_switches,
            '--indent-cases': allow_indent_cases,
            '--indent-namespaces': allow_indent_namespaces,
            '--indent-labels': allow_indent_labels,
            '--indent-preproc-block': allow_indent_preproc_block,
            '--indent-preproc-define': allow_indent_preproc_definition,
            '--indent-preproc-cond': allow_indent_preproc_conditionals,
            '--indent-col1-comments': allow_indent_column_one_comments,
            '--break-blocks': allow_pad_header_blocks,
            '--pad-oper': allow_pad_operators,
            '--pad-paren': allow_pad_parenthesis,
            '--pad-paren-out': allow_pad_parenthesis_out,
            '--pad-paren-in': allow_pad_parenthesis_in,
            '--delete-empty-lines': prohibit_empty_lines_in_func,
            '--break-closing-brackets': break_closing_braces,
            '--break-elseifs': break_elseifs,
            '--break-one-line-headers': break_one_line_headers,
            '--add-brackets': require_braces_at_one_line_conditionals,
            '--remove-brackets': prohibit_braces_from_one_line_conditionals,
            '--remove-comment-prefix': prohibit_comment_prefix
        }
        args = ['--suffix=none', '--dry-run']
        if bracket_style:
            args.append('--style=' + bracket_style)
        if use_spaces is True:
            args.append('-s' + str(indent_size))
        elif use_spaces is False:
            args.append('-t' + str(indent_size))
        args += (k for k, v in rules_map.items() if v)
        return args
