import os
import json
from model.game import Game
from model import participants as part
DATABASE_PATH = os.path.join(os.path.abspath("."), r"database.conf")
GAME_RESULT_SOURCE = os.path.join(os.path.abspath("."), r"game_res.conf")

class Backend:
    def __init__(self):
        with open(DATABASE_PATH, "r") as f:
            self.data = json.load(f)
        self.curGame = None



    def getAllParticipantsId(self):
        return list(self.data.keys())

    # def getAllParticipantsName(self):
    #     res = []
    #     for id in self.data.keys():
    #         res.append(self.data[id]['name'])
    #     return res

    def createNewGame(self, playersId):
        id = Game.generateId()
        self.curGame = Game(id, playersId)

    def shufflePlayers(self):
        return self.curGame.shuffle()


    def setTeamDivision(self, redTeamPlayerIds):
        return self.curGame.setDivision(redTeamPlayerIds)

    def settlement(self, side):
        self.curGame.settlement(side)

    def award(self):
        with open(GAME_RESULT_SOURCE, "r") as f:
            history = json.load(f)

        historyMatches = history['games']
        # TODO 剩下的部分



