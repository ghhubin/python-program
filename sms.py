# -*- coding:utf-8 -*-

from suds.client import Client
import time
import hashlib

def sendSMS(calledNumber,content):
    user_url="http://192.168.1.1/swdx/services/SmsBizService?wsdl"
    apName = 'AAAAAAAA'
    apPassword = 'BBBBBBBB'
    compcode = 'CCCCCCCC'
    userCode = 'DDDDDDDD'
    
    timeStamp = str(int(round(time.time() * 1000)))
    apPass=str(hashlib.md5(apName+apPassword+timeStamp).hexdigest())
    nowStr=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())



    client=Client(user_url)

    print(client)

    request = client.factory.create('ns3:SendMessageRequest')

    request.accountId = userCode
    request.apName = apName
    request.apPass = apPass
    request.compId = compcode
    request.id = 'my0001'
    request.timeStamp = timeStamp
    request.calledNumber = calledNumber
    request.callerNumber = '111'
    request.content = content+ ' ' +nowStr  
    request.endTime = nowStr
    request.sendTime = nowStr
    request.smsType = 1

    print request


    try:
         result = client.service.sendMessage(request)
    except Exception,e:
         print e
    
    print(result.returnCode)
    print(result.returnDesc)

if __name__ == '__main__':
    sendSMS('13901234567',u'短信测试。。。。  ')

    
