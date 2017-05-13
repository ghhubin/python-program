#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication 

def sendmail(local_dir,filename): 
    # 第三方 SMTP 服务
    mail_host="smtp.189.cn"  #设置服务器
    mail_user="XXXX@189.cn"    #用户名
    mail_pass="KKKKKKK"   #口令 
     
    sender = 'XXXXX@189.cn'
    receivers = ['XXXXX@189.cn']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
     
    #创建一个带附件的实例
    msg = MIMEMultipart()
    
    #构造附件
    att1 = MIMEApplication(open(local_dir+filename, 'rb').read())
    att1["Content-Disposition"] = 'attachment; filename='+filename #这里的filename可以任意写，写什么名字，邮件中显示什么名字
    msg.attach(att1)
    
    #加邮件头
    msg['to'] = 'XXXX@189.cn'
    msg['from'] = 'CCCCC@189.cn'
    msg['subject'] = 'screen'
    #发送邮件
    
    try:
        smtpObj = smtplib.SMTP() 
        smtpObj.connect(mail_host,25)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pass)  
        smtpObj.sendmail(sender, receivers, msg.as_string())
        print "邮件发送成功"
    except  Exception, e:    
        print str(e)

if __name__ == '__main__': 
    sendmail("e:\\program\\","test.bmp")       
