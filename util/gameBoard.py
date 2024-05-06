from .player import Player
from .balls import Balls
from typing import List, Dict
class GameBoard():

    players: List[Player] = []
    removed_players: Dict[str, Player] = {}
    balls:List[Balls] = []
    def __init__(self, nBalls):
        self.clearGameboard()
        self.createBalls(nBalls)
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
            retval[player.id] = {"location":[player.top,player.left], "size":player.width, "score":player.score}
        return retval
    
    def leadersDict(self):
        retval = {"leaders":[]}
        for player in self.players:
            retval["leaders"].append([player.id, player.score])
        new_leaders = sorted(retval["leaders"], key=lambda x: x[1])
        new_leaders.reverse()
        retval["leaders"] = new_leaders
        # print("retval",retval)
        return retval

    def gameState(self):
        if len(self.balls) == 0:
            # print("creating balls")
            self.createBalls(50)
        players = self.playersDict()
        balls = self.ballDict()
        leaders = self.leadersDict()
        retval = {"players":players, "balls":balls["balls"], "leaders":leaders["leaders"]}
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
    
    def updatePlayer(self, id:str, x:int, y:int, size:int=None, score=0):
        player = self.findPlayer(id)
        if player:
            player.updateLocation(x, y)
            player.updateSize(size)
            # player.updateScore(score)
        return self.playersDict()
    
    def createBalls(self, nBalls):
        retval = {"balls":[]}
        for i in range(0,nBalls):
            ball = Balls()
            self.balls.append(ball)
            retval["balls"].append(ball)
        return retval

    def removeBall(self, top, left): # every time you remove you get more 
        top = int(top)
        left = int(left)
        for ball in self.balls:
            abs_left = abs(ball.left - left)
            abs_top = abs(ball.top - top)
            if abs_left <= 2 and abs_top <= 2:
                self.balls.remove(ball)
                return self.ballDict()
        
        return self.ballDict()

    def ballDict(self):
        retval = {"balls":[]}
        for ball in self.balls:
            retval["balls"].append([ball.top, ball.left])
        return retval
    
    def clearGameboard(self):
        self.players = []
        self.removed_players = {}
        self.balls = []

    def restartGameboard(self):
        self.balls = []
        self.createBalls(100)
        for p in self.players:
            p.restartScore()
        for p in self.removed_players.values():
            p.restartScore()
        return self.gameState()