#!/usr/bin/python3
###############################################################################
# Author    :   Qianye Wu
# Email     :   ninipa1985@outlook.com
# Last modified : 2018-03-01 14:47
# Filename   : mymail.py
# Description    : 
###############################################################################

# -*- coding: utf-8 -*-

import os
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib

class Mymail(object):
    __doc__ = '''This is a module which is used for creating and sending email
    Only supports text format and attachment, html format if not supported
    example of obj creation ---
        mail = Mymail(mailServer=your_smtp_mailServer, mailPort=your_smtp_mailPort, mailPassword=your_smtp_mailPassword)
        sometimes your password could be "authorization code" depends on your mail service
    Methods ---
    1. build()
    2. send()
    '''

    def __init__(self, mailServer, mailPort, mailPassword):
        self.mailServer = mailServer
        self.mailPort = mailPort
        self.mailPassword = mailPassword

    def build(self, body, sender, receiver, title="", ccList=[], attachments=[]):
        '''
        :param body:
        :param sender:
        :param receiver:
        :param title:
        :param ccList:
        :param attachments:
        :return:
        build a MIME object which stores all the information of an email
        '''
        ### public variables provided by users
        #self.body                  # (str) if body is a file, loading the text in the file as email body
        #self.sender                # (str) email sender
        #self.receiver              # (str) email receiver, can be a list
        #self.title                 # (str) title of mail
        #self.ccList                # (str) cc list
        #self.attachments           # attachments, can be a list of files
        ### private variables
        #self._msg      # a MIME object stores all the information of email
        print("Start building email...")

        msg = MIMEMultipart()   # create a MIME multipart object
        ### build header
        self.sender = sender
        self.receiver = ";".join(receiver)
        self.title = Header(title, 'utf-8')
        self.ccList = ";".join(ccList)
        msg["From"] = self.sender
        msg["To"] = self.receiver
        msg["Subject"] = self.title
        msg["Cc"] = self.ccList
        ### build body
        if os.path.isfile(body):
            with open(body, 'r') as rf:
                fileContent = rf.readlines()
                self.body = "".join(fileContent)
        else:
            self.body = body
        msgBody = MIMEText(self.body, 'plain', 'utf-8')  # create a MIME text object for email body
        msg.attach(msgBody)
        ### build attachments
        if attachments:
            for attachFile in attachments:
                att = MIMEApplication(open(attachFile, 'rb').read())
                att.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachFile))
                msg.attach(att)
        ### set self._msg
        self._msg = msg
        print("Done")
        return 1

    def send(self):
        '''
        send the built email via SMTP
        '''
        try:
            print("Start sending email...")
            server = smtplib.SMTP(self.mailServer, self.mailPort)
            server.starttls()
            #server.set_debuglevel(1)
            server.login(self.sender, self.mailPassword)
            server.sendmail(self.sender, self.receiver, self._msg.as_string())
            server.quit()
            print("Done")
        except:
            print("Sending is failed")

######### test/example ########
if __name__ == "__main__":
    mailServer = "smtp-mail.outlook.com"
    mailPort = 587
    mailPassword = "cadence123"

    mail = Mymail(mailServer=mailServer, mailPort=mailPort, mailPassword=mailPassword)

    sender = "qianye_cdns@outlook.com"
    #receiver = ["ninipa@163.com", "qianye_cdns@163.com"]  #better to be a list
    #ccList = ["ninipa1985@outlook.com", ]
    receiver = ["ninipa@163.com", ]  #better to be a list
    ccList = ["qianye_cdns@163.com", ]
    title = "python email test 002"
    body = "mail_body.txt"
    #body = "This is a pure text body"
    attachments = ["attachment_001", "attachment_002"]
    #attachments =[]

    mail.build(body=body, sender=sender, receiver=receiver, title=title, ccList=ccList, attachments=attachments)

    mail.send()
