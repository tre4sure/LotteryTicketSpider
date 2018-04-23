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
#import pymysql.cursors

'''数据注释
AllInformation    所有的信息
PrizeInformation  某一页的信息
Issue             期号
PrizeNum          中奖号码
Date              开奖时间
'''

AllInformation = {}
PrizeInformation = []
Issue = []                                      
PrizeNum = []                                  
Date = []                                       


url = "https://www.mtc328.com/data/bjpk10/lotteryList/2018-04-22.json"

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

#爬取入口
def main(url):
    data = getHtmlInfo(url)
    ticketJson = json.loads(data)
    print("最新开奖信息为: \
            期号： %s,\
            中奖号码： %s,\
            开奖时间： %s"\
            %(ticketJson[0]['issue'],ticketJson[0]['openNum'],ticketJson[0]['openDateTime']))
    ticketData = []
    for tj in ticketJson:
        AddAttributes(tj)
        ticketData.append(ResolveToData(tj))
    result = getResults(ticketData)
    for i in range(1,11):
        if result[str(i)] >= 5:
            if ticketData[0]['Attributes'][str(i)] == 0:
                print("建议购买 号码为：后%d，连续次数为： %d"%(i,result[str(i)]))
            else:
                print("建议购买 号码为：前%d，连续次数为： %d"%(i,result[str(i)]))
    #print(result)
    
    #print(ticketJson)
    #print(AllInformation)

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
    return result
    #print(result)

#获取页面信息
def getHtmlInfo(_url):
    req = urllib.request.Request(url = _url, headers=headers)
    html = request.urlopen(req).read()
    data = html.decode('utf-8')
    return data

if __name__ == "__main__":
    main(url)