DEBUG_MODE = True
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
            print(self.level)
            print(len(self.stack))
            print(symbol)
            table = self.stack[self.level - 1]
            print()
            table.append(pair)
            

        else:
            print("Error: symbol " + symbol + " already exists")

    def push_empty_table(self):
        table = []
        self.level = 1
        self.stack.append(table)
        print("Se ha inicializado la tabla con un elemnto")
        

    def pop(self):
        if not self.empty():
            self.stack.pop()
            self.level = self.level - 1
        else:
            self.level = 0
            print("Error: pop in empty stack")

    def empty(self):

        return len(self.stack)==0

    def push(self,table):
        # print(self.stack)
        if (len(self.stack) - self.level) == 1:
            self.level = self.level + 1
        elif (len(self.stack) - self.level) == 0:
            self.stack.append(table)
            self.level = self.level + 1
        # print(self.stack)


    def __str__(self):
        #print(self.stack)
        mystring = str(self.stack)
        # for x in self.stack:
        #     for y in range(len(x)):
        #         if len(x) >= 1:
        #             mystring = mystring + "[ " + x[y][0] + ", " + str(x[y][1].type) + "], "
        #
        #         else:
        #             mystring = mystring + "[ ],"
        #
        # mystring = mystring + "]"
        return mystring


