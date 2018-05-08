'''
获取网页信息
'''
#!/usr/bin/python
#coding:utf-8
import urllib
from urllib import request
from bs4 import BeautifulSoup
import re
import os
import threading
import random
import time
import json
import win32api
import win32gui
import win32con
import socket
from HtmlTools import HtmlTools

socket.setdefaulttimeout(10)
ip_url = 'http://www.xicidaili.com/nn/'
url_mtc = "https://www.mtc328.com/data/bjpk10/lotteryList/%s.json"%(time.strftime('%Y-%m-%d',time.localtime(time.time())))
url_38011 = "https://www.38011.com/1/pk10/pk10list.php?lotCode=10001"

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

latestPrizeNum = []

#爬取入口
def main():
    #fun_mtc()
    fun_38011()
    

def fun_mtc():
    data_mtc = getHtmlInfo(url_mtc)
    ticketJson_mtc = json.loads(data_mtc)
    openMinute = time.strptime(ticketJson_mtc[0]['openDateTime'], "%Y-%m-%d %H:%M:%S").tm_min
    nowMinute = time.localtime().tm_min
    if abs(nowMinute - openMinute) >= 5:
        win32api.MessageBox(win32con.NULL, "拉取数据出现问题", '你好', win32con.MB_OK) 
        print("当前开奖信息为： \
                期号： %s,\
                中奖号码： %s,\
                开奖时间： %s"\
                %(ticketJson_mtc[0]['issue'],ticketJson_mtc[0]['openNum'],ticketJson_mtc[0]['openDateTime']))
        return
    global latestPrizeNum
    tmpPrizeNum = ticketJson_mtc[0]['openNum']
    if tmpPrizeNum == latestPrizeNum:
        return
    latestPrizeNum = tmpPrizeNum
    print("最新开奖信息为: \
            期号： %s,\
            中奖号码： %s,\
            开奖时间： %s"\
            %(ticketJson_mtc[0]['issue'],ticketJson_mtc[0]['openNum'],ticketJson_mtc[0]['openDateTime']))
    ticketData = []
    for tj in ticketJson_mtc:
        AddAttributes(tj)
        ticketData.append(ResolveToData(tj))
    result = getResults(ticketData)
    resultStr = ''
    for i in range(1,11):
        if result[str(i)] >= 7:
            if ticketData[0]['Attributes'][str(i)] == 0:
                resultStr += "建议购买 号码为：后%d，连续次数为： %d \n"%(i,result[str(i)])
            else:
                resultStr += "建议购买 号码为：前%d，连续次数为： %d \n"%(i,result[str(i)])
    if resultStr != '':
        print(resultStr)
        win32api.MessageBox(win32con.NULL, resultStr, '中奖信息', win32con.MB_OK) 

def fun_38011():
    data_38011 = getHtmlInfo(url_38011)
    if data_38011 == None:
        print('获取网络数据失败，将再次尝试...')
        return
    try:
        ticketJson_38011 = json.loads(data_38011)
    except json.JSONDecodeError as e:
        print(e)
        return
    data = ticketJson_38011['result']['data']
    openMinute = time.strptime(data[0]['preDrawTime'], "%Y-%m-%d %H:%M:%S").tm_min
    nowMinute = time.localtime().tm_min
    if nowMinute - openMinute >= 6 and nowMinute - openMinute > 0:
        win32api.MessageBox(win32con.NULL, "拉取数据出现问题", '你好', win32con.MB_OK) 
        print("当前开奖信息为:\
                期号： %s,\
                中奖号码： %s,\
                开奖时间： %s"\
                %(data[0]['preDrawIssue'],data[0]['preDrawCode'],data[0]['preDrawTime']))
        return
    global latestPrizeNum
    tmpPrizeNum = data[0]['preDrawCode']
    if tmpPrizeNum == latestPrizeNum:
        return
    latestPrizeNum = tmpPrizeNum
    print("最新开奖信息为: \
            期号： %s,\
            中奖号码： %s,\
            开奖时间： %s"\
            %(data[0]['preDrawIssue'],data[0]['preDrawCode'],data[0]['preDrawTime']))
    ticketData = []
    for d in data:
        AddAttributes_(d)
        ticketData.append(ResolveToData_(d))
    result = getResults(ticketData)
    print(result)
    resultStr = ''
    for i in range(1,11):
        if result[str(i)] >= 5:
            if ticketData[0]['Attributes'][str(i)] == 0:
                resultStr += "建议购买 号码为：后%d，连续次数为： %d \n"%(i,result[str(i)])
            else:
                resultStr += "建议购买 号码为：前%d，连续次数为： %d \n"%(i,result[str(i)])
    if resultStr != '':
        print(resultStr)
        win32api.MessageBox(win32con.NULL, resultStr, '中奖信息', win32con.MB_OK) 

def ResolveToData(json):
    data = {}
    data['openDateTime'] = json['openDateTime']
    data['issue'] = json['issue']
    data['openNum'] = json['openNum']
    data['Attributes'] = json['Attributes']
    return data

def ResolveToData_(json):
    data = {}
    data['openDateTime'] = json['preDrawTime']
    data['issue'] = json['preDrawIssue']
    data['openNum'] = json['preDrawCode']
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

def AddAttributes_(data):
    openNumStr = data['preDrawCode']
    openNum = openNumStr.split(',')
    Attributes = {}
    for num_s in openNum:
        num = int(num_s)
        if len(Attributes) < 5:
            Attributes[str(num)] = 0
        else:
            Attributes[str(num)] = 1
    data["Attributes"] = Attributes

def getResults(data):
    result = {}
    for i in range(1, 11):
        count = 1
        for j in range(len(data)-1):
            if data[j]['Attributes'][str(i)] == data[j+1]['Attributes'][str(i)]:
                count += 1
            else:
                result[str(i)] = count
                break
            result[str(i)] = count
    return result

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

def get_ip_list(url):
    htmlTools = HtmlTools()
    web_data = htmlTools.getHtmlInfo(url, headers)
    soup = BeautifulSoup(web_data, 'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append(tds[1].text + ':' + tds[2].text)
    return ip_list

if __name__ == "__main__":
    for ip in get_ip_list(ip_url):
        Proxy.append('http://'+ip)
    while True:
        main()
        time.sleep(5)
        pass
    win32api.MessageBox(win32con.NULL, '程序已断开，请重新启动', '结束信息', win32con.MB_OK) 