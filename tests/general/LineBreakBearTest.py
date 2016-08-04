import os
import unittest
from queue import Queue

from coalib.settings.Section import Section
from coalib.settings.Setting import Setting
from coala_utils.string_processing.Core import escape
from bears.general.LineBreakBear import LineBreakBear
from bears.general.AnnotationBear import AnnotationBear
from bears.general.LineLengthBear import LineLengthBear


class LineBreakBearTest(unittest.TestCase):

    def setUp(self):
        self.section = Section("")
        self.section.append(Setting('language', 'test'))
        self.section.append(Setting('max_line_length', 10))
        self.section.append(Setting('coalang_dir', escape(os.path.join(
            os.path.dirname(__file__), "test_files"), '\\')))
        self.annot_uut = AnnotationBear(self.section, Queue())

    def get_results(self, file, section=None):
        if section is None:
            section = self.section
        annot_results = self.annot_uut.execute("file", file)
        uut = LineBreakBear(section, Queue())
        arg_dict = {'dependency_results':
                    {AnnotationBear.__name__:
                     list(annot_results)},
                    'file': file}
        return list(uut.run_bear_from_section(["file"], arg_dict))

    def test_break_on_encapsulators(self):

        file = "text(greater than 10 letters)\n".splitlines(True)

        changed_file = ("text(\n"
                        "    greater than 10 letters)\n").splitlines(True)

        results = self.get_results(file)

        self.assertEqual(changed_file, results[0].diffs["file"].modified)

        file = "func(p1,(p2,p3,p4,p5))\n".splitlines(True)

        changed_file = ("func(p1,(\n"
                        "    p2,p3,p4,p5))\n").splitlines(True)
        results = self.get_results(file)

        self.assertEqual(changed_file, results[0].diffs["file"].modified)

        # Testing encapsulator after max_line_length
        file = "very_very_long_func(p1)\n".splitlines(True)
        results = self.get_results(file)
        self.assertEqual(results, [])

        # Test different types of encapsulators
        file = "func(p1,[p2,p3,p4,p5])\n".splitlines(True)
        changed_file = ("func(p1,[\n"
                        "    p2,p3,p4,p5])\n").splitlines(True)
        results = self.get_results(file)
        self.assertEqual(changed_file, results[0].diffs["file"].modified)

    def test_settings(self):

        file = "func(p1,(p2,p3,p4,p5))\n".splitlines(True)

        changed_file = ("func(p1,(\n"
                        "\tp2,p3,p4,p5))\n").splitlines(True)
        self.section.append(Setting('use_spaces', False))
        results = self.get_results(file)

        self.assertEqual(changed_file, results[0].diffs["file"].modified)
