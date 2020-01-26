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
    'int': 'TkInt',     # 
    #'bool': 'TkBool',   Entendi que hay 2 tipos de boolean

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

    #'TkCOpenPar',
    #'TkClosePar',
    'TkSemicolon',
    'TkComments',
    #'TkCommentsBlock'

] + list(reservedWords.values())

# Especificaciones de los tokens

#t_TkClosePar = r'\)'
t_TkSemicolon = r';'

t_TkComments = r'[-]{2}.*[\n]'


# Ignored Chars
t_ignore_Space = r'\s'             # Space
#t_ignore_Comment = r'\{\{.*\}\}'        # Comentarios - falta colocar el regex de {{}}
t_ignore_Line = r' \n'             # Salto de linea
t_ignore_Tab = r' \t'              # Tabuladores


ValidTokens = []                #Coleccion de tokens validos
InvalidTokens = []              #Coleccion de tokens invalidos



# Prove of import Functions (This class is ony for tokens, don't declare functions here) - Main is Lexer
