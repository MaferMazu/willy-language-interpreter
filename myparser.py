#!/usr/bin/env python3
from typing import Any
import os,sys
import lexer
import ply.yacc as yacc
import logging
from Structure import Structure
from myStack import myStack
from Node import *
from World import *
from Task import *
from ModelProcedure import *

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
ParserErrors = []

procedures= ModelProcedure()

newWorld = Any

stack = myStack()
stack.push_empty_table()

programBlock = []
createdWorlds = []
objectsInWorlds = []
booleansOfWorlds = []
tasks = []

activeWorld = Any
currentTask = Any

worldInstBool = False
taskBool = False
defineAsBool = False
validateFinalGoal = False
hasSetted = False
blockNumber = 0




def p_correctProgram(p):
    "correctProgram : program"
    print("Tu programa esta correcto")
    p[0] = p[1]
    # print(p[1].type,p[1].children)
    # print(p[1].children[0].type,p[1].children[1].type)
    # print(isinstance(p[0],Node))
    # print(str(p[0]))

def p_program(p):
    """
    program : worldBlock
            | taskBlock
            | worldBlock program
            | taskBlock program
    """
    if len(p)==2:
        p[0]=Node("Program Block:",[p[1]])
    else:
        p[0]=Node("Program Block:",[p[1],p[2]])
    print("Stack luego de leer un bloque" + "\n")
    print(stack)
    print("programBlock")
    print(programBlock[0][0])
    r = programBlock[0][1]["type"]
    print(r)
    print("\n")


def p_worldInstSet(p):
    """worldInstSet : worldInst TkSemicolon worldInstSet
                    | worldInst worldInstSet
                    | worldInst TkSemicolon
    """
    global worldInstBool

    if(worldInstBool):
        worldInstBool = False
    if len(p)==4:
        p[0]=Node("WorldInstancia:",[p[1],p[3]])
    else:
        if p[2]==";":
            p[0]=Node("WorldInstancia:",[p[1]],p[2])
        else:
            p[0]=Node("WorldInstancia:",[p[1],p[2]])

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
    global newWorld
    actualDir = p[2].children[0]
    print(actualDir, p[4], p[7])
    print(actualDir, p[5], p[8])
    if actualDir == "north":
        print("norte")
        if p[4]==p[7] and p[5]<=p[8]:
            p[0] = Node("WallSet:", [actualDir, p[3], p[4], p[5], p[6], p[7], p[8]])
            newWorld.setWall([p[4],p[5]],[p[7],p[8]],actualDir)
        else:
            data_error = {
                "type": "Bad token of " + actualDir + "Dimentions",
                "line": p.lineno(2),
                "column": p.lexpos(2) + 1,
            }
            errorSemantic(data_error)
    elif actualDir == "south":
        print("south")
        if p[4]==p[7] and p[5]>=p[8]:
            p[0] = Node("WallSet:", [actualDir, p[3], p[4], p[5], p[6], p[7], p[8]])
            newWorld.setWall([p[4], p[5]], [p[7], p[8]], actualDir)
        else:
            data_error = {
                "type": "Bad token of " + actualDir + "Dimentions",
                "line": p.lineno(2),
                "column": p.lexpos(2) + 1,
            }
            errorSemantic(data_error)
    elif actualDir == "east":
        print("east")
        if p[5]==p[8] and p[4]>=p[7]:
            p[0] = Node("WallSet:", [actualDir, p[3], p[4], p[5], p[6], p[7], p[8]])
            newWorld.setWall([p[4], p[5]], [p[7], p[8]], actualDir)
        else:
            data_error = {
                "type": "Bad token of " + actualDir + "Dimentions",
                "line": p.lineno(2),
                "column": p.lexpos(2) + 1,
            }
            errorSemantic(data_error)
    elif actualDir == "west":
        print("west")
        if p[5]==p[8] and p[4]<=p[7]:
            p[0] = Node("WallSet:", [actualDir, p[3], p[4], p[5], p[6], p[7], p[8]])
            newWorld.setWall([p[4], p[5]], [p[7], p[8]], actualDir)
        else:
            data_error = {
                "type": "Bad token of " + actualDir + "Dimentions",
                "line": p.lineno(2),
                "column": p.lexpos(2) + 1,
            }
            errorSemantic(data_error)
    else:
        data_error ={
            "type": "Bad token of Direcction" + actualDir,
            "line": p.lineno(2),
            "column": p.lexpos(2) + 1,
        }
        ##Deberia lanzarme error pero mientras colocaré pass
        # p_statement_print_error(p)
        errorSemantic(None)
        print('Bad definition of wall in World')


