import tkinter as tk
from backend import Backend
import tkinter.messagebox as msgbox

class Layout:
    def __init__(self):
        self.backend = Backend()

        self.tk = tk.Tk()

        self.cardinateFrame = tk.Frame(self.tk)
        self.cardinateValue = {}
        self.cardinateControl = {}

        self.teamDividFrame = tk.Frame(self.tk)
        self.playerValue = {}
        self.playerControl = {}
        self.initTkinter()
        self.redTeamList = None
        self.whiteTeamList = None

    def initTkinter(self):
        self.tk.title("welcome to niumaCup")
        for id in self.backend.getAllParticipantsId():
            checkVar = tk.IntVar()
            self.cardinateValue[id] = checkVar
            checkButton = tk.Checkbutton(self.cardinateFrame, text=self.backend.data[id]['name'], variable=checkVar, onvalue=1, offvalue=0)
            checkButton.pack()
            self.cardinateControl[id] = checkButton
        selectButton = tk.Button(self.cardinateFrame, text='确认参战人员', command=self.selectPlayers)
        selectButton.pack()
        self.cardinateFrame.pack()
        self.tk.mainloop()



    def throwErrorMessage(self, title, msg):
        msgbox.showinfo(title, msg)

    def selectPlayers(self):
        playerIdList = []
        for k, v in self.cardinateValue.items():
            if v.get() != 0:
                playerIdList.append(k)
        if len(playerIdList) != 10:
            self.throwErrorMessage("错误提醒", "参赛选手不为10人，当前选择参赛选手人数为%d" % len(playerIdList))
        else:
            self.backend.createNewGame(playerIdList)
            self.showTeamDivision(playerIdList)



    def shufflePlayers(self):
        self.backend.shufflePlayers()

    def showTeamDivision(self, playerIdList):
        for id in playerIdList:
            isSelected = tk.IntVar()
            self.playerValue[id] = isSelected
            playerCheckButton = tk.Checkbutton(self.teamDividFrame, text=self.backend.data[id]['name'], variable=isSelected, onvalue=1, offvalue=0)
            self.playerControl[id] = playerCheckButton
            playerCheckButton.pack()
        confirmDivisionButton = tk.Button(self.teamDividFrame, text='确认勾选的选手为一队', command=self.confirmDivision)
        shuffleDivisionButton = tk.Button(self.teamDividFrame, text='随机分配队伍', command=self.suffleDivision)
        confirmDivisionButton.pack()
        shuffleDivisionButton.pack()

        self.redTeamList = tk.Listbox(self.teamDividFrame)
        self.whiteTeamList = tk.Listbox(self.teamDividFrame)
        self.redTeamList.pack()
        self.whiteTeamList.pack()

        redWinButton = tk.Button(self.teamDividFrame, text='结算，红方胜！', command=self.settlementRed)
        whiteWinButton = tk.Button(self.teamDividFrame, text='结算，白方胜！', command=self.settlementWhite)
        redWinButton.pack()
        whiteWinButton.pack()

        self.teamDividFrame.pack(side=tk.RIGHT)
        self.showAwardFrame()



    def confirmDivision(self):
        playersCount = 0
        redTeamPlayerIds = []
        for k, v in self.playerValue.items():
            if v.get() == 1:
                playersCount += 1
                redTeamPlayerIds.append(k)
        if playersCount != 5:
            self.throwErrorMessage("分队错误", "已勾选为同一队的队员人数不为5， 当前已勾选的队员数为%d" % playersCount)
            return
        rt, wt = self.backend.setTeamDivision(redTeamPlayerIds)
        self.flashTeamDisplay(rt, wt)

    def suffleDivision(self):
        rt, wt = self.backend.shufflePlayers()
        self.flashTeamDisplay(rt, wt)

    def flashTeamDisplay(self, rt, wt):
        self.redTeamList.delete(0, tk.END)
        self.whiteTeamList.delete(0, tk.END)
        for id in rt:
            self.redTeamList.insert(tk.END, self.backend.data[id]['name'])
        for id in wt:
            self.whiteTeamList.insert(tk.END, self.backend.data[id]['name'])

    def settlementRed(self):
        self.settlement(0)
    def settlementWhite(self):
        self.settlement(1)

    def settlement(self, side):
        self.backend.settlement(side)

    def showAwardFrame(self):
        awardFrame = tk.Frame(self.tk)
        awardButton = tk.Button(awardFrame, text='结算，红方胜！', command=self.award)
        awardButton.pack()
        # TODO 输出框
        awardFrame.pack()


    def award(self):
        randomList = self.backend.award()
        print(randomList)


















if __name__ == '__main__':
    l = Layout()
    # l.initTkinter()
