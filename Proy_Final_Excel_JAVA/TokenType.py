from enum import Enum, auto

class TokenType(Enum):
    # Funciones Excel reconocidas
    FUNCTION   = auto()
    # Referencias a celdas
    CELL_RANGE = auto()
    CELL_REF   = auto()
    # Literales
    FLOAT      = auto()
    INTEGER    = auto()
    STRING     = auto()
    # Identificador genérico
    IDENTIFIER = auto()
    # Operadores (+, -, *, /, ^, <, >, =, <=, >=, <>)
    OPERATOR   = auto()
    # Delimitadores
    LPAREN     = auto()
    RPAREN     = auto()
    COMMA      = auto()
    SEMICOLON  = auto()
    # Especiales
    EOF        = auto()
    ERROR      = auto()
