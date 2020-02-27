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

def main():
#Main
Array= []

#Supongamos que encontré Object-type flores cyan
attributesObjects = {
    "world":"world1",
    "color": "cyan",
}
flores = Structure("Flor","Object",attributesObjects)
print(attributesObjects["color"])
Array.append(flores)

#Encontre un Wall
attributesObjects = {
    "world":"world1",
    "f1": "1",
    "c1": "2",
    "f2": "3",
    "c2": "1",
}
wall1 = Structure("","Wall",attributesObjects)
Array.append(wall1)

#Encontre un segundo Wall
attributesObjects = {
    "world":"world1",
    "f1": "2",
    "c1": "5",
    "f2": "5",
    "c2": "2",
}
wall1 = Structure("","Wall",attributesObjects)
Array.append(wall1)

attributesObjects = {
    "world":"world1",
    "color": "yellow",
}
flores = Structure("Sol","Object",attributesObjects)
Array.append(flores)

print(flores.getAttribute('color'))

if __name__ == "__main__":
    main()