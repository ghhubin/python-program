#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication 

def sendmail(local_dir,filename): 
    # ������ SMTP ����
    mail_host="smtp.189.cn"  #���÷�����
    mail_user="XXXX@189.cn"    #�û���
    mail_pass="KKKKKKK"   #���� 
     
    sender = 'XXXXX@189.cn'
    receivers = ['XXXXX@189.cn']  # �����ʼ���������Ϊ���QQ���������������
     
    #����һ����������ʵ��
    msg = MIMEMultipart()
    
    #���츽��
    att1 = MIMEApplication(open(local_dir+filename, 'rb').read())
    att1["Content-Disposition"] = 'attachment; filename='+filename #�����filename��������д��дʲô���֣��ʼ�����ʾʲô����
    msg.attach(att1)
    
    #���ʼ�ͷ
    msg['to'] = 'XXXX@189.cn'
    msg['from'] = 'CCCCC@189.cn'
    msg['subject'] = 'screen'
    #�����ʼ�
    
    try:
        smtpObj = smtplib.SMTP() 
        smtpObj.connect(mail_host,25)    # 25 Ϊ SMTP �˿ں�
        smtpObj.login(mail_user,mail_pass)  
        smtpObj.sendmail(sender, receivers, msg.as_string())
        print "�ʼ����ͳɹ�"
    except  Exception, e:    
        print str(e)

if __name__ == '__main__': 
    sendmail("e:\\program\\","test.bmp")       
