import os
import unittest


from vsg import vhdlFile
from vsg import rule_list
from vsg import severity
from vsg.tests import utils

sSourceDir = os.path.join(os.path.dirname(__file__),'..','..','code_examples','graphicsaccelerator')

lBresenhamer = utils.read_vhdlfile(os.path.join(sSourceDir,'Bresenhamer.vhd'))
oBresenhamer = vhdlFile.vhdlFile(lBresenhamer)
lDebouncer = utils.read_vhdlfile(os.path.join(sSourceDir,'Debouncer.vhd'))
oDebouncer = vhdlFile.vhdlFile(lDebouncer)
lVgatop = utils.read_vhdlfile(os.path.join(sSourceDir,'VGA_Top.vhd'))
oVgatop = vhdlFile.vhdlFile(lVgatop)
lPointer = utils.read_vhdlfile(os.path.join(sSourceDir,'Pointer.vhd'))
oPointer = vhdlFile.vhdlFile(lPointer)
lFreqDiv = utils.read_vhdlfile(os.path.join(sSourceDir,'FreqDiv.vhd'))
oFreqDiv = vhdlFile.vhdlFile(lFreqDiv)
lSynchronizer = utils.read_vhdlfile(os.path.join(sSourceDir,'Synchronizer.vhd'))
oSynchronizer = vhdlFile.vhdlFile(lSynchronizer)
lFrameBuffer =  utils.read_vhdlfile(os.path.join(sSourceDir,'FrameBuffer2.vhd'))
oFrameBuffer =  vhdlFile.vhdlFile(lFrameBuffer)

dConfig = utils.read_configuration(os.path.join(os.path.dirname(__file__),'..','..','..','..','styles', 'jcl.yaml'))
dConfig['debug'] = False

oSeverityList = severity.create_list({})

class testCodeExample(unittest.TestCase):

    def test_bresenhamer(self):
        oRuleList = rule_list.rule_list(oBresenhamer, oSeverityList)
        oRuleList.configure(dConfig)
        oRuleList.fix()

        lExpected = ['']

        utils.read_file(os.path.join(os.path.dirname(__file__),'Bresenhamer.fixed.vhd'), lExpected)

        self.assertEqual(lExpected, oBresenhamer.get_lines())

    def test_debouncer(self):
        oRuleList = rule_list.rule_list(oDebouncer, oSeverityList)
        oRuleList.configure(dConfig)
        oRuleList.fix()

        lExpected = ['']

        utils.read_file(os.path.join(os.path.dirname(__file__),'Debouncer.fixed.vhd'), lExpected)

        self.assertEqual(lExpected, oDebouncer.get_lines())

    def test_vga_top(self):
        oRuleList = rule_list.rule_list(oVgatop, oSeverityList)
        oRuleList.configure(dConfig)
        oRuleList.fix()

        lExpected = ['']

        utils.read_file(os.path.join(os.path.dirname(__file__),'VGA_Top.fixed.vhd'), lExpected)

        self.assertEqual(lExpected, oVgatop.get_lines())

    def test_pointer(self):
        oRuleList = rule_list.rule_list(oPointer, oSeverityList)
        oRuleList.configure(dConfig)
        oRuleList.fix()

        lExpected = ['']

        utils.read_file(os.path.join(os.path.dirname(__file__),'Pointer.fixed.vhd'), lExpected)

        self.assertEqual(lExpected, oPointer.get_lines())

    def test_freqdiv(self):
        oRuleList = rule_list.rule_list(oFreqDiv, oSeverityList)
        oRuleList.configure(dConfig)
        oRuleList.fix()

        lExpected = ['']

        utils.read_file(os.path.join(os.path.dirname(__file__),'FreqDiv.fixed.vhd'), lExpected)

        self.assertEqual(lExpected, oFreqDiv.get_lines())

    def test_synchronizer(self):
        oRuleList = rule_list.rule_list(oSynchronizer, oSeverityList)
        oRuleList.configure(dConfig)
        oRuleList.fix()

        lExpected = ['']

        utils.read_file(os.path.join(os.path.dirname(__file__),'Synchronizer.fixed.vhd'), lExpected)

        self.assertEqual(lExpected, oSynchronizer.get_lines())

    def test_framebuffer(self):
        oRuleList = rule_list.rule_list(oFrameBuffer, oSeverityList)
        oRuleList.configure(dConfig)
        oRuleList.fix()

        lExpected = ['']

        utils.read_file(os.path.join(os.path.dirname(__file__),'FrameBuffer2.fixed.vhd'), lExpected)

        self.assertEqual(lExpected, oFrameBuffer.get_lines())
