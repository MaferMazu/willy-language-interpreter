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
          if len(ini)==len(fin)==2 and (direction=="north" or direction=="south" or direction=="east" or direction=="west"):
               self.walls.append([ini,fin,direction])
               if direction=="north":
                    for x in range(ini[1],fin[1]):
                         position = self.board[x-1][ini[0]]
                         position[1]="/"
               if direction=="south":
                    for x in range(fin[1],ini[1]):
                         position = self.board[x-1][ini[0]]
                         position[1]="/"
               if direction=="east":
                    for x in range(fin[0],ini[0]):
                         position = self.board[ini[1]][x-1]
                         position[1]="/"
               if direction=="west":
                    for x in range(ini[0],fin[0]):
                         position = self.board[ini[1]][x-1]
                         position[1]="/"
               return True
          else:
               return False

     def setObjectInWorld(self,id,amount,position):
          newPosition= self.positionInBoard(position)
          itsHere = False
          if self.isObject(id):
               for x in self.objects:
                    if x[0] == id:
                         x[2] += amount
                         positionInBoard =self.board[newPosition[0]][newPosition[1]]
                         for y in positionInBoard[2]:
                              if y[0]==id:
                                   y[2] +=amount
                                   itsHere = True
                                   break
                         if not itsHere:
                              positionInBoard[2].append([id,amount])
               return True

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
          position = self.board[pair[1]-1][pair[0]]
          position[1]="W"
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

     def changeWorldBool(self,id,value):
          if self.isBool(id):
               for x in self.worldBools:
                    if x[0]==id:
                         x[1]=value
                         return True
          else:
               return False

     def getObjects(self):
          return self.objects

     def addObject(self,id,amount,color):
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

     def printBoard(self,itype="celdas"):
          ##Imprime matriz y el type dice qué imprimir
          rep = ""
          for column in self.board:
               for elem in column:
                    if itype=="celdas":
                         rep += "["+str(elem[0][0]+1)+", "+str(elem[0][1]+1)+"]" + "   "
                    else:
                         if elem[1]==" " and elem[2]!=[]:
                              rep += "o" + "   "
                         else:
                              rep += str(elem[1]) + "   "
               rep += "\n"
          print(rep)
          return rep

     def cellWallFree(self,pair):
          if len(pair)==2:
               # position = [pair([x,y]),willy(W) o wall(X),lista de pares([idObje,attributes])]
               position = self.positionInBoard(pair)
               return position[1] ==" "
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
          else:
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
         World1 = World()
         print(World1.getDimension())
         World1.setClearBoard([4,3])
         World1.printBoard()
main()