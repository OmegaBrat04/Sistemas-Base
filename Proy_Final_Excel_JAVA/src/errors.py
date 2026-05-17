
# Contiene el listener de errores que ANTLR4 invoca cuando encuentra un símbolo no reconocido

from typing import List

from antlr4.error.ErrorListener import ErrorListener


class LexerErrorListener(ErrorListener):
    
    #  Intercepta los errores léxicos de ANTLR4 sin detener el análisis.

    def __init__(self) -> None:
        super().__init__()
        self.errores: List[str] = []

    # Metodo que es invocado por ANTLR4 cuando encuentra un error léxico
    def syntaxError(self, recognizer, offendingSymbol,
                    line: int, column: int, msg: str, e) -> None:
        self.errores.append(
            f"Error léxico — línea {line}, columna {column + 1}: {msg}"
        )
