#!/usr/bin/env python3
from typing import Any
import os, sys
import lexer
import ply.yacc as yacc
import logging
from myStack import myStack
from Node import *
from World import *
from Task import *
from ModelProcedure import *
import copy

"""
    Analizador Semantico y sintactico + (Interpretador) De Willy*
    Primera fase del proyecto
    Traductores e Interpretadores (CI-3725)
    Maria Fernanda Magallanes (13-10787)
    Jesus Marcano (12-10359)
    E-M 2020

    Dentro de myparser, encontramos todos lo metodos que son encargados de desarrollar las producciones,
    estos de la forma: p_nombreFuncion
    dentro de ellos se hace split de los tokens recibidos para poder armar los distintos nodos que generaran el 
    arbol de lectura de nuestro parser. 
    
    En la primera seccion tenemos todas las definicones del World
    
    En la segunda seccion tenemos todas las definicios del Task
    
    En la tercera definicion tenemos los manejos de errores semanticos y sintaticos de Willy
    
    
    Aqui se componen las validaciones de la correcta escritura de las frases de ejecucion, 
    del orden que debe llevar cada una de las instrucciones, sobre si tenemos elementos repetidos dentro
    de un mismo conexto(scope) para poder hacer buenas definiciones de nuestras variabe y desaparecer ambiguedades. 
    
    En caso de error se colecta la linea, el token escrito y se le señala al usuario estos componentes a donde deberia corregir el script
"""

DEBUG_MODE = True
# parser: Any = yacc.parse(lexer)
# logging.basicConfig(
#         level = logging.DEBUG,
#         filename = "parselog.txt",
#         filemode = "w",
#         format = "%(filename)10s:%(lineno)4d:%(message)s"
#     )

precedence = (
    ('left', 'TkThen'),
    ('left', 'TkAnd', 'TkOr', 'TkElse'),
    ('right', 'TkNot', 'TkBegin'),  # Unary minus operator
)

# import some required globals from tokenizer
tokens = lexer.tokens
ParserErrors = []

procedures = ModelProcedure()

newWorld = Any

stack = myStack()
stack.push_empty_table()

programBlock = []
createdWorlds = []
objectsInWorlds = []
booleansOfWorlds = []
tasks = []

howManyTask = 0
activeWorld = Any
currentTask = Any

worldInstBool = False
taskBool = False
defineAsBool = False
validateFinalGoal = False
hasSetted = False
isBasketDeclared = False
firstDefineOnTask = False
blockNumber = 0


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
    global hasSetted
    hasSetted
    if len(p) == 2:
        p[0] = Node("Program Block:", [p[1]])
    else:
        p[0] = Node("Program Block:", [p[1], p[2]])

    r = programBlock[0][1]["type"]


def p_worldInstSet(p):
    """worldInstSet : worldInst worldInstSet
                    | worldInst

    """
    global worldInstBool

    if (worldInstBool):
        worldInstBool = False
    if len(p) == 4:
        p[0] = Node("WorldInstancia:", [p[1], p[3]])

    elif len(p) == 2:
        p[0] = Node("WorldInstancia:", [p[1]])
    else:
        p[0] = Node("WorldInstancia:", [p[1], p[2]])


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
    p[0] = Node("WorldInstructions", [p[1]])


def p_wallSet(p):
    """wallSet : TkWall directions TkFrom TkNum TkNum TkTo TkNum TkNum TkSemicolon"""
    global newWorld
    actualDir = p[2]

    if actualDir == "north":

        if p[4] == p[7] and p[5] <= p[8]:
            p[0] = Node("WallSet:", [p[2]])
            newWorld.setWall([p[4], p[5]], [p[7], p[8]], actualDir)
        else:
            data_error = {
                "type": "Bad definition of " + actualDir + "Dimentions",
                "line": p.lineno(2),
                "column": p.lexpos(2) + 1,
            }
            errorSemantic(data_error)
    elif actualDir == "south":

        if p[4] == p[7] and p[5] >= p[8]:
            p[0] = Node("WallSet:", [p[2]])
            newWorld.setWall([p[4], p[5]], [p[7], p[8]], actualDir)
        else:
            data_error = {
                "type": "Bad definition of" + actualDir + "Dimentions",
                "line": p.lineno(2),
                "column": p.lexpos(2) + 1,
            }
            errorSemantic(data_error)
    elif actualDir == "west":
        if p[5] == p[8] and p[4] >= p[7]:
            p[0] = Node("WallSet:", [p[2]])
            newWorld.setWall([p[4], p[5]], [p[7], p[8]], actualDir)
        else:
            data_error = {
                "type": "Bad definition of " + actualDir + "Dimentions",
                "line": p.lineno(2),
                "column": p.lexpos(2) + 1,
            }
            errorSemantic(data_error)
    elif actualDir == "east":
        if p[5] == p[8] and p[4] <= p[7]:
            p[0] = Node("WallSet:", [p[2]])
            newWorld.setWall([p[4], p[5]], [p[7], p[8]], actualDir)
        else:
            data_error = {
                "type": "Bad definition of " + actualDir + "Dimentions",
                "line": p.lineno(2),
                "column": p.lexpos(2) + 1,
            }
            errorSemantic(data_error)
    else:
        data_error = {
            "type": "Bad token of Direcction" + actualDir,
            "line": p.lineno(2),
            "column": p.lexpos(2) + 1,
        }

        errorSemantic(None)


