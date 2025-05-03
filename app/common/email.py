#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project -> File   ：kiss-account -> email
@IDE    ：PyCharm
@Author ：sven
@Date   ：2025/5/3 15:31
@Desc   ：
"""
from smtpd import SMTPServer
import smtplib

sender = 'no_reply@mydomain.com'
receivers = ['474416133@otherdomain.com']

message = """From: No Reply <no_reply@mydomain.com>
To: Person <person@otherdomain.com>
Subject: Test Email

This is a test e-mail message.
"""

try:
    smtp_obj = smtplib.SMTP('localhost')
    smtp_obj.sendmail(sender, receivers, message)
    print("Successfully sent email")
except smtplib.SMTPException:
    print("Error: unable to send email")