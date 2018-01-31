import cgi
import sqlite3
import datetime
import os
from http.cookies import *
from datetime import timedelta, date
#http://localhost:8080/test/cgi-bin/form.py
try:
    global con
    global cur
    con=sqlite3.connect("F:\Tom\staffapp.db")
    cur=con.cursor()
    global ht1
    global ht3
    global id
    global id1
    global type
    global dt
    global fd
    global td
    global approv
    global reason
    fd=''
    td=''

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

    def daterange(start_date, end_date):
        for n in range(int ((end_date - start_date).days)):
            yield start_date + timedelta(n)

    
    cur.execute('select name from staff_det where id='+str(id))
    nm=cur.fetchall()[0][0]
    #print(nm)

    cur.execute('select ldays from staff_det where id='+str(id))
    lrem=cur.fetchall()[0][0]
    cur.execute('select ccl from staff_det where id='+str(id))
    ccl=cur.fetchall()[0][0]
    #print(lrem)
    leave=15+int(ccl)-int(lrem)
    if leave<0:
        leave='NA'

    ht1='''
                    <html>
                     <head>
            <link rel="icon" href="../favicon.ico" type="image/x-icon">
                        <link rel="stylesheet" type="text/css" href="../style.css" />
                        <title>Leave Form</title>
                        <table width="100%" bgcolor="black">
                         <tr>
                            <td width="10%"><img src="../logo.jpg" alt="img" height="130" width="148" ></td>
                            <td width="90%"><img src="../clg4.jpg" alt="img" height="130" width="1170" ></td>
                        </tr>
                     </table>
                     </head>
                     <body>
                     <table width="100%" class="top">
           <tr>
           <td>
           <td align="center">
            <object data="../'''+str(id)+'''.JPG" class="profile">
            <img src="../100.JPG" alt="No image" class="profile"></object>
           </td>
           <td>'''+str(nm)+'''&emsp;|&emsp;
           Leave(s) remaining - '''+str(leave)+'''</td>
           <td align="right">&emsp;
           <a href="notify2.py">Leave History&emsp;</a>|&emsp;
           <a href="pwd_ch.py">Change Password&emsp;</a>|&emsp;
           <a href="stafflogin.py">Logout</a>&emsp;</td>
           </tr>
                     </table>
                     <div class="tpmenu">
                        <ul>
                            <li>
                            <a href="staff_al.py">AL</a>&emsp;
                            <a href="staff_ccl.py">CCL</a>&emsp;
                            <a href="form.py">CL</a>&emsp;
                            <a href="staff_half.py">HDL</a>&emsp;
                            <a href="staff_mat.py">ML</a>&emsp;
                            <a href="staff_od.py">OD</a>&emsp;
                            </li>
                        </ul>
                     <div>
            <table align="center" height=55>
                <tr>
                    <td style="font-family:Tahoma;font-size:24px;">Academic Leave</td>
                </tr>
            </table>
                     <form method="POST">
                     <table  align="Center" class="lf1">
                     <tr>
                       <td><b>&nbsp;Id</b></td>
                       <td>{id}</td>
                     </tr>
                     <tr>
                       <td><b>&nbsp;Date</b></td>
                        <td>From&nbsp;<input type="date" name="fromdt"  name="fromdt"
                        required name="fromdt" placeholder="From date" min="'''+str(datetime.date.today())+'''"/></td>
                     </tr>
                         <td></td>
                         <td>To&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input type="date" name="todt"
                         required name="todt" name="todt" placeholder="To date"  min="'''+str(datetime.date.today())+'''"/></td>
                     <tr>
            <td><b>&nbsp;Reason</b></td>
            <td><pre><textarea maxlength="100" name="r"   required rows="3" cols="35" placeholder="Enter reason (max. characters = 100)"></textarea>&emsp;</pre></td>
        </tr>
        <tr><td>&nbsp;
        I confirm the details&nbsp;</td><td><input type="checkbox" name="agree" required name="agree">Yes
        </td></tr>
        <tr><td></td><td>&nbsp;<input style="font-size:15px;" type="submit" name="submit" value="Get Substitution Form" /></td></tr>
    </table>
        </form>
        </body><br><br><br>
      <footer>
            <table style="width:100%;" align="center">
                <tr>
                    <td style="width:33%;text-align:center;font-size:18px;">3-5-1026, Narayanguda, Hyderabad, Telangana -500029</td>
                    <td style="width:33%;text-align:center;font-size:18px;">&emsp;&emsp;&emsp;Copyright &#169; KMIT</td>
                    <td style="width:33%;text-align:center;font-size:18px;">&emsp;&emsp;&emsp;Website:    <a href="http://www.kmit.in/" style="text-decoration:none"/>kmit.in</td>
                </tr>
            </table>
        </footer>
    </html>
    '''
    
    print(ht1.format(**locals()))
    
    if "submit" in form:
        cur.execute('select role from staff_det where id='+str(id))
        role=cur.fetchone()[0]
        approv=0
        if role=="co-ord":
            approv=1
        f=form.getvalue('fromdt').split('-')
        t=form.getvalue('todt').split('-')
        fd=datetime.date(int(f[0]),int(f[1]),int(f[2]))
        td=datetime.date(int(t[0]),int(t[1]),int(t[2]))
        cur.execute('select fdt,tdt from leave_tab where id='+str(id)+' and type="academic" and approv>2 order by fdt')
        data=cur.fetchall() 
        day1=0
        if len(data)!=0:
            f1=data[-1][0].split('-')
            t1=data[-1][1].split('-')
            fd1=datetime.date(int(f1[0]),int(f1[1]),int(f1[2]))
            td1=datetime.date(int(t1[0]),int(t1[1]),int(t1[2]))
            #print(data)
            q1=fd1
            while(q1<=td1):          #made changes regarding sunday
                if(q1.isoweekday()==7):
                    day1=day1+1
                q1=q1+datetime.timedelta(1)
            if fd.month==td.month:
                if (fd.month!=fd1.month and fd.month!=td1.month):
                    ndays=(td-fd).days-day1
                else:
                    ndays=(td-fd).days+1-day1
            else:
                if fd.month!=fd1.month and fd.month!=td1.month:
                    ndays=(td-fd).days-1-day1
                else:
                    ndays=(td-fd).days-day1
        else:
            q1=fd
            while(q1<=td):          #made changes regarding sunday
                if(q1.isoweekday()==7):
                    day1=day1+1
                q1=q1+datetime.timedelta(1)
            if td.month==fd.month:
                ndays=(td-fd).days-day1
            else:
                ndays=(td-fd).days-1-day1

        cur.execute('insert into leave_tab values(?,?,?,?,?,?,?,?,?,?)',(str(id),str(datetime.date.today()),'academic',str(form.getvalue('fromdt')),str(form.getvalue('todt')),approv,str(form.getvalue('r')),0,0,ndays))
        con.commit()
        ht='''
                <html>
                    <body onload="window.location='http://localhost:8080/test/cgi-bin/form2.py'"></body>
                </html>
            '''
        print(ht)

except Exception as e:
    html='''
    <html>
        <body onload="window.location='http://localhost:8080/test/cgi-bin/staff_err.py'"></body>
    </html>
    '''
    #print(html.format(**locals()))
    print(e)

