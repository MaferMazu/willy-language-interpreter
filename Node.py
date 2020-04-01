class Node:
     def __init__(self,type,children=None,leaf=None):
          self.type = type
          if children:
               self.children = children
          else:
               self.children = [ ]
          self.leaf = leaf

     def __str__(self, level=0):
          ret = "\t" * level + repr(self.value) + "\n"
          for child in self.children:
               ret += child.__str__(level + 1)
          return ret