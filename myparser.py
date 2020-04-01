#!/usr/bin/env python3
from typing import Any

import lexer
import ply.yacc as yacc
import logging
from Structure import Structure
from myStack import myStack
from Node import *

DEBUG_MODE = True
# parser: Any = yacc.parse(lexer)
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
    print(p[1].type,p[1].children)
    print(p[1].children[0].type,p[1].children[1].type)
    print(isinstance(p[0],Node))
    print(str(p[0]))

def p_program(p):
    """
    program : worldBlock
            | taskBlock
            | worldBlock program
            | taskBlock program
    """
    if len(p)==2:
        p[0]=Node("ProgramBlock",[p[1]])
    else:
        p[0]=Node("ProgramBlock",[p[1],p[2]])


def p_worldInstSet(p):
    """worldInstSet : worldInst TkSemicolon worldInstSet
                    | worldInst worldInstSet
                    | worldInst TkSemicolon
    """
    global worldInstBool
    if(worldInstBool):
        worldInstBool = False
    if len(p)==4:
        p[0]=Node("WorldInstancia",[p[1],p[3]],p[2])
    else:
        if p[2]==";":
            p[0]=Node("WorldInstancia",[p[1]],p[2])
        else:
            p[0]=Node("WorldInstancia",[p[1],p[2]])

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
    p[0]=Node("WorldInstructions",[p[1]])

def p_wallSet(p):
    """wallSet : TkWall directions TkFrom TkNum TkNum TkTo TkNum TkNum"""
    if ((p[2]=="north" and p[4]==p[7] and p[5]<=p[8]) or
            (p[2]=="south" and p[4]==p[7] and p[5]>=p[8]) or
            (p[2]=="east" and p[5]==p[8] and p[4]>=p[7]) or
            (p[2]=="west" and p[5]==p[8] and p[4]<=p[7])):
        p[0]= Node("WallSet",[p[2]],[p[1],p[3],p[4],p[5],p[6],p[7],p[8]])
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
    if len(p)==5:
        p[0] = Node("WorldBlock",[p[2],p[3]],[p[1],p[4]])
    else:
        p[0] = Node("WorldBlock",[p[2]],[p[1],p[3]])
    # print("Antes del pop")
    # print(stack)
    stack.pop()
    stack.insert(p[2],attributesObjects)
    print("Despues del pop")
    # print(stack)
    

def p_worldSet(p):
    '''worldSet : TkWorld TkNum TkNum 
                | empty'''
    if len(p)==4:
        p[0]=Node("WorldSet",[],[p[1],p[2],p[3]])
    else:
        p[0]=p[1]

def p_newObjType(p):
    '''newObjType : TkObjType ids TkOf TkColor colors'''
    global worldInstBool
    p[0]=Node("NewObjectType",[p[2],p[5]],[p[1],p[3],p[4]])
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

    if len(p)==8:
        p[0]=Node("PlaceObjWorld",[p[4]],[p[1],p[2],p[3],p[5],p[6],p[7]])
    else:
        p[0]=Node("PlaceObjWorld",[p[4]],[p[1],p[2],p[3],p[5],p[6]])

def p_setStartPosition(p):
    '''setStartPosition : TkStart TkAt TkNum TkNum TkHeading directions'''
    p[0]=Node("WillyStartPosition",[p[6]],[p[1],p[2],p[3],p[4],p[5]])

def p_setBasketCapacity(p):
    """setBasketCapacity : TkBasket TkOf TkCapacity TkNum"""
    p[0]=Node("BasketCapacity",[],[p[1],p[2],p[3],p[4]])

def p_newBoolean(p):
    '''newBoolean : TkBoolean ids TkWith TkInitial TkValue TkTrue 
                | TkBoolean ids TkWith TkInitial TkValue TkFalse
    '''
    p[0]=Node("NewBoolean",[p[2]],[p[1],p[3],p[4],p[5],p[6]])
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
            p[0]=Node("NewGoal",[p[2]],[p[1],p[3],p[4],p[5],p[6],p[7],p[8]])
            attributesObjects = {
                "type" : "Goal-IsAt",
                "line" : p.lineno(2),
                "column" : p.lexpos(2) + 1,
                "column_": p[7],
                "row": p[8]
            }
        else:
            p[0]=Node("NewGoal",[p[2],p[5]],[p[1],p[3],p[4],p[6],p[7],p[8]])
            attributesObjects = {
                "type" : "Goal-InBasket",
                "line" : p.lineno(2),
                "column" : p.lexpos(2) + 1,
                "amount": p[4],
                "id-object": p[5],
            }
    else:
        p[0]=Node("NewGoal",[p[2],p[5]],[p[1],p[3],p[4],p[6],p[7],p[8],p[9]])
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
    p[0]=Node("FinalGoal",[p[3]],[p[1],p[2]])

def p_finalGoalTest(p):
    '''finalGoalTest : ids
                     | disyuncionGoal
                     | conjuncionGoal
                     | negacionGoal
                     | TkParenL finalGoalTest TkParenR
    '''
    if len(p)==2:
        p[0]=Node("FinalGoal",[p[1]])
    else:
        p[0]=Node("FinalGoal",[p[2]],[p[1],p[3]])

def p_disyuncionGoal(p):
    '''disyuncionGoal : finalGoalTest TkOr finalGoalTest'''
    p[0]=Node("Disyuncion",[p[1],p[3]],p[2])

