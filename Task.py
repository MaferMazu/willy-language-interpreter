from World import World #Despues tengo que comentar esto

class Task:
    def __init__(self, id, instanceWorld):
        self.instructions = [] #todas mis instrucciones
        self.world = instanceWorld
        self.id = id
        self.node=None

    def getInstructions(self):
        return self.instructions

    def setInstructions(self,input):
        self.instructions.append(input)

    ####
    # Instructions
    ####

    def moveWilly(self):
        actualposition = self.world.getWillyPosition()
        pos = self.world.positionInBoard(actualposition[0])
        # print(self.world.getWillyPosition())
        # print(actualposition)
        newfront,newleft,newright = self.world.whereIsMyFrontLeftRight(actualposition[0],actualposition[1])
        # print(self.world.whereIsMyFrontLeftRight(actualposition[0], actualposition[1]))
        # print(newfront)
        # print(newleft)
        # print(newright)
        if newfront!=None and self.world.isCellWallFree(newfront):
            self.world.positionF = [newfront,actualposition[1]]
            position = self.world.positionInBoard(self.world.getWillyPosition()[0])
            self.world.board[position[0]][position[1]][1]="w"
            self.world.changeFLRBools(self.world.getWillyPosition()[0],self.world.getWillyPosition()[1])
            self.world.board[pos[0]][pos[1]][1]=" "
            self.world.getWillyPosition()
            # print("true")
            return True
        else:
            # print("false")
            return False

    def turnWilly(self,directionLR):
        # print("1111#########HEY#####")
        # print(self.world)
        pos = self.world.getWillyPosition()[1]
        # print("0000#####HEY#####")
        index = 0
        for x in range(0,4):
            if self.world.directions[x]== pos:
                index = x
        if directionLR == "left":
            new_direction=self.world.directions[(index-1)%4]
        elif directionLR == "right":
            new_direction=self.world.directions[(index+1)%4]
        self.world.positionF[1]=new_direction
        self.world.changeLookingBools(new_direction)
        self.world.changeFLRBools(self.world.getWillyPosition()[0],new_direction)
        return True

    def pickObject(self,id):
        return self.world.addObjectsInBasket(id,1)

    def dropObject(self,id):
        return self.world.setFreeObjectsInBasket(id,1)

