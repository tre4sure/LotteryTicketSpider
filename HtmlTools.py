import urllib
from urllib import request
from bs4 import BeautifulSoup

class HtmlTools:
    def __init__(self):
        return

    def getHtmlInfo(self, _url):
        req = urllib.request.Request(url = _url)
        html = request.urlopen(req).read()
        html = html.decode('utf-8')
        return html
