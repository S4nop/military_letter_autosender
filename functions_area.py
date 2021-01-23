import requests
import os.path
import json
from bs4 import BeautifulSoup
from bs4 import Comment
from enum import Enum
import re

'''
Usage
fbc = FacebookCrawler()
fbc.set_user("username")

fbc.addPagetoList or GroupList
fbc.auto~~.
or
fbc.pageFeed(...)
'''


'''
class FacebookCrawler:
    class Type(Enum):
        PAGE  = 0
        GROUP = 1

    targList = dict()

    def initDict(self):
        self.targList['Page'] = dict()
        self.targList['Group'] = dict()

    def readListfromString(self, strData):
        self.targList = json.loads(strData)

    def addList(self, page_Name, type, count = 5):
        if page_Name in self.targList[type.name]:
            return
        self.targList[type.name][page_Name] = dict()
        self.targList[type.name][page_Name]['tData'] = ""
        self.targList[type.name][page_Name]['count'] = count

    def pageFeed(self, pageName):
        req = requests.get("https://www.facebook.com/pg/" + pageName + "/posts/?ref=page_internal")
        soup = BeautifulSoup(req.content, "html.parser")

        contents = soup.select('.userContentWrapper')
        contents_no_notice = [x for x in contents if not x.select('._449j')]

        return self.__getFeed(self.type.PAGE, pageName, contents_no_notice)


    def groupFeed(self, groupName):
        req = requests.get("https://www.facebook.com/groups/" + groupName)
        mainSoup = BeautifulSoup(req.content, 'html.parser')

        commentData = mainSoup.find_all(string=lambda text: isinstance(text, Comment))
        soup = BeautifulSoup(bytes(commentData[1], 'utf-8'), 'html.parser')
        contents = soup.select('._3ccb')

        return self.__getFeed(self.type.GROUP, groupName, contents)

    def autoRunWithJSON(self):
        result = []
        for targ in self.targList['Page']:
            result.append('[[Page Name: ' + targ + ']]' + str(self.pageFeed(targ)))
        for targ in self.targList['Group']:
            result.append('[[Group Name: ' + targ + ']]' + str(self.groupFeed(targ)))
        self.writeUserFile(self.targList)
        return '\n'.join(result)

#private:
    def __getFeed(self, type, name, contents):
        timeID, count = self.getTimeData(name, type.name)
        if timeID != -1:
            contents = self.remDup(contents, timeID)
        contents_reversed = list(reversed(contents))

        texts = []
        for i in range(0, min(count, len(contents_reversed))):
            timeID = contents_reversed[i].find('a', {'class': '_5pcq'})['href']
            user_content = contents_reversed[i].find_all(attrs={'data-testid': 'post_message'})
            text = '\n[--Indented Text--]\n'.join(map(lambda x: x.text, user_content))
            print(text)
            texts.append(text)

        self.writeTimeData(name, type.name, timeID)

    def __getTimeData(self, targName, targType): #If page doesn't exist in file, return -1
        return self.targList[targType][targName]["tData"] if self.targList[targType][targName]['tData'] != "" else -1, self.targList[targType][targName]['count']

    def __writeTimeData(self, pageName, targType, timeData):
        self.targList[targType][pageName]['tData'] = timeData

    def __removeDuplication(self, html, oldTimeID):
        bup = html[:]
        for child in reversed(html):
            bup.pop()
            if(child.find('a', {'class':'_5pcq'})['href'] == oldTimeID):
                return bup
        return html

    def __removeNotice(self, respSoup):
        i = 0
        for child in respSoup:
            if(child.select('._449j')):
                i += 1
            else:
                break
        return respSoup[i : int(len(respSoup))]
'''



