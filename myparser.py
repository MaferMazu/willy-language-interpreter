#!/usr/bin/env python3
import lexer
import Node
import ply.yacc as yacc
import logging
from Structure import Structure 

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
    print("Place Len")
    print(len(p))
    if (len(p)<8):
        print("Probando")
        attributesObjects = {
            "amount": p[2],
            "object": p[4]
        }
        place = Structure("Place_bascket","Place",attributesObjects)
        print(place)

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
    '''finalGoal : TkFinalG TkIs finalGoalTest 
    '''

def p_finalGoalTest(p):
    '''finalGoalTest :  TkId TkAnd TkId
                     |  TkId TkOr TkId
                     |  TkNot TkId
                     |  TkParenL TkId TkParenR
                     |  TkId TkAnd finalGoalTest
                     |  TkId TkOr finalGoalTest
                     |  TkNot finalGoalTest
                     |  TkParenL TkId TkParenR finalGoalTest
    '''


def p_ids(p):
    "ids : TkId"
    pass

def p_taskBlock(p):
    '''taskBlock : TkBeginTask ids TkOn ids multiInstructions TkEndTask'''
    pass

def p_multiInstructions(p):
    '''multiInstructions : instructions
                        | empty
                        | instructions TkSemicolon multiInstructions'''
    pass

def p_primitiveInstructions(p):
    '''primitiveInstructions : TkMove
                    | TkTurnL
                    | TkTurnR
                    | TkPick ids
                    | TkDrop ids
                    | TkSet ids
                    | TkSet primitiveBoolean
                    | TkSet primitiveBoolean TkTo TkTrue
                    | TkSet primitiveBoolean TkTo TkFalse
                    | TkSet ids TkTo TkTrue
                    | TkSet ids TkTo TkFalse
                    | TkClear ids
                    | TkClear primitiveBoolean
                    | TkFlip primitiveBoolean
                    | TkFlip ids
                    | ids
                    | TkTerminate'''
    pass

def p_booleanTests(p):
    '''booleanTests : ids
                    | primitiveBoolean
                    | TkFound TkParenL ids TkParenR
                    | TkCarrying TkParenL ids TkParenR
                    | booleanTests TkAnd booleanTests
                    | booleanTests TkOr booleanTests
                    | TkNot booleanTests
                    | TkParenL booleanTests TkParenR'''
    pass

def p_primitiveBoolean(p):
    '''primitiveBoolean : TkFrontCl
                        | TkLeftCl
                        | TkRightCl
                        | TkLookingN
                        | TkLookingE
                        | TkLookingS
                        | TkLookingW'''
    pass

def p_instructions(p):
    '''instructions : primitiveInstructions
                    | TkIf booleanTests TkThen instructions
                    | TkIf primitiveInstructions TkThen instructions
                    | TkIf booleanTests TkThen primitiveInstructions
                    | TkIf primitiveInstructions TkThen primitiveInstructions
                    | TkIf booleanTests TkThen instructions TkElse instructions
                    | TkIf primitiveInstructions TkThen instructions TkElse instructions
                    | TkRepeat TkNum TkTimes instructions
                    | TkWhile booleanTests TkDo instructions
                    | TkBegin multiInstructions TkEnd
                    | TkDefine ids TkAs instructions
                    | TkSemicolon
                    '''
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