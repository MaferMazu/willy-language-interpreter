class World:
     def __init__(self):
          self.dimensions=[1,1]
          self.objects=[] #Formato [idObjeto,amountObject,colorObject]
          self.board=[] #Esto es una matriz con elementos de la forma [pair([x,y]),willy(W) o wall(/),lista de pares([idObje,amount])]
          self.walls=[] #Formato [[colum0,fila0],[colum1,fila1],direction]
          self.WPositionI = [[1,1],"north"]
          self.WPositionF = [[1,1],"north"]
          self.WCapacityOfBasket = 0
          self.WObjectsInBasket = [] #Formato [idObjeto,amountObject,colorObject]
          self.worldBools = [["front-clear",True], ["left-clear",True], ["right-clear",True], ["looking-north",True], ["looking-east",False], ["looking-south",False],["looking-west",False]] #Formato [id,value]
          self.directions=["north","west","south","east"]
     
     def getDimension(self):
          return self.dimensions

     def setDimension(self,pair):
          self.dimensions=pair
          self.setClearBoard(pair)
          return True

     def getWalls(self):
          return self.walls

     def insertWall(self,ini,fin,direction):
          #ini y fin son pares ordenados x,y
          if len(ini)==len(fin)==2 and ((direction=="north" and ini[0]==fin[0] and ini[1]<=fin[1]) or
            (direction=="south" and ini[0]==fin[0] and ini[1]>=fin[1]) or
            (direction=="east" and ini[1]==fin[1] and ini[0]>=fin[0]) or
            (direction=="west" and ini[1]==fin[1] and ini[0]<=fin[0])):
               self.walls.append([ini,fin,direction])
               if direction=="north":
                    for x in range(ini[1],fin[1]+1):
                         pair=self.positionInBoard([ini[0],x])
                         position = self.board[pair[0]][pair[1]]
                         position[1]="/"
               if direction=="south":
                    for x in range(fin[1],ini[1]):
                         pair=self.positionInBoard([ini[0],x])
                         position = self.board[pair[0]][pair[1]]
                         position[1]="/"
               if direction=="east":
                    for x in range(fin[0],ini[0]+1):
                         pair=self.positionInBoard([x,ini[1]])
                         position = self.board[pair[0]][pair[1]]
                         position[1]="/"
               if direction=="west":
                    for x in range(ini[0],fin[0]+1):
                         pair=self.positionInBoard([x,ini[1]])
                         position = self.board[pair[0]][pair[1]]
                         position[1]="/"
               return True
          else:
               return False

     def setObjectInWorld(self,id,amount,position):
          if self.cellWallFree(position):
               newPosition= self.positionInBoard(position)
               itsHere = False
               if self.isObject(id):
                    for x in self.objects:
                         if x[0] == id:
                              x[1] += amount
                              positionInBoard =self.board[newPosition[0]][newPosition[1]]
                              for y in positionInBoard[2]:
                                   if y[0]==id:
                                        y[1] +=amount
                                        itsHere = True
                                        break
                              if not itsHere:
                                   positionInBoard[2].append([id,amount])
                    return True
          else:
               return False

     def positionInBoard(self,position):
          dimension = self.getDimension()
          pair = [dimension[1]-position[1],position[0]-1]
          return pair

     
     def setWillyStart(self,pair,direction):
          self.WPositionI = [pair,direction]
          return True

     def getWillyStart(self):
          return self.WPositionI

     def setWillyPosition(self,pair,direction):
          self.WPositionF = [pair,direction]
          pos = self.positionInBoard(pair)
          self.board[pos[0],pos[1]][1]="W"
          return True

     """ def moveWilly(self):
          pos = self.getWillyPosition()
          if self.getValue("front-clear"):
               if pos[1]=="north":
                    newpos = self.positionInBoard() """

     def turnWilly(self,directionLR):
          pos = self.getWillyPosition()[1]
          index = 0
          for x in range(0,5):
               if self.directions[x]== pos:
                    index = x
               else:
                    return False
          if directionLR == "left":
               self.WPositionF[1]=self.directions[(index-1)%4]
          elif directionLR == "right":
               self.WPositionF[1]=self.directions[(index+1)%4]
          return True

     def getWillyPosition(self):
          return self.WPositionF

     def setCapacityOfBasket(self,num):
          self.WCapacityOfBasket = num
          return True

     def getCapacityOfBasket(self):
          return self.WCapacityOfBasket

     def getObjectsInBasket(self):
          return self.WObjectsInBasket

     def addObjectsInBasket(self,id,amount):
          if self.isObject(id):
               for x in self.objects:
                    if x[0]==id and x[1]>amount:
                         if not self.isObjectBasket(id):
                              self.WObjectsInBasket.append([x[0],amount,x[2]])
                         else:
                              for y in self.WObjectsInBasket:
                                   if y[0]==id:
                                        y[1] = y[1] + amount
                         x[1]=x[1]-amount
                         return True
          else:
               return False

     def addWorldBools(self,id,value):
          if not self.isBool(id):
               self.worldBools.append([id,value])
               return True
          return False

     def isObjectBasket(self,objectname):
          for x in self.WObjectsInBasket:
               if x[0]==objectname:
                    return True
          else:
               return False

     def getWorldBools(self):
          return self.worldBools
     
     def getValueBool(self,id):
          if self.isBool(id):
               for x in self.worldBools:
                    if x[0]==id:
                         return x[1]
          return None


     def changeBool(self,id,value):
          if self.isBool(id):
               for x in self.worldBools:
                    if x[0]==id:
                         x[1]=value
                         return True
          else:
               return False

     def getObjects(self):
          return self.objects

     def addObject(self,id,color,amount=0):
          if not self.isObject(id):
               self.objects.append([id,amount,color])
               return True
          else:
               return False

     def setClearBoard(self,pair):
          self.board = []
          if len(pair)==2:
               for i in range(0,pair[1]):
                    self.board.append([])
                    for j in range(0,pair[0]):
                         self.board[i].append([[j,pair[1]-i-1]," ",[]])
          return True

     def printBoard(self,itype=None):
          ##Imprime matriz y el type dice qué imprimir
          rep = ""
          for column in self.board:
               for elem in column:
                    if itype=="index":
                         rep += "["+str(elem[0][0]+1)+", "+str(elem[0][1]+1)+"]" + "   "
                    else:
                         if elem[1]==" ":
                              if elem[2]!=[]:
                                   rep += "[ O ]   "
                              else:
                                   rep += "[   ]   "
                         else:
                              rep += "[ "+str(elem[1]) + " ]   "
               rep += "\n"
          print(rep)
          return rep

     def cellWallFree(self,pair):
          if len(pair)==2:
               # position = [pair([x,y]),willy(W) o wall(X),lista de pares([idObje,attributes])]
               position = self.positionInBoard(pair)
               return self.board[position[0]][position[1]][1] != "/"
          else:
               return False
     
     def isObject(self,objectname):
          for x in self.objects:
               if x[0]==objectname:
                    return True
          else:
               return False
     
     def isBool(self,id):
          for x in self.worldBools:
               if x[0]==id:
                    return True
          else:
               return False

     def valueOfBool(self,id):
          for x in self.worldBools:
               if x[0]==id:
                    return x[1]
          else:
               return None

     def cellWithObject(self,pair,objectname):
          if len(pair)==2:
               # position = [pair([x,y]),willy(W) o wall(X),lista de pares([idObje,amount])]
               position = self.positionInBoard(pair)
               for x in self.board[position[0]][position[1]][2]:
                    #x = [idObjeto,amountObject,colorObject]
                    if x[0]==objectname:
                         return True
               return False
     
     def howMuchObjectsInCell(self,pair,objectname):
          if len(pair)==2:
               # position = [pair([x,y]),willy(W) o wall(X),lista de pares([idObje,amount])]
               position = self.positionInBoard(pair)
               for x in self.board[position[0]][position[1]][2]:
                    #x = [idObjeto,amountObject,colorObject]
                    if x[0]==objectname:
                         return x[1]
          else:
               return 0

     def howMuchObjectsInBasket(self,pair,objectname):
          if len(pair)==2:
               for x in self.WObjectsInBasket:
                    #x = [idObjeto,amountObject,colorObject]
                    if x[0]==objectname:
                         return x[1]
          else:
               return 0
     
     def whatColorIs(self,objects):
          mylist = self.objects
          for elem in mylist:
               #elem = [idObjeto,amountObject,colorObject]
               if elem[0]==objects:
                    return elem[2]
          return None

     def __str__(self):
          ret = self.printBoard("willy")
          return ret

