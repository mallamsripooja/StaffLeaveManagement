import cgi
import os
from http.cookies import *
#http://localhost:8080/test/cgi-bin/stafflogin.py
import sqlite3
try:
    con=sqlite3.connect("F:\Tom\staffapp.db")
    cur=con.cursor()
    ck=SimpleCookie()
    global unm
    global pwd
    global ln_u
    global ln_p
    global ln_s
    global ht2
    ln_u=''
    ln_p=''
    ln_s=''
    def new_win(uid):
        cur.execute('select role from staff_det where id='+uid)
        d=cur.fetchall()
        r1=d[0]
        r2=r1[0]
        ck['username']=uid
        print(ck.js_output());
        #cur.execute('insert into storage values('+uid+')')
        con.commit()
        if r2=='director':
            ht='''
                <html>
                    <body onload="window.location='http://localhost:8080/test/cgi-bin/frame.py'"></body>
                </html>
            '''
            print(ht)
        elif r2=='co-ord':
            ht='''
                <html>
                    <body onload="window.location='http://localhost:8080/test/cgi-bin/frame2.py'"></body>
                </html>
            '''
            print(ht)
        elif r2=='staff':
            ht='''
                <html>
                    <body onload="window.location='http://localhost:8080/test/cgi-bin/form.py'"></body>
                </html>
            '''
            print(ht)
        elif r2=='admin':
            ht='''
                <html>
                    <body onload="window.location='http://localhost:8080/test/cgi-bin/admin_get.py'"></body>
                </html>
            '''
            print(ht)
    def check_p(unm):
        cur.execute('select pwd from login_tab where id='+unm)
        d=cur.fetchall()
        global pwd
        global ln_p
        global ln_s
        lst=[]
        for i in d:
            lst.append(str(i[0]))
        if (pwd in lst)==True:
            ln_s='Login Successfull !'
            new_win(unm)
        else:
            ln_p='Invalid Password !'
    def check_u():
        cur.execute('select id from login_tab')
        d=cur.fetchall()
        global unm
        global ln_u
        lst=[]
        for i in d:
            lst.append(str(i[0]))
        if (unm in lst)==True:
            check_p(unm)
        else:
            ln_u='Invalid Username !'
    form=cgi.FieldStorage()
    print("Content-Type:text/html\n\n")
    pat='[0-9]{3}'
    ht1='''
    <html>
        <head>
            <link rel="icon" href="../favicon.ico" type="image/x-icon">
            <link rel="stylesheet" type="text/css" href="../style.css" />
            <title>Login Page</title>
            <table width="100%" bgcolor="black">
                <tr>
                    <td width="10%"><img src="../logo.jpg" alt="img" height="130" width="148" ></td>
                    <td width="90%"><img src="../clg4.jpg" alt="img" height="130" width="1180" ></td>
                </tr>
            </table>
            <table height="4%">
                <tr height="4%"></tr>
            </table>
            <table align="center">
                <tr>
                    <td style="font-family:Tahoma;font-size:24px;">Staff Login</td>
                </tr>
            </table>
        </head>
        <body>
        <br>
            <form method="post">
                <table align="center" class="login" width="23%" >
                    <tr height=20 >
                        <td></td>
                        <td style="text-align=center;color:red;">&emsp;&nbsp;{ln_u}</td>
                    </tr>
                    <tr height=30>
                        <td align="center"><b>Username</td>
                        <td align="center"><input type="text" name="username" required placeholder="Enter ID" autocomplete="off" autofocus/></td>
                    </tr>
                    <tr height=20>
                        <td></td>
                        <td style="text-align=center;color:red;">&emsp;&nbsp;{ln_p}</td>
                    </tr>
                    <tr height=20>
                        <td align="center"><b>Password</td>
                        <td align="center"><input type="password" name="password" placeholder="Enter Password" required pattern={pat} title="3 num password"/></td>
                    </tr>
                    <tr height=20>
                        <td></td>
                        <td style="text-align=center;color:green;">&emsp;&nbsp;{ln_s}</td>
                    </tr>
                    <tr height=20>
                        <td style="text-align=center;color:blue;" colspan=2>&nbsp;<a href="staff_pwd.py">Forgot Password?</a>&emsp;&emsp;
                            <input type="submit" name="submit" value="Login" style="font-size:13pt;font-family:'calibri';"/>
                        </td>
                    </tr>
                </table>
            </form>
            <br><br><br><br><br><br><br>
        </body>
        <footer>
            <table width="100%" align="center">
                <tr>
                    <td width="33%" align="center" style="font-size:18px;">3-5-1026, Narayanguda, Hyderabad, Telangana -500029</td>
                    <td width="33%" align="center" style="font-size:18px;">&emsp;&emsp;&emsp;Copyright &#169; KMIT</td>
                    <td width="33%" align="center" style="font-size:18px;">&emsp;&emsp;&emsp;Website:    <a href="http://www.kmit.in/" style="text-decoration:none;"/>kmit.in</td>
                </tr>
            </table>
        </footer>
       </html>
    '''
      
    unm=str(form.getvalue("username","Id"))
    pwd=str(form.getvalue("password","Pwd"))
    if "submit" in form:
        check_u()
    print(ht1.format(**locals()))

except Exception as err:
    html='''
    <html>
        <body onload="window.location='http://localhost:8080/test/cgi-bin/staff_err.py'"></body>
    </html>
    '''
    print(html.format(**locals()))
    print(err)