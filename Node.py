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

     def toString(self):
          ret=""

          if self.type=="Conjuncion" :
               ret += self.children[0].toString() + " or " + self.children[1].toString()
          elif self.type=="Disyuncion":
               ret += self.children[0].toString() + " and " + self.children[1].toString()
          elif self.type=="Parentesis":
               ret += "(" + self.children[0].toString() + ")"
          elif self.type=="Not":
               ret += "not "+ self.children[0].toString()
          else:
               for child in self.children:
                    if isinstance(child,Node):
                         ret += child.toString()
                    else:
                         ret = ret.rstrip("\n")
                         ret += str(child)
          return ret