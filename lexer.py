"""
    Analizador Lexicografico del Lenguaje GuardedUSB
    Primera fase del proyecto
    Traductores e Interpretadores (CI-3725)
    Maria Fernanda Magallanes (13-10787)
    Jesus Marcano (12-10359)
    E-M 2020
"""
from ply import lex
from LexerModels import TokenConstants
from LexerModels import LexerFunctions
from sys import argv
import sys

# AQUI SOLO SE HARA EL AREA DE INPUT PARA EL LEXER, LO QUE TENGA QUE VER CON EL READ ARCHIVO O UN MENU PARA EL USUARIO #
print("Hola mundo")
# TokenConstants.outHello()
# print(LexerFunctions.tk)
# Functions working

"""
Clase encargada de llevar todos los tokens:
Palabras Reservadas
Funciones
I/O
Arreglo de los tokens declarados
Especificaciones de los mismos
"""

from ply import lex
import re
from sys import argv

# Reserved Words
reservedWords = {
    # Wily's Words / functions
    'begin-world': 'TkBeginWorld',
    'end-world': 'TkEndWorld',
    'World': 'TkWorld',
    'Wall': 'TkWall',
    'Object-type': 'TkObjType',
    'Place': 'TkPlace',
    'Start': 'TkStart',
    'Basket': 'TkBasket',
    'Boolean': 'TkBoolean',
    'Goal': 'TkGoal',
    'Final': 'TkFinal',
    'basket': 'TkBasketLower',

    # Common Words - Oper - Used on previous words to build a instruction
    'from': 'TkFrom',
    'to': 'TkTo',
    'of': 'TkOf',
    'color': 'TkColor',
    'at': 'TkAt',
    'in': 'TkIn',
    'is': 'TkIs',
    'heading': 'TkHeading',
    'with': 'TkWith',
    'initial': 'TkInitial',
    'value': 'TkValue',
    # No se como ejemplificar: with initial value - se usa con Boolean

    # Colors
    'red': 'TkRed',
    'blue': 'TkBlue',
    'magenta': 'TkMagenta',
    'cyan': 'TkCyan',
    'green': 'TkGreen',
    'yellow': 'TkYellow',

    # Directions
    'north': 'TkNorth',
    'east': 'TkEast',
    'south': 'TkSouth',
    'west': 'TkWest',

    # Willy's Work Words

    # Data Type
    'int': 'TkInt',  #
    # 'bool': 'TkBool',   Entendi que hay 2 tipos de boolean

    # Conditionals
    'if': 'TkIf',
    'else': 'TkElse',
    'then': 'TkThen',

    # Loops
    'repeat': 'TkRepeat',
    'while': 'TkWhile',
    'times': 'TkTimes',

    # Aux
    'define': 'TkDefine',
    'begin': 'TkBegin',
    'end': 'TkEnd',
    'as': 'TkAs',

    # Willy's Actions
    'move': 'TkMove',
    'turn-left': 'TkTurnL',
    'turn-right': 'TkTurnR',
    'pick': 'TkPick',
    'drop': 'TkDrop',
    'set': 'TkSet',
    'clear': 'TkClear',
    'flip': 'TkFlip',
    'terminate': 'TkTerminate',
    'found': 'TkFound',
    'carrying': 'TkCarrying',

    # Booleans Primitives
    'front-clear': 'TkFrontCl',
    'left-clear': 'TkLeftCl',
    'right-clear': 'TkRightCl',
    'looking-north': 'TkLookingN',
    'looking-east': 'TkLookingE',
    'looking-south': 'TkLookingS',
    'looking-west': 'TkLookingW',

    # Boolean Values
    'true': 'TkTrue',
    'false': 'TkFalse',
    'or': 'TkOr',
    'and': 'TkAnd',
    'not': 'TkNot',
}
# Token's Lsit
tokens = [
             # Para las variables
             'TkId',

             #  Numeros enteros
             'TkNum',

             # Simbolos utilizados para denotar separadores

             # 'TkCOpenPar',
             # 'TkClosePar',
             'TkSemicolon',
             'TkComments',
             #'TkCommentsBlock'

         ] + list(reservedWords.values())

# Especificaciones de los tokens

# t_TkClosePar = r'\)'
t_TkSemicolon = r';'

t_TkComments = r'[-]{2}.*[\n]'

# Ignored Chars
t_ignore_Space = r'\s'  # Space
t_ignore_TkCommentsBlock = r'[{]{2}{.*}[}]{2}'        # Comentarios - falta colocar el regex de {{}}
t_ignore_Line = r' \n'  # Salto de linea
t_ignore_Tab = r' \t'  # Tabuladores

ValidTokens = []  # Coleccion de tokens validos
InvalidTokens = []  # Coleccion de tokens invalidos

# Prove of import Functions (This class is ony for tokens, don't declare functions here) - Main is Lexer
# Funciones Regulares

def t_TkNum(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_TkId(identificar):
    r'[a-zA-Z]+[a-zA-Z_0-9]*'
    identificar.type = reservedWords.get(identificar.value, 'TkId')
    return identificar


# Manejador de errores
def t_error(invalido):
    """ Funcion por "default" cuando encuentra un token que no pertenece a la lista de tokens """
    error = 'Caracter ilegal "' + str(invalido.value[0]) + '" en fila ' \
            + str(invalido.lineno) + ', columna ' + str(invalido.lexpos + 1)
    InvalidTokens.append(error)
    invalido.lexer.skip(1)


if len(argv) > 2:
    print("Uso del programa: python3 lexer.py <Nombre del archivo>")
    print("o utiizando: python3 lexer.py ")
    sys.exit()
elif len(argv) == 2:
    filepath = argv[1]
else:
    filepath = input('Archivo a Interpretar: ')

try:
    f = open(filepath, 'r')
    data = f.readline()
    token_prev = 'Unknown'
    lexer = lex.lex()
    while data:
        # pasamos la linea como data al lexer
        # Esto es con el fin de calcular bien la columna de los tokens
        lexer.input(data)

        # Iteramos sobre el la entrada para extraer los tokens
        # for tok in lexer:
        #    print(tok.type, tok.value, tok.lineno)
        tok = lexer.token()

        while tok:
            if (tok.type == 'TkNum'):
                token_info = str(tok.type) + ' ("' + str(tok.value) + '") ' \
                             + str(tok.lineno) + ' ' + str(tok.lexpos + 1)
            elif (tok.type == 'TkId'):
                token_info = str(tok.type) + ' ("' + str(tok.value) + '" , ' + token_prev + ') ' \
                             + str(tok.lineno) + ' ' + str(tok.lexpos + 1)
            else:
                token_info = str(tok.type) + ' ' + str(tok.lineno) + ' ' + str(tok.lexpos + 1)
                token_prev = str(tok.type)

            ValidTokens.append(token_info)
            tok = lexer.token()

        # leemos otra linea
        data = f.readline()

    # Cuando hay un error se imprime solo el error
    # Cuando no hay error se imprimen los tokens validos
    if (len(TokenConstants.InvalidTokens) > 0):
        for x in TokenConstants.InvalidTokens:
            print(x)
    else:
        for x in TokenConstants.ValidTokens:
            print(x)
    f.close()
except FileNotFoundError:
    print('Imposible abrir el archivo ' + filepath)
    sys.exit()
