from data import *
import re


def extract_instructions_only(content):
    def remove_multiline_comment(content):
        content = re.sub("(/\*\*(.|\n)*?\*/)", "", content)
        return content

    def clean_line(line):
        line = line.rstrip("\n")
        code, *_ = line.split("//")
        code = code.strip()
        return code
    content = remove_multiline_comment(content)
    lines = content.splitlines()
    clean_code = map(clean_line, lines)
    instructions = list(filter(None, clean_code))
    return instructions


def tokenizer_line(line, token_list):
    token = str()
    for char in line:
        if "\"" in token:
            token += char
            if token[-1] == "\"":
                token_list.append((token, identify_token(token)))
                token = str()
        elif char in data["symbol"]:
            # start a new token
            if char == "<":
                char = "&lt;"
            if char == ">":
                char = "&gt;"
            if token:
                token_list.append((token, identify_token(token)))
            token_list.append((char, identify_token(char)))
            token = str()
        elif char == " ":
            if token:
                token_list.append((token, identify_token(token)))
            token = str()
        else:
            token += char


def tokenizer(lines):
    token_list = []
    [tokenizer_line(line=line, token_list=token_list) for line in lines]
    return token_list
