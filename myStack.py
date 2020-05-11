DEBUG_MODE = True
import sys

"""
    Estructura de Pila para verificacion del interprete
    Primera fase del proyecto
    Traductores e Interpretadores (CI-3725)
    Maria Fernanda Magallanes (13-10787)
    Jesus Marcano (12-10359)
    E-M 2020
    
    Simulacion de una Pila que se encarga de verificar contextos dentro de dentro del mundo y dentro de la tarea
        con esta clase se puede ver si existe o no un elemento dentro de la pila y devuelve True or False, si el 
        elemento a insertar ya existe. De esta forma, no aseguramos si existen elementos repetidos dentro de nuestro 
        programa 
    
"""
class myStack:
    def __init__(self):
        self.stack = []
        self.level = 0

    def find(self,symbol):
        table = self.stack[len(self.stack) - 1]
        iFoundIt = False
        for element in table:
            if element[0] == symbol:
                iFoundIt = True
                break
        return iFoundIt

    def insert(self, symbol, data):
        if not self.find(symbol):
            pair = [symbol, data]
            table = self.stack[self.level - 1]
            table.append(pair)
        else:
            print("El elemento: " + str(symbol) + "existe en la pila y no podemos volver a agregarlo")
            sys.exit()

    def push_empty_table(self):
        table = []
        self.level = 1
        self.stack.append(table)

    def pop(self):
        if not self.empty():
            self.stack.pop()
            self.level = self.level - 1
        else:
            self.level = 0


    def empty(self):
        return len(self.stack)==0

    def push(self,table):
        if (len(self.stack) - self.level) == 1:
            self.level = self.level + 1
        elif (len(self.stack) - self.level) == 0:
            self.stack.append(table)
            self.level = self.level + 1

    def __str__(self):
        mystring = str(self.stack)
        return mystring