def p_worldDefinition(p):
    """
    worldDefinition : TkBeginWorld ids
    """
    type = {
        "type": "World"
    }
    global newWorld

    p[0] = Node("", [p[2]])
    data = [p[0].children[0], type]
    newWorld = World(p[2])
    newWorld.setDimension([1, 1])
    programBlock.append(data)


def p_worldBlock(p):
    """worldBlock : worldDefinition worldInstSet TkEndWorld
                  | worldDefinition TkEndWorld
    """
    id = p[1].children[0]
    global blockNumber
    global validateFinalGoal
    global createdWorlds
    attributesObjects = {
        "type": "World",
        "line": p.lineno(2),
        "column": p.lexpos(2) + 1,
    }
    dataFlag = {
        "ownerPrev": id,
        "WorldClass": "Aqui estara la clase del mundo"
    }
    if len(p) == 4:
        p[0] = Node("WorldBlock", [p[2]])
    else:
        p[0] = Node("WorldBlock", [p[2]])

    if blockNumber == 0:
        blockNumber = blockNumber + 1
    else:
        blockNumber = blockNumber + 1
    validateFinalGoal = False

    if len(stack.stack) > 1:
        stack.pop()
    stack.insert(id, attributesObjects)
    createdWorlds.append(newWorld)
    global hasSetted
    hasSetted = False

    print("###############")
    print("Estado inicial de " + str(newWorld.id))
    print("La posición de Willy es: " + str(newWorld.getWillyPosition()[0]) + " mirando hacia el " + str(
        newWorld.getWillyPosition()[1]))
    print("Lo que tiene en el basket es:\n", newWorld.getObjectsInBasket())
    print("El estado de los bools es:\n", newWorld.getBools())
    print("El final goal es:\n" + newWorld.getFinalGoal())
    print("El valor del final goal es: ", newWorld.getValueFinalGoal())
    print(newWorld)


def p_worldSet(p):
    """worldSet : TkWorld TkNum TkNum TkSemicolon
                | empty"""
    global newWorld
    global hasSetted
    if not hasSetted:
        if 0 != p[2] or (0 != p[3]):
            if len(p) == 4:
                p[0] = Node("WorldSet", [])
                newWorld.setDimension([p[2], p[3]])
            else:
                newWorld.setDimension([1, 1])
                p[0] = p[1]
        else:
            data_error = {
                "type": "0 dimention of World",
                "line": p.lineno(2),
                "column": p.lexpos(2) + 1,
            }
            errorSemantic(data_error)
    else:
        data_error = {
            "type": (
                        "To place objects in World:" + newWorld.id + "need to declare dimentions at start" + "\n" + "Can't replace dimentions"),
            "line": p.lineno(2),
            "column": p.lexpos(2) + 1,
        }
        errorSemantic(data_error)


def p_newObjType(p):
    """newObjType : TkObjType ids TkOf TkColor colors TkSemicolon"""
    global worldInstBool
    global newWorld
    id = p[2]

    if procedures.findObj(id, programBlock):
        data_error = {
            "type": "Objeto " + id + " contiene nombre de un World o Task",
            "line": p.lineno(2),
            "column": p.lexpos(2) + 1,
        }
        errorSemantic(data_error)

    else:
        p[0] = Node("NewObjectType", [p[2], p[5]])
        attributesObjects = {
            "type": "Object-type",
            "line": p.lineno(2),
            "column": p.lexpos(2) + 1,
            "color": p[5],
        }
        if worldInstBool:
            stack.insert(p[2], attributesObjects)

        else:
            table = []
            stack.push(table)
            stack.insert(p[2], attributesObjects)
            worldInstBool = True
        newWorld.setObjects(id, attributesObjects["color"])


