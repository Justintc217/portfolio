import string


def identify_token(token: str) -> str:
    if token[0] in string.digits:
        return "integerConstant"
    if token[0] == "\"":
        return "stringConstant"
    if token[0] in data["symbol"]:
        return "symbol"
    if token in data["keyword"]:
        return "keyword"
    else:
        return "identifier"


data = {
    "keyword": [
        "class",
        "constructor",
        "function",
        "method",
        "field",
        "static",
        "var",
        "int",
        "char",
        "boolean",
        "void",
        "true",
        "false",
        "null",
        "this",
        "let",
        "do",
        "if",
        "else",
        "while",
        "return",
    ],

    "symbol": "{}()[].,;+-*/&|<>=~"
}
