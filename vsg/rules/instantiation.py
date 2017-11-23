
from vsg import rule
from vsg import line
import re
import copy


class instantiation_rule(rule.rule):

    def __init__(self):
        rule.rule.__init__(self)
        self.name = 'instantiation'


class rule_001(instantiation_rule):
    '''
    Instantiation rule 001 checks for proper indent of instantiations.
    '''

    def __init__(self):
        instantiation_rule.__init__(self)
        self.identifier = '001'
        self.solution = 'Ensure proper indentation.'
        self.phase = 4

    def analyze(self, oFile):
        for iLineNumber, oLine in enumerate(oFile.lines):
            if oLine.isInstantiationDeclaration or oLine.isInstantiationPortAssignment or oLine.isInstantiationPortEnd or oLine.isInstantiationPortKeyword or oLine.isInstantiationGenericAssignment or oLine.isInstantiationGenericEnd or oLine.isInstantiationGenericKeyword:
                self._check_indent(oLine, iLineNumber)

    def _fix_violations(self, oFile):
        for iLineNumber in self.violations:
            self._fix_indent(oFile.lines[iLineNumber])


class rule_002(instantiation_rule):
    '''
    Instantiation rule 002 checks for a single space after the :
    '''

    def __init__(self):
        instantiation_rule.__init__(self)
        self.identifier = '002'
        self.solution = 'Ensure only one space after the :.'
        self.phase = 2

    def analyze(self, oFile):
        for iLineNumber, oLine in enumerate(oFile.lines):
            if oLine.isInstantiationDeclaration:
                if not re.match('^\s*\S+\s*:\s\S', oLine.line):
                    self.add_violation(iLineNumber)

    def _fix_violations(self, oFile):
        for iLineNumber in self.violations:
            self._enforce_one_space_after_word(oFile.lines[iLineNumber], ':')


class rule_003(instantiation_rule):
    '''
    Instantiation rule 003 checks for a single space before the :
    '''

    def __init__(self):
        instantiation_rule.__init__(self)
        self.identifier = '003'
        self.solution = 'Ensure only one space before the :.'
        self.phase = 2

    def analyze(self, oFile):
        for iLineNumber, oLine in enumerate(oFile.lines):
            if oLine.isInstantiationDeclaration:
                if not re.match('^\s*\S+\s:', oLine.line):
                    self.add_violation(iLineNumber)

    def _fix_violations(self, oFile):
        for iLineNumber in self.violations:
            self._enforce_one_space_before_word(oFile.lines[iLineNumber], ':')


class rule_004(instantiation_rule):
    '''
    Instantiation rule 004 checks for a blank line above the instantiation declaration.
    '''

    def __init__(self):
        instantiation_rule.__init__(self)
        self.identifier = '004'
        self.solution = 'Add blank line above instantiation declaration.'
        self.phase = 3

    def analyze(self, oFile):
        lFailureLines = []
        for iLineNumber, oLine in enumerate(oFile.lines):
            if oLine.isInstantiationDeclaration:
                self._is_blank_line_before(oFile, iLineNumber)

    def _fix_violations(self, oFile):
        for iLineNumber in self.violations[::-1]:
            self._insert_blank_line_above(oFile, iLineNumber)


class rule_005(instantiation_rule):
    '''
    Instantiation rule 005 checks the instantiation declaration and "port map" keywords are not on the same line.
    '''

    def __init__(self):
        instantiation_rule.__init__(self)
        self.identifier = '005'
        self.solution = 'Place "port map" keywords on the next line by itself'
        self.phase = 1

    def analyze(self, oFile):
        for iLineNumber, oLine in enumerate(oFile.lines):
            if oLine.isInstantiationDeclaration:
                if oLine.isInstantiationPortKeyword:
                    self.add_violation(iLineNumber)

    def _fix_violations(self, oFile):
        for iLineNumber in self.violations:
            oLine = oFile.lines[iLineNumber]
            iIndex = oLine.lineLower.find(' port ')
            oFile.lines.insert(iLineNumber + 1, copy.deepcopy(oLine))
            oLine.update_line(oLine.line[:iIndex])
            oLine.isInstantiationPortKeyword = False
            oLine = oFile.lines[iLineNumber + 1]
            oLine.update_line(oLine.line[iIndex:])
            oLine.isInstantiationDeclaration = False