def p_worldDefinition(p):
    """
    worldDefinition : TkBeginWorld ids
    """
    type = {
        "type": "World"
    }
    global newWorld
    # if p[2]
    print("###Reading world")
    print(stack)
    print("###Reading world")
    p[0] = Node("",[p[2]])
    data = [p[0].children[0], type]
    newWorld = World(p[2])
    newWorld.setDimension([1,1])
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
        "type" : "World",
        "line" : p.lineno(2),
        "column" : p.lexpos(2) + 1,
    }
    dataFlag = {
        "ownerPrev" : id,
        "WorldClass" : "Aqui estara la clase del mundo"
    }
    if len(p)==4:
        p[0] = Node("WorldBlock",[p[2]],[p[1],p[3]])
    else:
        p[0] = Node("WorldBlock",[p[2]],[p[1]])
    # print("Antes del pop")
    # print(stack)
    if blockNumber == 0:
        stack.insert("WorldBlock" + str(blockNumber), dataFlag)
        blockNumber = blockNumber + 1
    else:
        stack.insert("WorldBlock" + str(blockNumber), dataFlag)
        blockNumber = blockNumber + 1
    validateFinalGoal = False
    print(stack)
    stack.pop()
    stack.insert(id,attributesObjects)
    createdWorlds.append(newWorld)
    print(newWorld)
    print("Despues del pop")
#     # print(stack)


def p_worldSet(p):
    """worldSet : TkWorld TkNum TkNum
                | empty"""
    global newWorld
    global hasSetted
    if not hasSetted:
        if 0 != (p[2] or p[3]):
            if len(p) == 4:
                p[0] = Node("WorldSet", [], [p[1], p[2], p[3]])
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
            print("No puedes setear en 0 ninguno de los valores del mundo")
        print("Dimensiones del mundo" + str(newWorld.getDimension()))
    else:
        data_error = {
            "type": ("To place objects in World:" + newWorld.id + "need to declare dimentions at start" + "\n" + "Can't replace dimentions"),
            "line": p.lineno(2),
            "column": p.lexpos(2) + 1,
        }
        errorSemantic(data_error)





def p_newObjType(p):
    """newObjType : TkObjType ids TkOf TkColor colors"""
    global worldInstBool
    global newWorld
    id = p[2]
    print(p[2])
    if procedures.findObj(id, programBlock):
        data_error = {
            "type": "Objeto " + id + " contiene nombre de un World o Task",
            "line": p.lineno(2),
            "column": p.lexpos(2) + 1,
        }
        errorSemantic(data_error)
        print("Este elemento ya existe como Mundo o tarea")
    else:
        p[0] = Node("NewObjectType", [p[2], p[5]], [p[1], p[3], p[4]])
        attributesObjects = {
            "type": "Object-type",
            "line": p.lineno(2),
            "column": p.lexpos(2) + 1,
            "color": p[5],
        }
        # print(stack)
        # print(programBlock)
        # print("space")
        # print(procedures.find(id, programBlock))

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
    p[0]=p[1]
    p.set_lineno(0,p.lineno(1))

