import urllib
import random
import socket
import json
import time
import datetime
from urllib import request
from bs4 import BeautifulSoup

ip_url = 'http://www.xicidaili.com/nn/'
ticket_common_url = "https://www.mtc328.com/data/bjpk10/lotteryList/%s.json"

Proxy = []

User_Agent = [  
                'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',  
                'Opera/9.25 (Windows NT 5.1; U; en)',  
                'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',  
                'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',  
                'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',  
                'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',  
                "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",  
                "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",    
            ]

headers = {"User-Agent": random.choice(User_Agent)}

# 获取IP代理地址
def get_ip_list():
    req = request.Request(url = ip_url, headers = headers)
    html = request.urlopen(req).read()
    web_data = html.decode('utf-8')
    soup = BeautifulSoup(web_data, 'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append(tds[1].text + ':' + tds[2].text)
    return ip_list

#获取页面信息
def getHtmlInfo(_url):
    tmpProxy = {'http': random.choice(Proxy)}
    proxy_support = request.ProxyHandler(tmpProxy)
    opener = request.build_opener(proxy_support)
    opener.addheaders = [('User-Agent',random.choice(User_Agent))]
    request.install_opener(opener)
    try:
        response = request.urlopen(_url)
        data = response.read().decode('utf-8')
        response.close()
        return data
    except urllib.error.URLError as e:
        print(e.reason)
        data = None
        return data
    except socket.timeout as e:
        print("socket.timeout")
        data = None
        return data

def ResolveToData(json):
    data = {}
    data['openDateTime'] = json['openDateTime']
    data['issue'] = json['issue']
    data['openNum'] = json['openNum']
    data['Attributes'] = json['Attributes']
    return data

def AddAttributes(data):
    openNumStr = data['openNum']
    Attributes = {}
    for num in openNumStr:
        if len(Attributes) < 5:
            Attributes[str(num)] = 0
        else:
            Attributes[str(num)] = 1
    data["Attributes"] = Attributes


def main(ticket_url):
    data = getHtmlInfo(ticket_url)
    if data == None:
        return
    ticketJson = json.loads(data)
    openDate = time.strptime(ticketJson[0]['openDateTime'], "%Y-%m-%d %H:%M:%S")
    ticketData = []
    for tj in ticketJson:
        AddAttributes(tj)
        ticketData.append(ResolveToData(tj))
    maxContinuousTimes = {}
    for i in range(1,11):
        maxContinuousTimes[str(i)] = 1
    for i in range(1,11):
        count = 0
        for j in range(len(ticketData)-1):
            if ticketData[j]['Attributes'][str(i)] == ticketData[j+1]['Attributes'][str(i)]:
                count += 1
            else:
                if maxContinuousTimes[str(i)] < count:
                    maxContinuousTimes[str(i)] = count
                count = 0
    print("*********************%d 年%d 月%d 号 中奖信息*********************** \n"%(openDate.tm_year,openDate.tm_mon,openDate.tm_mday))
    for i in range(1,11):
        print('%d 号 的最高连续中奖次数为 %d \n'%(i, maxContinuousTimes[str(i)]))
    

if __name__ == "__main__":
    for ip in get_ip_list():
        Proxy.append('http://'+ip)
    begin = datetime.date(2018,4,1)
    end = datetime.date(2018,4,25)
    for i in range((end - begin).days+1):
        day = begin + datetime.timedelta(days=i)
        ticket_url = ticket_common_url%(day)
        main(ticket_url)
    