lexer grammar ExcelLexer;

// ══════════════════════════════════════════════════════════════════
//  FUNCIONES EXCEL
//  Regla de prioridad: reglas más específicas primero.
//  Y, O, NO solo son FUNCTION cuando van seguidas de '('.
// ══════════════════════════════════════════════════════════════════

FUNCTION
    : 'SUMA'
    | 'PROMEDIO'
    | 'MAX'
    | 'MIN'
    | 'CONTAR'
    | 'CONCATENAR'
    | 'POTENCIA'
    | 'RAIZ'
    | 'ABS'
    | 'REDONDEAR'
    | 'ENTERO'
    | 'SI'
    | ('Y' | 'O' | 'NO') { self._input.LA(1) == ord('(') }?
    ;

// ══════════════════════════════════════════════════════════════════
//  REFERENCIAS A CELDAS
//  CELL_RANGE DEBE ir antes que CELL_REF (maximal munch de ANTLR).
//  Soporta referencias absolutas ($A$1) y relativas (A1).
// ══════════════════════════════════════════════════════════════════

fragment COL_PART : '$'? [A-Z]+ ;
fragment ROW_PART : '$'? [0-9]+ ;
fragment CELL_ID  : COL_PART ROW_PART ;

CELL_RANGE : CELL_ID ':' CELL_ID ;
CELL_REF   : CELL_ID ;

// ══════════════════════════════════════════════════════════════════
//  LITERALES NUMÉRICOS
//  FLOAT DEBE ir antes que INTEGER.
// ══════════════════════════════════════════════════════════════════

FLOAT   : [0-9]+ '.' [0-9]+ ;
INTEGER : [0-9]+ ;

// ══════════════════════════════════════════════════════════════════
//  CADENAS DE TEXTO
// ══════════════════════════════════════════════════════════════════

STRING : '"' (~["\r\n])* '"' ;

// ══════════════════════════════════════════════════════════════════
//  OPERADORES
//  Los operadores de DOS caracteres DEBEN ir antes que los simples.
//  Traducciones aplicadas en Lexer.py:  <> → !=   |   = → ==
// ══════════════════════════════════════════════════════════════════

OPERATOR
    : '<='       // Menor o igual
    | '>='       // Mayor o igual
    | '<>'       // Diferente (Excel) → != (Java)
    | '+'
    | '-'
    | '*'
    | '/'
    | '^'        // Potencia (Excel) → Math.pow() (Java)
    | '<'
    | '>'
    | '='        // Igual (Excel)    → == (Java)
    ;

// ══════════════════════════════════════════════════════════════════
//  DELIMITADORES
// ══════════════════════════════════════════════════════════════════

LPAREN    : '(' ;
RPAREN    : ')' ;
COMMA     : ',' ;
SEMICOLON : ';' ;

// ══════════════════════════════════════════════════════════════════
//  IDENTIFICADORES GENÉRICOS
//  Letras + dígitos + guión bajo; NO puede empezar con dígito.
// ══════════════════════════════════════════════════════════════════

IDENTIFIER : [A-Za-z_][A-Za-z0-9_]* ;

// ══════════════════════════════════════════════════════════════════
//  ESPACIOS EN BLANCO  →  ignorados
// ══════════════════════════════════════════════════════════════════

WS : [ \t\r\n]+ -> skip ;

// ══════════════════════════════════════════════════════════════════
//  CATCH-ALL DE ERRORES
//  Todo carácter no reconocido genera token UNKNOWN.
// ══════════════════════════════════════════════════════════════════

UNKNOWN : . ;
