import random
class Player():
    def __init__(self, id:str, top:int=None, left:int=None, width:int=10, color=None ):
        self.id = id
        if top is None:
            self.top = random.randint(30,70)
        else:
            self.top = top

        if left is None:
            self.left = random.randint(30,70)
        else:
            self.left = left
        self.width = width
        self.color = color

    def __toDict__(self):
        return {"id":self.id,"location":[self.top,self.left],"size":self.width}
    
    def updateLocation(self, top:int, left:int):
        self.top = top
        self.left = left
        return self.__toDict__()
    
    def updateSize(self, width:int=None):
        if width:
            self.width = width
        return self.__toDict__()