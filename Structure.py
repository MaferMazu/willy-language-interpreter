DEBUG_MODE = True
class Structure:
    def __init__(self, name, typeOfObject, attribute):
        self.name = name
        self.typeOfObject = typeOfObject
        self.attribute = attribute

    def __str__(self):
        x = str(self.typeOfObject) + ": "
        if not self.name == "":
            x = x + str(self.name)
        x= x + "( "
        for y in self.attribute:
            attribute = str(y) + ": " + str(self.attribute[y]) + ", "
            x = x + attribute
        x= x + ")"
        return x

    def getAttribute(self,key):
        return self.attribute[str(key)]

    def setAttribute(self,key,value):
        self.attribute[str(key)]=str(value)
    
    def appendAttribute(self,key,value):
        self.attribute[str(key)]=str(value)

