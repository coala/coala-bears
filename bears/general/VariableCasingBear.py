from coalib.bearlib.languages.LanguageDefinition import LanguageDefinition
from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import RESULT_SEVERITY
from coalib.results.Result import Result
from coalib.results.Diff import Diff
from coalib.parsing.Globbing import fnmatch
import re


class VariableCasingBear(LocalBear):

    def run(self,
            filename,
            file,
            casing: str,
            language: str,
            language_family: str,
            ignore_globs=[]):
        """
        This bear ensures that an uniform standard is employed in
        variable naming. There are two casing standards supported:
        camelCasing and snake_casing.

        :param casing:          One among:
                                camelCasing, snake_casing, PascalCasing
        :param language:        Language from which keywords are ignored.
        :param language_family: Language family in which the language is
                                present.
        """
        cdict = {
            "camelCasing":  self.all_to_camel,
            "snake_casing": self.all_to_snake,
            "PascalCasing": self.all_to_pascal
        }
        if casing not in cdict:
            self.err(casing, "is not a valid casing")
            self.err("Valid: " + str(", ".join(list(cdict.keys()))))
            return
        else:
            convertor = cdict[casing]
        coalang_keys = LanguageDefinition(language_family, language)
        if coalang_keys.has_keys(["keywords", "special_chars"]):
            keywords = coalang_keys["keywords"]
            special_chars = coalang_keys["special_chars"]
            delim = re.escape(str(special_chars) + " \t\n")
            in_quotes = False
            result_texts = []
            text_changes = {}
            lines_changed = set()
            for line_number, line in enumerate(file, start=1):
                split = re.split("[" + delim + "]", line)
                for s in split:
                    if s.startswith("\""):
                        in_quotes = True
                        s = s[1:]
                    if in_quotes:
                        if s[-1:] == "\"" and s[-2:] != "\\\"":
                            in_quotes = False
                        continue
                    if len(s) == 0 or s[0].isdigit():
                        continue
                    if len(ignore_globs) > 0 and fnmatch(s, ignore_globs):
                        continue
                    if s not in keywords:
                        rep = convertor(s)
                        if s != rep:
                            text_changes[s] = rep
            if len(text_changes) > 0:
                for prev, new in text_changes.items():
                    diff = Diff(file)
                    first_line = -1
                    num_changes = 0
                    skip_var = False
                    for line_number, line in enumerate(file, start=1):
                        rep = re.sub("(?P<g1>[\\" + delim + "])" + prev +
                                     "(?P<g2>[\\" + delim + "])",
                                     "\g<g1>" + new + "\g<g2>", line)
                        if rep != line:
                            if line_number in lines_changed:
                                skip_var = True
                            lines_changed.add(line_number)
                            diff.change_line(line_number, line, rep)
                            num_changes += 1
                            if first_line == -1:
                                first_line = line_number
                    if skip_var:
                        continue
                    msg = "Change '" + prev + "' to '" + new + "'"
                    if num_changes > 1:
                        msg += ": " + str(num_changes) + " lines affected"
                    result_texts.append(msg)
                    vio = "The following name changes are suggested:"
                    vio += "".join("\n- " + string
                                   for string in result_texts)
                    yield Result.from_values(
                        self,
                        vio,
                        diffs={filename: diff},
                        file=filename,
                        line=first_line)
                    result_texts = []
        else:
            self.warn("keywords and special_chars not defined for", language)
            self.warn("Not running VariableCasingBear")

    def all_to_camel(self, line):
        i = 1
        flast = 0
        if line[-1:] == "_":
            flast = 1
        end = len(line) - flast
        rep = line[:1].lower()
        while i < end:
            if line[i] == '_' and line[i + 1].islower():
                rep += line[i + 1].upper()
                i += 1
            else:
                rep += line[i]
            i += 1
        if flast:
            rep += line[-1:]
        return rep

    def all_to_pascal(self, line):
        camel = self.all_to_camel(line)
        camel = camel[0].upper() + camel[1:]
        return camel

    def all_to_snake(self, line):
        i = 1
        end = len(line)
        rep = line[:1].lower()
        while i < end:
            # We only want to change complete words, not abbreviations
            # Example: abcDef becomes abc_def
            # but abCDEf should be ab_CD_ef (better than ab_c_d_ef)
            if line[i].isupper() and line[i - 1].islower():
                rep += "_"
                rep += line[i].lower()
            else:
                rep += line[i]
            i += 1
        return rep
