from World import *
from Task import *
class Node:
     def __init__(self,type,children=None,leaf=None):
          self.type = type
          if children:
               self.children = children
          else:
               self.children = [ ]
          self.leaf = leaf

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
               print(self.type)
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
                              mybool= mybool and (child.finalGoalValue(mundo, True))
                         else:
                              print("soy leaf y mi valor es:",child,mundo.getGoals(),mundo.getValueGoals(child))
                              mybool=mybool and mundo.getValueGoals(child)
                    
               return mybool
          else:
               return False

     def boolValue(self,mundo,mybool):
          
          if isinstance(mundo,World):
               print(self.type)
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
                    mybool = mybool and mundo.isObjectBasket(mundo.getWillyPosition()[0], self.children[0])
               else:
                    for child in self.children:
                         if isinstance(child,Node):
                              mybool= mybool and (child.boolValue(mundo,mybool))
                         else:
                              print("soy leaf y mi valor es:",child,mundo.getGoals(),mundo.getValueGoals(child))
                              mybool=mybool and mundo.getValueBool(child)
                    
               return mybool
          else:
               return False


     def executeMyTask(self,task):
          
          if isinstance(task,Task):
               print(self.type)

               if self.type=="Drop":
                    if task.world.isObjectBasket(self.children[0]) and task.world.isObject(self.children[0]):
                         task.dropObject(self.children[0])
               elif self.type=="Pick":
                    if task.world.isCellWithObject(task.world.getWillyPosition()[0],self.children[0]) and task.world.isObject(self.children[0]):
                         task.pickObject(self.children[0])
               elif self.type=="Clear":
                    task.world.changeBool(self.children[0], False)
               elif self.type=="Flip":
                    boolAux = task.world.getValueBool(self.children[0])
                    task.world.changeBool(self.children[0], not boolAux)
               elif self.type=="SetBool":
                    task.world.changeBool(self.children[0],self.children[1])
               elif self.type=="SetTrue":
                    task.world.changeBool(self.children[0],True)
               elif self.type=="Move":
                    task.moveWilly()
               elif self.type=="TL":
                    task.turnWilly("left")
               elif self.type=="TR":
                    task.turnWilly("right")
               elif self.type=="Terminate":
                    print(task.world)
               elif self.type=="ifSimple":
                    if self.children[0].boolValue(task.world,True):
                         self.children[1].executeMyTask(task)
               elif self.type=="ifCompound":
                    if self.children[0].boolValue(task.world,True):
                         self.children[1].executeMyTask(task)
                    else:
                         self.children[2].executeMyTask(task)
               elif self.type =="whileInst":
                    while self.children[0].boolValue(task.world,True):
                         self.children[1].executeMyTask(task)
               elif self.type =="Define As":
                    task.instructions.append([self.children[0].children[0],self.children[1]])
               elif self.type=="Repeat":
                    for i in range(0,self.children[0]+1):
                         self.children[1].executeMyTask(task)
               else:
                    defineas=False
                    for x in task.instructions:
                         if self.type==x[0]:
                              defineas = True
                              x[1].executeMyTask(task)
                    if not defineas:
                         for child in self.children:
                              if isinstance(child,Node):
                                   child.executeMyTask(task)
                              