def main():
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
         World1.insertWall([1,1],[1,3],"north")
         print("Insert wall [2,2],[3,2],north que NO se debe insertar porque la direccion no corresponde")
         print("Impresion del retorno: ",World1.insertWall([2,2],[3,2],"north"))
         print("Insert wall [2,2],[3,2],west si debería")
         print("Impresion del retorno: ",World1.insertWall([2,2],[3,2],"west"))
         World1.printBoard()
         print("Verifico mi list wall",World1.getWalls())
         World1.insertWall([7,7],[5,7],"east")
         World1.insertWall([5,7],[5,2],"south")
         World1.insertWall([1,7],[3,7],"west")
         print("inserto walls 7,7-5,7  5,7-5,2 y 1,7-3,7")
         World1.printBoard()
         print("Añadiendo un objeto con id flor, sin amount y color verde, debería decir true: ", World1.addObject("flor","cyan"))
         print("lista de objetos: ", World1.getObjects())
         print("metodo isObject para flor: ",World1.isObject("flor"))
         print("metodo isObject para mirror: ",World1.isObject("mirror"))
         print("setObjectInWorld 3 flores en 4,4:",World1.setObjectInWorld("flor",3,[4,4]))
         print("lista de objetos: ", World1.getObjects())
         World1.printBoard()
         print("setObjectInWorld + 5  flores en 4,4:",World1.setObjectInWorld("flor",5,[4,4]))
         print("lista de objetos: ", World1.getObjects())
         print("cellWithObject con cel 4,4 y flor: ",World1.cellWithObject([4,4],"flor"))
         print("howMuchObjectsInCell con cel 4,4 y flor: ",World1.howMuchObjectsInCell([4,4],"flor"))
         print("what color is flor: ",World1.whatColorIs("flor"))
         print("cellWithObject con cel 1,1 y flor: ",World1.cellWithObject([1,1],"flor"))
         ("howMuchObjectsInCell con cel 4,4 y mirror: ",World1.howMuchObjectsInCell([4,4],"mirror"))
         print("isObject mirror: ", World1.isObject("mirror"))
         print("addWorldBools willhapyy true: ",World1.addWorldBools("willhappy",True))
         print("añadirlo una segunda vez willhapyy true: ",World1.addWorldBools("willhappy",True))
         print("change willhapyy to false: ",World1.changeBool("willhappy",False))
         print("getValue willhapyy: ",World1.getValueBool("willhappy"))
         print("setObjectInWorld + 1  flores en 1,1 pero hay wall:",World1.setObjectInWorld("flor",1,[1,1]))
         print("isBool willhappy: ", World1.isBool("willhappy"))
         print("isBool happy: ", World1.isBool("happy"))

main()