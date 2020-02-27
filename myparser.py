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
    pass

def p_worldInstSet(p):
    '''worldInstSet : worldInst TkSemicolon worldInstSet
                    | worldInst worldInstSet
                    | worldInst TkSemicolon
    '''
    pass

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
    p[0]=p[1]

def p_wallSet(p):
    '''wallSet : TkWall directions TkFrom TkNum TkNum TkTo TkNum TkNum'''
    print("Probando")
    attributesObjects = {
        "direction": p[2],
        "column1": p[4],
        "row1": p[5],
        "column2":p[7],
        "row2": p[8]
    }
    p[0] = Structure("","WallSet",attributesObjects)
    print(p[0])
    

def p_worldBlock(p):
    '''worldBlock : TkBeginWorld ids worldInstSet TkEndWorld  
                    | TkBeginWorld ids TkEndWorld  '''

def p_worldSet(p):
    '''worldSet : TkWorld TkNum TkNum 
                | empty'''
    print("Probando")
    attributesObjects = {
        "column": p[2],
        "row": p[3],
    }
    p[0] = Structure("","WorldSet",attributesObjects)
    print(p[0])

def p_newObjType(p):
    '''newObjType : TkObjType ids TkOf TkColor colors'''
    print("Probando")
    attributesObjects = {
        "color": p[5]
    }
    p[0] = Structure(p[2],"New-Object-Type",attributesObjects)
    print(p[0])

def p_colors(p):
    '''colors : TkRed
                | TkBlue
                | TkMagenta
                | TkCyan
                | TkGreen
                | TkYellow'''
    p[0]=p[1]

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
        p[0] = Structure("Place_basket","Place",attributesObjects)
        print(p[0])
    else:
        print("Probando")
        attributesObjects = {
            "amount": p[2],
            "object": p[4],
            "column": p[6],
            "row": p[7]
        }
        p[0] = Structure("Place_object","Place",attributesObjects)
        print(p[0])

def p_setStartPosition(p):
    '''setStartPosition : TkStart TkAt TkNum TkNum TkHeading directions'''
    attributesObjects = {
        "column": p[3],
        "row": p[4],
        "head-direction": p[6]
    }
    p[0] = Structure("","StartPositionOfWilly",attributesObjects)
    print(p[0])

def p_setBasketCapacity(p):
    '''setBasketCapacity : TkBasket TkOf TkCapacity TkNum'''
    attributesObjects = {
        "amount": p[4]
    }
    p[0] = Structure("","BasketCapacityOfWilly",attributesObjects)
    print(p[0])

def p_newBoolean(p):
    '''newBoolean : TkBoolean ids TkWith TkInitial TkValue TkTrue 
                | TkBoolean ids TkWith TkInitial TkValue TkFalse
    '''
    attributesObjects = {
        "value": p[6]
    }
    p[0] = Structure(p[2],"Boolean",attributesObjects)
    print(p[0])

def p_newGoal(p):
    '''newGoal : TkGoal ids TkIs TkWilly TkIs TkAt TkNum TkNum
            | TkGoal ids TkIs TkNum ids TkObjectsLower TkIn TkBasket
            | TkGoal ids TkIs TkNum ids TkObjectsLower TkAt TkNum TkNum 
    '''
    if len(p)==8:
        if p[4]=="TkWilly":
            attributesObjects = {
                "column": p[7],
                "row": p[8]
            }
            p[0] = Structure(p[2],"newGoalWilly",attributesObjects)
            print(p[0])
        else:
            attributesObjects = {
                "amount": p[4],
                "id-object": p[5],
            }
            p[0] = Structure(p[2],"newGoalBasket",attributesObjects)
            print(p[0])
    else:
        attributesObjects = {
            "amount": p[4],
            "id-object": p[5],
            "column": p[8],
            "row": p[9]
        }
        p[0] = Structure(p[2],"newGoalPositionObject",attributesObjects)
        print(p[0])

def p_finalGoal(p):
    '''finalGoal : TkFinalG TkIs finalGoalTest'''

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
    p[0]=p[1]

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
    if len(p)==1:
        p[0]=p[1]

def p_primitiveBoolean(p):
    '''primitiveBoolean : TkFrontCl
                        | TkLeftCl
                        | TkRightCl
                        | TkLookingN
                        | TkLookingE
                        | TkLookingS
                        | TkLookingW'''
    p[0]=p[1]

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
    p[0]=p[1]


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