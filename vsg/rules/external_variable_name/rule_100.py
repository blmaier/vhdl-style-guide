# -*- coding: utf-8 -*-

from vsg.rules.whitespace_between_tokens import Rule
from vsg.token import external_variable_name as token


class rule_100(Rule):
    """
    This rule checks for a single space after the double less than.

    |configuring_whitespace_rules_link|

    **Violation**

    .. code-block:: vhdl

       <<     variable dut.fifo.wr_en : std_logic >>
       <<variable dut.fifo.wr_en : std_logic >>

    **Fix**

    .. code-block:: vhdl

       << variable dut.fifo.wr_en : std_logic >>
       << variable dut.fifo.wr_en : std_logic >>
    """

    def __init__(self):
        Rule.__init__(self)
        self.left_token = token.double_less_than
        self.right_token = token.variable_keyword