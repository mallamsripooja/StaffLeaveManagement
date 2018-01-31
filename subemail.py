#!/usr/bin/env python3
import smtplib
try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    reason='Heavy schedule'
    TEXT = "Your leave application is approved by co-ordinator.\nReason:"+reason
    SUBJECT='Leave response'
    msg = 'Subject: %s\n\nDear Manu,\n\n%s\n\nRegards,\nKMIT.' % (SUBJECT, TEXT)
    server.starttls()
    server.login("kmitleaveapp@gmail.com","kmit@2015")
    server.sendmail("kmitleaveapp@gmail.com","bhanu.chikku@gmail.com", msg)
    server.quit()
except Exception as e:
    print(e)
