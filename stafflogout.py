import cgi
import os
from http.cookies import *
import sqlite3
try:
    form=cgi.FieldStorage()
    print("Content-Type:text/html\n\n")
    con=sqlite3.connect("F:\Tom\staffapp.db")
    cur=con.cursor()
    if 'HTTP_COOKIE' in os.environ:
         cookie_string=os.environ.get('HTTP_COOKIE')
         ck=SimpleCookie()
         ck.load(cookie_string)
         if 'username' in cookie_string:
            id=ck['username'].value
            ck['username']=1
            print(ck.js_output());
         else:
            id="Nil"
    else:
        id="None"
    ht='''
                <html>
                    <body onload="window.location='http://localhost:8080/test/cgi-bin/stafflogin.py'"></body>
                </html>
            '''
    print(ht.format(**locals()))
except Exception as err:
    print(err)