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
                    <td style="font-family:Tahoma;font-size:24px;">On Duty Leave</td>
                </tr></table>'''
    ht2='''<form method="POST">
                     <table  align="Center" class="lf1" width="19%" border=0>
                     <tr>
                       <td><b>&nbsp;Id</b></td>
                       <td>{id}</td>
                     </tr>
                     <tr>
                       <td><b>&nbsp;Date&emsp;</b></td>
                        <td><input type="date" name="fromdt"
                        required min="'''+str(datetime.date.today())+'''"/></td>
                     </tr>
        <tr><td colspan=2 align="center"><input type="checkbox" name="agree" required name="agree">Confirm details</td></tr>
        <tr><td colspan=2 align="center"><input type="submit" name="sub1" value="Get substitution form"></td></tr>
    </table>
        </form>
        </body><br><br><br><br><br><br><br><br>'''

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

    if "sub2" in form:
        data=[form.getvalue('pr'),form.getvalue('name'),form.getvalue('yr'),form.getvalue('br'),form.getvalue('sec')]
        cur.execute('select fdt from leave_tab where id='+str(id)+' and type="onduty" and approv=0 or approv=1')
        data1=cur.fetchall()
        #print(data)
        j=0
        cur.execute('select role from staff_det where id='+str(id))
        role=cur.fetchone()[0]
        approv=0
        if role=="co-ord":
            approv=1
        for i in range(len(data[0])):
            if data[1][i]!='None':
                cur.execute('insert into leave_sub values(?,?,?,?,?,?)',(id,data1[-1][0],data[1][i],data[2][j]+'-'+data[3][j]+'-'+data[4][j],data[0][i],approv))
                con.commit()
                j+=1
        ht2='''
            <table align="center" height=55>
                <tr>
                    <td style="font-family:Tahoma;font-size:24px;">Leave Application sent!</td>
                </tr></table><br><br><br><br><br><br><br><br><br><br><br><br><br><br>
        '''

    if "sub1" in form:
        dt=form.getvalue('fromdt')
        cur.execute('select role from staff_det where id='+str(id))
        role=cur.fetchone()[0]
        approv=0
        if role=="co-ord":
            approv=1
        cur.execute('insert into leave_tab values(?,?,?,?,?,?,?,?,?,?)',(id,str(datetime.date.today()),'onduty',dt,dt,approv,'onduty',0,0,0))
        con.commit()
        h1='''
                <td><select name="yr">
                    <option value="" disabled selected>Year</option>
                    <option value="I">I</option>
                    <option value="II">II</option>
                    <option value="III">III</option>
                    <option value="IV">IV</option>
                </select></td>'''
        h2='''<td><select name="br">
                    <option value="" disabled selected>Branch</option>
                    <option value="CSE">CSE</option>
                    <option value="ECE">ECE</option>
                    <option value="EIE">EIE</option>
                    <option value="IT">IT</option>
                </select></td>'''
        h3='''<td><select name="sec">
                    <option value="" disabled selected>Section</option>
                    <option value="A">A</option>
                    <option value="B">B</option>
                    <option value="C">C</option>
                    <option value="D">D</option>
                    <option value="E">E</option>
                    <option value="F">F</option>
                    <option value="G">G</option>
                </select></td>'''
        cur.execute('select name,dept from staff_det where id>100 order by dept')
        db=cur.fetchall()
        htd='''<datalist id="catlist"><option value="" disabled selected>None</option>'''
        for e in db:
            htd=htd+'''<option value="'''+e[0]+'''" >'''+e[1]+'''</option>'''
        htd=htd+'''</datalist>'''
        h=htd+'''<td><input type="text" list="catlist" name="name" autocomplete="off" value="None"></td>'''
        ht2='''<form method=POST><table class="lf1" align="center" width="35%">
        <tr>
            <td align="center"><b>&nbsp;Period</td>
            <td align="center"><b>Name</td>
            <td align="center"><b>Year</td>
            <td align="center"><b>Branch</td>
            <td align="center"><b>Section</td>
        </tr>
        <tr>
            <td align="center"><input type="text" name="pr" value=1 size="1" readonly></td>
            '''+h+h1+h2+h3+'''
        </tr>
        <tr>
            <td align="center"><input type="text" name="pr" value=2 size="1" readonly></td>
            '''+h+h1+h2+h3+'''
        </tr>
        <tr>
            <td align="center"><input type="text" name="pr" value=3 size="1" readonly></td>
            '''+h+h1+h2+h3+'''
        </tr>
        <tr>
            <td align="center"><input type="text" name="pr" value=4 size="1" readonly></td>
            '''+h+h1+h2+h3+'''
        </tr>
        <tr>
            <td align="center"><input type="text" name="pr" value=5 size="1" readonly></td>
            '''+h+h1+h2+h3+'''
        </tr>
        <tr>
            <td align="center"><input type="text" name="pr" value=6 size="1" readonly></td>
            '''+h+h1+h2+h3+'''
        </tr>
        <tr>
            <td align="center"><input type="text" name="pr" value=7 size="1" readonly></td>
            '''+h+h1+h2+h3+'''
        </tr>
        <tr>
            <td colspan=5 align="center" style="color: red;">**Incase of free period, do not fill any corresponding field</td>
        </tr>
        <tr>
            <td colspan=5 align="center"><input type="submit" value="Submit" name="sub2"></td>
        </tr>
        </table>
        </form>
    </body><br><br>
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