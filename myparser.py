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
    print("Tu programa esta correcto")
    p[0] = p[1]


def p_program(p):
    '''
    program : worldBlock 
            | taskBlock 
            | worldBlock program
            | taskBlock program
    '''
    print(len(p))
    if(len(p) <= 2):
       # p[0] = p[1]
       print("WeHAsNOTInst")
    else:
        print("WeGotInst")
       # p[0] = p[1] + p[2]

def p_worldInstSet(p):
    '''worldInstSet : worldInst TkSemicolon worldInstSet
                    | worldInst worldInstSet
                    | worldInst TkSemicolon
    '''

def p_worldInst(p):
    ''' worldInst : worldSet  
                | wallSet  
                | newObjType  
                | setPlaceObjWorld  
                | setStartPosition 
                | setBasketCapacity  
                | newBoolean  
                | newGoal 
                | finalGoal  
    '''

def p_wallSet(p):
    '''wallSet : TkWall directions TkFrom TkNum TkNum TkTo TkNum TkNum'''
    pass

def p_worldBlock(p):
    '''worldBlock : TkBeginWorld ids worldInstSet TkEndWorld  
                    | TkBeginWorld ids TkEndWorld  '''
    #p[0] = p[1] + p[2] + p[3]

def p_worldSet(p):
    '''worldSet : TkWorld TkNum TkNum 
                | empty'''

def p_newObjType(p):
    '''newObjType : TkObjType ids TkOf TkColor colors'''

def p_colors(p):
    '''colors : TkRed
                | TkBlue
                | TkMagenta
                | TkCyan
                | TkGreen
                | TkYellow'''

def p_setPlaceObjWorld(p):
    '''setPlaceObjWorld : TkPlace TkNum TkOf ids TkAt TkNum TkNum
                        | TkPlace TkNum TkOf ids TkIn TkBasketLower
    '''

def p_setPlaceObjBasket(p):
    '''setPlaceObjBasket : TkPlace TkNum TkOf ids TkIn TkBasketLower'''

def p_setStartPosition(p):
    '''setStartPosition : TkStart TkAt TkNum TkNum TkHeading directions'''

def p_setBasketCapacity(p):
    '''setBasketCapacity : TkBasket TkOf TkCapacity TkNum'''

def p_newBoolean(p):
    '''newBoolean : TkBoolean ids TkWith TkInitial TkValue TkTrue 
                | TkBoolean ids TkWith TkInitial TkValue TkFalse
    '''

def p_newGoal(p):
    '''newGoal : TkGoal ids TkIs TkWilly TkIs TkAt TkNum TkNum
            | TkGoal ids TkIs TkNum ids TkObjectsLower TkIn TkBasket
            | TkGoal ids TkIs TkNum ids TkObjectsLower TkAt TkNum TkNum 
    '''
def p_finalGoal(p):
    '''finalGoal : TkFinalG TkIs ids 
            | TkFinalG TkIs ids TkAnd ids
            | TkFinalG TkIs ids TkOr ids
            | TkFinalG TkIs TkNot ids 
    '''

def p_ids(p):
    "ids : TkId"
    pass

def p_taskBlock(p):
    "taskBlock : ids"
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