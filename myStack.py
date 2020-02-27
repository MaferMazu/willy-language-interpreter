class myStack:
    def __init__(self):
        self.stack = []

    def find(self,symbol):
        iFoundIt = False
        for element in self.stack:
            if not isinstance(element, myStack) and isinstance(element, list):
                if element[0]==symbol:
                    print(element[1])
                    iFoundIt = True
        return iFoundIt

    def insert(self,symbol,data):
        if not self.find(symbol):
            pair = [symbol,data]
            self.stack.append(pair)
        else:
            print("Error: symbol " + symbol + " already exists")

    def push_empty_table(self):
        table = myStack()
        self.stack.append(table)

    def pop(self,symbol):
        if not empty:
            self.stack.pop()
        else:
            print("Error: pop in empty stack")

    def empty(self):
        return len(self.stack)==0

    def push(self,table):
        self.stack.append(table)