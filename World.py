class World:
    def __init__(self, id):
        self.id = id
        self.dimensions = [1, 1]
        self.objects = []  # Formato [idObjeto,amountObject,colorObject] tienen amount si fueron puestos en el mundo
        self.board = []  # Esto es una matriz con elementos de la forma [pair([x,y]),willy(W) o wall(/),lista de pares([idObje,amount])]
        self.walls = []  # Formato [[colum0,fila0],[colum1,fila1],direction]
        self.positionI = [[1, 1], "north"]
        self.positionF = [[1, 1], "north"]
        self.capacityOfBasket = 0
        self.objectsInBasket = []  # Formato [idObjeto,amountObject,colorObject]
        self.bools = [["front-clear", False], ["left-clear", False], ["right-clear", False], ["looking-north", False],
                      ["looking-east", False], ["looking-south", False], ["looking-west", False]]  # Formato [id,value]
        self.directions = ["north", "west", "south", "east"]
        self.goals = []  # Formato [id,tipo,objectOrPosition,position/None]
        self.finalgoal = [None, ""]  # Formato [Nodo,string]

    def __str__(self):
        return self.printBoard("", "willy")

    ####
    # Get y Set Basic
    ####
    def getDimension(self):
        return self.dimensions

    def setDimension(self, pair):
        self.dimensions = pair
        self.setClearBoard(pair)
        return True

    def getWalls(self):
        return self.walls

    def setWall(self, ini, fin, direction):
        # ini y fin son pares ordenados x,y
        if len(ini) == len(fin) == 2 and ((direction == "north" and ini[0] == fin[0] and ini[1] <= fin[1]) or
                                          (direction == "south" and ini[0] == fin[0] and ini[1] >= fin[1]) or
                                          (direction == "east" and ini[1] == fin[1] and ini[0] >= fin[0]) or
                                          (direction == "west" and ini[1] == fin[1] and ini[0] <= fin[0])):
            self.walls.append([ini, fin, direction])
            if direction == "north":
                for x in range(ini[1], fin[1] + 1):
                    pair = self.positionInBoard([ini[0], x])
                    position = self.board[pair[0]][pair[1]]
                    position[1] = "/"
            if direction == "south":
                for x in range(fin[1], ini[1]):
                    pair = self.positionInBoard([ini[0], x])
                    position = self.board[pair[0]][pair[1]]
                    position[1] = "/"
            if direction == "east":
                for x in range(fin[0], ini[0] + 1):
                    pair = self.positionInBoard([x, ini[1]])
                    position = self.board[pair[0]][pair[1]]
                    position[1] = "/"
            if direction == "west":
                for x in range(ini[0], fin[0] + 1):
                    pair = self.positionInBoard([x, ini[1]])
                    position = self.board[pair[0]][pair[1]]
                    position[1] = "/"
            return True
        else:
            return False

    ###Init of objects

    def getObjects(self):
        return self.objects

    def setObjects(self, id, color, amount=0):
        if not self.isObject(id):
            self.objects.append([id, amount, color])
            return True
        else:
            return False

    def setObjectInWorld(self, id, amount, position):
        if self.isCellWallFree(position):
            newPosition = self.positionInBoard(position)
            itsHere = False
            if self.isObject(id):
                for x in self.getObjects():
                    if x[0] == id:
                        x[1] += amount
                        positionInBoard = self.board[newPosition[0]][newPosition[1]]
                        for y in positionInBoard[2]:
                            if y[0] == id:
                                y[1] += amount
                                itsHere = True
                                break
                        if not itsHere:
                            positionInBoard[2].append([id, amount])
                        break
                return True
        else:
            return False

    def setGoals(self, id, typeOf, objectOrPosition, amount=None, position2=None):
        if not self.isGoal(id):
            if typeOf == "WillyIsAt" and isinstance(objectOrPosition, list):
                goal = [id, typeOf, objectOrPosition, None, None]
                self.goals.append(goal)
                return True
            elif typeOf == "ObjectInBasket" and isinstance(objectOrPosition, str) and isinstance(amount, int):
                goal = [id, typeOf, objectOrPosition, amount, None]
                self.goals.append(goal)
                return True
            elif typeOf == "ObjectInPosition" and isinstance(objectOrPosition, str) and isinstance(position2,
                                                                                                   list) and isinstance(
                    amount, int):
                goal = [id, typeOf, objectOrPosition, amount, position2]
                self.goals.append(goal)
                return True
        else:
            return False

    def getGoals(self):
        return self.goals

    def getValueGoals(self, goal):
        if goal == True or goal == False:
            print(goal, goal)
            return goal
        if self.isGoal(goal):
            for x in self.goals:
                if x[0] == goal:
                    if x[1] == "WillyIsAt":
                        print(goal,
                              x[2][1] == self.getWillyPosition()[0][1] and x[2][0] == self.getWillyPosition()[0][0])
                        return x[2][1] == self.getWillyPosition()[0][1] and x[2][0] == self.getWillyPosition()[0][0]

                    elif x[1] == "ObjectInBasket":
                        if self.isObjectBasket(x[2]):
                            print(goal, self.howMuchObjectsInBasket(x[2]) == x[3])
                            return self.howMuchObjectsInBasket(x[2]) == x[3]
                        else:
                            return False

                    elif x[1] == "ObjectInPosition":
                        if self.isCellWithObject(x[4], x[2]):
                            print(goal, self.howMuchObjectsInCell(x[4], x[2]) == x[3])
                            return self.howMuchObjectsInCell(x[4], x[2]) == x[3]
                        else:
                            print(goal, False)
                            return False

    def getValueFinalGoal(self):
        if self.finalgoal[1] != "":
            return self.finalgoal[0].finalGoalValue(self)
        else:
            return False

    def getFinalGoal(self):
        return self.finalgoal[1]

    def setFinalGoal(self, nodo, input):
        self.finalgoal[0] = nodo
        self.finalgoal[1] = self.finalgoal[1] + input

    """
     Init of Booleans
     """

    ####
    # Get y Set Bool
    ####
    def setBool(self, id, value):
        if not self.isBool(id):
            self.bools.append([id, value])
            return True
        return False

    def getBools(self):
        return self.bools

    def getValueBool(self, id):
        if self.isBool(id):
            for x in self.bools:
                if x[0] == id:
                    return x[1]
        return None

    def changeBool(self, id, value):
        if self.isBool(id):
            for x in self.bools:
                if x[0] == id:
                    x[1] = value
                    return True
        else:
            return False

    ####
    # Get y Set Willy and its Basket
    ####
    def setWillyStart(self, pair, direction):
        self.positionI = [pair, direction]
        self.setWillyPosition(pair, direction)
        return True

    def getWillyStart(self):
        return self.positionI

    def setWillyPosition(self, pair, direction):
        if self.isCellWallFree(pair):
            self.positionF = [pair, direction]
            pos = self.positionInBoard(pair)
            self.board[pos[0]][pos[1]][1] = "w"
            self.changeLookingBools(direction)
            self.changeFLRBools(self.getWillyPosition()[0], direction)
            return True
        else:
            return False

    def getWillyPosition(self):
        return self.positionF

    def setCapacityOfBasket(self, num):
        self.capacityOfBasket = num
        return True

    def getCapacityOfBasket(self):
        return self.capacityOfBasket

    def getObjectsInBasket(self):
        return self.objectsInBasket

    def setObjectsInBasket(self, id, amount):
        if self.isObject(id) and self.getCapacityOfBasket() > 0:
            if not self.isObjectBasket(id):
                self.objectsInBasket.append([id, amount])
            else:
                for y in self.objectsInBasket:
                    if y[0] == id:
                        y[1] = y[1] + amount

            newcapacity = self.getCapacityOfBasket() - amount
            self.setCapacityOfBasket(newcapacity)
            return True
        else:
            return False

    def addObjectsInBasket(self, id, amount):
        ready = False
        # Verifico si puedo agarrar objetos por mi basket capacity ysi el id existe
        if self.isObject(id) and self.getCapacityOfBasket() > 0:
            pair = self.positionInBoard(self.getWillyPosition()[0])
            listObjInCell = self.board[pair[0]][pair[1]][2]
            index = -1
            for i in range(0, len(listObjInCell)):
                # Verifico si en la celda en la que estoy en el area de objetos tengo a
                # alguien con el id y que la cantidad sea mayor a lo que quiero recoger
                if listObjInCell[i][0] == id and listObjInCell[i][1] >= amount:
                    self.setObjectsInBasket(id, amount)
                    # Modifico la lista de objects
                    for y in self.getObjects():
                        if y[0] == id:
                            y[1] = y[1] - amount

                    # Modifico la cantidad en la celda en la que estoy
                    listObjInCell[i][1] = listObjInCell[i][1] - amount
                    ready = True
                    if listObjInCell[i][1] == 0:
                        index = i
                    if index >= 0:
                        listObjInCell.pop(index)
            return ready
        else:
            return ready

    def setFreeObjectsInBasket(self, id, amount):
        index = -1
        if self.isObject(id) and self.isObjectBasket(id):
            for i in range(0, len(self.objectsInBasket)):
                objectInB = self.objectsInBasket[i]
                if objectInB[0] == id and objectInB[1] >= amount:
                    objectInB[1] = objectInB[1] - amount
                    if objectInB[1] == 0:
                        index = i
                    break
            if index >= 0:
                self.objectsInBasket.pop(index)

            self.capacityOfBasket += amount
            return self.setObjectInWorld(id, amount, self.getWillyPosition()[0])
        else:
            return False

    ####
    # Some Questions
    ####

    def isObjectBasket(self, objectname):
        return self.isGeneric(objectname, "ObjectBasket")

    def isObject(self, objectname):
        return self.isGeneric(objectname, "Object")

    def isBool(self, id):
        return self.isGeneric(id, "Bool")

    def isGoal(self, id):
        return self.isGeneric(id, "Goal")

    def isCellWallFree(self, pair):
        if len(pair) == 2:
            # position = [pair([x,y]),willy(W) o wall(X),lista de pares([idObje,attributes])]
            position = self.positionInBoard(pair)
            print("Position Here: ")
            print(position)
            # print(self.board)
            print(self)
            print("Position Up ^ ")
            if 1 <= pair[0] <= self.dimensions[0] and 1 <= pair[1] <= self.dimensions[1]:
                return self.board[position[0]][position[1]][1] != "/"
        else:
            return False

    def isCellWithObject(self, pair, objectname):
        if len(pair) == 2:
            # position = [pair([x,y]),willy(W) o wall(X),lista de pares([idObje,amount])]
            position = self.positionInBoard(pair)
            for x in self.board[position[0]][position[1]][2]:
                # x = [idObjeto,amountObject,colorObject]
                if x[0] == objectname:
                    return True
            return False

    def howMuchObjectsInCell(self, pair, objectname):
        if len(pair) == 2:
            # position = [pair([x,y]),willy(W) o wall(X),lista de pares([idObje,amount])]
            position = self.positionInBoard(pair)
            for x in self.board[position[0]][position[1]][2]:
                # x = [idObjeto,amountObject,colorObject]
                if x[0] == objectname:
                    return x[1]
        else:
            return 0

    def howMuchObjectsInBasket(self, objectname):
        for x in self.objectsInBasket:
            # x = [idObjeto,amountObject,colorObject]
            if x[0] == objectname:
                return x[1]
        return 0

    def whatColorIs(self, objects):
        mylist = self.getObjects()
        for elem in mylist:
            # elem = [idObjeto,amountObject,colorObject]
            if elem[0] == objects:
                return elem[2]
        return None

    ####
    # My personal functions
    ####

    def setClearBoard(self, pair):
        self.board = []
        if len(pair) == 2:
            for i in range(0, pair[1]):
                self.board.append([])
                for j in range(0, pair[0]):
                    self.board[i].append([[j, pair[1] - i - 1], " ", []])
        return True

    def positionInBoard(self, position):
        dimension = self.getDimension()
        print("0000#####HEY#####")
        print(position)
        print(isinstance(position[1], int))
        print(dimension)
        print("1111#####HEY#####")
        pair = [dimension[1] - position[1], position[0] - 1]
        return pair

    def printBoard(self, itype=None, reprint=None):
        ##Imprime matriz y el type dice qué imprimir
        rep = ""
        for column in self.board:
            for elem in column:
                if itype == "index":
                    rep += "[" + str(elem[0][0] + 1) + ", " + str(elem[0][1] + 1) + "]" + "   "
                else:
                    if elem[1] == " ":
                        if elem[2] != []:
                            rep += "[ * ]   "
                        else:
                            rep += "[   ]   "
                    else:
                        if elem[2] != []:
                            rep += "[ W ]   "
                        else:
                            rep += "[ " + str(elem[1]) + " ]   "
            rep += "\n"
        if reprint == None:
            print(rep)
        return rep

    def whereIsMyFrontLeftRight(self, position, direction):
        front = left = right = None
        if 1 <= position[0] <= self.dimensions[0] and 1 <= position[1] <= self.dimensions[1]:
            if direction == "north":
                if 1 <= position[1] + 1 <= self.dimensions[1]:
                    front = [position[0], position[1] + 1]
                if 1 <= position[0] - 1 <= self.dimensions[0]:
                    left = [position[0] - 1, position[1]]
                if 1 <= position[0] + 1 <= self.dimensions[0]:
                    right = [position[0] + 1, position[1]]

            elif direction == "west":
                if 1 <= position[1] + 1 <= self.dimensions[1]:
                    left = [position[0], position[1] + 1]
                if 1 <= position[1] - 1 <= self.dimensions[1]:
                    right = [position[0], position[1] - 1]
                if 1 <= position[0] + 1 <= self.dimensions[0]:
                    front = [position[0] + 1, position[1]]

            elif direction == "south":
                if 1 <= position[1] - 1 <= self.dimensions[1]:
                    front = [position[0], position[1] - 1]
                if 1 <= position[0] - 1 <= self.dimensions[0]:
                    right = [position[0] - 1, position[1]]
                if 1 <= position[0] + 1 <= self.dimensions[0]:
                    left = [position[0] + 1, position[1]]

            elif direction == "east":
                if 1 <= position[1] + 1 <= self.dimensions[1]:
                    right = [position[0], position[1] + 1]
                if 1 <= position[1] - 1 <= self.dimensions[1]:
                    left = [position[0], position[1] - 1]
                if 1 <= position[0] - 1 <= self.dimensions[0]:
                    front = [position[0] - 1, position[1]]
        return front, left, right

    def changeFLRBools(self, position, direction):
        newfront, newleft, newright = self.whereIsMyFrontLeftRight(position, direction)
        if newfront != None:
            self.changeBool("front-clear", self.isCellWallFree(newfront))
        else:
            self.changeBool("front-clear", False)
        if newleft != None:
            self.changeBool("left-clear", self.isCellWallFree(newleft))
        else:
            self.changeBool("left-clear", False)
        if newright != None:
            self.changeBool("right-clear", self.isCellWallFree(newright))
        else:
            self.changeBool("right-clear", False)
        return True

    def changeLookingBools(self, direction):
        for x in range(0, 4):
            if self.directions[x] == direction:
                self.changeBool("looking-" + direction, True)
            else:
                self.changeBool("looking-" + self.directions[x], False)

    def isGeneric(self, id, typeOf):
        if typeOf == "ObjectBasket":
            mylist = self.objectsInBasket
        elif typeOf == "Object":
            mylist = self.objects
        elif typeOf == "Bool":
            mylist = self.bools
        elif typeOf == "Goal":
            mylist = self.goals

        for x in mylist:
            if x[0] == id:
                return True
        else:
            return False


