'''
遗留问题：
1.如何使用IP代理（如何获取代理IP）
2.如何加入浏览器模拟
'''
#!/usr/bin/python
#coding:utf-8
# import urllib
# from urllib import request
# from bs4 import BeautifulSoup
# import re
from HtmlTools import HtmlTools
from AccessTools import AccessTools
import os
import re
import threading
import random
import time
import pymysql.cursors

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

proxy_list=[#这是我当时用的代理IP，请更新能用的IP
    '202.106.169.142:80',   
    '220.181.35.109:8080',  
    '124.65.163.10:8080',
    '117.79.131.109:8080',
    '58.30.233.200:8080',
    '115.182.92.87:8080',
    '210.75.240.62:3128',
    '211.71.20.246:3128',
    '115.182.83.38:8080',
    '121.69.8.234:8080',
        ]


user_agents = [  
                   'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',  
                   'Opera/9.25 (Windows NT 5.1; U; en)',  
                   'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',  
                   'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',  
                   'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',  
                   'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',  
                   "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",  
                   "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",    
                   ]   

res_tbody = r'<tbody>(.*?)</tbody>'
res_tr = r'<tr class="(.*?)">(.*?)</tr>'
res_td = r'<td>(.*?)</td>'

#爬取入口
def main(url, i):
    htmlTools = HtmlTools()
    accessTools = AccessTools()
    html = htmlTools.getHtmlInfo(url)
    Data = ResolveToData(html)
    for data in Data:
        ProcessData(data)
    accessTools.WriteToText(Data)
    # PrizeInformation = getPrizeInformation(m_tr)
    # AllInformation[i] = PrizeInformation
    #print(AllInformation)

#解析界面，提取数据
def ResolveToData(html):
    Data = []
    m_tr = re.findall(res_tr,html,re.S|re.M)
    for line in m_tr:
        m_td = re.findall(res_td,line[1],re.S|re.M)
        Data.append(m_td)
    return Data

#处理数据，添加属性
def ProcessData(Data):
    Property = {}
    prizeNumber = ''.join(Data[1])
    NumberList = prizeNumber.split(',')
    count = 1
    for n in NumberList:
        if count <= 5:
            Property[n] = -1
        else:
            Property[n] = 1
        count += 1
    Data.append(Property)

#获取某一期信息
def getPrizeInformation(m_tr):
    PrizeInformation = []
    for line in m_tr:
        m_td = re.findall(res_td,line[1],re.S|re.M)
        print(m_td)
        connection = pymysql.connect(host='localhost',
                        user='root',
                        password='caochen520',
                        db='lotteryticket',
                        charset='utf8',
                        cursorclass=pymysql.cursors.DictCursor)
        cursor = connection.cursor()
        sql = "INSERT INTO info__oper (期号, 中奖号码, 中奖时间) VALUES ('%s', '%s', '%s')"%(m_td[0], m_td[1], m_td[2])
        cursor.execute(sql)
        cursor.close()
        connection.commit()
        time.sleep(1)
        dic = {'期号':m_td[0],'中奖号码':m_td[1],'开奖时间':m_td[2]}
        PrizeInformation.append(dic)    
        Issue.append(m_td[0])
        PrizeNum.append(m_td[1])
        Date.append(m_td[2])
    return PrizeInformation

if __name__ == "__main__":
    main("http://www.bwlc.net/bulletin/prevtrax.html",1)
    # threads = []
    # for i in range(1, 15000):
    #     urls = "http://www.bwlc.net/bulletin/prevtrax.html?page=%d" %i
    #     t = threading.Thread( target = main,args = (urls, i))
    #     time.sleep(0.5)
    #     t.setDaemon(True)
    #     t.start()
    #     threads.append(t)