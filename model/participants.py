class Participant:
    def __init__(self, pid, name=""):
        # self.id = id
        self.id = pid
        self.name = name
        self.nickName = ""
        self.winCount = 0
        self.partCount = 0
        self.awardRate = 1.0

    def toDic(self):
        dic = {}
        dic['id'] = self.id
        dic['name'] = self.name
        dic['nickName'] = self.nickName
        dic['winCount'] = self.winCount
        dic['partCount'] = self.partCount
        dic['awardRate'] = self.partCount
        return dic

    def fromDic(self, dic):
        newP = Participant(dic['id'], dic['name']);
        newP.nickName = dic['nickName']
        newP.winCount = dic['winCount']
        newP.partCount = dic['partCount']
        newP.awardRate = dic['awardRate']
        return newP
