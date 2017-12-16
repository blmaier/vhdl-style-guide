import os
import sys
import unittest


from vsg import vhdlFile
from vsg import rule_list
from vsg.tests import utils

oIteration = vhdlFile.vhdlFile(os.path.join(os.path.dirname(__file__),'iteration_synth.vhd'))


class testCodeExample(unittest.TestCase):

    def test_iteration_synth(self):
        oRuleList = rule_list.list(oIteration)
        oRuleList.fix()
        lExpected = ['']
        utils.read_file(os.path.join(os.path.dirname(__file__),'iteration_synth.fixed.vhd'), lExpected)
        for iLineNumber, sLine in enumerate(lExpected):
            self.assertEqual(oIteration.lines[iLineNumber].line, sLine)