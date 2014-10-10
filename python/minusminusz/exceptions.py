# -*- coding: utf-8 -*-
"""
    minusminusz.exceptions
    ~~~~~~~~~~~~~~~~~~~~~~

    Implementation for all raised Exceptions

    :copyright: 12.2013 by Markus Ullmann
"""


class MMZBaseException(Exception):
    """Base class for all exceptions raised"""

    pass


class TokenizerContentError(MMZBaseException):
    """Raised whenever an error occurs during tokenization"""

    pass


class UnexpectedByteError(TokenizerContentError):
    """Raised during tokenizing if an unexpected byte appears"""

    def __init__(self, byte, line=0):
        self.byte = byte
        self.line = line

    def __str__(self):
        return "Byte '%s' was not expected on line %i" % (
            ord(self.byte),
            self.line
        )


class UnexpectedTokenError(MMZBaseException):
    """Raised when an unexpected token appears"""

    def __init__(self, token, line=0):
        self.line = line
        self.token = token

    def __str__(self):
        return "Token '%s' was not expected on line %i" % (
            repr(self.token),
            self.line
        )


class UnexpectedNodeError(MMZBaseException):
    """Raised when unexpected node is found during file class build"""

    def __init__(self, node, line=0):
        self.line = line
        self.node = node

    def __str__(self):
        if self.line:
            return "Node '%s' was not expected on line %i" % (
                repr(self.node),
                self.line
            )
        else:
            return "Node '%s' was not expected" % (
                repr(self.node)
            )


class IncompleteDocumentError(MMZBaseException):
    """Raised when parser finalizes but last node is not root"""

    pass