def p_setPlaceObjWorld(p):
    """setPlaceObjWorld : TkPlace TkNum TkOf ids TkAt TkNum TkNum
                        | TkPlace TkNum TkOf ids TkIn TkBasketLower
    """
    global newWorld
    global hasSetted
    hasSetted = True
    id = p[4]
    # print("#####ELEMENTOS")
    # print(id)
    amount = p[2]
    if p[2] != 0:
        if len(p) == 8:
            if (p[6] or p[7]) > 0:
                p[0] = Node("PlaceObjWorld", [p[4]], [p[1], p[2], p[3], p[5], p[6], p[7]])
                newWorld.setObjectInWorld(id, amount, [p[6],p[7]])
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
            newWorld.setObjectsInBasket(id, amount)
            p[0] = Node("PlaceObjWorld", [p[4]], [p[1], p[2], p[3], p[5], p[6]])
    else:
        data_error = {
            "type": "No puede colocar 0 objetos",
            "line": p.lineno(2),
            "column": p.lexpos(2) + 1,
            "color": p[5],
        }
        errorSemantic(data_error)


def p_setStartPosition(p):
    """setStartPosition : TkStart TkAt TkNum TkNum TkHeading directions"""
    global newWorld
    global hasSetted
    hasSetted = True
    print("######Esto es el dir: " + str(p[6]))
    if (p[3] or p[4]) <= 0:
        data_error = {
            "type": "Start posicion en 0 no es valido",
            "line": p.lineno(2),
            "column": p.lexpos(2) + 1,
        }
        errorSemantic(data_error)
    else:
        #Verificar las dimensiones del mundo
        print("dimesiones mundo: " + str(newWorld.getDimension()))
        dimen = newWorld.getDimension()

        if (p[3] > dimen[0]) or (p[4] > dimen[1]):
            data_error = {
                "type": "Willy is out of world",
                "line": p.lineno(2),
                "column": p.lexpos(2) + 1,
            }
            errorSemantic(data_error)
        else:
            newWorld.setWillyStart([p[3],p[4]], p[6])
            p[0]=Node("WillyStartPosition",[p[6]],[p[1],p[2],p[3],p[4],p[5]])

def p_setBasketCapacity(p):
    """setBasketCapacity : TkBasket TkOf TkCapacity TkNum"""
    global newWorld
    if p[4] == 0:
        data_error = {
            "type": "No permitido " + p[4] + " capacidad de Basket" ,
            "line": p.lineno(2),
            "column": p.lexpos(2) + 1,
        }
        errorSemantic(data_error)
    else:
        newWorld.setCapacityOfBasket(p[4])
        p[0]=Node("BasketCapacity",[],[p[1],p[2],p[3],p[4]])

def p_newBoolean(p):
    """newBoolean : TkBoolean ids TkWith TkInitial TkValue TkTrue
                  | TkBoolean ids TkWith TkInitial TkValue TkFalse
    """
    global newWorld
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
    newWorld.setBool(p[2], p[6])
    global booleansOfWorlds
    booleansOfWorlds.append([p[2],attributesObjects])


def p_newGoal(p):
    """newGoal : TkGoal ids TkIs TkWilly TkIs TkAt TkNum TkNum
            | TkGoal ids TkIs TkNum ids TkObjectsLower TkIn TkBasket
            | TkGoal ids TkIs TkNum ids TkObjectsLower TkAt TkNum TkNum
    """
    global newWorld
    global worldInstBool
    if len(p)==9:
        if p[4]=="willy":
            p[0]=Node("NewGoal",[p[2]],[p[1],p[3],p[4],p[5],p[6],p[7],p[8]])
            attributesObjects = {
                "type" : "WillyIsAt",
                "line" : p.lineno(2),
                "column" : p.lexpos(2) + 1,
                "column_": p[7],
                "row": p[8]
            }
            newWorld.setGoals(p[2],attributesObjects["type"],[p[7],p[8]])
        else:
            p[0]=Node("NewGoal: Object in Basket",[p[2],p[5]],[p[1],p[3],p[4],p[6],p[7],p[8]])
            attributesObjects = {
                "type" : "ObjectInBasket",
                "line" : p.lineno(2),
                "column" : p.lexpos(2) + 1,
                "amount": p[4],
                "id-object": p[5],
            }
            newWorld.setGoals(p[2], attributesObjects["type"], p[5], p[4])
    else:
        p[0]=Node("NewGoal: Object at position",[p[2],p[5]],[p[1],p[3],p[4],p[6],p[7],p[8],p[9]])
        attributesObjects = {
            "type" : "ObjectInPosition",
            "line" : p.lineno(2),
            "column" : p.lexpos(2) + 1,
            "amount": p[4],
            "id-object": p[5],
            "column_": p[8],
            "row": p[9]
        }
        print("SOY P9999999999")
        print(p[9])
        newWorld.setGoals(p[2], attributesObjects["type"],p[5], p[4], [p[8], p[9]])
    if worldInstBool:
        stack.insert(p[2], attributesObjects)
    else:
        table = []
        stack.push(table)
        stack.insert(p[2], attributesObjects)
        worldInstBool = True

