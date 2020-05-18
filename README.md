# Military Letter AutoSender

## Introduction

훈련소에 있는 사람에게 자동으로 인편을 보내주는 라이브러리입니다.

[Military Letter Crawler](https://github.com/nuxlear/military-letter-crawler "JunWon Hwang, WonMo Kang, SungHee Ryu") 프로젝트에서 시작되었으며
이 레포지토리의 프로젝트는 [Sanop(SungHee Ryu)](https://github.com/S4nop)가 개인적으로 진행중입니다.

## Requirements
Python 3.7 에서 작성된 코드입니다. 정상 동작을 위해 Python 3 버전 이상을 사용해주세요. 

필요한 라이브러리 및 패키지는 다음과 같습니다. 
```text
requests
beautifulsoup4
Comment
os.path
sys
json
```

## Worker Usage
```python
import military_letter_worker as mlw

#유저 파일 생성(1회만 필요)
ufm = mlw.UserFileManager('username')
ufm.addText("텍스트")
ufm.addFunctions("FunctionName", "params", "className")

#인편 전송(유저 파일 필요)
abm = mlw.AutoBodyMaker('username')
abm.sendLetter('username@email.com', 'password', 'addressee', 'letter_title')
```
* **addFunction**에 사용될 함수는 **function_area.py**에 작성되어야 합니다.

## Basically implemented functions
1. Naver news crawler
   ```python
   #Default Usage
   nn = NaverNews()
   nn.autoRun(NaverNews.NewsType.WORLD)

   #UserFileManager Usage
   ufm.addFunctions("autoRun", "NaverNews.NewsType.WORLD", "NaverNews")
   ```
3. Weather info crawler
   ```python
   #Default Usage
   wc = WeatherCrawler()
   wc.getWeather()

   #UserFileManager Usage
   ufm.addFunctions("getWeather", "", "WeatherCrawler")
   ```