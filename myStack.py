DEBUG_MODE = True
class myStack:
    def __init__(self):
        self.stack = []

    def find(self,symbol):
        table = self.stack(len(self.stack) - 1)
        IFoundIt = False
        for element in table:
            if element[0] == symbol:
                iFoundIt = True
                break
        return iFoundIt

    def insert(self, symbol, data):
        if not self.find(symbol):
            pair = [symbol, data]
            table = self.stack(len(self.stack) - 1)
            table.append(pair)

        else:
            print("Error: symbol " + symbol + " already exists")

    def push_empty_table(self):
        table = []
        self.stack.append(table)
        print("Se ha inicializado la tabla con un elemnto")

    def pop(self):
        if not empty:
            self.stack.pop()
        else:
            print("Error: pop in empty stack")

    def empty(self):
        return len(self.stack)==0

    def push(self,table):
        self.stack.append(table)

    def __str__(self):
        mystring = "["
        for x in self.stack:
            mystring = mystring + "[ " + x[0] + ", " + x[1].typeOfObject+ "], "
        mystring = mystring + "]"
        return mystring