def p_finalGoal(p):
    """finalGoal : TkFinalG TkIs finalGoalTest"""
    global validateFinalGoal
    if validateFinalGoal:
        data_error = {
            "type": "Only one final goal",
            "line": p.lineno(2),
            "column": p.lexpos(2) + 1,
        }
        errorSemantic(data_error)
    else:
        p[0] = Node("FinalGoal", [p[3]], [p[1], p[2]])
        ret = p[3].finalGoalToString()
        print("###########################")
        print("###########################")
        print(ret)
        print("###########################")
        print("###########################")
        validateFinalGoal=True
        newWorld.setFinalGoal(p[3],ret)
        print("Mi final goal",newWorld.getFinalGoal())
        print("Resultado Mi final goal",newWorld.getValueFinalGoal())



def p_finalGoalTest(p):
    """finalGoalTest : TkParenL finalGoalTest TkParenR
                     | negacionGoal
                     | conjuncionGoal
                     | disyuncionGoal
                     | ids
    """
    if len(p)==2:
        p[0]=Node("FinalGoal",[p[1]])
    else:
        p[0]=Node("Parentesis",[p[2]],[p[1],p[3]])

def p_disyuncionGoal(p):
    """disyuncionGoal : finalGoalTest TkOr finalGoalTest"""
    p[0]=Node("Disyuncion",[p[1],p[3]],p[2])

def p_conjuncionGoal(p):
    """conjuncionGoal : finalGoalTest TkAnd finalGoalTest"""
    p[0]=Node("Conjuncion",[p[1],p[3]],p[2])

def p_negacionGoal(p):
    """negacionGoal : TkNot finalGoalTest"""
    p[0]=Node("Not",[p[2]],p[1])

def p_ids(p):
    "ids : TkId"
    p[0]=p[1]
    p.set_lineno(0, p.lineno(1))
    p.set_lexpos(0, p.lexpos(1))

def p_taskBlock(p):
    """taskBlock : taskDefinition multiInstructions TkEndTask"""
    global taskBool
    global createdWorlds
    global currentTask

    attributesObjects = {
        "type": "Task",
        "line": p.lineno(2),
        "column": p.lexspan(2)[0] + 1,
    }

    p[0] = Node("Task", [p[1]])

    print("Antes del pop")
    stack.pop()
    stack.insert(p[1].children[0], attributesObjects)
    p[0].executeMyTask(currentTask)

    print("fin del task")




