import lexer
import Node
import ply.yacc as yacc
import logging
DEBUG_MODE = True
logging.basicConfig(
        level = logging.DEBUG,
        filename = "parselog.txt",
        filemode = "w",
        format = "%(filename)10s:%(lineno)4d:%(message)s"
    )
# import some required globals from tokenizer
tokens = lexer.tokens

def p_correctProgram(p):
    "correctProgram : program"
    p[0] = p[1]


def p_program(p):
    """
    program : worldBlock 
            | taskBlock 
            | worldBlock program
            | taskBlock program
    """
    print(len(p))
    if(len(p) <= 2):
        p[0] = p[1]
    else:
        P[0] = p[1] + p[2]

def p_wallSet(p):
    '''wallSet : TkWall directions TkFrom TkNum TkNum TkTo TkNum TkNum'''
    pass

def p_worldBlock(p):
    '''worldBlock : TkBeginWorld TkId instructions TkEndWorld worldBlock 
                    | TkBeginWorld TkId TkEndWorld worldBlock 
                    | TkBeginWorld TkId TkEndWorld '''
    p[0] = p[1] + p[2] + p[3]

def p_worldSet(p):
    '''worldSet : TkWorld TkNum TkNum 
                | empty'''

def p_newObjectType(p):
    '''newObjectType : TkObjectType TkId TkOf TkColor colors'''

def p_colors(p):
    '''colors : TkRed
                | TkBlue
                | TkMagenta
                | TkCyan
                | TkGreen
                | TkYellow'''

def p_setPlaceObjWorld(p):
    '''setPlaceObjWorld : TkPlace TkNum TkOf TkId TkAt TkNum TkNum'''

def p_setPlaceObjBasket(p):
    '''setPlaceObjBasket : TkPlace TkNum TkOf TkId TkIn TkBasketLower'''

def p_setStartPosition(p):
    '''setStartPosition : TkStart TkAt TkNum TkNum TkHeading directions'''

def p_setBasketCapacity(p):
    '''setBasketCapacity : TkBasket TkOf TkCapacity TkNum'''

def p_newBoolean(p):
    '''newBoolean : TkBoolean TkId TkWith TkInitial TkValue TkTrue 
                | TkBoolean TkId TkWith TkInitial TkValue TkFalse
    '''

def p_newGoal(p):
    '''newGoal : TkGoal TkId TkIs TkWilly TkIs TkAt TkNum TkNum
            | TkGoal TkId TkIs TkNum TkId TkObjects TkIn TkBasket
            | TkGoal TkId TkIs TkNum TkId TkObjects TkAt TkNum TkNum 
    '''

def p_instructions(p):
    "instructions : TkId"
    pass

def p_taskBlock(p):
    "taskBlock : TkId"
    pass

def p_directions(p):
    '''directions : TkNorth 
                | TkEast 
                | TkSouth 
                | TkWest'''
    pass

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print("Syntax error at token", p.type)
        # Just discard the token and tell the parser it's okay.
        parser.error
    else:
        print("Syntax error at EOF")

#parser = yacc.yacc()