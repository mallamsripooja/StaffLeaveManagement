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

    def insert():
        global dis
        cur.execute('select role from staff_det where id='+str(id))
        role=cur.fetchone()[0]
        approv=0
        if role=="co-ord":
            approv=1
        cur.execute('insert into leave_tab values(?,?,?,?,?,?,?,?,?,?)',(id,dt,'casual',fd,td,approv,reason,0,0,0))
        #cur.execute('delete from storage')
        con.commit()
        ht='''
                <html>
                    <body onload="window.location='http://localhost:8080/test/cgi-bin/form2.py'"></body>
                </html>
            '''
        print(ht)
    cur.execute('select name from staff_det where id='+str(id))
    nm=cur.fetchall()[0][0]
    #print(nm)

    cur.execute('select ldays from staff_det where id='+str(id))
    lrem=cur.fetchall()[0][0]
    cur.execute('select ccl from staff_det where id='+str(id))
    ccl=cur.fetchall()[0][0]
    leave=15+int(ccl)-int(lrem)
    if leave<0:
        leave='NA'
    #print(lrem)

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
                    <td style="font-family:Tahoma;font-size:24px;">Casual Leave</td>
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
            <td><pre><textarea maxlength="100" name="r"   name="r" rows="3" cols="35" placeholder="Enter reason (max. characters = 100)"></textarea>&emsp;</pre></td>
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
         #id1=int(form.getvalue('id',0))
         dt=str(datetime.date.today())
         fd=form.getvalue('fromdt')
         td=form.getvalue('todt')
         reason=str(form.getvalue('r'))
         approv=0
         insert()

except Exception as e:
    html='''
    <html>
        <body onload="window.location='http://localhost:8080/test/cgi-bin/staff_err.py'"></body>
    </html>
    '''
    print(html.format(**locals()))
    print(e)

