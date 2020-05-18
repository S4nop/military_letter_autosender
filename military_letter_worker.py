
import os.path
import sys
import builtins
import military_letter_sender
import functions_area

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

class AutoBodyMaker:
    username = ""
    userdata = []
    bodyResult = ""

    def __init__(self, username):
        self.username = username

    def sendLetter(self, uid, pw, targName, title):
        lc = military_letter_sender.LetterClient()
        lc.login(uid, pw)
        lc.send(targName, title, self.makeBody())

    def makeBody(self):
        self.userdata = self.__readFileData()
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
        args = dict(arg for arg in argstr[2].split(",")) if argstr[2].find(",") != -1 else argstr
        if type(args) == str:
            return self.__getNestedAttr(args)
        else:
            nargs = []
            for arg in args:
                nargs.append(self.__getNestedAttr(arg))
            return nargs


    def __getNestedAttr(self, attrstr):
        if attrstr[0] == "?":
            return attrstr

        attrs = attrstr.split(".") if attrstr.find(".") != -1 else attrstr
        cls = functions_area
        for attr in attrs:
            cls = getattr(cls, attr)
        return cls