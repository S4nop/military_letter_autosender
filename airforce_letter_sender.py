import requests



class LetterClient:
    host = 'https://atc.airforce.mil.kr:444'

    def __init__(self):
        self.session = requests.Session()

    def _post(self, endpoint, data):
        response = self.session.post(self.host + endpoint, data=data, verify=False)
        if response.status_code != 200:
            raise ConnectionError(f'Connection failed: [{response.status_code}] - {response.text}')
        return response.text

    def send_letter(self, seq_val, sodae_val, title, content):
        chkedContent = self.splitContent(content)

        for cont in chkedContent:
            self.send(seq_val, sodae_val, title, cont)

    def send(self, seq_val, sodae_val, title, content):

        endpoint = '/user/emailPicSaveEmail.action'
        data = {
            'siteId': 'tong-new',
            'parent': '%2Fuser%2FindexSub.action%3FcodyMenuSeq%3D156894686%26siteId%3Dtong-new%26menuUIType%3Dtop%26dum%3Ddum%26command2%3DwriteEmail%26searchCate%3D%26searchVal%3D%26page%3D1%26memberSeqVal%3D275171299%26sodaeVal%3D%25EB%25B3%2591%2B828%25EA%25B8%25B0',
            'page': '1',
            'command2': 'writeEmail',
            'searchCate': '',
            'searchVal': '',
            'letterSeq': '',
            'memberSeq': '',
            'memberSeqVal': seq_val,
            'sodaeVal': sodae_val,
            'senderZipcode': '16422',
            'senderAddr1': '경기도 수원시 팔달구 정자천로32번길 20',
            'senderAddr2': '165동 704호',
            'senderName': 'News_Bot',
            'relationship': 'Bot',
            'title': title,
            'contents': content,
            'password': 'qwer1234'
        }

        result = self._post(endpoint, data)
        result = result.split('"message">')[1].split('.</div>')[0]
        print(result)

    def splitContent(self, content):
        splited = content.split('\n')
        slen = 0
        bodies = []
        for i in splited.size():
            if slen + len(splited[i]) > 1450:
                bodies.append('\n'.join(splited[:i - 1] + '\n' +splited[i][:1450 - slen]))
                bodies.append(self.splitContent(splited[i][1450-slen + 1:] + '\n' + '\n'.join(splited[i + 1:])))
        return bodies