class rule_006(instantiation_rule):
    '''
    Instantiation rule 006 checks the "port map" keywords are lower case.
    '''

    def __init__(self):
        instantiation_rule.__init__(self)
        self.identifier = '006'
        self.solution = 'Change "port map" keywords to lowercase.'
        self.phase = 6

    def analyze(self, oFile):
        for iLineNumber, oLine in enumerate(oFile.lines):
            if oLine.isInstantiationPortKeyword:
                if not re.match('^.*port\s+map', oLine.line):
                    self.add_violation(iLineNumber)

    def _fix_violations(self, oFile):
        for iLineNumber in self.violations:
            self._lower_case(oFile.lines[iLineNumber], 'port')
            self._lower_case(oFile.lines[iLineNumber], 'map')


class rule_007(instantiation_rule):
    '''
    Instantiation rule 007 checks the closing ) for the port map is on it's own line.
    '''

    def __init__(self):
        instantiation_rule.__init__(self)
        self.identifier = '007'
        self.solution = 'Place closing ); on it\'s own line.'
        self.phase = 1

    def analyze(self, oFile):
        for iLineNumber, oLine in enumerate(oFile.lines):
            if oLine.isInstantiationPortEnd and oLine.isInstantiationPortAssignment:
                self.add_violation(iLineNumber)

    def _fix_violations(self, oFile):
        for iLineNumber in self.violations[::-1]:
            oFile.lines[iLineNumber].line = re.sub(r'\)(\s*);', r' \1 ', oFile.lines[iLineNumber].line)
            oFile.lines[iLineNumber].isInstantiationPortEnd = False
            oFile.lines.insert(iLineNumber + 1, line.line('  );'))
            oFile.lines[iLineNumber + 1].isInstantiationPortAssignement = False
            oFile.lines[iLineNumber + 1].indentLevel = oFile.lines[iLineNumber].indentLevel - 1


class rule_008(instantiation_rule):
    '''
    Instantiation rule 008 checks the instance name is uppercase in the instantiation declaration line.
    '''

    def __init__(self):
        instantiation_rule.__init__(self)
        self.identifier = '008'
        self.solution = 'Change instance name to all uppercase.'
        self.phase = 6

    def analyze(self, oFile):
        for iLineNumber, oLine in enumerate(oFile.lines):
            if oLine.isInstantiationDeclaration:
                self._is_uppercase(oLine.line.split()[0], iLineNumber)

    def _fix_violations(self, oFile):
        for iLineNumber in self.violations:
            self._upper_case(oFile.lines[iLineNumber], oFile.lines[iLineNumber].line.split()[0])


class rule_009(instantiation_rule):
    '''
    Instantiation rule 009 checks the entity name is uppercase in the instantiation declaration line.
    '''

    def __init__(self):
        instantiation_rule.__init__(self)
        self.identifier = '009'
        self.solution = 'Change entity name to all uppercase.'
        self.phase = 6

    def analyze(self, oFile):
        for iLineNumber, oLine in enumerate(oFile.lines):
            if oLine.isInstantiationDeclaration:
                if re.match('^\s*\w+\s+:\s+\w+', oLine.line):
                    self._is_uppercase(oLine.line.split()[2], iLineNumber)
                elif re.match('^\s*\w+:\w+', oLine.line):
                    lLine = oLine.line.split(':')[1].split()
                    self._is_uppercase(lLine[0], iLineNumber)
                else:
                    self._is_uppercase(oLine.line.split()[1], iLineNumber)

    def _fix_violations(self, oFile):
        for iLineNumber in self.violations:
            oLine = oFile.lines[iLineNumber]
            sLine = oLine.line.split(':')[1].split()[0]
            self._upper_case(oFile.lines[iLineNumber], sLine)


