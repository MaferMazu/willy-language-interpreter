class Task:
    def __init__(self,World):
        self.instructions="" #todas mis instrucciones
        self.world=World

    def getInstructions(self):
        return self.instructions

    def setInstructions(self,input):
        self.instructions=self.instructions + input