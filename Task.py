class Task:
    def __init__(self,World):
        self.instructions="" #todas mis instrucciones
        self.world=World

    def getInstructions(self):
        return self.instructions

    def setInstructions(self,input):
        self.instructions=self.instructions + input

    ####
    # Instructions
    ####

    def moveWilly(self):
        actualposition = self.world.getWillyPosition()
        pos = self.world.positionInBoard(actualposition[0])
        newfront,newleft,newright = self.world.whereIsMyFrontLeftRight(actualposition[0],actualposition[1])
        if newfront!=None and self.world.isCellWallFree(newfront):
            self.world.positionF = [newfront,actualposition[1]]
            position = self.world.positionInBoard(self.world.getWillyPosition()[0])
            self.world.board[position[0]][position[1]][1]="w"
            self.world.changeFLRBools(self.world.getWillyPosition()[0],self.world.getWillyPosition()[1])
            self.world.board[pos[0]][pos[1]][1]=" "
            return True
        else:
            return False

    def turnWilly(self,directionLR):
        pos = self.world.getWillyPosition()[1]
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
        return self.world.setObjectsInBasket(id,1)

    def dropObject(self,id):
        return self.world.setFreeObjectsInBasket(id,1)