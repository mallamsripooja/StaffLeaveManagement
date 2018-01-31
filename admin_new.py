import cgi
import os
from http.cookies import *
import sqlite3
import datetime
import msvcrt
import smtplib
import nsm2
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
    msvcrt.setmode(0, os.O_BINARY)
    msvcrt.setmode(1, os.O_BINARY)
    print("Content-Type:text/html\n\n")
    if int(id)==1:
        html='''
        <html>
            <body onload="window.location='http://localhost:8080/test/cgi-bin/stafflogin.py'"></body>
        </html>
        '''
        print(html.format(**locals()))
    
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
           <a href="stafflogout.py">Logout</a>&emsp;</td>
           </tr>
           </table>
           <br>
            <table align="center" height=55>
                <tr>
                    <td align="center" style="font-family:Tahoma;font-size:24px;">New Record</td>
                </tr></table>'''
    sid=form.getvalue('id')
    #print(sid)
    htd='''<datalist id="dept-list">
        <option value="H&S">H&S</option>
        <option value="CSE">CSE</option>
        <option value="ECE">ECE</option>
        <option value="EIE">EIE</option>
        <option value="IT">IT</option>
        </datalist>
        <datalist id="desg-list">
        <option value="Professor">Professor</option>
        <option value="Asst.Prof">Assistant Professor</option>
        <option value="Asso.Prof">Associate Professor</option>
        <option value="Lab.In.">Lab Incharge</option>
        <option value="Lab.Asst">Lab Assistant</option>
        </datalist>
        <datalist id="role-list">
        <option value="staff">Staff</option>
        <option value="co-ord">Co-ordinator</option>
        <option value="admin">Admin</option>
        <option value="director">Director</option>
        </datalist>
        <datalist id="qual-list">
        <option value="Ph.D">Ph.D</option>
        <option value="M.Sc">M.Sc</option>
        <option value="M.Tech">M.Tech</option>
        <option value="B.Tech">B.Tech</option>
        </datalist>
        <datalist id="cord-list">'''
    cur.execute('select id,name,lastname from staff_det where role="co-ord"')#co-ord datalist
    spdata=cur.fetchall()
    #print(spdata)
    for ele in spdata:
        htd=htd+'''<option value="'''+str(ele[0])+'''">'''+ele[1]+'''</option>'''
    htd=htd+'''</datalist>
        <datalist id="yr-join">'''#datalist for yr of join from 2007 -- current year
    yr=2007
    cur_yr=datetime.date.today().year
    while yr!=(cur_yr+1):
        htd=htd+'''<option value="'''+str(yr)+'''">'''+str(yr)+'''</option>'''
        yr+=1
    htd=htd+'''</datalist>'''# readonly in input of id disables modification
    pat='[789][0-9]{9}'
    ht2=htd+'''
<form enctype="multipart/form-data" method=POST>
<table align="center" class="lf1" border=0>
    <tr>
        <td>&emsp;<b>Id</b></td>
        <td><b>Name</b></td>
    </tr>
    <tr>
        <td>&emsp;<input type="text" name="id" autocomplete="off" required autofocus></td>
        <td><textarea name="name" rows=1 autocomplete="off" required></textarea></td>
    </tr>
    <tr>
        <td colspan=2>&emsp;<b>Upload Photo </b>&emsp;
        <input type="file" name="file_img"></td>
    </tr>
    <tr>
        <td>&emsp;<b>Address </b></td></tr>
    <tr><td colspan=2>&emsp;<textarea name="addr" cols=47 rows=3 required></textarea>&emsp;</td>
    </tr>
    <tr>
        <td>&emsp;<b>Email </b></td>
        <td><b>Mobile </b></td></tr>
    <tr><td>&emsp;<input type="email" name="email" autocomplete="off" required></td>
        <td><input type="tel" name="mob" autocomplete="off" pattern={pat} required>&emsp;</td>
    </tr>
    <tr>
        <td>&emsp;<b>Department </b></td>
        <td><b>Designation </b></td></tr>
    <tr><td>&emsp;<input type="text" name="dept" list="dept-list" autocomplete="off" required></td>
        <td><input type="text" name="desg" list="desg-list" autocomplete="off" required>&emsp;</td>
    </tr>
    <tr>
        <td>&emsp;<b>Qualification </b></td>
        <td><b>Role </b></td></tr>
    <tr><td>&emsp;<input type="text" name="qual" list="qual-list" autocomplete="off" required></td>
        <td><input type="text" name="role" list="role-list" autocomplete="off" required>&emsp;</td>
    </tr>
    <tr>
        <td>&emsp;<b>Co-ordinator </b></td>
        <td><b>Year of join </b></td></tr>
    <tr><td>&emsp;<input type="text" name="cord" list="cord-list" autocomplete="off" required></td>
        <td><input type="text" name="yr" list="yr-join" autocomplete="off" required>&emsp;</td>
    </tr>
    <tr>
        <td colspan=2 align="center"><input type="submit" name="sub1" value="Save Changes"></td>
    </tr>
</table>
</form><br><br><br><br><br>
    '''
    if "sub1" in form:#to save changes in new details form
        fileitem = form['file_img']
        # Test if the file was uploaded
        if fileitem.filename:
        # strip leading path from file name to avoid directory traversal attacks
            fn = os.path.basename(fileitem.filename)
            open('../../' + fn, 'wb').write(fileitem.file.read())
            message = 'The file "' + fn + '" was uploaded successfully'
        else:
            message = 'No file was uploaded'

        SUBJECT='New Account - KMIT leave app'
        r='To use KMIT leave app services login with Username : Your id & Password : '+str(form.getvalue('id'))+'.This is your temporary password'
        r=r+' once you login you can change your passsword using "Change Password" link.'
        msg = 'Subject: %s\n\nDear Staff,\n\n%s\n\nRegards,\nKMIT.' % (SUBJECT,r)
        cur.execute('select email from staff_det where id=100')
        em=cur.fetchall()
        e=em[0]
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("kmitleaveapp@gmail.com","kmit@2015")
        server.sendmail("kmitleaveapp@gmail.com",e[0], msg)
        server.quit()
        r='Use KMIT leave app Username - Your id and Temporary Password - '+str(form.getvalue('id'))+'. Change password using link in the page'
        nsm2.smscall('9553079490','kmit',r,str(form.getvalue('mob')))

        cur.execute('insert into staff_det values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(form.getvalue('id'),str(form.getvalue('name')).capitalize(),str(form.getvalue('dept')),str(form.getvalue('desg'))
                                                                                 ,str(form.getvalue('addr')),str(form.getvalue('mob')),str(form.getvalue('email'))
                                                                                 ,str(form.getvalue('qual')),str(form.getvalue('role')),str(form.getvalue('cord')),0,str(form.getvalue('yr')),0,0))
        cur.execute('insert into login_tab values(?,?)',(str(form.getvalue('id')),str(form.getvalue('id'))))
        con.commit()


    print((ht1+ht2).format(**locals()))


except Exception as err:
    html='''
    <html>
        <body onload="window.location='http://localhost:8080/test/cgi-bin/staff_err.py'"></body>
    </html>
    '''
    #print(html.format(**locals()))
    print(err)