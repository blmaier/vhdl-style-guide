# -*- coding: utf-8 -*-

from vsg import parser
from vsg.token import external_variable_name as token
from vsg.vhdlFile import utils
from vsg.vhdlFile.classify import subtype_indication


def detect(iToken, lObjects):
    """
    external_variable_name ::=
        << variable external_pathname : subtype_indication >>
    """

    if utils.are_next_consecutive_tokens(["<<", "variable"], iToken, lObjects):
        return classify(iToken, lObjects)

    return iToken


def classify(iToken, lObjects):
    iCurrent = utils.assign_next_token_required("<<", token.double_less_than, iToken, lObjects)
    iCurrent = utils.assign_next_token_required("variable", token.variable_keyword, iToken, lObjects)
    iCurrent = utils.assign_next_token(token.external_pathname, iToken, lObjects)

    iCurrent = utils.assign_parenthesis_as_todo(iCurrent, lObjects)

    iCurrent = utils.assign_next_token_required(":", token.colon, iCurrent, lObjects)

    iCurrent = subtype_indication.classify(iCurrent, lObjects)

    iCurrent = utils.assign_next_token_required(">>", token.double_greater_than, iToken, lObjects)

    return iCurrent