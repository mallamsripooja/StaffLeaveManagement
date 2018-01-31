import cgi
import datetime
import os
from http.cookies import *
import sqlite3
try:
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
    con=sqlite3.connect("F:\Tom\staffapp.db")
    cur=con.cursor()
    cur.execute('select * from leave_tab where id='+str(id)+' and approv=3 or approv=4 and not type="maternity"')
    data=cur.fetchall()
    cur.execute('select name from staff_det where id='+str(id))
    nm=cur.fetchall()[0][0]
    hh='''
       <html>
       <head>
            <link rel="icon" href="../favicon.ico" type="image/x-icon">
       <table bgcolor="black" width="100%">
           <tr>
             <td><img src="../logo.jpg" width="148" height="130"/></td>
             <td><img src="../clg4.jpg" width="1187" height="130"/></td>
           </tr>
        </table>
        <link rel="stylesheet" type="text/css" href="../style.css"/>
       <title>Leave History</title>
       </head>
       <body>
            <table width="100%" class="top">
            <tr>
           <td>&emsp;Hi, '''+str(nm)+'''<td>
           <td align="right"><a href="stafflogin.py">Logout</a>&emsp;</td></td>
            </tr>
            </table><br>
            <table align="center" height=50>
                <tr>
                    <td style="font-family:Tahoma;font-size:24px;">Leave History</td>
                </tr>
            </table><br>
       <form>
       <table class="lf1" align="center" border="0">
         <tr><b>
           <td align="center">&emsp;Appplied Date&emsp;</td>
           <td align="center">&emsp;Type&emsp;</td>
           <td align="center">&emsp;&emsp;From&emsp;&emsp;</td>
           <td align="center">&emsp;&emsp;&emsp;To&emsp;&emsp;&emsp;</td>
           <td align="center">&emsp;No. of days&emsp;</td>
           <td align="center">&emsp;Reason&emsp;</td>
           </b>
           </tr>       
'''
    #print(data)
    for i in data:
        k=i[1].split('-')
        h=i[3].split('-')
        g=i[4].split('-')
        cpy=i[-1]
        if i[2]=='onduty':
            cpy=1
        h1='''
        <tr>
           <td align="center" class="one">'''+str(k[2])+'-'+str(k[1])+'-'+str(k[0])+'''</td>
           <td align="center" class="two">'''+str(i[2]).capitalize()+'''</td>
           <td align="center" class="one">'''+str(h[2])+'-'+str(h[1])+'-'+str(h[0])+'''</td>
           <td align="center" class="two">'''+str(g[2])+'-'+str(g[1])+'-'+str(g[0])+'''</td>
           <td align="center" class="one">'''+str(cpy)+'''</td>
           <td align="center" class="two">'''+str(i[6]).capitalize()+'''</td>
        </tr>
'''
        hh=hh+h1

    
    cur.execute('select ldays from staff_det where id='+str(id))
    f=cur.fetchall()
    cur.execute('select ccl from staff_det where id='+str(id))
    ccl=cur.fetchall()[0][0]
    f1=f[0]
    ht='''
    <tr>
        <td align="center" colspan=6 style="font-size: 18px;font-family : tahoma;">Total leaves taken&emsp;-&emsp;'''+str(f1[0])+'''</td>
    </tr>'''
    if f1[0]>15:
        ht7='''
          <tr>
             <td style="color:red;" align="center" colspan=6><b>You have already taken   '''+str(f1[0]-15-ccl)+''' unpaid leaves</b></td>
          </tr>'''
        ht=ht+ht7
        
    hy='''</table>
    </form>
    </body>
    </html>
'''
    hf=hh+ht+hy
    print(hf.format(**locals()))

except Exception as e:
    print(e)

