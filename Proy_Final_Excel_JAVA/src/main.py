
from __future__ import annotations

import os
import sys

# Forzar UTF-8 en stdout para que los caracteres especiales se muestren correctamente
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Añadir src/ al path para poder importar Lexer
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lexer import Lexer




def analizar_linea(numero: int, expresion: str) -> None:
    # Analiza una sola expresión e imprime sus tokens.
    expresion = expresion.strip()

    # Ignorar líneas vacías y comentarios
    if not expresion or expresion.startswith('#'):
        return

    print(f"\n  Línea {numero:>2}: {expresion}")
    lexer  = Lexer(expresion)
    lexer.scan_tokens()
    lexer.print_tokens()


def analizar_archivo(ruta: str) -> None:
    nombre = os.path.basename(ruta)
    print(f"============================================================")
    print(f"  Archivo : {nombre}")
    print(f"============================================================")

    try:
        with open(ruta, encoding='utf-8') as f:
            lineas = f.readlines()
    except FileNotFoundError:
        print(f" Archivo no encontrado: {ruta}")
        return

    procesadas = 0
    for i, linea in enumerate(lineas, start=1):
        if linea.strip() and not linea.strip().startswith('#'):
            analizar_linea(i, linea)
            procesadas += 1

    print(f"\n  Expresiones analizadas : {procesadas}")


def main() -> None:
    print(f"\n============================================================")
    print("    Analizador Léxico — ExcelToJava")
    print("    Fórmulas Excel → código Java")
    print(f"============================================================")

    # Raíz del proyecto = un nivel arriba de src/
    raiz     = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    test_dir = os.path.join(raiz, 'tests')

    for categoria in ('valid', 'invalid'):
        carpeta = os.path.join(test_dir, categoria)

        if not os.path.isdir(carpeta):
            print(f"\n Carpeta no encontrada: {carpeta}")
            continue

        archivos = sorted(f for f in os.listdir(carpeta) if f.endswith('.txt'))

        if not archivos:
            print(f"\n  No se encontraron archivos .txt en: {carpeta}")
            continue

        print(f"\n============================================================")
        print(f"    Categoría: {categoria.upper()}")
        print(f"============================================================")

        for archivo in archivos:
            analizar_archivo(os.path.join(carpeta, archivo))

    print(f"\n============================================================")
    print("    Análisis léxico completado.")
    print(f"============================================================")


if __name__ == "__main__":
    main()
