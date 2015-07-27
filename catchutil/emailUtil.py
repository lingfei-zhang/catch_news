# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText


class EmailUtil(object):
    email_addr = ""
    email_passwd = ""
    to_email_addr = ""
    smtp_server = ""

    def send_mail(self, msg):
        msg = MIMEText(msg, 'plain', 'utf-8')
        server = smtplib.SMTP(smtp_server, 25)
        server.login(email_addr, email_passwd)
        server.sendmail(email_addr, to_email_addr, msg.as_string())
        server.quit()
    pass