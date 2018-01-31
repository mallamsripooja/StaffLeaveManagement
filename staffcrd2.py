import cgi
import smtplib
import datetime
import sqlite3
import os
from http.cookies import *

try:
    global cid
    if 'HTTP_COOKIE' in os.environ:
         cookie_string=os.environ.get('HTTP_COOKIE')
         ck=SimpleCookie()
         ck.load(cookie_string)
         if 'username' in cookie_string:
            cid=ck['username'].value
         else:
            cid="Nil"
    else:
        cid="None"
    global lst
    global r
    lst=[]
    #cid=103
    print("Content-Type:text/html\n\n")
    form=cgi.FieldStorage()
    con=sqlite3.connect("F:\Tom\staffapp.db")
    cur=con.cursor()
    def update(n,ap):
        cur.execute('select id from staff_det where name="'+n+'"')
        ba=cur.fetchall()
        temp=ba[0]
        cur.execute('update leave_tab set approv='+ap+' where id='+str(temp[0])+' and approv=0')
        con.commit()
        return
    cur.execute('select l.date from leave_tab l join staff_det s on l.id=s.id where l.approv=0 and s.cord='+str(cid))
    d1=cur.fetchall()
    h1='''
    <html>
        <head><title>Co-ordinater</title>
            <link rel="icon" href="../favicon.ico" type="image/x-icon">
        <table bgcolor="black" width="100%">
           <tr>
             <td><img src="../logo.jpg" width="148" height="130"/></td>
             <td><img src="../clg4.jpg" width="1187" height="130"/></td>
           </tr>
        </table>
        <link rel="stylesheet" type="text/css" href="../style.css"/>
        </head>
    <body>
        <form>
        <table width="100%" bgcolor="lightyellow">
           <tr>
           <td align="left" width="25%" style="font-size:16px;font-family:verdana;font-weight:bold;"><a href="notify2.py" style="text-decoration:none">Get my leave details&emsp;</a></td>
           <td align="right" width="25%" style="font-size:16px;font-family:verdana;font-weight:bold;"><a href="form.py" style="text-decoration:none">Get leave form&emsp;</a></td>
           <td align="right" width="35%" ><a href="stafflogin.py" style="text-decoration:none">
           <input type="button" name="logout" style="font-size:16px;font-family:verdana;font-weight:bold;color:green;border-color:green;background-color:lightyellow;" value="Logout"/></a></td>
           </tr>
        </table><br>
        </form>
        <form>
       <table class="lf2" align="center" width="100%" border="0">
       <caption style="color:purple;"><h2>Leave-Application(s)</h2></caption> 
       <tr>
       <td class="zero" width="25%" align="center"><h4>Name</h4></td>
       <td class="zero" align="center" width="15%"><h4>Date of substitution</h4></td>
       <td class="zero" align="center" width="20%"><h4>Substitution Name</h4></td>
       <td class="zero" align="center" width="8%"><h4>period</h4></td>
       <td class="zero" align="center" width="12%"><h4>class</h4></td>
       <td class="zero" align="center" width="30%"><h4>Reason</h4></td>
       <td class="zero" align="center" width="30%"><h4>Approval</h4></td>
       <td class="zero" align="center" width="15%"><h4>Opinion</h4></td>
       </tr>
    '''
    dt=[]
    for i in d1:
        dt.append(i[0])
    dt=list(set(dt))
    for i in dt:
        m=i.split('-')
        o=m[2]+'-'+m[1]+'-'+m[0]
        h2='''
      <tr align="center"><td class="three" width="20%"><h4>'''+o+'''</h4></td></tr>
      '''
        t=[]
        cur.execute('select l.id,l.reason,l.fdt,l.tdt,l.type from leave_tab l join staff_det sd on l.id=sd.id where date="'+str(i)+'"'+" and approv=0 and sd.cord="+str(cid))
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
            c=b-a
            day=int(c.days)+1
            p=d3[0]
            cur.execute('select ldays from staff_det where id='+str(k[0]))
            ld=cur.fetchall()
            ld1=ld[0]
            h3='''
            <tr>
            <td class="one"><b><i><c style="color:blue;" title='''+p[0]+'''>'''+p[0]+'''</i></b></c><br>&nbsp;
            <br><b>Type of leave:</b>'''+k[4].capitalize()+'''</br></c>&nbsp;
            <br><b>From date:</b>'''+k[2].capitalize()+'''</br>&nbsp;
            <br><b>To date:</b>'''+k[3].capitalize()+'''</br>&nbsp;
            <br><b>No.of days:</b>'''+str(day)+'''</br>&nbsp;
            <br><b>Leaves taken:</b>'''+str(ld1[0])+'''</br></td>'''
            cur.execute('select date from leave_sub where id='+str(k[0])+' and approv=0')
            datesub=cur.fetchall()
            if len(datesub)==0:
                h4='''
                    <td class="two" align="center">---</td>
                    <td class="one" align="center">---</td>
                    <td class="two" align="center">---</td>
                    <td class="one" align="center">---</td>
                   '''
            else:
                datesub=list(set(datesub))
                h4=''
                ln=[]
                lc=[]
                lp=[]
                h4='<td align="center"  class="two">'
                datesub.sort()
                for ele1 in datesub:
                    h4=h4+'<br>'+ele1[0]+'<br><br><br><br>'
                    cur.execute('select s,sc,period from leave_sub where id='+str(k[0])+' and date="'+str(ele1[0])+'"')
                    details=cur.fetchall()
                    for q in range(len(details)):
                        ln.append(details[q][0])
                        lc.append(details[q][1])
                        lp.append(details[q][2])
                h4=h4+'</td>'
                h5='<td align="center"  class="one">'
                for ele1 in ln:
                    h5=h5+'<br>'+ele1+'<br>'
                h5=h5+'</td>'
                h6='<td align="center"  class="two">'
                for ele1 in lp:
                    h6=h6+'<br>'+ele1+'<br>'
                h6=h6+'</td>'
                h7='<td align="center"  class="one">'
                for ele1 in lc:
                    h7=h7+'<br>'+ele1+'<br>'
                h7=h7+'</td>'
                h4=h4+h5+h6+h7
                
                        
            
            h5='''<td class="two" align="center">'''+k[1].capitalize()+'''</td>&nbsp;
            <td class="one"><input type="radio" name='''+p[0]+''' required value=1 />Yes<br><br>
            <input type="radio" name='''+p[0]+''' value=-1 />No</td>
            <td class="two" align="center">
            <textarea rows=5 cols=30 name='''+str(k[0])+''' required title="Enter the reason for rejection"></textarea>
            </td>
            </tr>
            '''
            h3=h3+h4+h5
            h2=h2+h3
            lst.append(p[0])
        h1=h1+h2
    h6='''<tr  height="50"><td align="right"><input type="submit" value="submit" name="submit"/></td></tr></table></form>
            </body>
      <footer>
            <table style="width:100%;" align="center">
                <tr>
                    <td style="width:33%;text-align:center;">3-5-1026, Narayanguda, Hyderabad, Telangana -500029</td>
                    <td style="width:33%;text-align:center;">Copyright &#169; KMIT</td>
                    <td style="width:33%;text-align:center;">Website:    <a href="http://www.kmit.in/" style="text-decoration:none"/>kmit.in</td>
                </tr>
            </table>
        </footer>
       </html>
'''
    ht=h1+h6
    global val
    val=[]
    for i in range(len(lst)):
        q=form.getvalue(lst[i])
        val.append(q)
    con.commit()
    htemp=''    
    if "submit" in form:
        for i in range(len(lst)):
            cur.execute('select id from staff_det where name="'+lst[i]+'"')
            rin=cur.fetchall()
            rin1=rin[0]

            r=str(form.getvalue(str(rin1[0])))
            #print(r)
            cur.execute('update leave_tab set cr="'+str(r)+'" where id='+str(rin1[0])+' and approv=0')
            update(lst[i],val[i])
            con.commit()
            #print('\n',r)
            msg=r
            #print(msg)

            cur.execute('select email from staff_det where id=102')
            em=cur.fetchall()
            e=em[0]
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login("kmitleaveapp@gmail.com","kmit@2015")
            server.sendmail("kmitleaveapp@gmail.com",e[0], msg)
            server.quit()
        htemp='''
<html>
  <body onload="window.location='staffcrd2.py'">
    
  </body>
</html>
'''
    print(ht.format(**locals()))
    print(htemp)      
    
except Exception as e:
    print(e)