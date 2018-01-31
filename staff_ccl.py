import cgi
import math
import sqlite3
import datetime
import os
import calendar
from http.cookies import *
from datetime import timedelta, date
try:
    global con
    global cur
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

    form=cgi.FieldStorage()
    print("Content-Type:text/html\n\n")
    cur.execute('select name from staff_det where id='+str(id))
    nm=cur.fetchall()[0][0]
    cur.execute('select ldays from staff_det where id='+str(id))
    lrem=cur.fetchall()[0][0]
    cur.execute('select ccl from staff_det where id='+str(id))
    ccl=cur.fetchall()[0][0]
    leave=15+int(ccl)-int(lrem)
    if leave<0:
        leave='NA'
    #arrow heads - &#10095;&#10095;&emsp;
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
                    <td style="font-family:Tahoma;font-size:24px;">Compensate Casual Leave</td>
                </tr></table>'''
    ht2='''<form method="POST">
                     <table  align="Center" class="lf1" width="23%" border=0>
                     <tr>
                       <td><b>&nbsp;Id</b></td>
                       <td>{id}</td>
                     </tr>
                     <tr>
                       <td><b>&nbsp;From Date&emsp;</b></td>
                        <td><input type="date" name="fromdt"
                        required max="'''+str(datetime.date.today())+'''"/></td>
                     </tr>
                     <tr>
                       <td><b>&nbsp;To Date&emsp;</b></td>
                        <td><input type="date" name="todt"
                        required max="'''+str(datetime.date.today())+'''"/></td>
                     </tr>
                     <tr>
                       <td><b>&nbsp;Work done&emsp;</b></td>
                        <td>
                            <textarea cols=20 rows=5 required name="reason" placeholder="Enter work done" maxlength=100></textarea>
                        </td>
                     </tr>
        <tr><td colspan=2 align="center"><input type="checkbox" name="agree" required name="agree">Confirm details</td></tr>
        <tr><td colspan=2 align="center"><input type="submit" name="sub1" value="Submit"></td></tr>
    </table>
        </form>
        </body><br>'''

    ht3='''
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
    if "sub1" in form:
        #print(form.getvalue('fromdt'),int(form.getvalue('months')))
        fdt=form.getvalue('fromdt').split('-')
        fdt=datetime.date(int(fdt[0]),int(fdt[1]),int(fdt[2]))
        tdt=form.getvalue('todt').split('-')
        tdt=datetime.date(int(tdt[0]),int(tdt[1]),int(tdt[2]))
        #print(fdt,tdt)
        #Gave approv=4 for mat-leave
        cur.execute('select role from staff_det where id='+str(id))
        role=cur.fetchone()[0]
        approv=0
        if role=="co-ord":
            approv=1
        cur.execute('insert into leave_tab values(?,?,?,?,?,?,?,?,?,?)',(id,str(datetime.date.today()),'ccl',fdt,tdt,approv,form.getvalue('reason'),0,0,((tdt-fdt+datetime.timedelta(1)).days)))
        con.commit()
        ht2='''
            <table align="center" height=60>
                <tr>
                    <td style="font-family:Tahoma;font-size:24px;">Leave Application sent!</td>
                </tr></table><br><br><br><br><br><br><br><br><br><br><br><br><br><br>
        '''
    print((ht1+ht2+ht3).format(**locals()))

except Exception as err:
    html='''
    <html>
        <body onload="window.location='http://localhost:8080/test/cgi-bin/staff_err.py'"></body>
    </html>
    '''
    print(html.format(**locals()))
    print(err)