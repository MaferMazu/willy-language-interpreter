from World import *
from Task import *
import time

"""
    Simulador y Arbol del programa
    Primera fase del proyecto
    Traductores e Interpretadores (CI-3725)
    Maria Fernanda Magallanes (13-10787)
    Jesus Marcano (12-10359)
    E-M 2020
    
    
    Node es la estructura de un Nodo en particular dentro del Arbol de instrucciones generado por las producciones
    de neustro parser e interpretador
     
     
     Junto a esto, tenemos 3 componentes grandes que encargan de realizar la simulacion del Task
     
     - finalGoalToString y finalGoalValue: Estas funciones se encargan de hacer manejable al usuario, en formato String
          la interterpretacion de los Final Goal, a manera de que el usuario pueda ver el resultado del mismo, ademas
          de las correspondientes validaciones para saber si el programa llego al objetivo definido por el usuario
     
     - boolValue: Se encarga de evaluar el estado del booleando del World al cual se esta aplicando el nodo del Task.
          Esto a manera de poder cambiar verificar y modificar el valor de los booleando primitivos de Willy como los definidos por el usuario
          
     - executeMyTask: Este es el encargado de hacer el recorrido del Arbol que generan las producciones que creamos dentro del parser
     
     Para una ejecucion a manera de Debbugger tenemos: 
          - timer: este solo se encarga de impresion de salidas cada x cantidad de segundos, de forma automatica o previo un input de enter del usuario
     
     
"""

