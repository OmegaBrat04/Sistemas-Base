from dataclasses import dataclass
from typing import Any
from TokenType import TokenType

@dataclass
class Token:
    type:    TokenType
    value:   Any
    linea:   int
    columna: int

    def __str__(self) -> str:
        return f"Token({self.type.name:<12}, {repr(self.value):<20}, linea={self.linea}, col={self.columna})"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        if not isinstance(other, Token):
            return False
        return self.type == other.type and self.value == other.value

    def isType(self, token_type: TokenType) -> bool:
        return self.type == token_type

    def isFunction(self)   -> bool: return self.isType(TokenType.FUNCTION)
    def isCellRange(self)  -> bool: return self.isType(TokenType.CELL_RANGE)
    def isCellRef(self)    -> bool: return self.isType(TokenType.CELL_REF)
    def isFloat(self)      -> bool: return self.isType(TokenType.FLOAT)
    def isInteger(self)    -> bool: return self.isType(TokenType.INTEGER)
    def isString(self)     -> bool: return self.isType(TokenType.STRING)
    def isIdentifier(self) -> bool: return self.isType(TokenType.IDENTIFIER)
    def isOperator(self)   -> bool: return self.isType(TokenType.OPERATOR)
    def isLParen(self)     -> bool: return self.isType(TokenType.LPAREN)
    def isRParen(self)     -> bool: return self.isType(TokenType.RPAREN)
    def isComma(self)      -> bool: return self.isType(TokenType.COMMA)
    def isSemicolon(self)  -> bool: return self.isType(TokenType.SEMICOLON)
    def isEOF(self)        -> bool: return self.isType(TokenType.EOF)
    def isError(self)      -> bool: return self.isType(TokenType.ERROR)

    def has_value(self, expected: Any) -> bool:
        return self.value == expected

    def matches(self, token_type: TokenType, value: Any = None) -> bool:
        if value is None:
            return self.isType(token_type)
        return self.isType(token_type) and self.has_value(value)
