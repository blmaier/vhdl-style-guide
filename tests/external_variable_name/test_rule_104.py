# -*- coding: utf-8 -*-

import os
import unittest

from tests import utils
from vsg import vhdlFile
from vsg.rules import external_variable_name

sTestDir = os.path.dirname(__file__)

lFile, eError = vhdlFile.utils.read_vhdlfile(os.path.join(sTestDir, "rule_104_test_input.vhd"))


class test_rule(unittest.TestCase):
    def setUp(self):
        self.oFile = vhdlFile.vhdlFile(lFile)
        self.assertIsNone(eError)

    def test_rule_104(self):
        oRule = external_variable_name.rule_104()
        self.assertTrue(oRule)
        self.assertEqual(oRule.name, "external_variable_name")
        self.assertEqual(oRule.identifier, "104")

        lExpected = [12, 13]

        oRule.analyze(self.oFile)
        self.assertEqual(lExpected, utils.extract_violation_lines_from_violation_object(oRule.violations))

    def test_fix_rule_104(self):
        oRule = external_variable_name.rule_104()
        oRule.indent_style = "spaces"

        oRule.fix(self.oFile)

        lActual = self.oFile.get_lines()

        lExpected_spaces = []
        lExpected_spaces.append("")
        utils.read_file(os.path.join(sTestDir, "rule_104_test_input.fixed.vhd"), lExpected_spaces)

        self.assertEqual(lExpected_spaces, lActual)

        oRule.analyze(self.oFile)
        self.assertEqual(oRule.violations, [])