#!/usr/local/bin/python3
from typing import Any, List
from token_type import TokenType as TT
from token import Token
import error_handler


class Scanner:
    keywords = {
        "and": TT.AND,
        "class": TT.CLASS,
        "else": TT.ELSE,
        "false": TT.FALSE,
        "for": TT.FOR,
        "fun": TT.FUN,
        "if": TT.IF,
        "nil": TT.NIL,
        "or": TT.OR,
        "print": TT.PRINT,
        "return": TT.RETURN,
        "super": TT.SUPER,
        "this": TT.THIS,
        "true": TT.TRUE,
        "var": TT.VAR,
        "while": TT.WHILE,
    }

    def __init__(self, source: str):
        self.source = source
        self.tokens: List[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1

    def scan_tokens(self) -> List[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TT.EOF, "", None, self.line))
        return self.tokens

    def scan_token(self) -> None:
        c = self.advance()
        if c == '(':
            self.add_token(TT.LEFT_PAREN)
        elif c == ')':
            self.add_token(TT.RIGHT_BRACE)
        elif c == '{':
            self.add_token(TT.LEFT_BRACE)
        elif c == '}':
            self.add_token(TT.RIGHT_BRACE)
        elif c == ',':
            self.add_token(TT.COMMA)
        elif c == '.':
            self.add_token(TT.DOT)
        elif c == '-':
            self.add_token(TT.MINUS)
        elif c == '+':
            self.add_token(TT.PLUS)
        elif c == ';':
            self.add_token(TT.SEMICOLON)
        elif c == '*':
            self.add_token(TT.STAR)
        elif c == '!':
            self.add_token(TT.BANG_EQUAL if self.match('=') else TT.BANG)
        elif c == '=':
            self.add_token(TT.EQUAL_EQUAL if self.match('=') else TT.EQUAL)
        elif c == '<':
            self.add_token(TT.LESS_EQUAL if self.match('=') else TT.LESS)
        elif c == '>':
            self.add_token(TT.GREATER_EQUAL if self.match('=') else TT.GREATER)
        elif c == '/':
            if self.match('/'):
                # a comment goes until the end of the line
                while self.peek() != '\n' and not self.is_at_end():
                    self.advance()
            else:
                self.add_token(TT.SLASH)
        elif c == ' ' or c == '\t' or c == '\t':
            # do nothing
            pass
        elif c == '\n':
            self.line += 1
        elif c == '"':
            self.string()
        elif self.is_digit(c):
            self.number()
        elif self.is_alpha(c):
            self.identifier()
        else:
            error_handler.error(self.line, "Unexpected Character.")

    def string(self) -> None:
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()

        if self.is_at_end():
            error_handler.error(self.line, "Unterminated String.")
            return

        # the closing "
        self.advance()

        # trim the surrounding quotes
        value = self.source[self.start + 1:self.current - 1]
        self.add_token_(TT.STRING, value)

    def number(self) -> None:
        while self.is_digit(self.peek()):
            self.advance()

        # look for a fractional part
        if self.peek() == '.' and self.is_digit(self.peek_next()):
            # consume the "."
            self.advance()
            while self.is_digit(self.peek()):
                self.advance()

        self.add_token_(TT.NUMBER, float(self.source[self.start:self.current]))

    def identifier(self) -> None:
        while self.is_alpha_numeric(self.peek()):
            self.advance()

        text = self.source[self.start:self.current]
        token_type = self.keywords.get(text)
        if token_type is None:
            token_type = TT.IDENTIFIER

        self.add_token(token_type)

    def match(self, expected: str) -> bool:
        if self.is_at_end():
            return False
        if self.peek() != expected:
            return False

        self.current += 1
        return True

    def peek(self) -> str:
        if self.is_at_end():
            return "\0"

        return self.source[self.current]

    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return "\0"

        return self.source[self.current + 1]

    def is_digit(self, c: str) -> bool:
        return c.isdigit()

    def is_alpha(self, c: str) -> bool:
        return c.isalpha() or c == "_"

    def is_alpha_numeric(self, c: str) -> bool:
        return self.is_alpha(c) or self.is_digit(c)

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def advance(self) -> str:
        self.current += 1
        return self.source[self.current - 1]

    def add_token(self, token_type: TT) -> None:
        self.add_token_(token_type, None)

    def add_token_(self, token_type: TT, literal: Any) -> None:
        text = self.source[self.start:self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))