""" def main():
    print("Corriendo!")
    if __name__== "__main__" :
         print("####\nEmpezó la prueba\n####\n\n")
         World1 = World()
         print("####\nInicializado\n####")
         print("Dimensiones: ",World1.getDimension())
         World1.setDimension([7,9])
         print("SetDimension 7 9 then print board with index")
         World1.printBoard("index")
         print("getWalls: ",World1.getWalls())
         print("Insert wall [1,1],[1,3],north")
         World1.setWall([1,1],[1,3],"north")
         print("Insert wall [2,2],[3,2],north que NO se debe insertar porque la direccion no corresponde")
         print("Impresion del retorno: ",World1.setWall([2,2],[3,2],"north"))
         print("Insert wall [2,2],[3,2],west si debería")
         print("Impresion del retorno: ",World1.setWall([2,2],[3,2],"west"))
         World1.printBoard()
         print("Verifico mi list wall",World1.getWalls())
         World1.setWall([7,7],[5,7],"east")
         World1.setWall([5,7],[5,2],"south")
         World1.setWall([1,7],[3,7],"west")
         print("inserto walls 7,7-5,7  5,7-5,2 y 1,7-3,7")
         World1.printBoard()
         print("Añadiendo un objeto con id flor, sin amount y color verde, debería decir true: ", World1.setObjects("flor","cyan"))
         print("lista de objetos: ", World1.getObjects())
         print("metodo isObject para flor: ",World1.isObject("flor"))
         print("metodo isObject para mirror: ",World1.isObject("mirror"))
         print("setObjectInWorld 3 flores en 4,4:",World1.setObjectInWorld("flor",3,[4,4]))
         print("lista de objetos: ", World1.getObjects())
         World1.printBoard()
         print("setObjectInWorld + 5  flores en 4,4:",World1.setObjectInWorld("flor",5,[4,4]))
         print("lista de objetos: ", World1.getObjects())
         print("isCellWithObject con cel 4,4 y flor: ",World1.isCellWithObject([4,4],"flor"))
         print("howMuchObjectsInCell con cel 4,4 y flor: ",World1.howMuchObjectsInCell([4,4],"flor"))
         print("what color is flor: ",World1.whatColorIs("flor"))
         print("isCellWithObject con cel 1,1 y flor: ",World1.isCellWithObject([1,1],"flor"))
         ("howMuchObjectsInCell con cel 4,4 y mirror: ",World1.howMuchObjectsInCell([4,4],"mirror"))
         print("isObject mirror: ", World1.isObject("mirror"))
         print("setBool willhapyy true: ",World1.setBool("willhappy",True))
         print("añadirlo una segunda vez willhapyy true: ",World1.setBool("willhappy",True))
         print("change willhapyy to false: ",World1.changeBool("willhappy",False))
         print("getValue willhapyy: ",World1.getValueBool("willhappy"))
         print("setObjectInWorld + 1  flores en 1,1 pero hay wall:",World1.setObjectInWorld("flor",1,[1,1]))
         print("isBool willhappy: ", World1.isBool("willhappy"))
         print("isBool happy: ", World1.isBool("happy"))
         print("Insertar a Willy en 7,9",World1.setWillyPosition([7,9],"north"))
         print(World1)
         front,left,right = World1.whereIsMyFrontLeftRight([1,1],"west")
         print("1,1 My front left right",front,left,right)
         print("setWilly 2,1 west",World1.setWillyPosition([2,1],"west"))
         print(World1)
         print(World1.getBools())
         print(World1.moveWilly())
         print(World1.getBools())
         print(World1.getBools())
         print("turn willy left (miro al north)",World1.turnWilly("left"))
         print("turn willy left (miro al este)",World1.turnWilly("left"))
         print("turn willy right (miro al norte)",World1.turnWilly("right"))
         print(World1.getBools())
         print("set 5 flor en ",World1.setObjectInWorld("flor",5,[2,1]))
         print(World1)
         print(World1.getWillyPosition()[1])
         World1.turnWilly("left")
         World1.moveWilly()
         print(World1)
         print(World1.objects)
         World1.setCapacityOfBasket(20)
         print("agarrar 3 flores ",World1.addObjectsInBasket("flor",3))
         print("13 - 3 flores ",World1.objects)
         print("20-3 ",World1.capacityOfBasket)
         print("3 flores ",World1.objectsInBasket)
         print("Mirror: ", World1.setObjects("mirror","blue"))
         print("Table: ", World1.setObjects("table","gray"))
         print("2 mirror en pos actual:",World1.setObjectInWorld("mirror",2,[2,1]))
         print("agarrar 1 mirror ",World1.addObjectsInBasket("mirror",1))
         print("pickObject",World1.pickObject("mirror"))
         print("agarrar 2 flores ",World1.addObjectsInBasket("flor",2))
         print("obj ",World1.objects)
         print("basket capacity",World1.capacityOfBasket)
         print("my basket ",World1.objectsInBasket)
         print("drop 1 flor ",World1.dropObject("flor"))
         print("obj ",World1.objects)
         print("basket capacity",World1.capacityOfBasket)
         print("my basket ",World1.objectsInBasket)
         print("drop 2 mirrors ",World1.setFreeObjectsInBasket("mirror",2))
         print("obj ",World1.objects)
         print("basket capacity",World1.capacityOfBasket)
         print("my basket ",World1.objectsInBasket)
         print("head ",World1.getWillyPosition()[1])
         World1.turnWilly("right")
         World1.turnWilly("right")
         World1.moveWilly()
         print("drop flor y mirror:",World1.dropObject("flor"),World1.dropObject("mirror"))
         World1.moveWilly()
         World1.turnWilly("left")
         World1.turnWilly("left")
         World1.moveWilly()
         print("pick flor y mirror:",World1.pickObject("flor"),World1.pickObject("mirror"))
         World1.turnWilly("right")
         World1.turnWilly("right")
         World1.moveWilly()
         World1.moveWilly()
         World1.turnWilly("left")
         print(World1.moveWilly())
         print(World1.moveWilly())
         print(World1.moveWilly())
         print(World1)

         World1.setGoals("goal1","WillyIsAt",[1,2])
         print(World1.getGoals())
main() """