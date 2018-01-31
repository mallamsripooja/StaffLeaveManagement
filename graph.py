import cgi
import os,sys
import cgi
import sqlite3
from http.cookies import *

import matplotlib.pyplot as plt
import numpy as np

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
        
form = cgi.FieldStorage()
con=sqlite3.connect("F:\Tom\staffapp.db")
cur=con.cursor()

cur.execute('select dept from staff_det where id='+str(id))
dept=cur.fetchone()[0]
cur.execute('select ldays,ccl,id from staff_det where dept="'+dept+'"')
lst=cur.fetchall()
leaves=[]
colors=[]
Id=[]
for l1 in lst:
    leaves.append(int(l1[0])-int(l1[1]))
    Id.append(l1[2])
for i in leaves:
    if i>=15:
        colors.append('#FE4400')
    elif i>10 and i<15:
        colors.append('#FF7441')
    elif i>0 and i<=10:
        colors.append('#FFA382')
#print(colors)        
xcount=np.arange(len(leaves))
plt.title('Leaves taken by different faculty members\n',fontsize=18,color='green')
plt.bar(xcount,leaves,width=.3,alpha=0.9,align="center",color=colors)
plt.xlabel("Id of the faculty member",color="blue",fontsize=14)
plt.ylabel("\nTotal number of leaves taken",color="blue",fontsize=14)
plt.xticks(xcount,Id)
plt.savefig("../../barGraph.png")
print("Content-Type: text/html\n")
ht='''<html><body><div style="width:580px;height:580px;overflow:hidden;" >
   <img src="../barGraph.png" width="580px" height="auto">
</div></body></html>'''
print(ht.format(**locals()))

