from World import *
from Task import *
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
               # print(self.type)
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
                              # print("soy leaf y mi valor es:",child,mundo.getGoals(),mundo.getValueGoals(child))
                              mybool=mybool and mundo.getValueGoals(child)
                    
               return mybool
          else:
               return False

     def boolValue(self,mundo,mybool):
          
          if isinstance(mundo,World):
               # print(self.type)
               if self.type=="Conjuncion":
                    left = self.children[0].boolValue(mundo,mybool)
                    rigth = self.children[1].boolValue(mundo,mybool)
                    mybool= mybool and (mundo.getValueGoals(left) and mundo.getValueGoals(rigth))
               elif self.type=="Disyuncion":
                    left = self.children[0].boolValue(mundo,mybool)
                    rigth = self.children[1].boolValue(mundo,mybool)
                    # print("SOYYYYYYYYYYYYYYYYYYYYYYYYYYYYY EL SEXY OOOOOOOO")
                    mybool= mybool and (mundo.getValueGoals(left) or mundo.getValueGoals(rigth))
                    # print(mybool)
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
                              # print("soy leaf y mi valor es:", child, mundo.getBools(), mundo.getValueBool(child))
                              mybool=mybool and mundo.getValueBool(child)
                              # print(mybool)
               return mybool
          else:
               return False


     def executeMyTask(self,task):
          # print("####HEELL YEA")
          # # print(task)
          if isinstance(task,Task) and not task.fin:
               # print(self.type)
               if not task.world.getValueFinalGoal():
                    if self.type=="Drop":
                         if task.world.isObjectBasket(self.children[0]) and task.world.isObject(self.children[0]):
                              if not task.dropObject(self.children[0]):
                                   print("No se puede hacer el drop con:",self.children[0])
                    elif self.type=="Pick":
                         # print("ESTAMOS RECOGIENDO")
                         if task.world.isCellWithObject(task.world.getWillyPosition()[0],self.children[0]) and task.world.isObject(self.children[0]):
                              if not task.pickObject(self.children[0]):
                                   print("No se puede hacer el pick con:",self.children[0])
                         #print("Pick")
                    elif self.type=="Clear":
                         if not task.world.changeBool(self.children[0], False):
                              print("No se puede hacer el clear con:",self.children[0])
                    elif self.type=="Flip":
                         boolAux = task.world.getValueBool(self.children[0])
                         if not task.world.changeBool(self.children[0], not boolAux):
                              print("No se puede hacer el flip con:",self.children[0])
                    elif self.type=="SetBool":
                         if not task.world.changeBool(self.children[0],self.children[1]):
                              print("No se puede hacer el setbool con:",self.children[0])
                    elif self.type=="SetTrue":
                         if not task.world.changeBool(self.children[0],True):
                              print("No se puede hacer el settrue con:",self.children[0])
                    elif self.type=="Move":
                         if not task.moveWilly():
                              print("Willy no se pudo mover, y su configuración actual es:",task.world.getWillyPosition())
                    elif self.type=="TL":
                         if not task.turnWilly("left"):
                              print("No pudo haver turn-left:")
                    elif self.type=="TR":
                         if not task.turnWilly("right"):
                              print("No pudo haver turn-right:")
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
                    elif self.type=="ifSimple":
                         if self.children[0].boolValue(task.world,True):
                              self.children[1].executeMyTask(task)
                              #print("Ifsimpledentro")
                    elif self.type=="ifCompound":
                         if self.children[0].boolValue(task.world,True):
                              self.children[1].executeMyTask(task)
                         else:
                              self.children[2].executeMyTask(task)
                    elif self.type =="whileInst":
                         print("MY WHILEEEEEEEE condicion: ",self.children[0],self.children[0].boolValue(task.world,True))
                         while self.children[0].boolValue(task.world,True):
                              if task.fin:
                                   break
                              print("WHILE")
                              self.children[1].executeMyTask(task)
                    elif self.type =="Define As":
                         task.instructions.append([self.children[0].children[0],self.children[1]])
                    elif self.type=="Repeat":
                         for i in range(0,self.children[0]):
                              if task.fin:
                                   break
                              self.children[1].executeMyTask(task)
                    elif self.type=="MyInstruction":
                         if task.instructions!=[]:
                              for x in task.instructions:
                                   if self.children[0]==x[0]:
                                        x[1].executeMyTask(task)
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
                    

