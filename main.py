import re

class Token:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"Token({self.name!r}, {self.value!r})"


KEYWORDS = [
    "let",
]

TOKEN_RULES = {
    "NUMBER": r"\d+(?:\.\d*)?(?:e\d+)?",
    "STRING": r"""(?:"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')""",
    "KEYWORD": r"\b(?:" + "|".join(map(re.escape, KEYWORDS)) + r")\b",
    "OPERATOR": r"[+\-=*/%^()]",
    "IDENTIFIER": r"[A-Za-z_][A-Za-z_0-9]*",
    "SEMICOLON": r";",
}

TOKEN_REGEX = re.compile(
    "|".join(
        f"(?P<{name}>{pattern})"
        for name, pattern in TOKEN_RULES.items()
    )
)

def tokenize(line):
    tokens = []

    for match in TOKEN_REGEX.finditer(line):
        if match.group().isspace():
            continue

        tokens.append(Token(match.lastgroup, match.group()))

    return tokens


line = "let v = 30;"
tokens = tokenize(line)

print(tokens)
