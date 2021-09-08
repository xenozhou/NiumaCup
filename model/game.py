import time
from datetime import datetime
import random
import json
import os
GAME_RESULT_SOURCE = os.path.join(os.path.abspath("."), r"game_res.conf")

class Game:
    def __init__(self, gameId, playersId):
        self.id = gameId
        self.players = playersId
        self.isSettled = 0 # 是否结算
        self.redTeam = []
        self.whiteTeam = []
        self.createTime = datetime.now().isoformat()
        self.settleTime = ""

    # 生成对局id
    @staticmethod
    def generateId():
        now = time.time()
        return int(now)

    def getDivisionRes(self):
        return self.redTeam, self.whiteTeam

    #  随机分组
    def shuffle(self):
        self.redTeam = []
        self.whiteTeam = []
        for id in self.players:
            if random.random() > 0.5:
                if len(self.redTeam) < 5:
                    self.redTeam.append(id)
                else:
                    self.whiteTeam.append(id)
            else:
                if len(self.whiteTeam) < 5:
                    self.whiteTeam.append(id)
                else:
                    self.redTeam.append(id)
        return self.redTeam, self.whiteTeam


    def setDivision(self, redTeamPlayerIds):
        self.redTeam = redTeamPlayerIds
        self.whiteTeam = []
        for id in self.players:
            if id not in self.redTeam:
                self.whiteTeam.append(id)
        return self.redTeam, self.whiteTeam


    #  结算
    def settlement(self, side):
        self.settleTime = datetime.now().isoformat()
        if side == 0:
            self.saveResult(self.redTeam, self.whiteTeam)
        else:
            self.saveResult(self.whiteTeam, self.redTeam)

        # 重设id以及生成时间
        self.id = Game.generateId()
        self.createTime = datetime.now().isoformat()





    #  取消上一次结算
    def cancelSettlement(self):
        with open(GAME_RESULT_SOURCE, "r") as f:
            history = json.load(f)
        history.pop(history['lasteGameId'], "empty")
        history["lastGameId"] = -1
        with open(GAME_RESULT_SOURCE, "w") as f:
            json.dump(history, f, indent=4, ensure_ascii=False)


    def saveResult(self, winTeam, loseTeam):
        with open(GAME_RESULT_SOURCE, "r") as f:
            history = json.load(f)
        history['games'][self.id] = {
            "id": self.id,
            "generatedTime": self.createTime,
            "settlementTime": self.settleTime,
            "winMembers": winTeam,
            "loseMembers": loseTeam,
            "isSettled": self.isSettled
        }
        history["lastGameId"] = self.id
        print(history)
        with open(GAME_RESULT_SOURCE, "w") as f:
            json.dump(history, f, indent=4, ensure_ascii=False)



