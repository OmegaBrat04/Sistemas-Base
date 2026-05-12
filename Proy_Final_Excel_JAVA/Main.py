from Lexer import Lexer

def analizar(descripcion: str, expresion: str):
    print(f"\n{'═'*62}")
    print(f"  Caso   : {descripcion}")
    print(f"  Entrada: {expresion}")
    print(f"{'═'*62}")
    lexer  = Lexer(expresion)
    tokens = lexer.scan_tokens()
    lexer.print_tokens()

def main():
    print("\n" + "═"*62)
    print("    Analizador Léxico — Traductor Excel → Java")
    print("    Usando ANTLR4 + clases propias")
    print("═"*62)

    # Casos válidos
    analizar(
        "Suma de rango simple",
        "SUMA(A1:B5)"
    )
    analizar(
        "SI con operador diferente (<> → !=)",
        "SI(A1<>10, SUMA(B1:B5), 0)"
    )
    analizar(
        "Potencia (^ conservado para fase de traducción)",
        "POTENCIA(A1, 2)"
    )
    analizar(
        "Función Y lógica (solo si sigue '(')",
        "Y(A1>0, B1<10)"
    )
    analizar(
        "Función O lógica",
        "O(A1=1, B1=2)"
    )
    analizar(
        "Función NO lógica",
        "NO(A1>5)"
    )
    analizar(
        "Referencias absolutas ($)",
        "PROMEDIO($A$1:$C$3)"
    )
    analizar(
        "Operadores relacionales combinados",
        "SI(A1>=10, MAX(B1:B5), MIN(C1:C5))"
    )
    analizar(
        "Literal flotante e entero",
        "3.14 + 10"
    )
    analizar(
        "Cadena de texto (STRING)",
        'CONCATENAR("Hola", " ", "Mundo")'
    )
    analizar(
        "Y solo sin paréntesis → IDENTIFIER",
        "Y"
    )
    analizar(
        "Punto y coma como separador alternativo",
        "SUMA(A1;B1;C1)"
    )

    # Casos con errores léxicos
    print("\n" + "═"*62)
    print("    Casos con errores léxicos esperados")
    print("═"*62)

    analizar(
        "Símbolo desconocido (@)",
        "@variable"
    )
    analizar(
        "Identificador inválido (empieza con dígito)",
        "SUMA(123abc)"
    )

    print("\nAnálisis léxico completado.")


if __name__ == "__main__":
    main()
