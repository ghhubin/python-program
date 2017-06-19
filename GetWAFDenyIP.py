# -*- coding: utf-8 -*-
import httplib,urllib2
import urllib
import re,sys,json
from bs4 import BeautifulSoup
import ConfigParser

import ssl
ssl._create_default_https_context = ssl._create_unverified_context   #忽略证书验证

global_str = {'cookie':'','hash':'','siteinfo':'','hostname':'','username':'','password':'','filehandler':''}  

def getLoginHash():
    url = '/login/requireLogin'
    headers = {
         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36',
         'Content-Type': 'application/x-www-form-urlencoded',
         'Connection' : 'close',
         'Referer'    : 'https://10.36.40.241/',
         'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
         'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    }
    try:
        conn = httplib.HTTPSConnection(global_str['hostname'], 443)
        conn.request("GET", url, None, headers)
        response = conn.getresponse()
    except Exception, e:
        print e
        return -1
    if (response.status != 200):
    	print response.status
    	return -1
    global_str['cookie'] = response.getheader('set-cookie')

    html_page = response.read()
    p_hash = re.compile('<input type="hidden" name="hash" value="(.*?)" />', re.S)
    r_hash = re.search(p_hash, html_page)  
    global_str['hash'] = r_hash.group().replace('<input type="hidden" name="hash" value="', '').replace('" />', '').strip()
    return 0

def login():
    data = {"user[account]":global_str['username'],"user[password]":global_str['password'],"hash":global_str['hash']}   #用户名密码
    url = '/login/login'

    headers = {
         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36',
         'Content-Type': 'application/x-www-form-urlencoded',
         'Connection' : 'close',
         'Cookie' : global_str['cookie'],
         'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
         'Referer': 'https://10.36.40.241/login/requireLogin',
         'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    }

    post_data = urllib.urlencode(data)
    try:
        conn = httplib.HTTPSConnection(global_str['hostname'], 443)
        conn.request("POST", url, post_data, headers)
        response = conn.getresponse()
        result = response.read()
    except Exception, e:
        print e
        return -1
    #print 'login'
    #print result
    if ((response.status != 200) or not ('success' in result)) :
    	print response.status
    	print response.read() 
    	return -1
    cookies = response.getheader('set-cookie')
    p_cookies = re.compile('PHPSESSID=(.*?);', re.S)
    r_cookies = re.findall(p_cookies, cookies)  
    for cookie in r_cookies:
        global_str['cookie'] = 'PHPSESSID=' + cookie
        #print  global_str['cookie']
    return 0
     
def getSiteInfo():
    url = '/security/manageIPBlacklist/getSiteInfoTree'
    headers = {
         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36',
         'Content-Type': 'application/x-www-form-urlencoded',
         'Connection' : 'close',
         'Referer'    : 'https://10.36.40.241/security/manageIPBlacklist/index',
         'Cookie' : global_str['cookie'],
         'Content-Type':'text/plain;charset=UTF-8',
         'Accept':'application/json, text/javascript, */*',
    }
    try:
        conn = httplib.HTTPSConnection(global_str['hostname'], 443)
        conn.request("GET", url, None, headers)
        response = conn.getresponse()
    except Exception, e:
        print e
        return -1
    if (response.status != 200):
        print response.status
        return -1 
    #global_str['cookie'] = response.getheader('set-cookie')
    global_str['siteinfo'] = response.read()
    return 0    

def getOneSiteDenyIP(name,siteid):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection' : 'close',
        'Cookie' : global_str['cookie'],
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'deflate',
        'Referer': 'https://10.36.40.241/security/manageIPBlacklist/requireIPBlacklist/siteid/1',
        'Upgrade-Insecure-Requests': '1'
    }
    fh = global_str['filehandler']
    print '#'+name    #打印组名字
    fh.write('\n#'+name+'\n')
    curpagenum = 1
    totalpagenum = 0
    while True:
        url = '/security/manageIPBlacklist/requireIPBlacklist?currPage=' + str(curpagenum) + '&siteid=' + siteid + '&sourceIP='
        try:
            conn = httplib.HTTPSConnection(global_str['hostname'], 443)
            conn.request("GET", url, None, headers)
            response = conn.getresponse()
        except Exception, e:
            print e
            return -1
        html_page = response.read()
        if (response.status != 200):
            print response.status
            print page
            return -1 

        soup = BeautifulSoup(html_page,"html.parser")
        #取第一个页面时，取总页数
        if curpagenum == 1:
            text1 = soup.find("div", class_="cmn_page").get_text()
            totalpagenum = int(re.search(re.compile('/(\d+)',re.S), text1).group().replace('/',''))
            if totalpagenum == 0:  #总页数为0，表示没有封禁IP
                print u'#没有封禁IP'.encode('gbk')
                fh.write(u'#没有封禁IP'.encode('gbk')+'\n')
                break
        
        #当前页的所有封禁IP
        tr_list = soup.html.body.find("table",class_="cmn_table").find("tr")
        tr_list = tr_list.find_next("tr")   #跳过标题
        while tr_list:
            ip_info = ''
            td = tr_list.find("td")
            td = td.find_next("td") 
            ip_info += td.string +','     #ip
            td = td.find_next("td")   
            ip_info += td.string +','      #begin time
            td = td.find_next("td")   
            ip_info += td.string +','       #end time
            td = td.find_next("td")  
            ip_info += td.string +','    #blocking type
            td = td.find_next("td")   
            ip_info += td.string +','              #blocking policy name
            td = td.find_next("td") 
            ip_info += td.find('a').string       #blocking policy
            print ip_info
            fh.write(ip_info.encode('gbk')+'\n')
            tr_list = tr_list.find_next("tr")
        
        #判断是否继续循环，取下一页
        if curpagenum >= totalpagenum:
            break
        curpagenum = curpagenum + 1
    return 0

def getAllDenyIP():
    if getLoginHash() != 0:
        print 'Get login hash error!'
        sys.exit(-1) 
    if login() != 0:
        print  'login error!'
        sys.exit(-1) 
    if getSiteInfo() != 0:
        print 'get site info error!'
        sys.exit(-1)
    
    jdata = json.loads(global_str['siteinfo'])
    for i in range(len(jdata)): 
        #print jdata[i]['id']
        #print jdata[i]['text'].encode('utf-8','ignore')
        getOneSiteDenyIP(jdata[i]['text'].encode('gbk'),jdata[i]['id'])

def getConfigFile():
    '''
[config]
host=xxx.xxx.xxx.xxx
username=xxxx
password=xxxxx
    '''
    config = ConfigParser.ConfigParser()
    config.read("config.ini")
    global_str['hostname'] = config.get("config", "host")
    global_str['username'] = config.get("config", "username")
    global_str['password'] = config.get("config", "password")
    return 0

if __name__ == "__main__":
    getConfigFile()
    global_str['filehandler'] = file('denyIPlist.txt', 'w') 
    getAllDenyIP()
    global_str['filehandler'].close() 