class rule_010(instantiation_rule):
    '''
    Instantiation rule 010 ensures the alignment of the => operator for every port in the instantiation.
    '''

    def __init__(self):
        instantiation_rule.__init__(self)
        self.identifier = '010'
        self.solution = 'Inconsistent alignment of "=>" in port assignments of instantiation.'
        self.phase = 5

    def analyze(self, oFile):
        lGroup = []
        fGroupFound = False
        iStartGroupIndex = None
        for iLineNumber, oLine in enumerate(oFile.lines):
            if oLine.isInstantiationPortKeyword and not fGroupFound:
                fGroupFound = True
                iStartGroupIndex = iLineNumber
            if oLine.isInstantiationPortEnd:
                lGroup.append(oLine)
                fGroupFound = False
                self._check_keyword_alignment(iStartGroupIndex, '=>', lGroup)
                lGroup = []
                iStartGroupIndex = None
            if fGroupFound:
                if oLine.isInstantiationPortAssignment and not oLine.isInstantiationPortKeyword:
                    lGroup.append(oLine)
                else:
                    lGroup.append(line.line('Removed line'))

    def _fix_violations(self, oFile):
        self._fix_keyword_alignment(oFile)


class rule_011(instantiation_rule):
    '''
    Instantiation rule 011 checks the port name is uppercase.
    '''

    def __init__(self):
        instantiation_rule.__init__(self)
        self.identifier = '011'
        self.solution = 'Uppercase port name.'
        self.phase = 6

    def analyze(self, oFile):
        for iLineNumber, oLine in enumerate(oFile.lines):
            if oLine.isInstantiationPortAssignment and not oLine.isInstantiationPortKeyword:
                self._is_uppercase(oLine.line.split()[0], iLineNumber)

    def _fix_violations(self, oFile):
        for iLineNumber in self.violations:
            oLine = oFile.lines[iLineNumber]
            self._upper_case(oLine, oLine.line.split()[0])


class rule_012(instantiation_rule):
    '''
    Instantiation rule 012 checks the instantiation declaration and "generic map" keywords are not on the same line.
    '''

    def __init__(self):
        instantiation_rule.__init__(self)
        self.identifier = '012'
        self.solution = 'Place "generic map" keywords on the next line by itself'
        self.phase = 1

    def analyze(self, oFile):
        for iLineNumber, oLine in enumerate(oFile.lines):
            if oLine.isInstantiationDeclaration:
                if oLine.isInstantiationGenericKeyword:
                    self.add_violation(iLineNumber)

    def _fix_violations(self, oFile):
        for iLineNumber in self.violations:
            oLine = oFile.lines[iLineNumber]
            iIndex = oLine.lineLower.find(' generic ')
            oFile.lines.insert(iLineNumber + 1, copy.deepcopy(oLine))
            oLine.update_line(oLine.line[:iIndex])
            oLine.isInstantiationGenericKeyword = False
            oLine = oFile.lines[iLineNumber + 1]
            oLine.update_line(oLine.line[iIndex:])
            oLine.isInstantiationDeclaration = False


class rule_013(instantiation_rule):
    '''
    Instantiation rule 013 checks the "generic map" keywords are lower case.
    '''

    def __init__(self):
        instantiation_rule.__init__(self)
        self.identifier = '013'
        self.solution = 'Change "generic map" keywords to lowercase.'
        self.phase = 6

    def analyze(self, oFile):
        for iLineNumber, oLine in enumerate(oFile.lines):
            if oLine.isInstantiationGenericKeyword:
                if not re.match('^.*generic\s+map', oLine.line):
                    self.add_violation(iLineNumber)

    def _fix_violations(self, oFile):
        for iLineNumber in self.violations:
            self._lower_case(oFile.lines[iLineNumber], 'generic')
            self._lower_case(oFile.lines[iLineNumber], 'map')