startTime = time.time()
class Node:
     def __init__(self,type,children=None):
          self.type = type
          if children:
               self.children = children
          else:
               self.children = [ ]

     def __str__(self, level=0):
          ret = "  " * level + self.type + "\n"
          for child in self.children:
               if isinstance(child,Node):
                    ret += child.__str__(level + 1)
               else:
                    ret = ret.rstrip("\n")
                    ret += " " + str(child) + "\n"
          return ret

     def finalGoalToString(self):
          ret=""
          if self.type=="Conjuncion" :
               ret += self.children[0].finalGoalToString() + " and " + self.children[1].finalGoalToString()
          elif self.type=="Disyuncion":
               ret += self.children[0].finalGoalToString() + " or " + self.children[1].finalGoalToString()
          elif self.type=="Parentesis":
               ret += "(" + self.children[0].finalGoalToString() + ")"
          elif self.type=="Not":
               ret += "not "+ self.children[0].finalGoalToString()
          else:
               for child in self.children:
                    if isinstance(child,Node):
                         ret += child.finalGoalToString()
                    else:
                         ret = ret.rstrip("\n")
                         ret += str(child)
          return ret

     def finalGoalValue(self,mundo,mybool):
          if isinstance(mundo,World):
               if self.type=="Conjuncion":
                    left = self.children[0].finalGoalValue(mundo,mybool)
                    rigth = self.children[1].finalGoalValue(mundo,mybool)
                    mybool= mybool and (mundo.getValueGoals(left) and mundo.getValueGoals(rigth))
               elif self.type=="Disyuncion":
                    left = self.children[0].finalGoalValue(mundo,mybool)
                    rigth = self.children[1].finalGoalValue(mundo,mybool)
                    mybool= mybool and (mundo.getValueGoals(left) or mundo.getValueGoals(rigth))
               elif self.type=="Parentesis":
                    u = self.children[0].finalGoalValue(mundo,mybool)
                    mybool= mybool and ((u))
               elif self.type=="Not":
                    u = self.children[0].finalGoalValue(mundo,mybool)
                    mybool= mybool and (not u)
               else:
                    for child in self.children:
                         if isinstance(child,Node):
                              mybool= mybool and (child.finalGoalValue(mundo,mybool))
                         else:
                              mybool=mybool and mundo.getValueGoals(child)
                    
               return mybool
          else:
               return False

     def boolValue(self,mundo,mybool):
          if isinstance(mundo,World):
               if self.type=="Conjuncion":
                    left = self.children[0].boolValue(mundo,mybool)
                    rigth = self.children[1].boolValue(mundo,mybool)
                    mybool= mybool and (mundo.getValueGoals(left) and mundo.getValueGoals(rigth))
               elif self.type=="Disyuncion":
                    left = self.children[0].boolValue(mundo,mybool)
                    rigth = self.children[1].boolValue(mundo,mybool)
                    mybool= mybool and (mundo.getValueGoals(left) or mundo.getValueGoals(rigth))
               elif self.type=="Parentesis":
                    u = self.children[0].boolValue(mundo,mybool)
                    mybool= mybool and ((u))
               elif self.type=="Not":
                    u = self.children[0].boolValue(mundo,mybool)
                    mybool= mybool and (not u)
               elif self.type=="Found":
                    mybool= mybool and mundo.isCellWithObject(mundo.getWillyPosition()[0],self.children[0])
               elif self.type == "Carrying":
                    mybool = mybool and mundo.isObjectBasket(self.children[0])
               else:
                    for child in self.children:
                         if isinstance(child,Node):
                              mybool= mybool and (child.boolValue(mundo,mybool))
                         else:
                              mybool=mybool and mundo.getValueBool(child)
               return mybool
          else:
               return False

     def timer(self, task):
          if task.time == "man":
               input('Let us wait for user input. \n')
               print("###############")
               print("Estado final de " + str(task.world.id) + " luego de haber ejecutado " + str(task.id))
               print("La posición de Willy es: " + str(task.world.getWillyPosition()[0]) + " mirando hacia el " + str(
                    task.world.getWillyPosition()[1]))
               print("Lo que tiene en el basket es:\n", task.world.getObjectsInBasket())
               # print("El estado de los bools es:\n", task.world.getBools())
               print("El final goal es:\n" + task.world.getFinalGoal())
               print("El valor del final goal es: ", task.world.getValueFinalGoal())
               print(task.world)
          else :
               if task.time > 0:
                    print('Going to sleep for', task.time, 'seconds.')
                    time.sleep(task.time)
                    print("###############")
                    print("Estado final de " + str(task.world.id) + " luego de haber ejecutado " + str(task.id))
                    print("La posición de Willy es: " + str(task.world.getWillyPosition()[0]) + " mirando hacia el " + str(
                         task.world.getWillyPosition()[1]))
                    print("Lo que tiene en el basket es:\n", task.world.getObjectsInBasket())
                    # print("El estado de los bools es:\n", task.world.getBools())
                    print("El final goal es:\n" + task.world.getFinalGoal())
                    print("El valor del final goal es: ", task.world.getValueFinalGoal())
                    print(task.world)
               else:
                    pass

     def executeMyTask(self,task):
          if isinstance(task,Task) and not task.fin:
               if not task.world.getValueFinalGoal():
                    if self.type=="Drop":
                         if task.world.isObjectBasket(self.children[0]) and task.world.isObject(self.children[0]):
                              if not task.dropObject(self.children[0]):
                                   print("No se puede hacer el drop con:",self.children[0])
                         self.timer(task)
                    elif self.type=="Pick":
                         if task.world.isCellWithObject(task.world.getWillyPosition()[0],self.children[0]) and task.world.isObject(self.children[0]):
                              if not task.pickObject(self.children[0]):
                                   print("No se puede hacer el pick con:",self.children[0])
                         self.timer(task)
                    elif self.type=="Clear":
                         if not task.world.changeBool(self.children[0], False):
                              print("No se puede hacer el clear con:",self.children[0])
                         self.timer(task)
                    elif self.type=="Flip":
                         boolAux = task.world.getValueBool(self.children[0])
                         if not task.world.changeBool(self.children[0], not boolAux):
                              print("No se puede hacer el flip con:",self.children[0])
                         self.timer(task)
                    elif self.type=="SetBool":
                         if not task.world.changeBool(self.children[0],self.children[1]):
                              print("No se puede hacer el setbool con:",self.children[0])
                         self.timer(task)
                    elif self.type=="SetTrue":
                         if not task.world.changeBool(self.children[0],True):
                              print("No se puede hacer el set true con:",self.children[0])
                         self.timer(task)
                    elif self.type=="Move":
                         if not task.moveWilly():
                              print("Willy no se pudo mover, y su configuración actual es:",task.world.getWillyPosition())
                         self.timer(task)
                    elif self.type=="TL":
                         if not task.turnWilly("left"):
                              print("No pudo hacer turn-left:")
                         self.timer(task)
                    elif self.type=="TR":
                         if not task.turnWilly("right"):
                              print("No pudo hacer turn-right:")
                         self.timer(task)
                    elif self.type=="Terminate":
                         print("###############")
                         print("Estado final de "+str(task.world.id) +" luego de haber ejecutado "+str(task.id))
                         print("La posición de Willy es: "+ str(task.world.getWillyPosition()[0]) + " mirando hacia el " + str(task.world.getWillyPosition()[1]))
                         print("Lo que tiene en el basket es:\n", task.world.getObjectsInBasket())
                         print("El estado de los bools es:\n", task.world.getBools())
                         print("El final goal es:\n" + task.world.getFinalGoal())
                         print("El valor del final goal es: ",task.world.getValueFinalGoal())
                         print(task.world)
                         task.fin=True
                         self.timer(task)
                    elif self.type=="ifSimple":
                         if self.children[0].boolValue(task.world,True):
                              self.children[1].executeMyTask(task)
                         self.timer(task)
                    elif self.type=="ifCompound":
                         if self.children[0].boolValue(task.world,True):
                              self.children[1].executeMyTask(task)
                         else:
                              self.children[2].executeMyTask(task)
                         self.timer(task)
                    elif self.type =="whileInst":
                         while self.children[0].boolValue(task.world,True):
                              if task.fin:
                                   break
                              self.children[1].executeMyTask(task)
                         self.timer(task)
                    elif self.type =="Define As":
                         task.instructions.append([self.children[0].children[0],self.children[1]])
                         self.timer(task)
                    elif self.type=="Repeat":
                         for i in range(0,self.children[0]):
                              if task.fin:
                                   break
                              self.children[1].executeMyTask(task)
                         self.timer(task)
                    elif self.type=="MyInstruction":
                         if task.instructions!=[]:
                              for x in task.instructions:
                                   if self.children[0]==x[0]:
                                        x[1].executeMyTask(task)
                         self.timer(task)
                    else:
                         
                         for child in self.children:
                              if isinstance(child,Node):
                                   if child.type=="Terminate":
                                        child.executeMyTask(task)
                                        break
                                   else:
                                        child.executeMyTask(task)
               else:
                    print("###############")
                    print("Estado final de "+str(task.world.id) +" luego de haber ejecutado "+str(task.id))
                    print("La posición de Willy es: "+ str(task.world.getWillyPosition()[0]) + " mirando hacia el " + str(task.world.getWillyPosition()[1]))
                    print("Lo que tiene en el basket es:\n", task.world.getObjectsInBasket())
                    print("El estado de los bools es:\n", task.world.getBools())
                    print("El final goal es:\n" + task.world.getFinalGoal())
                    print("El valor del final goal es: ",task.world.getValueFinalGoal())
                    print(task.world)
                    task.fin=True
                    self.timer(task)
                    