def p_conjuncionGoal(p):
    '''conjuncionGoal : finalGoalTest TkAnd finalGoalTest'''
    p[0]=Node("Conjuncion",[p[1],p[3]],p[2])

def p_negacionGoal(p):
    '''negacionGoal : TkNot finalGoalTest'''
    p[0]=Node("Negación",[p[2]],p[1])

def p_ids(p):
    "ids : TkId"
    p[0]=p[1]
    p.set_lineno(0, p.lineno(1))
    p.set_lexpos(0, p.lexpos(1))

def p_taskBlock(p):
    '''taskBlock : TkBeginTask ids TkOn ids multiInstructions TkEndTask'''
    global taskBool
    attributesObjects = {
            "type" : "Task",
            "line" : p.lineno(2),
            "column" : p.lexpos(2) + 1,
        }
    print("Antes del pop")
    print(stack)
    stack.pop()
    stack.insert(p[2], attributesObjects)
    # print("Despues del pop")
    print(stack)
    print("fin del task")
    # print(stack)

def p_multiInstructions(p):
    '''multiInstructions : instructions
                        | empty
                        | instructions TkSemicolon multiInstructions'''
    if len(p)==2:
        p[0]=p[1]
    else:
        p[0]=Node("MultiInstrucción",[p[1],p[3]],p[2])


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
                    | TkId
                    | TkTerminate'''
    global taskBool
    if len(p)==2:
        p[0]=Node("PrimitiveInstruction",[],p[1])
    if len(p)==3:
        p[0]=Node("PrimitiveInstruction",[p[2]],p[1])
    elif len(p)>= 4:
        p[0]=Node("PrimitiveInstruction",[p[2]],[p[1],p[3],p[4]])
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
    """booleanTests : ids
                    | primitiveBoolean
                    | TkFound TkParenL ids TkParenR
                    | TkCarrying TkParenL ids TkParenR
                    | conjuncionBool
                    | disyuncionBool
                    | negacionBool
                    | TkParenL booleanTests TkParenR
                    """
    if len(p)==2:
        p[0]=Node("BooleanTest",[p[1]])
    if len(p)==5:
        p[0]=Node("BooleanTest",[p[3]],[p[1],p[2],p[4]])
    if len(p)==4:
        p[0]=Node("BooleanTest",[p[2]],[p[1],p[3]])

def p_disyuncionBool(p):
    '''disyuncionBool : booleanTests TkOr booleanTests'''
    p[0]=Node("Disyuncion",[p[1],p[3]],p[2])

def p_conjuncionBool(p):
    '''conjuncionBool : booleanTests TkAnd booleanTests'''
    p[0]=Node("Conjuncion",[p[1],p[3]],p[2])

def p_negacionBool(p):
    '''negacionBool : TkNot booleanTests'''
    p[0]=Node("Negación",[p[2]],p[1])

def p_primitiveBoolean(p):
    """primitiveBoolean : TkFrontCl
                        | TkLeftCl
                        | TkRightCl
                        | TkLookingN
                        | TkLookingE
                        | TkLookingS
                        | TkLookingW
                        """
    p[0]=p[1]

def p_instructions(p):
    """instructions : primitiveInstructions
                    | TkIf booleanTests TkThen instructions
                    | TkIf booleanTests TkThen instructions TkElse instructions
                    | TkRepeat TkNum TkTimes instructions
                    | TkWhile booleanTests TkDo instructions
                    | TkBegin multiInstructions TkEnd
                    | instructionDefineAs instructions
                    """
    if len(p)==2:
        p[0]= Node("Instructions",[p[1]])
    elif len(p)==3:
        p[0]= Node("Instructions",[p[1],p[2]])
    elif len(p)==4:
        p[0]= Node("Instructions",[p[2]],[p[1],p[3]])
    elif len(p)==5:
        if p[1]=="TkRepeat":
            p[0]= Node("Instructions",[p[4]],[p[1],p[2],p[3]])
        else:
            p[0] = Node("Instructions",[p[2],p[4]],[p[1],p[3]])
    elif len(p)==7:
        p[0]= Node("Instructions",[p[2],p[4],p[6]],[p[1],p[3],p[5]])

    print("Primer elemento de p: ")
    print(p)
    if len(p)==3:
        global defineAsBool
        attributesObjects = {
            "type": "Instruction",
            "line": p.lineno(1),
            "column": p.lineno(1) + 1,
        }
        stack.pop()
        stack.insert(p[1].children,attributesObjects)
        defineAsBool = False


# def p_instructionDefine(p):
#     '''instructionDefine : instructionDefineAs instructions'''
#     p[0]=Node("Define",[p[1],p[2]])
#     stack.pop()

def p_instructionDefineAs(p):
    '''instructionDefineAs : TkDefine ids TkAs'''
    print("EUREKA")
    p[0]=Node("DefineAs",[p[2]],[p[1],p[3]])
    global defineAsBool
    defineAsBool = False
    """ attributesObjects = {
        "type" : "Instruction",
        "line" : p.lineno(2),
        "column" : p.lexpos(2) + 1,
        } """
    if defineAsBool:
        print("La variable es TRUE")
    else:
        print("la variable es false, procedemos a pusherar" + "\n")
        print(stack)
        print("Aqui estuvo el stack")
        table = []
        stack.push(table)
        defineAsBool = True

def p_directions(p):
    '''directions : TkNorth 
                | TkEast 
                | TkSouth 
                | TkWest'''
    p[0]=Node("Direction",[],p[1])


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
        parser.errok()
    else:
        print("Syntax error at EOF")

