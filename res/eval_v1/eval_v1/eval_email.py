# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header
# 发送邮件
# To change this template file, choose Tools | Templates

class EvalEmail(object):
    
    def __init__(self):
        self.server = 'smtp.qq.com'
        self.username = '1070993165@qq.com'
        self.password = 'xsbijabriqmxbfff'
        self.msg_from = '<1070993165@qq.com>'

    def send_email(self,send_to,subject,content):
        
        msg=MIMEText(content,'html','utf-8')

        msg['From'] = self.msg_from
        msg['To'] = '<%s>' % send_to
        msg['Subject'] = Header(subject,'utf-8').encode()

        smtp=smtplib.SMTP_SSL(self.server, 465)
        smtp.set_debuglevel(1)
        smtp.login(self.username,self.password)
        smtp.sendmail(self.msg_from,send_to,msg.as_string())
        smtp.quit()