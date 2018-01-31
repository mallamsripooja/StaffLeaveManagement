import cgi
import sqlite3
import datetime
import os
from http.cookies import *

try:
    global di
    if 'HTTP_COOKIE' in os.environ:
         cookie_string=os.environ.get('HTTP_COOKIE')
         ck=SimpleCookie()
         ck.load(cookie_string)
         if 'username' in cookie_string:
            di=ck['username'].value
         else:
            di="Nil"
    else:
        di="None"
    print("Content-Type:text/html\n\n")
    form=cgi.FieldStorage()
    con=sqlite3.connect("F:\Tom\staffapp.db")
    cur=con.cursor()
    cur.execute('select l.id,l.fdt,l.tdt,l.type from leave_tab l join staff_det s on s.id=l.id where l.approv=4 and l.tdt>="'+str(datetime.date.today())+'" and s.cord='+str(di))
    data=cur.fetchall()
    
    h1='''<html>
<link rel="stylesheet" type="text/css" href="../style-c.css"/><body><form>
<table>
'''
    for i in data:
        cur.execute('select name from staff_det where id='+str(i[0]))
        name=cur.fetchone()
        h2='''<tr><td>'''+str(name[0])+'''  is on  '''+str(i[3])+''' leave from '''+str(i[1])+''' to '''+str(i[2])+'''</td></tr>'''
        h1=h1+h2
    h1=h1+'''</table></form></body></html> '''
    if len(data)==0: 
        h1='''<html><link rel="stylesheet" type="text/css" href="../style-c.css"/><body><p>Nothing to display</p></body></html>'''
    print(h1.format(**locals()))
except Exception as e:
    print(e)
    
