
from vsg.rules import single_space_after_token as Rule

from vsg.token import alias_declaration as token


class rule_100(Rule):
    '''
    This rule checks for a single space after the colon for the subtype_indication.

    **Violation**

    .. code-block:: vhdl

       alias alias_designator :    subtype_indication is name;
       alias alias_designator :subtype_indication is name;

    **Fix**

    .. code-block:: vhdl

       alias alias_designator : subtype_indication is name;
       alias alias_designator : subtype_indication is name;
    '''
    def __init__(self):
        Rule.__init__(self, 'alias_declaration', '100', [token.colon])
        self.solution = 'Ensure a single space after :.'