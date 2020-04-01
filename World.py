class World:
     def __init__(self):
          self.dimensions=[1,1]
          self.objects=[] #Formato [idObjeto,amountObject,colorObject]
          self.walls=[]
          self.WPositionI = None
          self.WHeadposition = None
          self.WCapacityOfBasket = 0
          self.WPosition = None
          self.WObjectsInBasket = [] #Formato [idObjeto,amountObject,colorObject]
     
     def getDimension(self):
          return self.dimensions
     
     def HowMuchObjects(self,objects,list):
          for elem in list:
               if elem[0]==objects:
                    return elem[1]
          return 0
     
     def HowColorIs(self,objects,list):
          for elem in list:
               if elem[0]==objects:
                    return elem[2]
          return None


     def __str__(self):
          ret = " De momento "
          return ret