import tkinter as tk
from backend import Backend
import tkinter.messagebox as msgbox
import time
import _thread

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
        self.awardFrame = tk.Frame(self.tk)

        self.initTkinter()
        self.awardOutput = None
        self.redTeamList = None
        self.whiteTeamList = None




    def initTkinter(self):

        self.tk.title("welcome to niumaCup")
        sw = self.tk.winfo_screenwidth()
        # 得到屏幕宽度
        sh = self.tk.winfo_screenheight()
        # 得到屏幕高度
        ww = 700
        wh = 500
        # 窗口宽高为100
        x = (sw - ww) / 2
        y = (sh - wh) / 2
        self.tk.geometry("%dx%d+%d+%d" % (ww, wh, x, y))
        labelStep1 = tk.Label(self.cardinateFrame, text="第一步，选择参赛选手\n👇")
        labelStep1.pack(side=tk.TOP)
        for id in self.backend.getAllParticipantsId():
            checkVar = tk.IntVar()
            self.cardinateValue[id] = checkVar
            checkButton = tk.Checkbutton(self.cardinateFrame, text=self.backend.data[id]['name'], variable=checkVar, onvalue=1, offvalue=0)
            checkButton.pack(side=tk.TOP, anchor='w')
            self.cardinateControl[id] = checkButton
        selectButton = tk.Button(self.cardinateFrame, text='确认参战人员', command=self.selectPlayers)
        selectButton.pack(side=tk.TOP)
        self.cardinateFrame.pack(side=tk.LEFT)
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
        labelStep2 = tk.Label(self.teamDividFrame, text="第二步，划分队伍\n👇")
        labelStep2.pack(side=tk.TOP, anchor='w')
        for id in playerIdList:
            isSelected = tk.IntVar()
            self.playerValue[id] = isSelected
            playerCheckButton = tk.Checkbutton(self.teamDividFrame, text=self.backend.data[id]['name'], variable=isSelected, onvalue=1, offvalue=0)
            self.playerControl[id] = playerCheckButton
            playerCheckButton.pack(side=tk.TOP, anchor='w')
        confirmDivisionButton = tk.Button(self.teamDividFrame, text='确认勾选的选手为一队', command=self.confirmDivision)
        shuffleDivisionButton = tk.Button(self.teamDividFrame, text='随机分配队伍', command=self.suffleDivision)
        confirmDivisionButton.pack(side=tk.TOP, anchor='w')
        shuffleDivisionButton.pack(side=tk.TOP, anchor='w')



        self.teamDividFrame.pack(side = tk.LEFT)
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
        self.redTeamList = tk.Listbox(self.awardFrame)
        self.whiteTeamList = tk.Listbox(self.awardFrame)
        self.redTeamList.pack(side=tk.LEFT)
        self.whiteTeamList.pack(side=tk.LEFT)

        redWinButton = tk.Button(self.awardFrame, text='结算，红方胜！', command=self.settlementRed)
        whiteWinButton = tk.Button(self.awardFrame, text='结算，白方胜！', command=self.settlementWhite)
        redWinButton.pack(side=tk.TOP)
        whiteWinButton.pack(side=tk.TOP)

        awardButton = tk.Button(self.awardFrame, text='开始抽奖', command=self.award)
        awardButton.pack()
        self.awardOutput = tk.Text(self.awardFrame, width=30, height=30)
        self.awardOutput.pack()
        self.awardFrame.pack(side=tk.LEFT)


    def award(self):
        randomList = self.backend.award()
        if len(randomList) == 0:
            self.throwErrorMessage("抽奖错误", "不存在未参与抽奖的比赛！请至少先结算一场比赛！")
            return
        self.asyncFunc(self.awardResultDisplay, (randomList,))


    def awardResultDisplay(self, randomList):
        for rand in randomList:
            self.awardOutput.delete(1.0, tk.END)
            self.awardOutput.insert(tk.INSERT, rand+"\n")
            time.sleep(0.2)
        self.awardOutput.insert(tk.INSERT, "让我们恭喜这个逼获奖👆")

    def asyncFunc(self, func, args):
        _thread.start_new_thread(func, args)
        # try:
        #     _thread.start_new_thread(func, args)
        # except:
        #     self.throwErrorMessage("程序内部错误", "请联系xenozhou！")



















if __name__ == '__main__':
    l = Layout()
    # l.initTkinter()
