class ModelProcedure:

    def __init__(self):

        self.symbol = ""

    def find(self, symbol, array):
        print("Init ModelProcedure")
        table = array
        i_found_it = False
        for element in table:
            print(element)
            print(element[0])
            print(symbol)
            if element[0] == symbol:
                i_found_it = True
                break
        print("End MdodelProcedure")
        return i_found_it