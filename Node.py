from World import *
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

     def finalGoalValue(self,mundo):
          mybool = True
          if isinstance(mundo,World):

               if self.type=="Conjuncion" :
                    left = self.children[0].finalGoalValue()
                    rigth = self.children[1].finalGoalValue()
                    mybool= mybool and (mundo.getValueGoals(left) and mundo.getValueGoals(rigth))
               elif self.type=="Disyuncion":
                    left = self.children[0].finalGoalValue()
                    rigth = self.children[1].finalGoalValue()
                    mybool= mybool and (mundo.getValueGoals(left) or mundo.getValueGoals(rigth))
               elif self.type=="Parentesis":
                    u = self.children[0].finalGoalValue()
                    mybool= mybool and ((u))
               elif self.type=="Not":
                    u = self.children[0].finalGoalValue()
                    mybool= mybool and (not u)
               else:
                    for child in self.children:
                         if isinstance(child,Node):
                              mybool= mybool and (child.finalGoalValue())
                         else:
                              mybool=mybool and mundo.getValueGoals(child)
                    
               return mybool
          else:
               return False