def p_colors(p):
    """colors : TkRed
                | TkBlue
                | TkMagenta
                | TkCyan
                | TkGreen
                | TkYellow
    """
    p[0] = p[1]
    p.set_lineno(0, p.lineno(1))


def p_setPlaceObjWorld(p):
    """setPlaceObjWorld : TkPlace TkNum TkOf ids TkAt TkNum TkNum TkSemicolon
                        | TkPlace TkNum TkOf ids TkIn TkBasketLower TkSemicolon
    """
    global newWorld
    global hasSetted
    global isBasketDeclared
    hasSetted = True
    id = p[4]
    #
    #
    amount = p[2]
    if p[2] != 0:
        if len(p) == 9:
            if (p[6] or p[7]) > 0:
                p[0] = Node("PlaceObjWorld", [p[4]])
                newWorld.setObjectInWorld(id, amount, [p[6], p[7]])
                # TODO : Falta validar la posicion en el mundo con respecto a las posiciones del mundo
            else:
                data_error = {
                    "type": "Posicion nula del mundo en a la hora de colocar objetos",
                    "line": p.lineno(2),
                    "column": p.lexpos(2) + 1,
                    "color": p[5],
                }
                errorSemantic(data_error)
        else:
            if isBasketDeclared:
                newWorld.setObjectsInBasket(id, amount)
                p[0] = Node("PlaceObjWorld", [p[4]])
            else:
                data_error = {
                    "type": "No puede colocar elementos en un Basket sin capacidad" + str(id),
                    "line": p.lineno(2),
                    "column": p.lexpos(2) + 1,
                    "objeto": id,
                }
                errorSemantic(data_error)
    else:
        data_error = {
            "type": "No puede colocar 0 objetos",
            "line": p.lineno(2),
            "column": p.lexpos(2) + 1,
            "color": p[5],
        }
        errorSemantic(data_error)


def p_setStartPosition(p):
    """setStartPosition : TkStart TkAt TkNum TkNum TkHeading directions TkSemicolon"""
    global newWorld
    global hasSetted
    hasSetted = True

    if (p[3] or p[4]) <= 0:
        data_error = {
            "type": "Start posicion en 0 no es valido",
            "line": p.lineno(2),
            "column": p.lexpos(2) + 1,
        }
        errorSemantic(data_error)
    else:
        # Verificar las dimensiones del mundo
        dimen = newWorld.getDimension()

        if (p[3] > dimen[0]) or (p[4] > dimen[1]):
            data_error = {
                "type": "Willy is out of world",
                "line": p.lineno(2),
                "column": p.lexpos(2) + 1,
            }
            errorSemantic(data_error)
        else:
            newWorld.setWillyStart([p[3], p[4]], p[6])
            p[0] = Node("WillyStartPosition", [p[6]])


def p_setBasketCapacity(p):
    """setBasketCapacity : TkBasket TkOf TkCapacity TkNum TkSemicolon"""
    global newWorld
    global isBasketDeclared
    if p[4] == 0:
        data_error = {
            "type": "No permitido " + p[4] + " capacidad de Basket",
            "line": p.lineno(2),
            "column": p.lexpos(2) + 1,
        }
        errorSemantic(data_error)
    else:
        isBasketDeclared = True
        newWorld.setCapacityOfBasket(p[4])
        p[0] = Node("BasketCapacity", [])


def p_newBoolean(p):
    """newBoolean : TkBoolean ids TkWith TkInitial TkValue TkTrue TkSemicolon
                  | TkBoolean ids TkWith TkInitial TkValue TkFalse TkSemicolon
    """
    global newWorld
    p[0] = Node("NewBoolean", [p[2]])
    global worldInstBool
    auxVal = False

    if p[6] == "true":
        auxVal = True
    elif p[6] == "false":
        auxVal = False

    attributesObjects = {
        "type": "Bool",
        "line": p.lineno(2),
        "column": p.lexpos(2) + 1,
        "value": auxVal,
    }
    if worldInstBool:
        stack.insert(p[2], attributesObjects)
    else:
        table = []
        stack.push(table)
        stack.insert(p[2], attributesObjects)
        worldInstBool = True
    newWorld.setBool(p[2], auxVal)
    global booleansOfWorlds
    booleansOfWorlds.append([p[2], attributesObjects])


