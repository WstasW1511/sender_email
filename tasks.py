# -*- coding: utf-8 -*-
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from celery import Celery
from configparser import ConfigParser


app = Celery('send', backend='redis://localhost', broker='redis://localhost:6379/0')

def send_email(add_to,subject,body_massage):
    msg = MIMEMultipart()
    try:
        config = ConfigParser()
        config.read('./config.ini')
        config = config._sections
        addr_from = config['system']['from']
        password = config['system']['password']
        host_name_server = config['system']['host_name_server']
        port = config['system']['port']

        msg['To'] = add_to
        msg['Subject'] = subject
        msg['From'] = addr_from
        msg.add_header("Disposition-Notification-To", "1")
        msg.add_header('Return-Receipt-To', addr_from)
        body = body_massage
        if body != '':
            msg.attach(MIMEText(body, 'plain'))
        try:
            ff = open('./templates/email_template.html','r')
            i = ff.read()
            x=i[i.find('<img')+9:i.find('" style')+1]
            html=i.replace(x,'"cid:image1"')
            msg.attach(MIMEText(html, 'html'))
            ff.close()
            f=open('./static/images/1.jpeg', 'rb')
            msgImage = MIMEImage(f.read())
            f.close()
            msgImage.add_header('Content-ID', '<image1>')
            msg.attach(msgImage)
        except Exception as e:
            print (e)
        text = msg.as_string()
        server = smtplib.SMTP(str(host_name_server),int(port))
        server.starttls()
        server.login(addr_from, password)
        server.sendmail(addr_from,add_to,text)
        server.quit()
    except Exception as e:
        print(e)


@app.task
def send_email_task(add_to,subject,body_massage):
    send_email(add_to, subject, body_massage)
    return
