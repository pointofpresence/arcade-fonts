# pylint: disable=missing-module-docstring

CHARS = [
    None, None, None, "0", "1", "2", "3", "4",
    "5", "6", "7", "8", "9", "A", "B", "C",
    "D", "E", "F", "G", "H", "I", "J", "K",
    "L", "M", "N", "O", "P", "Q", "R", "S",
    "T", "U", "V", "W", "X", "Y", "Z", "-",
    "#", "?", "!", "©", None, ",", ".", ":",
    "=", None, None, None, None, None, None, None,
    None, None, None, "+", "(", None, None, None,
    "_", None, None, "%", ")", ";", "/", None,
    None, None, None, None, None, None, None, None,
    None, None, None, None, None, None, None, None,
    None, None, None, None, None, None, None, None,
    None, None, None, None, None, None, None, None,
    None, None, None, None, None, None, None, None,
    None, None, None, None, None, None, None, None,
    "\"", "$", "&", "'", "*", "<", ">", "@",
    "[", "]", "^", "_", "`", "{", "}", "|",
    "~", "А",
]

CHAR_CODES = [ord(c) if c else 0 for c in CHARS]
