class ModelProcedure:

    def __init__(self):

        self.symbol = ""

    def find(self,symbol, array):
        table = array
        iFoundIt = False
        for element in table:
            if element[0][0] == symbol:
                iFoundIt = True
                break
        return iFoundIt