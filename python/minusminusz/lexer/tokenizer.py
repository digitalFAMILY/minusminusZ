# -*- coding: utf-8 -*-
"""
    minusminusz.lexer.tokenizer
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tokenize by char or feed

    :copyright: 12.2013 by Markus Ullmann
"""

from minusminusz.exceptions import *

# Tokens
(
    TOKEN_COMMAND, TOKEN_COMMENT,
    TOKEN_STRING, TOKEN_NUMBER,
    TOKEN_NEWLINE
) = range(0,5)
def _map_numbers_to_names():
    tokens = {}
    for name, value in globals().iteritems():
        if name.startswith("TOKEN_"):
            tokens[value] = name
    return tokens

# Parser states
(
    STATE_NEW, STATE_COMMAND,
    STATE_STRING, STATE_NUMBER,
    STATE_COMMENT_DETECT, STATE_COMMENT,
) = range(0,6)

# char categories
_WHITESPACES = "\t "
_COMMENT_SINGLE_CHARS = "#"
_COMMENT_MULTI_CHARS = "/"

# asterisk export definition
__all__ = (
    'MMZToken', 'MMZTokenizer',
) + tuple(_map_numbers_to_names().values())


class MMZToken(object):
    """Holds splitted data from a stream"""

    __slots__ = ('tokentype', 'content')

    def __init__(self, tokentype, content):
        self.tokentype = tokentype
        self.content = content

    def __eq__(self, other):
        return self.tokentype == other.tokentype and self.content == other.content

    def __repr__(self):
        # map token type to name
        types = dict()
        for name, value in globals().iteritems():
            if name.startswith("TOKEN_"):
                types[value] = name
        if self.content is None:
            return "<%s type %s>" % (self.__class__.__name__, types[self.tokentype])
        elif len(self.content) == 1:
            if ord(self.content) > 31:
                return "<%s type %s content char '%s'>" % (self.__class__.__name__, types[self.tokentype], self.content)
            else:
                return "<%s type %s content byte %s>" % (self.__class__.__name__, types[self.tokentype], ord(self.content))
        else:
            return "<%s type %s content %s length %s>" % (self.__class__.__name__, types[self.tokentype], self.content, len(self.content))



class MMZTokenizer(object):
    """Yields MMZTokens from given data"""

    def __init__(self):
        self.comment_char_count = 0
        self.line = 1
        self.lineposition = 1
        self.state = STATE_NEW
        self.result = []

    def __process_byte(self, byte):
        """Processes exactly one byte, returns token if token is complete"""

        self.lineposition += 1

        # PyPy optimization
        current_state = self.state

        # starting a new token:
        #import pdb;pdb.set_trace()
        if current_state is STATE_NEW:
            if byte == '\n':
                self.line += 1
                return MMZToken(TOKEN_NEWLINE, None)
            elif byte in _COMMENT_SINGLE_CHARS:
                self.state = STATE_COMMENT
            elif byte in _COMMENT_MULTI_CHARS:
                self.state = STATE_COMMENT_DETECT
                self.comment_char_count = 1
            elif 0 <= ord(byte) < 32:
                self.state = STATE_COMMAND
                self.result.append(byte)
            elif 33 <= ord(byte) < 127:
                self.state = STATE_STRING
                self.result.append(byte)
            else:
                raise UnexpectedByteError(byte, self.line)

        # comment?
        elif current_state is STATE_COMMENT_DETECT:
            if byte in _COMMENT_MULTI_CHARS:
                self.comment_char_count += 1
                if self.comment_char_count == 3:
                    self.state = STATE_COMMENT
            elif byte and byte in _WHITESPACES:
                content = _COMMENT_MULTI_CHARS * self.comment_char_count
                self.state = STATE_NEW
                return MMZToken(TOKEN_STRING, content)
            elif byte and byte == "\n":
                content = _COMMENT_MULTI_CHARS * self.comment_char_count
                self.state = STATE_NEW
                return MMZToken(TOKEN_STRING, content), MMZToken(TOKEN_NEWLINE, None)
            else:
                self.result.extend(_COMMENT_MULTI_CHARS * self.comment_char_count)
                self.state = STATE_STRING

        # comment!
        elif current_state is STATE_COMMENT:
            # comments automatically end on line break
            if byte and byte == "\n":
                content = "".join(self.result)
                self.result = []
                self.state = STATE_NEW
                return MMZToken(TOKEN_COMMENT, content), MMZToken(TOKEN_NEWLINE, None)
            else:
                self.result.append(byte)

        # commands are one byte atm followed by whitespace
        elif current_state is STATE_COMMAND:
            if byte in _WHITESPACES:
                content = "".join(self.result)
                self.state = STATE_NEW
                self.result = []
                return MMZToken(TOKEN_COMMAND, content)
            else:
                # when multibyte commands are wanted, modify here
                raise TokenizerContentError("Unexpected multibyte COMMAND on line %i" % self.line)

        # strings
        elif current_state is STATE_STRING:
            if byte and byte in _WHITESPACES:
                self.state = STATE_NEW
                content = "".join(self.result)
                self.result = []
                return MMZToken(TOKEN_STRING, content)
            elif byte and byte == "\n":
                self.state = STATE_NEW
                content = "".join(self.result)
                self.result = []
                return MMZToken(TOKEN_STRING, content), MMZToken(TOKEN_NEWLINE, None)
            else:
                self.result.append(byte)

    def feed(self, data):
        """Tokenize stream as data comes in, to be called many times, don't forget to finalize."""

        for byte in data:
            retval = self.__process_byte(byte)
            if retval is not None:
                # Yield tokens directly, iter over lists if they come back from process char
                # this should really be changed later...
                if isinstance(retval, MMZToken):
                    yield retval
                else:
                    for listentry in retval:
                        if listentry is not None:
                            yield listentry

    def finalize(self):
        if self.state in [STATE_STRING, STATE_NUMBER, STATE_COMMAND]:
            yield self.feed("\n")
        self.line = 1
