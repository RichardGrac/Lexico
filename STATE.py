from enum import Enum


class STATE(Enum):
    # Estados generales
    ERROR = 0
    BEGGIN = 1
    END = 2
    # Comentario Simple | Comentario multiple
    SIMPLE_COMMENT = 3
    IN_MULTIPLE_COMMENT = 4
    IN_MULTIPLE_COMMENT_END = 5  # Asterisco antes de cerrar
    # Operadores
    ADDITION = 6
    SUBSTRACTION = 7
    DIFFERENCE = 8
    MULTIPLICATION = 9
    # Operadores logicos
    DOUBLE_ADDITION = 10
    DOUBLE_SUBSTRACTION = 11
    # Cadena
    IN_STRING = 12
    # Numeros
    IN_NUMERAL = 13
    IN_FLOAT = 14
    # Comparacion
    IN_LESS = 15
    IN_GREATER = 16
    IN_NEGATION = 17
    IN_ASSIGNMENT = 18
