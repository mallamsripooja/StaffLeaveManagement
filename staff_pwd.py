import cgi
import os
import sqlite3
import nsm2
import smtplib
try:
    con=sqlite3.connect("F:\Tom\staffapp.db")
    cur=con.cursor()
    form=cgi.FieldStorage()
    print("Content-Type:text/html\n\n")
    ht1='''
    <html>
        <head>
            <link rel="icon" href="../favicon.ico" type="image/x-icon">
            <link rel="stylesheet" type="text/css" href="../style.css" />
            <title>Forgot Password</title>
            <table width="100%" bgcolor="black">
                <tr>
                    <td width="10%"><img src="../logo.jpg" alt="img" height="130" width="148" ></td>
                    <td width="90%"><img src="../clg4.jpg" alt="img" height="130" width="1180" ></td>
                </tr>
            </table>
            </head>'''
    ht2='''<body><br>
            <table align="center" height=60>
                <tr>
                    <td style="font-family:Tahoma;font-size:24px;" align="center">Not a problem</td></tr>
                    <tr><td style="font-family:Tahoma;font-size:14px;" align="center">1. Enter your id and submit</td></tr>
                    <tr><td style="font-family:Tahoma;font-size:14px;" align="center">2. Receive your password via SMS & email</td>
                </tr></table>
        <br><br><br>
        <form method=POST>
            <table class="lf1" align="center">
                <tr>
                    <td>&emsp;<b>Id</b>&emsp;<input type="text" name="id" placeholder="Enter your id"></td>
                    <td align="center">&nbsp;<input type="submit" name="sub" value="Submit">&emsp;</td>
                </tr>
            </table>
            </form>
            </body>'''
    ht3='''<br><br><br><br><br><br>
        <br><br><br><br><br>
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
    if "sub" in form:#sub -- to receive pwd
        id=form.getvalue('id')
        cur.execute('select id from staff_det')
        id_list=cur.fetchall()#fetching ids as tuples
        only_id=[]#to extract ids from tuples
        for ele in id_list:
            only_id.append(ele[0])
        if int(int(id) in only_id)==1:
            #To send SMS
            cur.execute('select pwd from login_tab where id='+str(id))
            msg_pwd=cur.fetchall()[0][0]#retrieving password from db
            cur.execute('select mob from staff_det where id='+str(id))
            msg_mob=str(cur.fetchall()[0][0])#retrieving mobile number from db
            msg='Your password for staff leave application is '+str(msg_pwd)
            nsm2.smscall('9553079490','kmit',msg,msg_mob)

            #To send email
            cur.execute('select name,lastname from staff_det where id='+str(id))
            msg_nm=cur.fetchall()[0]#retrieving first name,last name
            cur.execute('select email from staff_det where id='+str(id))
            msg_em=cur.fetchall()[0][0]#retrieving email
            TEXT = "Your leave application password is "+str(msg_pwd)
            SUBJECT='Forgot Password?'
            msg = 'Subject: %s\n\n%s,\n\n%s\n\nRegards,\nKMIT.' % (SUBJECT,msg_nm[0], TEXT)
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login("kmitleaveapp@gmail.com","kmit@2015")
            server.sendmail("kmitleaveapp@gmail.com",msg_em, msg)
            server.quit()

            ht2='''<body><br>
            <table align="center" height=60>
                <tr>
                    <td style="font-family:Tahoma;font-size:24px;" align="center">Password sent, please check your inbox</td></tr>
                </tr></table></body><br><br><br><br><br><br><br><br><br><br>
            '''
        else:
            ht2='''<body><br>
            <table align="center" height=60>
                <tr>
                    <td style="font-family:Tahoma;font-size:24px;" align="center">Entered Id is incorrect!</td></tr>
                </tr></table></body><br><br><br><br><br><br><br><br><br><br>
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