
from __future__ import annotations

import os
import sys
from typing import List

#  Añadir la raíz del proyecto al path 
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import antlr4
from grammar.generated.ExcelLexer import ExcelLexer as ANTLRExcelLexer  

from tokens import Token, TokenType
from errors import LexerErrorListener


# Traducción de operadores Excel a Java 
OPERATOR_TRANSLATIONS: dict[str, str] = {
    '<>': '!=',   
    '=':  '==',  
}


# Diccionario de traducción de tipos de ANTLR a TokenType
ANTLR_TO_TOKEN_TYPE: dict[str, TokenType] = {
    'FUNCTION':   TokenType.FUNCTION,
    'CELL_RANGE': TokenType.CELL_RANGE,
    'CELL_REF':   TokenType.CELL_REF,
    'FLOAT':      TokenType.FLOAT,
    'INTEGER':    TokenType.INTEGER,
    'STRING':     TokenType.STRING,
    'IDENTIFIER': TokenType.IDENTIFIER,
    'OPERATOR':   TokenType.OPERATOR,
    'LPAREN':     TokenType.LPAREN,
    'RPAREN':     TokenType.RPAREN,
    'COMMA':      TokenType.COMMA,
    'SEMICOLON':  TokenType.SEMICOLON,
    'UNKNOWN':    TokenType.ERROR,
}


# Clase Lexer que convierte la fuente en tokens
class Lexer:

    # Constructor
    def __init__(self, fuente: str) -> None:
        self.fuente:  str         = fuente
        self.tokens:  List[Token] = []
        self.errores: List[str]   = []


    def scan_tokens(self) -> List[Token]:
        # Tokeniza la fuente y retorna la lista de Token.
        input_stream = antlr4.InputStream(self.fuente)
        antlr_lexer  = ANTLRExcelLexer(input_stream)

        # Listener personalizado para errores léxicos
        error_listener = LexerErrorListener()
        antlr_lexer.removeErrorListeners()
        antlr_lexer.addErrorListener(error_listener)

        stream = antlr4.CommonTokenStream(antlr_lexer)
        stream.fill()
        self.errores = error_listener.errores

        # Chequeo de adyacencia: detectar INTEGER/FLOAT pegado a IDENTIFIER
        raw = [t for t in stream.tokens if t.type != antlr4.Token.EOF]
        for i in range(len(raw) - 1):
            curr, nxt = raw[i], raw[i + 1]
            curr_sym = (antlr_lexer.symbolicNames[curr.type]
                        if 0 < curr.type < len(antlr_lexer.symbolicNames) else '')
            nxt_sym  = (antlr_lexer.symbolicNames[nxt.type]
                        if 0 < nxt.type  < len(antlr_lexer.symbolicNames) else '')
            if curr_sym in ('INTEGER', 'FLOAT') and nxt_sym == 'IDENTIFIER':
                # Son adyacentes si el IDENTIFIER empieza justo donde termina el número
                if nxt.line == curr.line and nxt.column == curr.column + len(curr.text):
                    self.errores.append(
                        f"Error léxico — línea {curr.line}, columna {curr.column + 1}: "
                        f"identificador inválido '{curr.text}{nxt.text}' "
                        f"(los identificadores no pueden comenzar con un dígito)"
                    )

        for antlr_token in stream.tokens:
            token = self._convertir(antlr_token, antlr_lexer)
            if token is not None:
                self.tokens.append(token)

        return self.tokens

    def _convertir(self, antlr_token, antlr_lexer) -> Token | None:
        # Convierte un antlr4.Token a nuestro Token interno.
        ttype = antlr_token.type
        text  = antlr_token.text
        linea = antlr_token.line
        col   = antlr_token.column + 1   # ANTLR usa índice 0, lo convierte a 1

        # EOF
        if ttype == antlr4.Token.EOF:
            return Token(TokenType.EOF, '', linea, col)

        # Nombre simbólico del tipo (ej. 'FUNCTION', 'OPERATOR', …)
        sym_name = (
            antlr_lexer.symbolicNames[ttype]
            if 0 < ttype < len(antlr_lexer.symbolicNames)
            else 'UNKNOWN'
        )

        our_type = ANTLR_TO_TOKEN_TYPE.get(sym_name, TokenType.ERROR)

        # Transformaciones de valor
        value = text

        if our_type == TokenType.OPERATOR:
            value = OPERATOR_TRANSLATIONS.get(text, text)

        elif our_type == TokenType.STRING:
            value = text[1:-1]          # Quitar comillas

        elif our_type == TokenType.FLOAT:
            value = float(text)

        elif our_type == TokenType.INTEGER:
            value = int(text)

        # Token desconocido, registra error adicional con contexto
        if sym_name == 'UNKNOWN':
            self.errores.append(
                f"Error léxico — línea {linea}, columna {col}: "
                f"símbolo desconocido '{text}'"
            )
            return Token(TokenType.ERROR, text, linea, col)
        return Token(our_type, value, linea, col)


    def print_tokens(self) -> None:
        # Imprime la lista de tokens y errores
        validos = [t for t in self.tokens if not t.isEOF()]

        print(f"  Tokens reconocidos : {len(validos)}")
        for i, token in enumerate(validos, 1):
            print(f"  {i:>3}: {token}")

        if self.errores:
            print("  Errores léxicos :")
            for err in self.errores:
                print(f" {err}")
