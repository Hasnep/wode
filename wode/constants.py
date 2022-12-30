from string import ascii_letters

from wode.types import List

DIGITS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
LETTERS = List(ascii_letters)
WHITESPACE_CHARACTERS = [" ", "\t", "\r", "\n"]
VALID_IDENTIFIER_PREFIXES = ["_"] + LETTERS
VALID_IDENTIFIER_CHARACTERS = ["_"] + LETTERS + DIGITS
