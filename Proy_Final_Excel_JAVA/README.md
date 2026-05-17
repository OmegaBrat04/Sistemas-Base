# ExcelToJava — Analizador Léxico

Analizador léxico que traduce fórmulas matemáticas de Excel a código Java.  
Convierte funciones como `SUMA(A1:B5)` o `POTENCIA(A1, 2)` en su equivalente Java (`Math.pow(A1, 2)`).

---

## Información del Curso

| Campo       | Detalle                                                            |
| ----------- | ------------------------------------------------------------------ |
| Materia     | Programacion de Sistemas de Base 1                                 |
| Institución | Universidad Autonoma de Tamaulipas. Facultad de Ingenieria Tampico |
| Semestre    | Octavo Semestre                                                    |
| Profesor    | Muñoz Quintero Dante Adolfo                                        |

## Integrantes del Equipo

| Nombre                         | Matrícula  |
| ------------------------------ | ---------- |
| Martinez Acuña Brandon         | 2223330174 |
| Diaz Villareal Celine Michelle | 2223339025 |
| Ibarra Loredo Juan Jesus       | 2223330167 |
| Cabrera Reyes Carlos Alberto   | 2223330142 |

---

## Descripción del Lenguaje

**ExcelToJava** es un lenguaje fuente basado en la sintaxis de funciones matemáticas de Microsoft Excel.  
El analizador léxico toma una expresión Excel como entrada y produce una lista ordenada de tokens que pueden usarse en fases posteriores de compilación.

---

## Tokens Reconocidos

| Token      | Descripción                          | Ejemplo              |
| ---------- | ------------------------------------ | -------------------- |
| FUNCTION   | Función Excel reconocida             | `SUMA`, `SI`         |
| CELL_RANGE | Rango de celdas                      | `A1:B5`, `$A$1:$C$3` |
| CELL_REF   | Referencia a celda individual        | `A1`, `$B$2`         |
| FLOAT      | Número de punto flotante             | `3.14`               |
| INTEGER    | Número entero                        | `42`                 |
| STRING     | Cadena de texto entre comillas       | `"Hola"`             |
| IDENTIFIER | Identificador genérico               | `mi_var`             |
| OPERATOR   | Operador aritmético o relacional     | `+`, `<>`, `=`       |
| LPAREN     | Paréntesis de apertura               | `(`                  |
| RPAREN     | Paréntesis de cierre                 | `)`                  |
| COMMA      | Coma (separador de argumentos)       | `,`                  |
| SEMICOLON  | Punto y coma (separador alternativo) | `;`                  |
| EOF        | Fin de entrada                       | —                    |
| ERROR      | Símbolo desconocido (error léxico)   | `@`, `#`             |

---

## Estructura del Proyecto

```
Proy_Final_Excel_JAVA/
├── src/
│   ├── main.py        ← Punto de entrada
│   ├── lexer.py       ← Lógica del analizador léxico
│   ├── tokens.py      ← Definición de TokenType y Token
│   └── errors.py      ← Manejo de errores léxicos
├── grammar/
│   ├── ExcelLexer.g4  ← Gramática ANTLR4
│   └── generated/     ← Código Python generado por ANTLR4
├── tests/
│   ├── valid/         ← Entradas válidas (.txt)
│   └── invalid/       ← Entradas con errores léxicos (.txt)
├── docs/
│   └── entregable_final.pdf
├── capturas/
└── README.md
```

---

## Cómo Ejecutar

### Requisitos

- Python 3.10+
- `antlr4-python3-runtime` instalado:
  ```bash
  pip install antlr4-python3-runtime==4.13.2
  ```

### Ejecutar el analizador léxico

Desde la **raíz del proyecto**:

```bash
python src/main.py
```

El programa leerá automáticamente todos los archivos `.txt` de `tests/valid/` y `tests/invalid/`.

---

## Ejemplos de Uso

**Entrada** (`tests/valid/test01.txt`):

```
SUMA(A1:B5)
POTENCIA(A1, 2)
```

**Salida esperada**:

```
  Línea  1: SUMA(A1:B5)
    1. Token(FUNCTION     | valor='SUMA'              | línea=1, col=1)
    2. Token(LPAREN       | valor='('                 | línea=1, col=5)
    3. Token(CELL_RANGE   | valor='A1:B5'             | línea=1, col=6)
    4. Token(RPAREN       | valor=')'                 | línea=1, col=11)
```
