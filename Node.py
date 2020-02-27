class Node:
    def __init__(self,data):
        self.data=data
        self.children = []

    def add_child(self,Node):
        self.children.append(Node)