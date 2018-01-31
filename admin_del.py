import cgi
import os
from http.cookies import *
import sqlite3
import datetime
try:
    global form
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
    ht1='''
                    <html>
                     <head>
            <link rel="icon" href="../favicon.ico" type="image/x-icon">
                        <link rel="stylesheet" type="text/css" href="../style.css" />
                        <title>Admin</title>
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
           <td align="right">
           <img src="../100.JPG" alt="No image" class="profile"></td>
           <td>Admin</td>
           <td align="center"><a href="admin_get.py">Get details</a>&emsp;|&emsp;
           <a href="admin_new.py">Add a record</a>&emsp;|&emsp;
           <a href="admin_del.py">Delete a record</a>&emsp;|&emsp;
           <a href="admin_sms.py">SMS leave</a>&emsp;|&emsp;
           <a href="record.py">Who's on leave?</a>&emsp;
           </td>
           <td align="right">
           <a href="stafflogin.py">Logout</a>&emsp;</td>
           </tr>
           </table>
           <br>
            <table align="center" height=55>
                <tr>
                    <td align="center" style="font-family:Tahoma;font-size:24px;">Delete Record</td>
                </tr></table>'''
    ht2='''
    <form method=POST>
    <table class="lf1" align="center">
        <tr>
            <td>&emsp;<b>Id</b>
            <input type="text" name="id" required autocomplete="off" placeholder="Enter staff id">&emsp;</td>
        </tr>
        <tr>
            <td>&emsp;<textarea name="reason" required rows=3 cols=25 placeholder="Enter reason for leaving" title="Enter reason for leaving"></textarea>&emsp;</td>
        </tr>
        <tr>
            <td align="center"><input type="submit" name="sub" value="Delete record"></td>
        </tr>
    </table>
    </form>
    '''
    ht3='''
    <br><br><br><br><br><br><br>
    <br><br><br><br><br><br><br>
    <br><br>
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
    if "sub" in form:
        cur.execute('select id from staff_det')
        id_tup=cur.fetchall()
        id_lst=[]
        for ele in id_tup:
            id_lst.append(ele[0])
        sid=int(form.getvalue('id'))
        if int(sid in id_lst)==1:#incomplete add det to exstaff_det
            cur.execute('select * from staff_det where id='+str(sid))
            info=cur.fetchall()[0]
            #print(info)
            #print(form.getvalue('reason'))
            cur.execute('insert into exstaff_det values(?,?,?,?,?,?,?,?,?,?,?,?)',(str(sid),info[1],info[2],info[3],info[4],info[5],info[6],info[7],
                                                                                   info[8],info[-3],datetime.date.today().year,form.getvalue('reason')))
            cur.execute('delete from staff_det where id='+str(sid))
            cur.execute('delete from login_tab where id='+str(sid))
            con.commit()
            ht2='''
            <table align="center">
            <tr>
            <td align="center" style="font-family:Tahoma;font-size:24px;">Record Deleted</td>
            </tr>
            </table><br>
            '''
        else:
            ht2='''
            <table align="center">
            <tr>
            <td align="center" style="font-family:Tahoma;font-size:24px;">Invalid Id</td>
            </tr>
            </table><br>
            '''
    print((ht1+ht2+ht3).format(**locals()))
except Exception as err:
    html='''
    <html>
        <body onload="window.location='http://localhost:8080/test/cgi-bin/staff_err.py'"></body>
    </html>
    '''
    #print(html.format(**locals()))
    print(err)