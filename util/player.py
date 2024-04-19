class Player():
    def __init__(self, socket, id:str, x:int, y:int, radius:int, color=None ):
        self.id = id
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.socket = socket

    def __toDict__(self):
        return {"id":self.id,"location":[self.x,self.y],"size":self.radius}
    
    def updateLocation(self, x:int, y:int):
        self.x = x
        self.y = y
        return self.__toDict__()
    
    def updateSize(self, radius:int=None):
        if radius:
            self.radius = radius
        return self.__toDict__()