class rule_014(instantiation_rule):
    '''
    Instantiation rule 014 checks the closing ) for the generic map is on it's own line.
    '''

    def __init__(self):
        instantiation_rule.__init__(self)
        self.identifier = '014'
        self.solution = 'Place closing ) on it\'s own line.'
        self.phase = 1

    def analyze(self, oFile):
        for iLineNumber, oLine in enumerate(oFile.lines):
            if oLine.isInstantiationGenericEnd and (oLine.isInstantiationGenericAssignment or oLine.isInstantiationGenericKeyword):
                self.add_violation(iLineNumber)

    def _fix_violations(self, oFile):
        for iLineNumber in self.violations[::-1]:
            oFile.lines[iLineNumber].line = re.sub(r'\)(\s*);', r' \1 ', oFile.lines[iLineNumber].line)
            oFile.lines[iLineNumber].isInstantiationGenericEnd = False
            oFile.lines.insert(iLineNumber + 1, line.line('  );'))
            oFile.lines[iLineNumber + 1].isInstantiationGenericAssignement = False
            oFile.lines[iLineNumber + 1].indentLevel = oFile.lines[iLineNumber].indentLevel - 1


class rule_015(instantiation_rule):
    '''
    Instantiation rule 015 ensures the alignment of the => operator for every generic in the instantiation.
    '''

    def __init__(self):
        instantiation_rule.__init__(self)
        self.identifier = '015'
        self.solution = 'Inconsistent alignment of "=>" in generic assignments of instantiation.'
        self.phase = 5

    def analyze(self, oFile):
        lGroup = []
        fGroupFound = False
        iStartGroupIndex = None
        for iLineNumber, oLine in enumerate(oFile.lines):
            if oLine.isInstantiationGenericKeyword and not fGroupFound:
                fGroupFound = True
                iStartGroupIndex = iLineNumber
            if oLine.isInstantiationGenericEnd:
                lGroup.append(oLine)
                fGroupFound = False
                self._check_keyword_alignment(iStartGroupIndex, '=>', lGroup)
                lGroup = []
                iStartGroupIndex = None
            if fGroupFound:
                if oLine.isInstantiationGenericAssignment:
                    lGroup.append(oLine)
                else:
                    lGroup.append(line.line('Removed line'))

    def _fix_violations(self, oFile):
        self._fix_keyword_alignment(oFile)


class rule_016(instantiation_rule):
    '''
    Instantiation rule 016 checks the generic name is uppercase.
    '''

    def __init__(self):
        instantiation_rule.__init__(self)
        self.identifier = '016'
        self.solution = 'Uppercase generic name.'
        self.phase = 6

    def analyze(self, oFile):
        for iLineNumber, oLine in enumerate(oFile.lines):
            if oLine.isInstantiationGenericAssignment and not oLine.isInstantiationGenericKeyword:
                self._is_uppercase(oLine.line.split()[0], iLineNumber)

    def _fix_violations(self, oFile):
        for iLineNumber in self.violations:
            lLine = oFile.lines[iLineNumber].line.split('=>')
            self._upper_case(oFile.lines[iLineNumber], lLine[0].rstrip().lstrip())


class rule_017(instantiation_rule):
    '''
    Instantiation rule 016 checks for generic map keyword and generic assignment on the same line.
    '''

    def __init__(self):
        instantiation_rule.__init__(self)
        self.identifier = '017'
        self.solution = 'Move generic assignment to it\'s own line.'
        self.phase = 1

    def analyze(self, oFile):
        for iLineNumber, oLine in enumerate(oFile.lines):
            if oLine.isInstantiationGenericAssignment and oLine.isInstantiationGenericKeyword:
                self.add_violation(iLineNumber)

    def _fix_violations(self, oFile):
        for iLineNumber in self.violations[::-1]:
            oFile.lines.insert(iLineNumber + 1, copy.deepcopy(oFile.lines[iLineNumber]))
            oLine = oFile.lines[iLineNumber]
            oLine.update_line(oLine.line.split('(')[0] + ' (')
            oLine.isInstantiationGenericAssignment = False
            oLine = oFile.lines[iLineNumber + 1]
            oLine.update_line('  ' + oLine.line.split('(')[1])
            oLine.isInstantiationGenericKeyword = False


class rule_018(instantiation_rule):
    '''
    Instantiation rule 018 checks for a single space between map and (
    '''

    def __init__(self):
        instantiation_rule.__init__(self)
        self.identifier = '018'
        self.solution = 'Ensure a single space exists between "map" and (.'
        self.phase = 2

    def analyze(self, oFile):
        for iLineNumber, oLine in enumerate(oFile.lines):
            if oLine.isInstantiationGenericKeyword or oLine.isInstantiationPortKeyword:
                if not re.match('^.*\smap\s\(', oLine.lineLower):
                    self.add_violation(iLineNumber)

    def _fix_violations(self, oFile):
        for iLineNumber in self.violations:
            self._enforce_one_space_after_word(oFile.lines[iLineNumber], 'map')


