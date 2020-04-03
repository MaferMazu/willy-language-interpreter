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