class UnmatchedIndentError(Exception):

    def __init__(self, open_indent, close_indent):
        Exception.__init__(self, "Unmatched " + open_indent + ", " +
                           close_indent + " pair")


class ExpectedIndentError(Exception):

    def __init__(self, line):
        Exception.__init__(self, "Expected indent after line: " + str(line))