def p_newGoal(p):
    """newGoal : TkGoal ids TkIs TkWilly TkIs TkAt TkNum TkNum TkSemicolon
            | TkGoal ids TkIs TkNum ids TkObjectsLower TkIn TkBasket TkSemicolon
            | TkGoal ids TkIs TkNum ids TkObjectsLower TkAt TkNum TkNum TkSemicolon
    """
    global newWorld
    global worldInstBool
    if len(p) == 10:
        if p[4] == "willy":
            p[0] = Node("NewGoal", [p[2]])
            attributesObjects = {
                "type": "WillyIsAt",
                "line": p.lineno(2),
                "column": p.lexpos(2) + 1,
                "column_": p[7],
                "row": p[8]
            }
            newWorld.setGoals(p[2], attributesObjects["type"], [p[7], p[8]])
        else:
            p[0] = Node("NewGoal: Object in Basket", [p[2], p[5]])
            attributesObjects = {
                "type": "ObjectInBasket",
                "line": p.lineno(2),
                "column": p.lexpos(2) + 1,
                "amount": p[4],
                "id-object": p[5],
            }
            newWorld.setGoals(p[2], attributesObjects["type"], p[5], p[4])
    else:
        p[0] = Node("NewGoal: Object at position", [p[2], p[5]])
        attributesObjects = {
            "type": "ObjectInPosition",
            "line": p.lineno(2),
            "column": p.lexpos(2) + 1,
            "amount": p[4],
            "id-object": p[5],
            "column_": p[8],
            "row": p[9]
        }

        newWorld.setGoals(p[2], attributesObjects["type"], p[5], p[4], [p[8], p[9]])
    if worldInstBool:
        stack.insert(p[2], attributesObjects)
    else:
        table = []
        stack.push(table)
        stack.insert(p[2], attributesObjects)
        worldInstBool = True


def p_finalGoal(p):
    """finalGoal : TkFinalG TkIs finalGoalTest TkSemicolon"""
    global validateFinalGoal
    if validateFinalGoal:
        data_error = {
            "type": "Only one final goal",
            "line": p.lineno(2),
            "column": p.lexpos(2) + 1,
        }
        errorSemantic(data_error)
    else:
        p[0] = Node("FinalGoal", [p[3]])
        ret = p[3].finalGoalToString()
        validateFinalGoal = True
        newWorld.setFinalGoal(p[3], ret)


def p_finalGoalTest(p):
    """finalGoalTest : TkParenL finalGoalTest TkParenR
                     | negacionGoal
                     | conjuncionGoal
                     | disyuncionGoal
                     | ids
    """
    if len(p) == 2:
        p[0] = Node("FinalGoal", [p[1]])
    else:
        p[0] = Node("Parentesis", [p[2]])


def p_disyuncionGoal(p):
    """disyuncionGoal : finalGoalTest TkOr finalGoalTest"""
    p[0] = Node("Disyuncion", [p[1], p[3]])


def p_conjuncionGoal(p):
    """conjuncionGoal : finalGoalTest TkAnd finalGoalTest"""
    p[0] = Node("Conjuncion", [p[1], p[3]])


def p_negacionGoal(p):
    """negacionGoal : TkNot finalGoalTest"""
    p[0] = Node("Not", [p[2]])


def p_ids(p):
    "ids : TkId"
    p[0] = p[1]
    p.set_lineno(0, p.lineno(1))


def p_taskBlock(p):
    """taskBlock : taskDefinition multiInstructions TkEndTask"""
    global taskBoolz
    global createdWorlds
    global currentTask

    attributesObjects = {
        "type": "Task",
        "line": p.lineno(2),
        "column": p.lexspan(2)[0] + 1,
    }

    p[0] = Node("Task", [p[1], p[2]])

    if len(stack.stack) > 1:
        global firstDefineOnTask
        firstDefineOnTask = False
        stack.pop()
    stack.insert(p[1].children[0], attributesObjects)
    print("INICIA LA EJECUCION DEL TASK")
    p[0].executeMyTask(currentTask)
    print("###############")
    print("Estado final de " + str(currentTask.world.id) + " luego de haber ejecutado " + str(currentTask.id))
    print("La posición de Willy es: " + str(currentTask.world.getWillyPosition()[0]) + " mirando hacia el " + str(
        currentTask.world.getWillyPosition()[1]))
    print("Lo que tiene en el basket es:\n", currentTask.world.getObjectsInBasket())
    print("El estado de los bools es:\n", currentTask.world.getBools())
    print("El final goal es:\n" + currentTask.world.getFinalGoal())
    print("El valor del final goal es: ", currentTask.world.getValueFinalGoal())
    print(currentTask.world)
    currentTask.fin = False



