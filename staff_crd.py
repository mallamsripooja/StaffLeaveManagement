import cgi
import datetime
import sqlite3
import smtplib
import nsm2
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
    lst=[]
    #di=102
    print("Content-Type:text/html\n\n")
    form=cgi.FieldStorage()
    con=sqlite3.connect("F:\Tom\staffapp.db")
    cur=con.cursor()
    def update(n,ap):
        cur.execute('select id from staff_det where name="'+n+'"')
        ba=cur.fetchall()
        temp=ba[0]
        cur.execute('update leave_tab set approv='+ap+' where id='+str(temp[0])+' and approv=0')
        cur.execute('update leave_sub set approv='+ap+' where id='+str(temp[0])+' and approv=0')
        con.commit()
        return 
    cur.execute('select l.date from leave_tab l join staff_det s on l.id=s.id where l.approv=0 and s.cord='+str(di)+' order by date desc')
    #cur.execute('select l.date from leave_tab l join staff_det s on l.id=s.id where l.approv=0 order by date desc')
    d1=cur.fetchall()
    #print(d1)
    h1='''
<html>
<body>
<form> <link rel="stylesheet" type="text/css" href="../style-c.css"/><h2 align="center">Leave application(s)</h2>'''

    dt=[]
    for i in d1:
        dt.append(i[0])
    dt=(list(set(dt)))
    for i in dt:
        m=i.split('-')
        o=m[2]+'-'+m[1]+'-'+m[0]
        h2=''
        t=[]
        
        cur.execute('select l.id,l.reason,l.fdt,l.tdt,l.type from leave_tab l join staff_det sd on l.id=sd.id where date="'+str(i)+'"'+" and approv=0 and sd.cord="+str(di))
        #cur.execute('select l.id,l.reason,l.fdt,l.tdt,l.type from leave_tab l join staff_det sd on l.id=sd.id where date="'+str(i)+'" and approv=0')
        temp=cur.fetchall()

        for j in temp:
            t.append(j)
        for k in t:
            cur.execute('select name from staff_det where id='+str(k[0]))
            d3=cur.fetchall()
            h=k[2].split('-')
            g=k[3].split('-')
            a=datetime.date(int(h[0]),int(h[1]),int(h[2]))
            b=datetime.date(int(g[0]),int(g[1]),int(g[2]))
            #c=b-a
            #day=int(c.days)+1
           # removed days
            p=d3[0]
            cur.execute('select ldays,ccl from staff_det where id='+str(k[0]))
            ld=cur.fetchall()
            ld1=ld[0]
            h3='''<table class="lf1" width="100%" border="0"><tr><td colspan=4><table border="0" width="50%"><tr><td><b>Applied date: </b></td><td>'''+o+'''</td></tr>
            <tr><td><b>Name:</b></td><td style="color: blue;" colspan=2><b><i>'''+p[0]+'''</i></b></tr>
            <tr><td><b>Leaves  : </b>'''+str(ld1[0])+' of '+' 15 </td><td>'+'''<b>CCl(s) : </b> '''+str(ld1[1])+'''</td></tr>
            <tr><td width="50%"><b>Type of leave: </b></td><td style="color: orangered;">'''+k[4].upper()+'''</td></tr></c>&nbsp;
            <tr><td width="50%"><b>Reason: </b></td><td>'''+k[1].capitalize()+'''</td></tr>
            <tr><td width="60%"><b>From : </b>'''+k[2].capitalize()+'''</td>&ensp;&ensp;
            <td width="60%"><b>To : </b>'''+k[3].capitalize()+'''</td></tr>&nbsp;</table></td>
            <td>
            <object data="../'''+str(k[0])+'''.JPG" class="profile" height=130 width=130>
            <img src="../100.JPG" alt="No image" class="profile" height=130 width=130></object></td></tr>
            '''
            cur.execute('select date,s,sc,period from leave_sub where id='+str(k[0])+' and approv=0 order by date')
            datesub=cur.fetchall()
            htest='''<tr><td><table border="0" width="100%"><caption><b>Substitutions</b></caption><tr>
            <td align="center"><b>Date</b></td>
            <td align="center"><b>Name</b></td>
            <td align="center"><b>Class</b></td>
            <td align="center"><b>Period</b></td>
            </tr>'''
            h4=''
            for sub1 in datesub:
                hh='''
                <tr><td align="center">'''+str(sub1[0])+'''</td>
                <td align="center">'''+str(sub1[1])+'''</td>
                <td align="center">'''+str(sub1[2])+'''</td>
                <td align="center">'''+str(sub1[3])+'''</td></tr>'''
                h4=h4+hh

            h5='''<tr><td  colspan=4><table width="100%" border="0"><tr><td><b>Approval</b></td><td><input type="radio" name="'''+p[0]+'''"  value=1 />Yes
            <input type="radio" name="'''+p[0]+'''" required value=-1 />No</td></tr>
            <tr><td><b>Remarks</b></td>
            <td><textarea rows=1 cols=30 maxlength=60 name='''+str(k[0])+''' title="Enter the reason for rejection">Leave Granted</textarea>
            </td></tr></table></table></td></tr><br><br></table><br>
            '''
            
            h3=h3+htest+h4+h5
            h2=h2+h3
            lst.append(p[0])
        h1=h1+h2
    cur.execute('select * from leave_tab l join staff_det s on l.id=s.id where l.approv=0 and s.cord='+str(di))
    ap=cur.fetchall()

    if len(ap)==0:
        h1='''<html>
<link rel="stylesheet" type="text/css" href="../style-c.css"/><body><p>There are no leave application(s)</p></body></html>'''
        print(h1.format(**locals()))
    else:
        h1=h1+'''<br><input type="submit" value="submit" name="submit"/></form></body></html>'''
        print(h1.format(**locals()))
       
        global val
        val=[]
        for i in range(len(lst)):
            q=form.getvalue(lst[i])
           # if(q==None):
            #    q='0'
            val.append(q)
        #print(val)
        con.commit()
        htemp=''   
        if "submit" in form:
            for i in range(len(lst)):
                cur.execute('select id from staff_det where name="'+lst[i]+'"')
                rin=cur.fetchall()
                rin1=rin[0]
                r=form.getvalue(str(rin1[0]))
                cur.execute('update leave_tab set cr="'+str(r)+'" where id='+str(rin1[0])+' and approv=0')
                update(lst[i],val[i])
                con.commit()
                SUBJECT='Leave response'
                msg = 'Subject: %s\n\nDear Applicant,\n\n%s\n\nRegards,\nKMIT.' % (SUBJECT, r)
                cur.execute('select email from staff_det where id='+str(rin1[0]))
                em=cur.fetchall()
                e=em[0]
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login("kmitleaveapp@gmail.com","kmit@2015")
                server.sendmail("kmitleaveapp@gmail.com",e[0], msg)
                server.quit()
            htemp='''
<html>
  <body onload="window.location='staff_crd.py'">
  </body>
</html>
'''
    
        #print(h1.format(**locals()))
        print(htemp)
    #print(di)      
    

except Exception as e:
    print(e)
