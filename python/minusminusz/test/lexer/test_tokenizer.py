# -*- coding: utf-8 -*-
"""
    minusminusz.test.lexer
    ~~~~~~~~~~~~~~~~~~~~~~

    Checks lexer implementation parts to actually do something useful

    :copyright: 10.2014 by Markus Ullmann
"""

import unittest

from minusminusz.lexer.tokenizer import (
	TOKEN_COMMAND, TOKEN_COMMENT,
    TOKEN_STRING, TOKEN_NUMBER,
    TOKEN_NEWLINE,
    MMZToken, MMZTokenizer
)

class TokenizerTestCase(unittest.TestCase):
	def test_command_range(self):
		tokenizer = MMZTokenizer()
		# spec says all chars 0-31 but 10 is excempted as it is newline
		ranges = [range(0,10), range(11,32)]
		for testrange in ranges:
			for byte in testrange:
				stream = chr(byte) + " "
				tokens = [token for token in tokenizer.feed(stream)]
				self.assertTrue(len(tokens), 1)
				self.assertEqual(tokens[0], MMZToken(TOKEN_COMMAND, chr(byte)))

	def test_comments(self):
		tokenizer = MMZTokenizer()

		# single char comment
		stream = "# Test comment\n"
		tokens =[ token for token in tokenizer.feed(stream)]
		self.assertTrue(len(tokens), 1)
		self.assertEqual(tokens[0], MMZToken(TOKEN_COMMENT, stream[1:-1]))

		# multi char comment
		stream = "/// Test comment\n"
		tokens =[ token for token in tokenizer.feed(stream)]
		self.assertTrue(len(tokens), 1)
		self.assertEqual(tokens[0], MMZToken(TOKEN_COMMENT, stream[3:-1]))

		# not a multichar comment
		stream = "/ Test comment\n"
		tokens =[ token for token in tokenizer.feed(stream)]
		self.assertEqual(tokens, [MMZToken(TOKEN_STRING, "/"), MMZToken(TOKEN_STRING, "Test"), MMZToken(TOKEN_STRING, "comment"), MMZToken(TOKEN_NEWLINE, None)])

		# also not a multichar comment
		stream = "// Test comment\n"
		tokens =[ token for token in tokenizer.feed(stream)]
		self.assertEqual(tokens, [MMZToken(TOKEN_STRING, "//"), MMZToken(TOKEN_STRING, "Test"), MMZToken(TOKEN_STRING, "comment"), MMZToken(TOKEN_NEWLINE, None)])

