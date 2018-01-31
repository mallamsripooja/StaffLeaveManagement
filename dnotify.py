import cgi
import sqlite3
import datetime
try:
    print("Content-Type:text/html\n\n")
    form=cgi.FieldStorage()
    con=sqlite3.connect("F:\Tom\staffapp.db")
    cur=con.cursor()
    cur.execute('select id,fdt,tdt,type from leave_tab where approv=4 and tdt>="'+str(datetime.date.today())+'"')
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
        h1='''<html>
<link rel="stylesheet" type="text/css" href="../style-c.css"/><body><p>Nothing to display</p></body></html>'''
    print(h1.format(**locals()))
except Exception as e:
    print(e)
    
