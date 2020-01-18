"""
Clase encargada de llevar todos los tokens:
Palabras Reservadas
Funciones
I/O
Arreglo de los tokens declarados
Especificaciones de los mismos
"""

from ply import lex

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

    # Common Words - Oper - Used on previous words to build a instruction
    'from': 'TkFrom',
    'to': 'TkTo',
    'of': 'TkOf',
    'color': 'TkColor',
    'at': 'TkAt',
    'in': 'TkIn',
    'is': 'TkIs',
    'heading': 'TkHeading',
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
    # 'int': 'TkInt',     # No se si lo vamos a usar
    'bool': 'TkBool',   # Entendi que hay 2 tipos de boolean

    # Conditionals
    'if': 'TkIf',
    'fi': 'Tkfi',
    'else': 'TkElse',
    'then': 'TkThen',

    # Loops
    'for': 'TkFor',
    'repeat': 'TkRepeat',
    'while': 'TkWhile',
    'times': 'TkTimes',

    # Aux
    'define': 'TkDefine',
    'begin': 'TkBegin',
    'end': 'TkEnd',
    'as': 'TkAs',
    'and': 'TkAnd',
    'or': 'TkOr',
    'not': 'TkNot',


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
}


def outHello():
    print("Estamos conectando correctamente")
