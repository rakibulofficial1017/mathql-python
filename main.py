import re
class Token:
    def __init__(self, name, value):
        self.name = name
        self.value = value

TOKEN_RULES = {
    "NUMBER": r"(\d+(\.\d*)?(e\d+)?",
    "STRING": r"(\"|')[^\1]*\1",
    "OPERATOR": r"(\+|-|=|*|/|%|^|\(|\))",
    "IDENTIFIER": r"[A-Za-z_][A-Za-z_0-9]*"
}

line = "let v = 30"

lptr = 0
rptr = 1
tokens = []

