class instanceWorld:

    def __init__(self, tkBeginWorld, tkId, instructions, tkEndWolrd):
        self.tkBeginWorld = tkBeginWorld
        self.tkId = tkId
        self.instructions = instructions
        self.tkEndWolrd = tkEndWolrd


class instructions:

    def __init__(self, intruction, instructionType):
        self.instruction = intruction
        self.instructions = instructionType


class setWorld:

    def __init__(self, tkWorld, tkIntCol, tkIntRow):
        self.tkWorld = tkWorld
        self.tkIntRow = tkIntRow
        self.tkIntCol = tkIntCol


class setWall:
    def __init__(self, tkWall, direction, tkIntColFrom, tkIntRowFrom, tkTo, tkIntColTo, tkIntRowTo):
        self.tkWall = tkWall
        self.direction = direction
        self.tkIntRowFrom = tkIntRowFrom
        self.tkIntColFrom = tkIntColFrom
        self.tkTo = tkTo
        self.tkIntRowTo = tkIntRowTo
        self.tkIntColTo = tkIntColTo


class objectType:
    def __init__(self, tkObjectType, tkId, tlkOf, tkColor, color):
        self.tkObjectType = tkObjectType
        self.tkId = tkId
        self.tlkOf = tlkOf
        self.tkColor = tkColor
        self.color = color

class setPlace:
    def __init__(self, tkPlace, amount, tkOf, tkIdObject, tkAt, col, row):
        self.tkPlace = tkPlace
        self.amount = amount
        self.tkOf = tkOf
        self.tkIdObject = tkIdObject
        self.tkAt = tkAt
        self.col = col
        self.row = row

class willyStartAt:
    def __init__(self, tkStart, tkAt, col, row, tkHeading, orientation):
        self.tkStart = tkStart
        self.tkHeading = tkHeading
        self.orientation = orientation
        self.tkAt = tkAt
        self.col = col
        self.row = row

class setBasketCapacity:
    def __init__(self, tkBasket, tkOf, tkCapacity, capacity):
        self.tkBasket = tkBasket
        self.tkOf = tkOf
        self.tkCapacity = tkCapacity
        self.capacity = capacity

class setBoolean:
    def __init__(self, tkBoolean, tkId, tkWith, tkInitial, tkValue, tkBool):
        self.tkBoolean = tkBoolean
        self.tkId = tkId
        self.tkWith = tkWith
        self.tkInitial = tkInitial
        self.tkValue = tkValue
        self.tkBool = tkBool

class setGoal:
    def __init__(self, tkGoal, tkId, codition):
        self.tkGoal = tkGoal
        self.tkId = tkId
        self.goalTest = codition

class goalPosition:
    def __init__(self, tkWilly, tkIs, tkAt, col, row):
        self.tkWilly = tkWilly
        self.tkIs = tkIs
        self.tkAt = tkAt
        self.col = col
        self.row = row

class goalObjectBasket:
    def __init__(self, intNumber, tkId, tkObject, tkInt, tkBasket):
        self.intNumber = intNumber
        self.tkId = tkId
        self.tkObject = tkObject
        self.tkIntcol = tkInt
        self.tkBasket = tkBasket

class goalObjectAtPlace:
    def __init__(self, intNumber, tkId, tkObject, tkAt, col, row):
        self.intNumber = intNumber
        self.tkId = tkId
        self.tkObject = tkObject
        self.tkAt = tkAt
        self.col = col
        self.row = row


class instanceTask:
    def __init__(self, tkBeginTask, id, tkOn, worldId, taskInstructions, tkEndTask):
        self.tkBeginTask = tkBeginTask
        self.id = id
        self.tkOn = tkOn
        self.worldId = worldId
        self.taskInstructions = taskInstructions
        self.tkEndTask = tkEndTask

class ifThen:
    def __init__(self, tkIf, tkBool, tkThen, instruction):
        self.tkIf = tkIf
        self.tkBool = tkBool
        self.tkThen = tkThen
        self.instructions = instruction

class ifThenElse:
    def __init__(self, tkIf, tkBool, tkThen, instruction,tkElse, instruction2):
        self.tkIf = tkIf
        self.tkBool = tkBool
        self.tkThen = tkThen
        self.instructions = instruction
        self.tkThen = tkThen
        self.instructions2 = instruction2

class repeat:
    def __init__(self, tkInt, tkTimes, instruction):
        self.tkInt = tkInt
        self.tkTimes = tkTimes
        self.instruction = instruction

class whileLoop:
    def __init__(self, tkWhile, tkBool, tkDo, instruction):
        self.tkWhile = tkWhile
        self.tkBool = tkBool
        self.tkDo = tkDo
        self.instruction = instruction

class beginIntructions:
    instructions = []
    def __init__(self, tkBegin, instruction, tkEnd):
        self.tkBegin = tkBegin
        self.instructions = instruction
        self.tkEnd = tkEnd

class defineInstructions:
    def __init__(self, tkDefine, tkId, tkAs, instruction):
        self.tkDefine = tkDefine
        self.tkId = tkId
        self.tkAs = tkAs
        self.instruction = instruction

class firstIf:
    def __init__(self, tkIf, tkBool, tkThen, instruction):
        self.tkIf = tkIf
        self.tkBool = tkBool
        self.tkThen = tkThen
        self.instructions = instruction

class singleIdInst:
    def __init__(self, tkInst, id):
        self.tkInst = tkInst
        self.id = id

class dualIdInst:
    def __init__(self, instruction, id1, id2):
        self.instrcution = instruction
        self.id1 = id1
        self.id2 = id2

class changeBool:
    def __init__(self, tkSet, id, valueIn, valueOut, id2):
        self.tkSet = tkSet
        self.id = id
        self.valueIn = valueIn
        self.valueOut = valueOut
        self.id2 = id2

class testBools:
    def __init__(self, bool1, oper, bool2):
        self.bool1 = bool1
        self.oper = oper
        self.bool2 = bool2

class sigleOper:
    def __init__(self, oper, bool):
        self.oper = oper
        self.bool = bool

class  sigleton:
    def __init__(self, bool):
        self.bool = bool