class rule_019(instantiation_rule):
    '''
    Instantiation rule 019 checks for a blank line below the end of the port declaration.
    '''

    def __init__(self):
        instantiation_rule.__init__(self)
        self.identifier = '019'
        self.solution = 'Add blank line below instantiation declaration.'
        self.phase = 3

    def analyze(self, oFile):
        lFailureLines = []
        for iLineNumber, oLine in enumerate(oFile.lines):
            if oLine.isInstantiationPortEnd:
                self._is_blank_line_after(oFile, iLineNumber)

    def _fix_violations(self, oFile):
        for iLineNumber in self.violations[::-1]:
            self._insert_blank_line_below(oFile, iLineNumber)


class rule_020(instantiation_rule):
    '''
    Instantiation rule 020 checks for a port assignment on the same line as the port map keywords.
    '''

    def __init__(self):
        instantiation_rule.__init__(self)
        self.identifier = '020'
        self.solution = 'Move port assignment to it\'s own line.'
        self.phase = 1

    def analyze(self, oFile):
        lFailureLines = []
        for iLineNumber, oLine in enumerate(oFile.lines):
            if oLine.isInstantiationPortAssignment and oLine.isInstantiationPortKeyword:
                self.add_violation(iLineNumber)

    def _fix_violations(self, oFile):
        for iLineNumber in self.violations[::-1]:
            oFile.lines.insert(iLineNumber + 1, copy.deepcopy(oFile.lines[iLineNumber]))
            oLine = oFile.lines[iLineNumber]
            oLine.update_line(oLine.line.split('(')[0] + ' (')
            oLine.isInstantiationPortAssignment = False
            oLine = oFile.lines[iLineNumber + 1]
            oLine.update_line('  ' + oLine.line.split('(')[1])
            oLine.isInstantiationPortKeyword = False


class rule_021(instantiation_rule):
    '''
    Instantiation rule 021 checks multiple port assignments on the same line.
    '''

    def __init__(self):
        instantiation_rule.__init__(self)
        self.identifier = '021'
        self.solution = 'Move multiple port assignments to their own lines.'
        self.phase = 1

    def analyze(self, oFile):
        lFailureLines = []
        for iLineNumber, oLine in enumerate(oFile.lines):
            if oLine.isInstantiationPortAssignment:
                if re.match('^\s*\S+\s*=>\s*\S+,\s*\S+\s*=>', oLine.line):
                    self.add_violation(iLineNumber)

    def _fix_violations(self, oFile):
        for iLineNumber in self.violations[::-1]:
            oLine = oFile.lines[iLineNumber]
            iNumberOfPorts = oLine.line.count(',') + 1
            # Replicate ports ###
            for iIndex in range(1, iNumberOfPorts):
                oFile.lines.insert(iLineNumber, copy.deepcopy(oLine))
            # Split ports
            for iIndex in range(0, iNumberOfPorts):
                oLine = oFile.lines[iLineNumber + iIndex]
                lPorts = oLine.line.split(',')
                oLine.update_line(lPorts[iIndex] + ',')


class rule_022(instantiation_rule):
    '''
    Instantiation rule 022 checks for a single space after the => operator.
    '''

    def __init__(self):
        instantiation_rule.__init__(self)
        self.identifier = '022'
        self.solution = 'Only a single space after => operator.'
        self.phase = 2

    def analyze(self, oFile):
        lFailureLines = []
        for iLineNumber, oLine in enumerate(oFile.lines):
            if oLine.isInstantiationPortAssignment and not oLine.isInstantiationPortKeyword:
                if not re.match('^.*=>\s\S+', oLine.line):
                    self.add_violation(iLineNumber)

    def _fix_violations(self, oFile):
        for iLineNumber in self.violations:
            self._enforce_one_space_after_word(oFile.lines[iLineNumber], '=>')
