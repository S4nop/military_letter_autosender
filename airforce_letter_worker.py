
import os.path
import sys
import airforce_letter_sender as als
import functions_area
import schedule
import time

class Sender:
    sender = als.LetterClient()
    def send(self, seq_val, sodae_val, autolettermaker):
        let = autolettermaker.makeLetter()
        self.sender.send(seq_val, sodae_val, '<공군은 인편에 줄바꿈이 없어요 :: 오늘의 소식>', let[1].replace('<br>', '<    >'))

class Scheduler:
    autolettermaker: object
    scheduler = schedule
    sender = Sender()

    def __init__(self, seq_val, sodae_val, autolettermaker):
        self.autolettermaker = autolettermaker
        self.seq_val = seq_val
        self.sodae_val = sodae_val

    def setScheduler(self, sendOnWeekends):
        self.scheduler.every().monday.at("13:00").do(
            self.sender.send, self.seq_val, self.sodae_val, self.autolettermaker
        )
        self.scheduler.every().tuesday.at("13:00").do(
            self.sender.send, self.seq_val, self.sodae_val, self.autolettermaker
        )
        self.scheduler.every().wednesday.at("13:00").do(
            self.sender.send, self.seq_val, self.sodae_val, self.autolettermaker
        )
        self.scheduler.every().thursday.at("13:00").do(
            self.sender.send, self.seq_val, self.sodae_val, self.autolettermaker
        )
        self.scheduler.every().friday.at("13:00").do(
            self.sender.send, self.seq_val, self.sodae_val, self.autolettermaker
        )
        if sendOnWeekends:
            print("[LOG] : Scheduler will send letter even weekends")
            self.scheduler.every().saturday.at("17:00").do(
                self.sender.send, self.seq_val, self.sodae_val, self.autolettermaker
            )
            self.scheduler.every().sunday.at("17:00").do(
                self.sender.send, self.seq_val, self.sodae_val, self.autolettermaker
            )

    def run(self):
        while True:
            self.scheduler.run_pending()
            time.sleep(60)

class UserFileManager:
    username = ""
    userdata = []

    def __init__(self, username):
        self.username = username

    #Usage : addFunction(function name, parameters, class name)
    def addFunction(self, featName, params, className="builtins"):
        self.userdata.append([className, featName, params])
        print("[LOG] : " + str(self.userdata) + "is successfully added to list")

    def addText(self, text):
        self.userdata.append(["?Text", text, ""])

    def getData(self):
        return self.userdata

    def writeFile(self):
        text = ""
        for data in self.userdata:
            text = text + data[0] + "*::*" + data[1] + "*::*" + data[2] + "@##@"
        text = text.rstrip("@##@")

        with open('user_' + self.username + '.dat', mode='wt', encoding='utf-8') as w:
            w.write(text)

    def readFile(self):
        filePath = 'user_' + self.username + '.dat'
        self.userdata = []
        if os.path.isfile(filePath):
            print("[LOG] : " + self.username + "'s File exists. Start reading user data file.")
            with open(filePath, encoding='utf-8') as r:
                datas = r.readlines()[0].split("@##@")

            for data in datas:
                self.userdata.append(data.split("*::*"))
            return 0
        print("[LOG] : " + self.username + "'s File is not exist. You should create user data file with UserDataFileManager class.")
        return -1

#TODO : Need to implement makeTitle Function!
class AutoLetterMaker:
    username = ""
    userdata = []
    bodyResult = ""
    title = "오늘의 소식"

    def __init__(self, username):
        self.username = username

    def makeLetter(self):
        return [self.title, self.makeBody()]

    def makeTitle(self):
        pass

    def makeBody(self):
        self.userdata = self.__readFileData()
        self.bodyResult = ""
        for data in self.userdata:
            #Parse arguments for function call
            if data[0] != "?Text":
                self.bodyResult += self.__runFunctions(data)
            else:
                self.bodyResult += data[1] + "\n"

        return self.bodyResult

    def appendLine(self, text):
        self.bodyResult += "\n" + text

    def __runFunctions(self, data):
        args = self.__makeArgs(data[2]) if data[2] != "" else ""
        print("[LOG] : " + data[0] +"::"+ data[1] + " function successfully called")
        if data[0] != "builtins":
            cls = getattr(functions_area, data[0])()
            return getattr(cls, data[1])() if args == "" else getattr(cls, data[1])(args)

        return getattr(getattr(sys.modules[__name__], data[0]), data[1])(args) + "<br>"

    def __readFileData(self):
        udfm = UserFileManager(self.username)
        udfm.readFile()
        return udfm.getData()

    def __makeArgs(self, argstr):
        args = argstr.split(",") if argstr.find(",") != -1 else argstr
        if type(args) == str:
            return self.__getNestedAttr(args.strip())
        else:
            nargs = []
            for arg in args:
                nargs.append(self.__getNestedAttr(arg.strip()))
            return nargs


    def __getNestedAttr(self, attrstr):
        if attrstr.startswith('?Text_'):
            return attrstr
        elif attrstr.startswith('?Num_'):
            return int(attrstr.split('?Num_')[1])

        attrs = attrstr.split(".") if attrstr.find(".") != -1 else attrstr
        cls = functions_area
        for attr in attrs:
            cls = getattr(cls, attr)
        return cls