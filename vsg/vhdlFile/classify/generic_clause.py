
from vsg.token import generic_clause as token


def beginning(dVars, lObjects):
    '''
    Classifies generic clauses:

        generic ( generic_list ) ;
    '''
    for iObject, oObject in enumerate(lObjects):
        if not dVars['bGenericClauseKeywordFound']:
            classify_keyword(oObject, iObject, lObjects, dVars)
        else:
            if not dVars['bGenericClauseOpenParenthesisFound']:
                classify_open_parenthesis(oObject, iObject, lObjects, dVars)

def classify_keyword(oObject, iObject, lObjects, dVars):
    sValue = oObject.get_value()
    if sValue.lower() == 'generic':
        lObjects[iObject] = token.keyword(sValue)
        dVars['bGenericClauseKeywordFound'] = True


def classify_open_parenthesis(oObject, iObject, lObjects, dVars):
    if oObject.get_value() == '(':
        lObjects[iObject] = token.open_parenthesis()
        dVars['bGenericClauseOpenParenthesisFound'] = True


def ending(dVars, lObjects):
    '''
    Classifies generic clauses:

        generic ( generic_list ) ;
    '''
    for iObject, oObject in enumerate(lObjects):
        classify_close_parenthesis(oObject, iObject, lObjects, dVars)
        classify_semicolon(oObject, iObject, lObjects, dVars)


def classify_close_parenthesis(oObject, iObject, lObjects, dVars):
    if oObject.get_value() == ')':
        lObjects[iObject] = token.close_parenthesis()


def classify_semicolon(oObject, iObject, lObjects, dVars):
    if oObject.get_value() == ';':
        lObjects[iObject] = token.semicolon()
        dVars['bGenericClauseKeywordFound'] = False
        dVars['bGenericClauseOpenParenthesisFound'] = False