def p_taskDefinition(p):
    """
    taskDefinition : TkBeginTask ids TkOn ids
    """
    global activeWorld
    global programBlock
    global currentTask


    # print(procedures.find(p[4], createdWorlds).id)
    if procedures.find(p[4], createdWorlds) is not None:

        activeWorld = procedures.find(p[4], createdWorlds)
        # print("######### elemento")
        # print(activeWorld)
        # print(activeWorld.id)
        # print(activeWorld.getDimension())
        # print("elemento  #########")
        type = {
            "type": "Task"
        }
        p[0] = Node("", [p[2], p[1]])
        data = [p[0].children[0], type]
        # print("11111 INSTANCIA")
        # print(isinstance(activeWorld, World))
        # print("22222 INSTANCIA")
        currentTask = Task(p[2], activeWorld)
        programBlock.append(data)
        # print(stack)
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
    if len(p)==2:
        p[0]=Node("MultiInstruction",[p[1]])
    else:
        p[0]=Node("MultiInstruction",[p[1],p[3]])


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
    attributesObjects = {}
    if p[1] == ("drop" or "pick"):
        print(p[2])
        print(activeWorld.id)
        print(activeWorld.isObject(p[2]))
        if activeWorld.isObject(p[2]):
            if p[1] == "pick" and activeWorld.isCellWithObject(activeWorld.getWillyPosition()[0],p[2]):
                p[0] = Node("Pick",[p[2]])
                
            elif p[1] == "drop" and activeWorld.isObjectBasket(p[2]):
                p[0] = Node("Drop",[p[2]])
                
        else:
            data_error = {
                "type": "Objeto " + p[2] + " No existe en el mudno ",
                "line": p.lineno(2),
                "column": p.lexpos(2) + 1,
            }
            errorSemantic(data_error)

    elif p[1] == ("clear" or "flip"):
        if activeWorld.isBool(p[2]):
            if p[1] == "clear":
                p[0] = Node("Clear",[p[2]])
                
            elif p[1] == "flip":
                p[0] = Node("Flip",[p[2]])
                
        else:
            data_error = {
                "type": "Booleano " + p[2] + " No existe en el mudno ",
                "line": p.lineno(2),
                "column": p.lexpos(2) + 1,
            }
            errorSemantic(data_error)

    elif p[1] == 'set':
        if activeWorld.isBool(p[2]):
            if len(p) == 5:
                p[0]=Node("SetBool",[p[2],p[4]])
                
            else:
                p[0]=Node("SetBool",[p[2]])
    elif p[1] == "move":
        p[0]=Node("Move",[p[1]])
    elif p[1] == "turn-left":
        p[0]=Node("TL",[p[1]])
        
    elif p[1] == "turn-right":
        p[0]=Node("TR",[p[1]])
        
        
    elif p[1] == "terminate":
        data_error = {
            "type": "Ha finalizado la corrida con exito",
            "line": p.lineno(1),
            "column": p.lexpos(1) + 1,
        }
        p[0]=Node("Terminate",[p[1]])
        
        finish(data_error)
    
    
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
    global activeWorld
    global currentTask
    if len(p)==2:
        p[0]=Node("BooleanTest",[p[1]])
    elif len(p)==5:
        if p[1] == "found":
            p[0]=Node("Found",[p[3]])
        elif p[1] == "carrying" :
            p[0] = Node("Carrying", [p[3]])
            
    elif len(p)==4:
        p[0]=Node("Parentesis",[p[2]],[p[1],p[3]])

        #sys.exit()



def p_disyuncionBool(p):
    """disyuncionBool : booleanTests TkOr booleanTests"""
    p[0]=Node("Disyuncion",[p[1],p[3]],p[2])

def p_conjuncionBool(p):
    """conjuncionBool : booleanTests TkAnd booleanTests"""
    p[0]=Node("Conjuncion",[p[1],p[3]],p[2])

def p_negacionBool(p):
    """negacionBool : TkNot booleanTests"""
    p[0]=Node("Not",[p[2]],p[1])

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
    p.set_lineno(0,p.lineno(1))

