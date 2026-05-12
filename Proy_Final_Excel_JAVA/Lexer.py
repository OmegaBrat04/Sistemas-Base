import os
from typing import List

import antlr4
from antlr4.error.ErrorListener import ErrorListener
from generated.ExcelLexer import ExcelLexer as ANTLRExcelLexer

from TokenType import TokenType
from Token import Token

# Traducción de operadores Excel → Java
OPERATOR_TRANSLATIONS = {
    '<>': '!=', 
    '=':  '==',
}

# Mapeo de nombres simbólicos ANTLR → TokenType 
ANTLR_TO_TOKEN_TYPE = {
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


class _LexerErrorListener(ErrorListener):
    """Recoge errores léxicos reportados por ANTLR sin detener el análisis."""

    def __init__(self):
        super().__init__()
        self.errores: List[str] = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.errores.append(
            f"Error léxico — línea {line}, columna {column + 1}: {msg}"
        )


class Lexer:
    """
    Envolvente sobre el lexer generado por ANTLR4.

    Los errores léxicos quedan en  lexer.errores  (lista de strings).
    """

    def __init__(self, fuente: str):
        self.fuente:  str         = fuente
        self.tokens:  List[Token] = []
        self.errores: List[str]   = []

    # API principal

    def scan_tokens(self) -> List[Token]:
        """Tokeniza la fuente y retorna la lista de Token."""
        input_stream   = antlr4.InputStream(self.fuente)
        antlr_lexer    = ANTLRExcelLexer(input_stream)

        # Sustituir listener de errores para capturarlos sin excepción
        error_listener = _LexerErrorListener()
        antlr_lexer.removeErrorListeners()
        antlr_lexer.addErrorListener(error_listener)

        stream = antlr4.CommonTokenStream(antlr_lexer)
        stream.fill()

        self.errores = error_listener.errores

        for antlr_token in stream.tokens:
            token = self._convertir(antlr_token, antlr_lexer)
            if token is not None:
                self.tokens.append(token)

        return self.tokens

    # Conversión interna

    def _convertir(self, antlr_token, antlr_lexer) -> 'Token | None':
        """Convierte un antlr4.Token a Token."""
        ttype = antlr_token.type
        text  = antlr_token.text
        linea = antlr_token.line
        col   = antlr_token.column + 1   # ANTLR usa índice 0

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
            # Traducción Excel → Java
            value = OPERATOR_TRANSLATIONS.get(text, text)

        elif our_type == TokenType.STRING:
            # Quitar comillas delimitadoras
            value = text[1:-1]

        elif our_type == TokenType.FLOAT:
            value = float(text)

        elif our_type == TokenType.INTEGER:
            value = int(text)

        # Token desconocido → registrar error adicional
        if sym_name == 'UNKNOWN':
            self.errores.append(
                f"Error léxico — línea {linea}, columna {col}: "
                f"símbolo desconocido '{text}'"
            )
            return Token(TokenType.ERROR, text, linea, col)

        return Token(our_type, value, linea, col)

    def print_tokens(self):
        """Imprime la lista de tokens y errores en formato tabular."""
        validos = [t for t in self.tokens if not t.isEOF()]
        print(f"\n{'─'*62}")
        print(f"  Tokens reconocidos: {len(validos)}")
        print(f"{'─'*62}")
        for i, token in enumerate(validos, 1):
            print(f"  {i:>3}. {token}")

        if self.errores:
            print(f"\n{'─'*62}")
            print("  Errores léxicos:")
            print(f"{'─'*62}")
            for err in self.errores:
                print(f"  ✗ {err}")

        print(f"{'─'*62}\n")
