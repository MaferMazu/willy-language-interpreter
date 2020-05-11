DEBUG_MODE = True
import sys

class ModelProcedure:
    def __init__(self):
        self.symbol = []

    def findObj(self, symbol, array):
        # print("Init ModelProcedure")
        table = array
        i_found_it = False
        for element in table:
            # print(element)
            # print(element[0])
            # print(symbol)
            if element[0] == symbol:
                i_found_it = True
                break
        # print("End MdodelProcedure")
        return i_found_it

    def find(self, symbol, array):
        # print("Init ModelProcedure")
        table = array
        i_found_it = False
        element =  None
        for element in table:
#             # print(element)
#             # print("#### ### ###")
#             # print(not True)
            if element.id == symbol:
                i_found_it = True
                break
        # print("End MdodelProcedure")

        if i_found_it:
            # print(element.id)
            return element
        else:
            return None
