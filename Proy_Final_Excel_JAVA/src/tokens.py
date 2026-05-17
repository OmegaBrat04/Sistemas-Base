
from __future__ import annotations

from enum import Enum, auto
from typing import Any

# Enumeracion con los 14 tipos de token del lenguaje
class TokenType(Enum):
    #  Funciones Excel 
    FUNCTION   = auto()   # SUMA, PROMEDIO, SI, POTENCIA, …

    #  Referencias a celdas 
    CELL_RANGE = auto()   # A1:B5, $A$1:$C$3
    CELL_REF   = auto()   # A1, $B$2

    #  Literales numéricos 
    FLOAT      = auto()   # 3.14
    INTEGER    = auto()   # 42

    #  Literal de texto 
    STRING     = auto()   # "Hola"

    #  Identificadores genéricos 
    IDENTIFIER = auto()   # nombre_variable, Y (sin paréntesis)

    #  Operadores 
    OPERATOR   = auto()   # +, -, *, /, ^, <, >, <=, >=, <>, =

    #  Delimitadores 
    LPAREN    = auto()    # (
    RPAREN    = auto()    # )
    COMMA     = auto()    # ,
    SEMICOLON = auto()    # ;

    #  Control 
    EOF   = auto()
    ERROR = auto()


#  Token — Unidad léxica individual
class Token:

    # Constructor
    def __init__(self, type: TokenType, value: Any,
                 line: int = 0, column: int = 0) -> None:
        self.type:   TokenType = type
        self.value:  Any       = value
        self.line:   int       = line
        self.column: int       = column

    # Formatea el token para impresion en pantalla
    def __str__(self) -> str:
        return (
            f"({self.type.name} , "
            f"{self.value!r} , "
            f"línea={self.line}, col={self.column})"
        )

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Token):
            return False
        return self.type == other.type and self.value == other.value

    #  Consultas de tipo 

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

    # Checa si el token es de cierto tipo y tiene un valor 
    def matches(self, token_type: TokenType, value: Any = None) -> bool:
        if value is None:
            return self.isType(token_type)
        return self.isType(token_type) and self.has_value(value)
