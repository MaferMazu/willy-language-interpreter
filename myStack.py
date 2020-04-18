DEBUG_MODE = True
import sys
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


