import os
import json
import random
from model.game import Game
from model import participants as part

DATABASE_PATH = os.path.join(os.path.abspath("."), r"database.conf")
GAME_RESULT_SOURCE = os.path.join(os.path.abspath("."), r"game_res.conf")


class Backend:
    def __init__(self):
        with open(DATABASE_PATH, "r") as f:
            self.data = json.load(f)
        self.curGame = None
        self.winRateBonus = 2

    def getAllParticipantsId(self):
        return list(self.data.keys())

    # def getAllParticipantsName(self):
    #     res = []
    #     for id in self.data.keys():
    #         res.append(self.data[id]['name'])
    #     return res

    def reflashDataBase(self, history, winMap, playMap):
        for k, v in winMap.items():
            self.data[k]["winCount"] += v
        for k, v in playMap.items():
            self.data[k]["partCount"] += v

        with open(GAME_RESULT_SOURCE, 'w') as f:
            json.dump(history, f, indent=4, ensure_ascii=False)
        with open(DATABASE_PATH, 'w') as f:
            json.dump(self.data, f,  indent=4, ensure_ascii=False)

    def dirtyDataToDisk(self):
        with open(DATABASE_PATH, "w") as f:
            json.dump(self.data, f,  indent=4, ensure_ascii=False)

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
        unsettledMatches = history['games']['unsettled']
        winnersMap = {}
        playersMap = {}
        for k, v in unsettledMatches.items():
            winners = v.get("winMembers", [])
            losers = v.get("loseMembers", [])
            for winner in winners:
                winTime = winnersMap.get(winner, 0)
                winTime += 1
                winnersMap[winner] = winTime
                playTime = playersMap.get(winner, 0)
                playTime += 1
                playersMap[winner] = playTime
            for loser in losers:
                playTime = playersMap.get(loser, 0)
                playTime += 1
                playersMap[loser] = playTime
        for k in list(unsettledMatches.keys()):
            history['games']['settled'][k] = unsettledMatches.pop(k)
        self.reflashDataBase(history, winnersMap, playersMap)
        return self.awardHelper(winnersMap, playersMap)

    def awardHelper(self, wmap, pmap):
        rateMap = {}
        for k, v in pmap.items():
            rateMap[k] = 1

        playerNames = []
        playerRates = []
        randomTime = 30
        randomRes = []
        for k, v in wmap.items():
            rateMap[k] = rateMap[k] + self.winRateBonus * v
        for k, v in pmap.items():
            playerNames.append(self.data[k]['name'])
            playerRates.append(rateMap[k])
        print("playerRates:")
        print(playerRates)
        if len(playerRates) == 0:
            return randomRes

        prefix = [0 for _ in range(len(playerRates)+1)]
        for i in range(len(playerRates)):
            prefix[i + 1] = prefix[i] + playerRates[i]
        for i in range(randomTime):
            rand = random.random() * prefix[-1]
            idx = self.binarySearch(rand, prefix)
            randomRes.append(playerNames[idx])
        print(randomRes)
        print(playerNames)
        print(playerRates)
        return randomRes

    def binarySearch(self, target, nums):
        left = 1
        r = len(nums)
        while left < r:
            m = int((left + r) / 2)
            if nums[m] >= target:
                r = m
            else:
                left = m + 1
        return left - 1
