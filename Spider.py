import requests
from bs4 import BeautifulSoup

class Spider:
    def __init__(self, url, headers=None, coockies=None):
        self.url = url
        self.headers = headers
        self.coockies = coockies

    def getHTML(self):
        try:
            response = requests.get(url=self.url, headers=self.headers, timeout=5)
            return response.text
        except:
            return "Sorry, due to some reason, you failed to visit the page."

    def setSoup(self):
        html = self.getHTML()
        self.soup = BeautifulSoup(html, 'html.parser')

    def findTag(self, tagName):
        return self.soup.find_all(tagName)

    def findTagByAttrs(self, tagName, attrs):
        return self.soup.find_all(tagName, attrs)

    def getBeautifyHTML(self):
        return self.soup.prettify()