from World import World #Despues tengo que comentar esto

""" Taks - Simulador II
    Traductores e Interpretadores (CI-3725)
    Maria Fernanda Magallanes (13-10787)
    Jesus Marcano (12-10359)
    E-M 2020
    
    
    Task es el encargado de almacenar las instrucciones creadas por el usuairo y de sumylar el movimiento de willy dentro del mundo
    
    Taks esta comprendido por una definicion inciial que contiene
        self.instructions Instrucciones que crea el usuario "distintas a las primitivas"
        self.world "Mundo Asociado al Task"
        self.id "identificador del Taks"
        self.node "Nodo referente al arbol para saber quienes son los hijos de esta instruccion"
        self.fin = "Variable para saber si se cumplio el Final Goal"
        
    Ademas de lo anterior, contamos con "time" variable de Tipo any, que puede ser un float o string, que contiene los 
        segundos o la forma de ejecucion del programa
        
    Las funciones :
        - moveWilly
        - turnWilly
        - pickObject
        - dropObject
        Todas estas competen a acciones de Willy dentro del mundo donde tienes: cambio de orientacion en el tablero, movimiento, 
        interaccion con objetos
        
    add_element: Metodo estatico que se encarga de setear el tiempo desde que se llama la ejecución del programa
"""

class Task:

    time = any
    def __init__(self, id, instanceWorld):
        self.instructions = [] #todas mis instrucciones
        self.world = instanceWorld
        self.id = id
        self.node=None
        self.fin = False


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
        newfront,newleft,newright = self.world.whereIsMyFrontLeftRight(actualposition[0],actualposition[1])
        if newfront!=None and self.world.isCellWallFree(newfront):
            self.world.positionF = [newfront,actualposition[1]]
            position = self.world.positionInBoard(self.world.getWillyPosition()[0])
            self.world.board[position[0]][position[1]][1]="w"
            self.world.changeFLRBools(self.world.getWillyPosition()[0],self.world.getWillyPosition()[1])
            self.world.board[pos[0]][pos[1]][1]=" "
            self.world.getWillyPosition()

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
        return self.world.addObjectsInBasket(id,1)

    def dropObject(self,id):
        return self.world.setFreeObjectsInBasket(id,1)

    @staticmethod
    def add_element(x):
        Task.time = x
