import cgi
import sqlite3
import datetime
import os
from http.cookies import *
try:
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
    print("Content-Type:text/html\n\n")
    form=cgi.FieldStorage()
    cur.execute('select name from staff_det where id='+str(id))
    nm=cur.fetchall()[0][0]
    #print(nm)

    cur.execute('select ldays from staff_det where id='+str(id))
    lrem=cur.fetchall()[0][0]
    cur.execute('select ccl from staff_det where id='+str(id))
    ccl=cur.fetchall()[0][0]
    #print(lrem)
    h1='''
<html>
        <head>
            <link rel="icon" href="../favicon.ico" type="image/x-icon">
        <link rel="stylesheet" type="text/css" href="../style-c.css"/>
        <link rel="stylesheet" type="text/css" href="../style.css"/><title>Co-ord</title>
        <table bgcolor="black">
           <tr>
             <td><img src="../logo.jpg" width="148" height="130"/></td>
             <td><img src="../clg4.jpg" width="1170" height="130"/></td>
           </tr>
        </table>
     
  </head>
 



    <body>
        <form method="POST">
           <table width="100%" class="top">
           <tr>
           <td>
           <td align="center">
            <object data="../'''+str(id)+'''.JPG" class="profile">
            <img src="../100.JPG" alt="No image" class="profile"></object>
           </td>
           <td>'''+str(nm)+'''&emsp;|&emsp;
           Leave(s) remaining - '''+str(15+int(ccl)-int(lrem))+'''</td>
           <td align="right">&emsp;
           <a href="notify2.py">Leave History&emsp;</a>|&emsp;
           <a href="stafflogin.py">Logout</a>&emsp;</td>
           </tr>
           </table>

        <div id="opt1" class="tpmenu">
        <br><br><a href="staff_crd.py" target="iframe">Leave Application(s)</a>
        <br><br><a href="crecord.py" target="iframe">Leave Reports</a>
        <br><br><a href="cnotify.py" target="iframe">Notification(s)</a>
        <br><br><a href="form.py" >Leave Form</a>

        </div>

        <div id="opt2">
        <iframe src="staff_crd.py" width=100% height=100% name="iframe" frameborder=none>
        
        </iframe>
        </div>
        </form>
      
        
        </body>
    </html>'''

    print(h1.format(**locals()))
except Exception as e:
    print(e)
