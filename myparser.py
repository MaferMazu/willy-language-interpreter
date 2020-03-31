#!/usr/bin/env python3
from typing import Any

import lexer
import ply.yacc as yacc
import logging
from Structure import Structure
from myStack import myStack

DEBUG_MODE = True

logging.basicConfig(
        level = logging.DEBUG,
        filename = "parselog.txt",
        filemode = "w",
        format = "%(filename)10s:%(lineno)4d:%(message)s"
    )


# import some required globals from tokenizer
tokens = lexer.tokens

stack = myStack()
stack.push_empty_table()

worldInstBool = False
taskBool = False
defineAsBool = False

def p_correctProgram(p):
    "correctProgram : program"
    print("Tu programa esta correcto")
    p[0] = p[1]
    print(stack)

def p_program(p):
    """
    program : worldBlock
            | taskBlock
            | worldBlock program
            | taskBlock program
    """

    pass

def p_worldInstSet(p):
    """worldInstSet : worldInst TkSemicolon worldInstSet
                    | worldInst worldInstSet
                    | worldInst TkSemicolon
    """
    global worldInstBool
    if(worldInstBool):
        worldInstBool = False
    pass

def p_worldInst(p):
    """ worldInst : worldSet
                | wallSet
                | newObjType
                | setPlaceObjWorld
                | setStartPosition
                | setBasketCapacity
                | newBoolean
                | newGoal
                | finalGoal
    """
    p[0]=p[1]



def p_wallSet(p):
    """wallSet : TkWall directions TkFrom TkNum TkNum TkTo TkNum TkNum"""
    if ((p[2]=="north" and p[4]==p[7] and p[5]<=p[8]) or
            (p[2]=="south" and p[4]==p[7] and p[5]>=p[8]) or
            (p[2]=="east" and p[5]==p[8] and p[4]>=p[7]) or
            (p[2]=="west" and p[5]==p[8] and p[4]<=p[7])):
            pass
    else:
        ##Deberia lanzarme error pero mientras colocaré pass
        # p_statement_print_error(p)
        print('Bad definition of wall in World')
    

def p_worldBlock(p):
    """worldBlock : TkBeginWorld ids worldInstSet TkEndWorld
                    | TkBeginWorld ids TkEndWorld
    """
    attributesObjects = {
        "type" : "World",
        "line" : p.lineno(2),
        "column" : p.lexpos(2) + 1,
    }
    
    p[0] = Structure(p[2], "WorldBlock", attributesObjects)
    print("Antes del pop")
    print(stack)
    stack.pop()
    stack.insert(p[2],attributesObjects)
    print("Despues del pop")
    print(stack)
    

def p_worldSet(p):
    '''worldSet : TkWorld TkNum TkNum 
                | empty'''
    print(p[0])

def p_newObjType(p):
    '''newObjType : TkObjType ids TkOf TkColor colors'''
    global worldInstBool
    print("Hey pila aqui")
    print("Hey pila aqui")
    attributesObjects = {
        "type" : "Object-type",
        "line" : p.lineno(2),
        "column" : p.lexpos(2) + 1,
        "color": p[5],
    }
    if worldInstBool:
        stack.insert(p[2],attributesObjects)
    else:
        table = []
        stack.push(table)
        stack.insert(p[2], attributesObjects)
        worldInstBool = True

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
        pass
    else:
        pass

def p_setStartPosition(p):
    '''setStartPosition : TkStart TkAt TkNum TkNum TkHeading directions'''
    pass

def p_setBasketCapacity(p):
    """setBasketCapacity : TkBasket TkOf TkCapacity TkNum"""
    pass

def p_newBoolean(p):
    '''newBoolean : TkBoolean ids TkWith TkInitial TkValue TkTrue 
                | TkBoolean ids TkWith TkInitial TkValue TkFalse
    '''
    global worldInstBool
    attributesObjects = {
        "type" : "Bool",
        "line" : p.lineno(2),
        "column" : p.lexpos(2) + 1,
        "value": p[6],
    }
    if worldInstBool:
        stack.insert(p[2],attributesObjects)
    else:
        table = []
        stack.push(table)
        stack.insert(p[2], attributesObjects)
        worldInstBool = True