def p_instructions(p):
    """instructions : primitiveInstructions
                    | ifSimple
                    | ifCompound
                    | TkRepeat TkNum TkTimes instructions
                    | whileInst
                    | TkBegin multiInstructions TkEnd
                    | instructionDefineAs instructions
                    | TkSemicolon
                    """
    if len(p)==2:
        p[0]= Node("Instructions",[p[1]])

    elif len(p)==3:
        p[0]= Node("Define As",[p[1],p[2]])
        global defineAsBool
        # print("#####IN RUN DEFINE")
        attributesObjects = {
            "type": "Instruction",
            "line": p.lineno(1),
            "column": p.lineno(1) + 1,
        }
        # print(stack)
        stack.pop()
        stack.insert(p[1].children[0], attributesObjects)
        # print(stack)
        defineAsBool = False
        # print("#####IN RUN DEFINE")
    elif len(p)==4:
        p[0]= Node("Begin",[p[2]],[p[1],p[3]])
    elif len(p)==5:
        if p[1]=="repeat":
            if p[2] <= 0:
                int = p[2]
                data_error = {
                    "type": "Bad definition number of iteration for repeat - actual: " + int,
                    "line": p.lineno(2),
                    "column": p.lexpos(2) + 1,
                }
                errorSemantic(data_error)
            else:
                p[0] = Node("Repeat", [p[2],p[4]], [p[1], p[3]])

    elif len(p)==7:
        p[0]= Node("Instructions",[p[2],p[4],p[6]],[p[1],p[3],p[5]])

    # print("Primer elemento de p: ")
    # print(p)



# def p_instructionDefine(p):
#     '''instructionDefine : instructionDefineAs instructions'''
#     p[0]=Node("Define",[p[1],p[2]])
#     stack.pop()

def p_ifSimple(p):
    """ ifSimple : TkIf booleanTests TkThen instructions
    """
    p[0] = Node('ifSimple', [p[2],p[4]],[p[1],p[3]])

def p_ifCompound(p):
    """ ifCompound : TkIf booleanTests TkThen instructions TkElse instructions
    """
    p[0] = Node('ifCompound', [p[2],p[4],p[6]], [p[1],p[3],p[5]])

def p_whileInst(p):
    """ whileInst : TkWhile booleanTests TkDo instructions
    """
    p[0] = Node('whileInst', [p[2],p[4]],[p[1],p[3]])


def p_instructionDefineAs(p):
    """instructionDefineAs : TkDefine ids TkAs"""
    # print("EUREKA")
    # print(p[2])
    p[0]=Node("Define as",[p[2]])
    global defineAsBool
    # print("Define" + str(p[2]))
    # print(stack)
    # print("Define")
    defineAsBool = False

    """ attributesObjects = {
        "type" : "Instruction",
        "line" : p.lineno(2),
        "column" : p.lexpos(2) + 1,
        } """
    if defineAsBool:
        defineAsBool = False
    else:
        # print("la variable es false, procedemos a pusherar" + "\n")
        # # print(stack)
        # print("Aqui estuvo el stack")
        table = []
        stack.push(table)
        # print("Nuevo Contexto")
        # print(stack)
        # print("Nuevo Contexto")
        defineAsBool = True

def p_directions(p):
    """directions : TkNorth
                | TkEast
                | TkSouth
                | TkWest
    """
    p[0]=Node("Direction",[p[1]],p[1])


def p_empty(p):
    'empty :'
    pass


# def p_statement_print_error(p):
#     'statement : PRINT error'
#     print("Syntax error in print statement. Bad expression")

def p_error(p):
    global ParserErrors
    print(p)
    if p is not None:
        error = 'Error del Parser "' + str(p.type) + '" en fila ' \
                + str(p.lineno) + ', columna ' + str(p.lexpos)
        ParserErrors.append(error)
        print(ParserErrors)
    else:
        print("Syntax error at EOF")

    sys.exit()

def errorSemantic(err):
    global ParserErrors
    print(err)
    if err is not None:
        error = 'Error del Parser "' + str(err["type"]) + '" en fila ' \
                + str(err["line"]) + ', columna ' + str(err["column"])
        ParserErrors.append(error)
        print(ParserErrors)

    else:
        print("Syntax error at EOF")

    sys.exit()

def finish(data):
    # print(data)
    if data is not None:
        Message = "Programa finalizado con exito"
        print(Message)
    sys.exit()


