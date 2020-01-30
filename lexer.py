"""
    Analizador Lexicografico del Lenguaje GuardedUSB
    Primera fase del proyecto
    Traductores e Interpretadores (CI-3725)
    Maria Fernanda Magallanes (13-10787)
    Jesus Marcano (12-10359)
    E-M 2020
"""

from ply import lex
from sys import argv
import os,sys

# AQUI SOLO SE HARA EL AREA DE INPUT PARA EL LEXER, LO QUE TENGA QUE VER CON EL READ ARCHIVO O UN MENU PARA EL USUARIO #


# Reserved Words

tokens = [
             'TkBeginWorld',
             'TkEndWorld',
             'TkObjType',
             'TkTurnL',
             'TkTurnR',
             'TkFrontCl',
             'TkLeftCl',
             'TkRightCl',
             'TkLookingN',
             'TkLookingE',
             'TkLookingS',
             'TkLookingW',
             'TkFinalG',
             'TkBeginTask',
             'TkEndTask',

             # Simbolos utilizados para denotar separadores
             'TkSemicolon',
             'TkTab',
             'TkId',
             'TkNum',
]

reserved = {
    # Wily's Words / functions

    'World': 'TkWorld',
    'Wall': 'TkWall',
    'Place': 'TkPlace',
    'Start': 'TkStart',
    'Basket': 'TkBasket',
    'Boolean': 'TkBoolean',
    'Goal': 'TkGoal',


    # Common Words - Oper - Used on previous words to build a instruction
    'from': 'TkFrom',
    'to': 'TkTo',
    'of': 'TkOf',
    'color': 'TkColor',
    'at': 'TkAt',
    'in': 'TkIn',
    'is': 'TkIs',
    'on': 'TkOn',
    'heading': 'TkHeading',
    'with': 'TkWith',
    'initial': 'TkInitial',
    'value': 'TkValue',
    'capacity': 'TkCapacity',
    'basket':'TkBasketLower',
    'objects': 'TkObjectsLower',
 

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
    'as': 'TkAs',

    # Willy's Actions
    'move': 'TkMove',
    'pick': 'TkPick',
    'drop': 'TkDrop',
    'set': 'TkSet',
    'clear': 'TkClear',
    'flip': 'TkFlip',
    'terminate': 'TkTerminate',
    'found': 'TkFound',
    'carrying': 'TkCarrying',


    # Boolean Values
    'true': 'TkTrue',
    'false': 'TkFalse',
    'or': 'TkOr',
    'and': 'TkAnd',
    'not': 'TkNot',

    #Other
    'begin': 'TkBegin',
    'end': 'TkEnd',
}

# Token's List
tokens += list(reserved.values())

# Especificaciones de los tokens
t_TkSemicolon = r';'
t_TkTab = r' \t'


# Ignored Chars
t_ignore_TkCommentsBlock = r'[\{]{2}.*[}]{2}'        
t_ignore_TkComments = r'[\-]{2}.*'
t_ignore_TkSpace = r'\s'


ValidTokens = []  # Coleccion de tokens validos
InvalidTokens = []  # Coleccion de tokens invalidos

# Prove of import Functions (This class is ony for tokens, don't declare functions here) - Main is Lexer

# Funciones Regulares
def t_TkBeginWorld(t):
    r'begin\-world'
    return t

def t_TkEndWorld(t):
    r'end\-world'
    return t

def t_TkObjType(t):
    r'Object\-type'
    return t

def t_TkTurnL(t):
    r'turn\-left'
    return t

def t_TkTurnR(t):
    r'turn\-right'
    return t

def t_TkFrontCl(t):
    r'front\-clear'
    return t

def t_TkLeftCl(t):
    r'left\-clear'
    return t

def t_TkRightCl(t):
    r'right\-clear'
    return t

def t_TkLookingN(t):
    r'looking\-north'
    return t

def t_TkLookingE(t):
    r'looking\-east'
    return t

def t_TkLookingS(t):
    r'looking\-south'
    return t

def t_TkLookingW(t):
    r'looking\-west'
    return t 

def t_TkFinalG(t):
    r'Final[\s]+goal'
    return t

def t_TkBeginTask(t):
    r'begin\-task'
    return t

def t_TkEndTask(t):
    r'end\-task'
    return t

def t_newLine(line):
    r'\n+'
    line.lexer.lineno += len(line.value)


# Manejador de errores
def t_error(invalido):
    """ Funcion por "default" cuando encuentra un token que no pertenece a la lista de tokens """
    error = 'Caracter ilegal "' + str(invalido.value[0]) + '" en fila ' \
            + str(invalido.lineno) + ', columna ' + str(invalido.lexpos + 1)
    InvalidTokens.append(error)
    invalido.lexer.skip(1)

def t_TkId(identificar):
    r'[a-zA-Z]+[0-9]*[a-zA-Z_0-9]*'
    identificar.type = reserved.get(identificar.value, 'TkId')
    return identificar

def t_TkNum(t):
    r'\d+'
    t.value = int(t.value)
    return t



#############################
###### Leer el archivo ######
#############################

lexer = lex.lex()

if len(argv) > 2:
    print("Uso del programa: python lexer.py <Nombre del archivo>")
    print("o utiizando: python3 lexer.py ")
    sys.exit()
elif len(argv) == 2:
    filepath = argv[1]
else:
    filepath = input('Archivo a Interpretar: ')

try:
    f = open(filepath, 'r')
    data = f.readline()
    output=""

    while data:
        # pasamos la linea como data al lexer
        # Esto es con el fin de calcular bien la columna de los tokens
        lexer.input(data)
        column=0
        controlSpace=True
        # Iteramos sobre el la entrada para extraer los tokens
        tok = lexer.token()
        while tok:
            if controlSpace==False:
                while column < (tok.lexpos):
                    output+=" "
                    column+=1
                column += len(str(tok.value))
            else:
                column += len(str(tok.value))
                controlSpace=False

            if (tok.type == 'TkId' or tok.type == 'TkNum'):
                token_info = str(tok.type) + '(valor="' + str(tok.value)+'", linea='  + str(tok.lineno)+', columna='  + str(tok.lexpos + 1)+')'
            else:
                token_info = str(tok.type) + '(linea=' +str(tok.lineno)+', columna='  + str(tok.lexpos + 1)+')'
            
            ValidTokens.append(token_info)
            output+= token_info
            # Agarro el siguiente token
            tok = lexer.token()
        output+="\n"
            
        # Leemos otra linea
        data = f.readline()

    # Cuando hay un error se imprime solo el error
    # Cuando no hay error se imprimen los tokens validos
    if (len(InvalidTokens) > 0):
        print(InvalidTokens[0])
    else:
        print(output)

except FileNotFoundError:
    print('Imposible abrir el archivo ' + filepath)
    sys.exit()