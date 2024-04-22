from .player import Player
from typing import List, Dict
class GameBoard():

    players: List[Player] = []
    removed_players: Dict[str, Player] = {}

    def __init__(self):
        self.clearGameboard()
        return
    
    def addPlayer(self, player:Player):
        if player.id == "Guest":
            return
        elif player.id in self.removed_players:
            new_player = self.removed_players.pop(player.id)
            self.players.append(new_player)
            
        else:
            self.players.append(player)

    def playersDict(self): # id: {location, size}
        retval = {}
        for player in self.players:
            retval[player.id] = {"location":[player.top,player.left], "size":player.width}
        return retval
    
    def removePlayer(self, id:str):
        for player in self.players:
            if player.id == id:
                self.players.remove(player)
                self.removed_players[player.id] = player
                break
        return self.playersDict()
    
    def findPlayer(self, id:str) -> Player:
        for player in self.players:
            if player.id == id:
                return player
        return None
    
    def updatePlayer(self, id:str, x:int, y:int, size:int=None):
        player = self.findPlayer(id)
        if player:
            player.updateLocation(x, y)
            player.updateSize(size)
        return self.playersDict()
    
    def clearGameboard(self):
        self.players = []