class NaverNews():
    soup = ""
    class NewsType(Enum):
        POLITIC     = 0
        ECONOMY     = 1
        SOCIETY     = 2
        LIFECULTURE = 3
        WORLD       = 4
        ITSCIENCE   = 5

    def getNewsPage(self):
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Whale/2.8.108.15 Safari/537.36'}
        newsPage = requests.get("https://news.naver.com", headers=headers)
        self.soup = BeautifulSoup(newsPage.content, "html.parser")

    def getNewsTitles(self, newsType):
        texts = []
        news_part = self.soup.select(".com_list")[newsType.value]
        texts.append(news_part.select(".com_list > dl > dd > a")[0].get_text())
        for child in news_part.select(".com_list > div > ul > li > a > strong"):
            texts.append(child.get_text())

        print('\\')
        tmp =  '<br>'.join(texts).replace("\\", "")
        return tmp

    def autoRun(self, newsType):
        self.getNewsPage()
        return self.getNewsTitles(newsType)
'''
class GoogleNews:
    soup = ""
    CONST_HEADLINE_URL = "https://news.google.com/?hl=ko&gl=KR&ceid=KR%3Ako"
    CONST_KOR_URL = "https://news.google.com/topics/CAAqIQgKIhtDQkFTRGdvSUwyMHZNRFp4WkRNU0FtdHZLQUFQAQ?hl=ko&gl=KR&ceid=KR%3Ako"
    CONST_WORLD_URL = "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtdHZHZ0pMVWlnQVAB?hl=ko&gl=KR&ceid=KR%3Ako"
    CONST_BUSINESS_URL = "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtdHZHZ0pMVWlnQVAB?hl=ko&gl=KR&ceid=KR%3Ako"
    CONST_SCI_TECH_URL = "https://news.google.com/topics/CAAqKAgKIiJDQkFTRXdvSkwyMHZNR1ptZHpWbUVnSnJieG9DUzFJb0FBUAE?hl=ko&gl=KR&ceid=KR%3Ako"
    CONST_ENTERTAIN_URL = "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNREpxYW5RU0FtdHZHZ0pMVWlnQVAB?hl=ko&gl=KR&ceid=KR%3Ako"
    CONST_SPORTS_URL = "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp1ZEdvU0FtdHZHZ0pMVWlnQVAB?hl=ko&gl=KR&ceid=KR%3Ako"
    CONST_HEALTH_URL = "https://news.google.com/topics/CAAqIQgKIhtDQkFTRGdvSUwyMHZNR3QwTlRFU0FtdHZLQUFQAQ?hl=ko&gl=KR&ceid=KR%3Ako"

    #param1 : newsURL, param2 : num
    def getNewsTitles(self, *args):
        newsPage = requests.get(args[0])
        soup = BeautifulSoup(newsPage.content, "html.parser")
        texts = []
        for i in range(0, args[1]):
            texts.append(soup.select(".DY5T1d")[i].get_text())
        return '\n'.join(texts)
'''
#Weather Crawler Class
class WeatherCrawler:

    def parseWeatherInfo(self, tBodySoup):
        date = tBodySoup.select(".date")[0].get_text().replace('\n', '')
        morning = tBodySoup.select(".weather_inner")[0].get_text().replace('\n', '')
        afternoon = tBodySoup.select(".weather_inner")[1].get_text().replace('\n', '')
        temperature = tBodySoup.select(".cell_temperature")[0].get_text().replace('\n', '')

        return '(' + date + '::' + morning + '::' + afternoon + '::' + temperature + ')'

    def getWeather(self):
        req = requests.get("https://weather.naver.com/today/15230109")
        soup = BeautifulSoup(req.content, 'html.parser')
        respSoup = soup.select(".week_list")

        result = []
        for child in respSoup[0].select(".week_item"):
            result.append(self.parseWeatherInfo(child))

        return '<br>'.join(result)

class WorldFootBall:
    def getwFootballNews(self):
        newsPage = requests.get("https://sports.news.naver.com/wfootball/index.nhn")
        self.soup = BeautifulSoup(newsPage.content, "html.parser")
        texts = []
        for child in self.soup.select(".news_list > li > a"):
            texts.append(child.get_text())
        return '<br>'.join(texts)

class Corona:
    def getTodayData(self):
        soup = BeautifulSoup(requests.get("http://ncov.mohw.go.kr/").content, "html.parser")
        texts = []
        for child in soup.select(".liveNum > .liveNum"):
            texts.append(re.sub('\d\)', '\g<0><br>', re.sub('\n\+|\?\n|\n','',child.get_text().strip())))
        return '<br>'.join(texts).replace('=', '')