def p_taskDefinition(p):
    """
    taskDefinition : TkBeginTask ids TkOn ids
    """
    global activeWorld
    global programBlock
    global currentTask
    global howManyTask
    howManyTask = howManyTask + 1

    if procedures.find(p[4], createdWorlds) is not None:

        activeWorld = procedures.find(p[4], createdWorlds)
        newInstanceWorld = copy.deepcopy(activeWorld)

        type = {
            "type": "Task"
        }
        p[0] = Node("", [p[2], p[1]])
        data = [p[0].children[0], type]

        currentTask = Task(p[2], newInstanceWorld)
        programBlock.append(data)

    else:
        data_error = {
            "type": "Invalid name of World: " + p[2] + " in " + p[4],
            "line": p.lineno(2),
            "column": p.lexpos(2) + 1,
        }
        errorSemantic(data_error)


def p_multiInstructions(p):
    """multiInstructions : instructions
                         | empty
                         | instructions TkSemicolon multiInstructions
    """

    if len(p) == 2:
        p[0] = Node("MultiInstruction", [p[1]])
    else:
        p[0] = Node("MultiInstruction", [p[1], p[3]])


def p_primitiveInstructions(p):
    """primitiveInstructions : TkMove
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
                             | TkTerminate
    """
    global activeWorld
    global taskBool
    global objectsInWorlds
    global currentTask
    auxBool = False
    attributesObjects = {}

    if (p[1] == "pick"):

        if activeWorld.isObject(p[2]):

            p[0] = Node("Pick", [p[2]])

        else:
            data_error = {
                "type": "Objeto " + p[2] + " No existe en el mudno ",
                "line": p.lineno(2),
                "column": p.lexpos(2) + 1,
            }
            errorSemantic(data_error)
    elif p[1] == "drop":
        if activeWorld.isObject(p[2]):
            p[0] = Node("Drop", [p[2]])
        else:
            data_error = {
                "type": "Objeto " + p[2] + " No existe en el mudno ",
                "line": p.lineno(2),
                "column": p.lexpos(2) + 1,
            }
            errorSemantic(data_error)
    elif p[1] == "clear":
        if activeWorld.isBool(p[2]):
            if p[1] == "clear":
                p[0] = Node("Clear", [p[2]])

        else:
            data_error = {
                "type": "Booleano " + p[2] + " No existe en el mudno ",
                "line": p.lineno(2),
                "column": p.lexpos(2) + 1,
            }
            errorSemantic(data_error)
    elif p[1] == "flip":
        if activeWorld.isBool(p[2]):
            p[0] = Node("Flip", [p[2]])
        else:
            data_error = {
                "type": "Booleano " + p[2] + " No existe en el mudno ",
                "line": p.lineno(2),
                "column": p.lexpos(2) + 1,
            }
    elif p[1] == "set":
        if activeWorld.isBool(p[2]):
            if len(p) == 5:
                if p[4] == "true":
                    auxBool = True
                elif p[4] == "false":
                    auxBool = False
                p[0] = Node("SetBool", [p[2], auxBool])
            else:
                p[0] = Node("SetTrue", [p[2]])
        if len(p) == 3:
            attributesObjects = {
                "type": "Bool",
                "line": p.lineno(2),
                "column": p.lexpos(2) + 1,
                "value": True,
            }

        elif len(p) == 5:
            if p[4] == "true":
                auxBool = True
            elif p[4] == "false":
                auxBool = False
            attributesObjects = {
                "type": "Bool",
                "line": p.lineno(2),
                "column": p.lexpos(2) + 1,
                "value": auxBool,
            }

    if len(p) == 2:
        if p[1] == 'move':

            p[0] = Node("Move", [p[1]])
        elif p[1] == "turn-left":
            p[0] = Node("TL", [p[1]])

        elif p[1] == "turn-right":
            p[0] = Node("TR", [p[1]])


        elif p[1] == "terminate":
            data_error = {
                "type": "Ha finalizado la corrida con exito",
                "line": p.lineno(1),
                "column": p.lexpos(1) + 1,
            }
            p[0] = Node("Terminate", [p[1]])
            # finish(data_error)
        else:
            p[0] = Node("MyInstruction", [p[1]])


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
    global activeWorld
    global currentTask
    if len(p) == 2:
        p[0] = Node("BooleanTest", [p[1]])
    elif len(p) == 5:
        if p[1] == "found":
            p[0] = Node("Found", [p[3]])
        elif p[1] == "carrying":
            p[0] = Node("Carrying", [p[3]])

    elif len(p) == 4:
        p[0] = Node("Parentesis", [p[2]])


