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
        msg['From'] = "sever <%s>" % self.email_addr
        msg['Subject'] = "server error"
        server = smtplib.SMTP(self.smtp_server, 25)
        server.set_debuglevel(1)
        server.login(self.email_addr, self.email_passwd)
        server.sendmail(self.email_addr, self.to_email_addr, msg.as_string())
        server.quit()