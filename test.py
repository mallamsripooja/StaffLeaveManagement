import os,sys
import cgi
import sqlite3
import matplotlib.pyplot as plt
form = cgi.FieldStorage()
con=sqlite3.connect("F:\Tom\staffapp.db")
cur=con.cursor()
form=cgi.FieldStorage()
cur.execute('select ldays,ccl,dept from staff_det')
c=cur.fetchall()
dep=['H&S','CSE','ECE','IT','EIE']
labels=dep
hs=[]
cse=[]
ece=[]
it=[]
eie=[]
t1=0
for c1 in c:
      t1=c1[0]-c1[1]
      if(t1!=0):
            if(c1[2]==dep[0]):
                  hs.append(t1)
            elif(c1[2]==dep[1]):
                  cse.append(t1)
            elif(c1[2]==dep[2]):
                  ece.append(t1)
            elif(c1[2]==dep[3]):
                  it.append(t1)
            else:
                  eie.append(t1)
slices=[sum(hs),sum(cse),sum(ece),sum(it),sum(eie)]
colors=['#FE4400','#FF642B','#FF7441','#FF7D4D','#FFA382']
plt.title('Leaves taken by each department',fontsize=16)
plt.pie(slices,labels=labels,colors=colors,startangle=-20,shadow=True,autopct='%.2f%%')
plt.legend(loc='upper left')
plt.axis("equal")
plt.savefig( "../../pieDiag.png")# width="700" height="500"
print("Content-Type: text/html\n")
ht='''<html><body><div style="width:580px;height:580px;overflow:hidden;" >
   <img src="../pieDiag.png" width="580px" height="auto">
</div></body></html>'''
print(ht.format(**locals()))