""" def main():
    # print("Corriendo!")
    if __name__== "__main__" :
        # print("####\nEmpezó la prueba\n####\n\n")
        World1 = World()
        # print("####\nInicializado\n####")
        # print("Dimensiones: ",World1.getDimension())
        World1.setDimension([7,9])
        # print("SetDimension 7 9 then print board with index")
        # World1.printBoard("index")
        # print("getWalls: ",World1.getWalls())
        # print("Insert wall [1,1],[1,3],north")
        World1.setWall([1,1],[1,3],"north")
        # print("Insert wall [2,2],[3,2],north que NO se debe insertar porque la direccion no corresponde")
        # print("Impresion del retorno: ",World1.setWall([2,2],[3,2],"north"))
        # print("Insert wall [2,2],[3,2],west si debería")
        # print("Impresion del retorno: ",World1.setWall([2,2],[3,2],"west"))
        # World1.printBoard()
        # print("Verifico mi list wall",World1.getWalls())
        World1.setWall([7,7],[5,7],"east")
        World1.setWall([5,7],[5,2],"south")
        World1.setWall([1,7],[3,7],"west")
        # print("inserto walls 7,7-5,7  5,7-5,2 y 1,7-3,7")
        # World1.printBoard()
        # print("Añadiendo un objeto con id flor, sin amount y color verde, debería decir true: ", World1.setObjects("flor","cyan"))
        # print("lista de objetos: ", World1.getObjects())
        # print("metodo isObject para flor: ",World1.isObject("flor"))
        # print("metodo isObject para mirror: ",World1.isObject("mirror"))
        # print("setObjectInWorld 3 flores en 4,4:",World1.setObjectInWorld("flor",3,[4,4]))
        # print("lista de objetos: ", World1.getObjects())
        # World1.printBoard()
        # print("setObjectInWorld + 5  flores en 4,4:",World1.setObjectInWorld("flor",5,[4,4]))
        # print("lista de objetos: ", World1.getObjects())
        # print("isCellWithObject con cel 4,4 y flor: ",World1.isCellWithObject([4,4],"flor"))
        # print("howMuchObjectsInCell con cel 4,4 y flor: ",World1.howMuchObjectsInCell([4,4],"flor"))
        # print("what color is flor: ",World1.whatColorIs("flor"))
        # print("isCellWithObject con cel 1,1 y flor: ",World1.isCellWithObject([1,1],"flor"))
        ("howMuchObjectsInCell con cel 4,4 y mirror: ",World1.howMuchObjectsInCell([4,4],"mirror"))
        # print("isObject mirror: ", World1.isObject("mirror"))
        # print("setBool willhapyy true: ",World1.setBool("willhappy",True))
        # print("añadirlo una segunda vez willhapyy true: ",World1.setBool("willhappy",True))
        # print("change willhapyy to false: ",World1.changeBool("willhappy",False))
        # print("getValue willhapyy: ",World1.getValueBool("willhappy"))
        # print("setObjectInWorld + 1  flores en 1,1 pero hay wall:",World1.setObjectInWorld("flor",1,[1,1]))
        # print("isBool willhappy: ", World1.isBool("willhappy"))
        # print("isBool happy: ", World1.isBool("happy"))
        # print("Insertar a Willy en 7,9",World1.setWillyPosition([7,9],"north"))
        # print(World1)
        front,left,right = World1.whereIsMyFrontLeftRight([1,1],"west")
        # print("1,1 My front left right",front,left,right)
        # print("setWilly 2,1 west",World1.setWillyPosition([2,1],"west"))
        # print(World1)
        # print(World1.getBools())
        Task1=Task(World1)
        # print(Task1.moveWilly())
        # print(World1.getBools())
        # print(World1.getBools())
        # print("turn willy left (miro al north)",Task1.turnWilly("left"))
        # print("turn willy left (miro al este)",Task1.turnWilly("left"))
        # print("turn willy right (miro al norte)",Task1.turnWilly("right"))
        # print(World1.getBools())
        # print("set 5 flor en ",World1.setObjectInWorld("flor",5,[2,1]))
        # print(World1)
        # print(World1.getWillyPosition()[1])
        Task1.turnWilly("left")
        Task1.moveWilly()
        # print(World1)
        # print(World1.objects)
        World1.setCapacityOfBasket(20)
        # print("agarrar 3 flores ",World1.addObjectsInBasket("flor",3))
        # print("13 - 3 flores ",World1.objects)
        # print("20-3 ",World1.capacityOfBasket)
        # print("3 flores ",World1.objectsInBasket)
        # print("Mirror: ", World1.setObjects("mirror","blue"))
        # print("Table: ", World1.setObjects("table","gray"))
        # print("2 mirror en pos actual:",World1.setObjectInWorld("mirror",2,[2,1]))
        # print("agarrar 1 mirror ",World1.addObjectsInBasket("mirror",1))
        # print("pickObject",Task1.pickObject("mirror"))
        # print("agarrar 2 flores ",World1.addObjectsInBasket("flor",2))
        # print("obj ",World1.objects)
        # print("basket capacity",World1.capacityOfBasket)
        # print("my basket ",World1.objectsInBasket)
        # print("drop 1 flor ",Task1.dropObject("flor"))
        # print("obj ",World1.objects)
        # print("basket capacity",World1.capacityOfBasket)
        # print("my basket ",World1.objectsInBasket)
        # print("drop 2 mirrors ",World1.setFreeObjectsInBasket("mirror",2))
        # print("obj ",World1.objects)
        # print("basket capacity",World1.capacityOfBasket)
        # print("my basket ",World1.objectsInBasket)
        # print("head ",World1.getWillyPosition()[1])
        Task1.turnWilly("right")
        Task1.turnWilly("right")
        Task1.moveWilly()
        # print("drop flor y mirror:",Task1.dropObject("flor"),Task1.dropObject("mirror"))
        Task1.moveWilly()
        Task1.turnWilly("left")
        Task1.turnWilly("left")
        Task1.moveWilly()
        # print("pick flor y mirror:",Task1.pickObject("flor"),Task1.pickObject("mirror"))
        Task1.turnWilly("right")
        Task1.turnWilly("right")
        Task1.moveWilly()
        Task1.moveWilly()
        Task1.turnWilly("left")
        # print(Task1.moveWilly())
        # print(Task1.moveWilly())
        # print(Task1.moveWilly())
        # print(World1)
        World1.setGoals("goal1","WillyIsAt",[1,2])
        # print(World1.getGoals())

main()  """