def p_disyuncionBool(p):
    """disyuncionBool : booleanTests TkOr booleanTests"""
    p[0] = Node("Disyuncion", [p[1], p[3]])


def p_conjuncionBool(p):
    """conjuncionBool : booleanTests TkAnd booleanTests"""
    p[0] = Node("Conjuncion", [p[1], p[3]])


def p_negacionBool(p):
    """negacionBool : TkNot booleanTests"""
    p[0] = Node("Not", [p[2]])


def p_primitiveBoolean(p):
    """primitiveBoolean : TkFrontCl
                        | TkLeftCl
                        | TkRightCl
                        | TkLookingN
                        | TkLookingE
                        | TkLookingS
                        | TkLookingW
                        """
    p[0] = p[1]
    p.set_lineno(0, p.lineno(1))


def p_instructions(p):
    """instructions : primitiveInstructions
                    | ifInstruction
                    | TkSemicolon
                    | whileInst
                    | TkBegin multiInstructions TkEnd
                    | TkRepeat TkNum TkTimes instructions
                    | instructionDefineAs instructions

                    """
    global firstDefineOnTask
    if len(p) == 2:
        p[0] = Node("Instructions", [p[1]])

    elif len(p) == 3:
        p[0] = Node("Define As", [p[1], p[2]])
        global defineAsBool
        attributesObjects = {
            "type": "Instruction",
            "line": p.lineno(1),
            "column": p.lineno(1) + 1,
        }
        stack.pop()
        if firstDefineOnTask == False:
            table = []
            stack.push(table)
            firstDefineOnTask = True

        stack.insert(p[1].children[0], attributesObjects)
        defineAsBool = False
    elif len(p) == 4:
        p[0] = Node("Begin", [p[2]])
    elif len(p) == 5:
        if p[1] == "repeat":
            if p[2] <= 0:
                int = p[2]
                data_error = {
                    "type": "Bad definition number of iteration for repeat - actual: " + int,
                    "line": p.lineno(2),
                    "column": p.lexpos(2) + 1,
                }
                errorSemantic(data_error)
            else:
                p[0] = Node("Repeat", [p[2], p[4]])


def p_ifInstruction(p):
    """ ifInstruction : TkIf booleanTests TkThen instructions
                      | TkIf booleanTests TkThen instructions TkElse instructions
    """
    if len(p) == 5:
        p[0] = Node('ifSimple', [p[2], p[4]])
    else:
        p[0] = Node('ifCompound', [p[2], p[4], p[6]])


def p_whileInst(p):
    """ whileInst : TkWhile booleanTests TkDo instructions
    """
    p[0] = Node('whileInst', [p[2], p[4]])


def p_instructionDefineAs(p):
    """instructionDefineAs : TkDefine ids TkAs"""
    p[0] = Node("Define as", [p[2]])
    global defineAsBool
    defineAsBool = False

    """ attributesObjects = {
        "type" : "Instruction",
        "line" : p.lineno(2),
        "column" : p.lexpos(2) + 1,
        } """
    if defineAsBool:
        defineAsBool = False
    else:
        table = []
        stack.push(table)
        defineAsBool = True


def p_directions(p):
    """directions : TkNorth
                | TkEast
                | TkSouth
                | TkWest
    """
    p[0] = p[1]


def p_empty(p):
    'empty :'
    pass


def p_error(p):
    global ParserErrors

    if p is not None:
        error = 'Error de sintaxis "' + str(p.value) + '" en fila ' \
                + str(p.lineno)
        ParserErrors.append(error)
        print(ParserErrors)
    else:
        print("Syntax error at EOF")

    sys.exit()


def errorSemantic(err):
    global ParserErrors

    if err is not None:
        error = 'Error con "' + str(err["type"]) + '" en linea ' \
                + str(err["line"])
        ParserErrors.append(error)
        print(ParserErrors)

    else:
        print("Syntax error at EOF")

    sys.exit()


def finish(data):
    if data is not None:
        Message = "Programa finalizado con exito"
        print(Message)
    sys.exit()
