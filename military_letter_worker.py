
import os.path
import sys
import military_letter_sender as mls
import functions_area
import schedule
import time

class Sender:
    sender = mls.LetterClient()
    def login_and_send(self, id, pw, name, autolettermaker):
        let = autolettermaker.makeLetter()
        self.sender.login(id, pw)
        self.sender.send(name, let[0], let[1])

class Scheduler:
    autolettermaker: object
    scheduler = schedule
    sender = Sender()
    id: str
    pw: str
    name: str

    def __init__(self, id, pw, name, autolettermaker):
        self.autolettermaker = autolettermaker
        self.id = id
        self.pw = pw
        self.name = name

    def setScheduler(self, sendOnWeekends):
        self.scheduler.every().monday.at("17:00").do(
            self.sender.login_and_send, self.id, self.pw, self.name, self.autolettermaker
        )
        self.scheduler.every().tuesday.at("17:00").do(
            self.sender.login_and_send, self.id, self.pw, self.name, self.autolettermaker
        )
        self.scheduler.every().wednesday.at("17:00").do(
            self.sender.login_and_send, self.id, self.pw, self.name, self.autolettermaker
        )
        self.scheduler.every().thursday.at("17:00").do(
            self.sender.login_and_send, self.id, self.pw, self.name, self.autolettermaker
        )
        self.scheduler.every().friday.at("17:00").do(
            self.sender.login_and_send, self.id, self.pw, self.name, self.autolettermaker
        )
        if sendOnWeekends:
            print("[LOG] : Scheduler will send letter even weekends")
            self.scheduler.every().saturday.at("17:00").do(
                self.sender.login_and_send, self.id, self.pw, self.name, self.autolettermaker
            )
            self.scheduler.every().sunday.at("17:00").do(
                self.sender.login_and_send, self.id, self.pw, self.name, self.autolettermaker
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
                self.bodyResult += data[1] + "<br>"

        return self.bodyResult

    def appendLine(self, text):
        self.bodyResult += "<br>" + text

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