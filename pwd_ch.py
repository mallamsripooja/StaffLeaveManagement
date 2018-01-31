import cgi
import math
import sqlite3
import datetime
import os
import calendar
from http.cookies import *
from datetime import timedelta, date
try:
    global con
    global cur
    con=sqlite3.connect("F:\Tom\staffapp.db")
    cur=con.cursor()
    if 'HTTP_COOKIE' in os.environ:
         cookie_string=os.environ.get('HTTP_COOKIE')
         ck=SimpleCookie()
         ck.load(cookie_string)
         if 'username' in cookie_string:
            id=ck['username'].value
         else:
            id="Nil"
    else:
        id="None"

    form=cgi.FieldStorage()
    print("Content-Type:text/html\n\n")
    no_match=''
    if "sub" in form:
        new=form.getvalue('new')
        renew=form.getvalue('renew')
        if new==renew:
            cur.execute('update login_tab set pwd="'+str(renew)+'" where id='+str(id))
            con.commit()
            html='''
                    <html>
                        <body onload="window.location='http://localhost:8080/test/cgi-bin/form.py'"></body>
                    </html>'''
            print(html.format(**locals()))
        else:
            no_match='Password does not match !'
    ht1='''
                    <html>
                     <head>
            <link rel="icon" href="../favicon.ico" type="image/x-icon">
                        <link rel="stylesheet" type="text/css" href="../style.css" />
                        <title>Change Password</title>
                        <table width="100%" bgcolor="black">
                         <tr>
                            <td width="10%"><img src="../logo.jpg" alt="img" height="130" width="148" ></td>
                            <td width="90%"><img src="../clg4.jpg" alt="img" height="130" width="1170" ></td>
                        </tr>
                     </table>
                     </head>
                     <body><br><br>
            <table align="center" height=55>
                <tr>
                    <td style="font-family:Tahoma;font-size:24px;">Change Password</td>
                </tr></table><br><br>
                <form method=POST>
            <table align="center" class="lf1">
                <tr>
                    <td>&emsp;<b>Id</b></td><td>'''+str(id)+'''&emsp;</td>
                </tr>
                <tr>
                    <td>&emsp;<b>New password</b></td><td><input type="password" name="new" autofocus>&emsp;</td>
                </tr>
                <tr>
                    <td>&emsp;<b>Confirm password</b>&emsp;</td><td><input type="password" name="renew">&emsp;</td>
                </tr>
                <tr>
                    <td colspan=2 align="center" style="color : red;">{no_match}</td>
                </tr>
                <tr>
                    <td colspan=2 align="center"><input type="submit" name="sub" value="Submit"></td>
                </tr>
            </table>
            </form>
            </body><br><br><br><br><br><br><br>
      <footer>
            <table style="width:100%;" align="center">
                <tr>
                    <td style="width:33%;text-align:center;font-size:18px;">3-5-1026, Narayanguda, Hyderabad, Telangana -500029</td>
                    <td style="width:33%;text-align:center;font-size:18px;">&emsp;&emsp;&emsp;Copyright &#169; KMIT</td>
                    <td style="width:33%;text-align:center;font-size:18px;">&emsp;&emsp;&emsp;Website:    <a href="http://www.kmit.in/" style="text-decoration:none"/>kmit.in</td>
                </tr>
            </table>
        </footer>
    </html>'''
    print(ht1.format(**locals()))

except Exception as err:
    html='''
    <html>
        <body onload="window.location='http://localhost:8080/test/cgi-bin/staff_err.py'"></body>
    </html>
    '''
    print(html.format(**locals()))
    print(err)