def p_newGoal(p):
    """newGoal : TkGoal ids TkIs TkWilly TkIs TkAt TkNum TkNum
            | TkGoal ids TkIs TkNum ids TkObjectsLower TkIn TkBasket
            | TkGoal ids TkIs TkNum ids TkObjectsLower TkAt TkNum TkNum
    """
    global worldInstBool
    if len(p)==9:
        if p[4]=="TkWilly":
            attributesObjects = {
                "type" : "Goal-IsAt",
                "line" : p.lineno(2),
                "column" : p.lexpos(2) + 1,
                "column_": p[7],
                "row": p[8]
            }
        else:
            attributesObjects = {
                "type" : "Goal-InBasket",
                "line" : p.lineno(2),
                "column" : p.lexpos(2) + 1,
                "amount": p[4],
                "id-object": p[5],
            }
    else:
        attributesObjects = {
            "type" : "Goal-ObjectIn",
            "line" : p.lineno(2),
            "column" : p.lexpos(2) + 1,
            "amount": p[4],
            "id-object": p[5],
            "column_": p[8],
            "row": p[9]
        }
    if worldInstBool:
        stack.insert(p[2], attributesObjects)
    else:
        table = []
        stack.push(table)
        stack.insert(p[2], attributesObjects)
        worldInstBool = True

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
    global taskBool
    attributesObjects = {
            "type" : "Task",
            "line" : p.lineno(2),
            "column" : p.lexpos(2) + 1,
        }
    if taskBool:
        stack.insert(p[2], attributesObjects)
    else:
        table = []
        stack.push(table)
        stack.insert(p[2], attributesObjects)
        taskBool = True
    print("fin del task")
    print(stack)

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
    global taskBool
    if p[1] == "set":
        if len(p) == 3:
            attributesObjects = {
                "type" : "Bool",
                "line" : p.lineno(2),
                "column" : p.lexpos(2) + 1,
                "value": "true",
            }

        if len(p) == 5:
            attributesObjects = {
                "type" : "Bool",
                "line" : p.lineno(2),
                "column" : p.lexpos(2) + 1,
                "value": p[4],
            }

        if taskBool:
            stack.insert(p[2],attributesObjects)
        else:
            table = []
            stack.push(table)
            stack.insert(p[2], attributesObjects)
            taskBool = True
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
    """instructions : primitiveInstructions
                    | TkIf booleanTests TkThen instructions
                    | TkIf primitiveInstructions TkThen instructions
                    | TkIf booleanTests TkThen primitiveInstructions
                    | TkIf primitiveInstructions TkThen primitiveInstructions
                    | TkIf booleanTests TkThen instructions TkElse instructions
                    | TkIf primitiveInstructions TkThen instructions TkElse instructions
                    | TkRepeat TkNum TkTimes instructions
                    | TkWhile booleanTests TkDo instructions
                    | TkBegin multiInstructions TkEnd
                    | instructionDefineAs instructions
                    | TkSemicolon
                    """

    if p[1] != "instructionDefineAs":
        global defineAsBool
        attributesObjects = {
            "type": "Instruction",
            "line" : p.lineno(2),
            "column" : p.lexpos(2) + 1,
        }
        if len(p) > 3:
            print(p[2])
            print(p[0])
            stack.insert(p[2], p[0])
        else:
            print("Esto es un ;")

    else:
        stack.pop()
        stack.insert(p[1],p[0])
        defineAsBool = False
        pass

def p_instructionDefine(p):
    '''instructionDefine : instructionDefineAs instructions'''
    stack.pop()

def p_instructionDefineAs(p):
    '''instructionDefineAs : TkDefine ids TkAs'''
    print("EUREKA")
    global defineAsBool
    defineAsBool = False
    attributesObjects = {
        "type" : "Instruction",
        "line" : p.lineno(2),
        "column" : p.lexpos(2) + 1,
        }
    if defineAsBool:
        print("La variable es TRUE")
    else:
        table = []
        stack.push(table)
        defineAsBool = True

def p_directions(p):
    '''directions : TkNorth 
                | TkEast 
                | TkSouth 
                | TkWest'''
    p[0]=p[1]


def p_empty(p):
    'empty :'
    pass


# def p_statement_print_error(p):
#     'statement : PRINT error'
#     print("Syntax error in print statement. Bad expression")

def p_error(p):
    if p:
        print("Syntax error at token", p.type)
        # Just discard the token and tell the parser it's okay.
        parser.error()
    else:
        print("Syntax error at EOF")

