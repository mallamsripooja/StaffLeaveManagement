import cgi
import os
from http.cookies import *
import sqlite3
import datetime
import msvcrt
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
                    <td align="center" style="font-family:Tahoma;font-size:24px;">Admin</td>
                </tr>
                <tr>
                    <td align="center" style="font-family:Tahoma;font-size:18px;">Get details / Edit details</td>
                </tr></table>'''
    ht2='''
    <form method=POST>
    <table align="center" class="lf1" width="15%">
        <tr>
            <td align="center">&emsp;<b>Id</b>&emsp;</td>
            <td align="center"><input type="text" name="id" placeholder="Enter staff id" autofocus autocomplete="off"></td>
        </tr>
        <tr>
            <td colspan=2 align="center"><input type="submit" name="sub" value="Get details"><td>
        </tr>
    </table>
    </form>
    '''
    if "sub" in form:#submitting id to get details
        sid=form.getvalue('id')
        #print(sid)
        cur.execute('select * from staff_det where id='+str(sid))
        data=cur.fetchall()[0]
        #print(data)
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
    <form method=POST>
    <table align="center" class="lf1" border=0>
        <tr>
            <td>&emsp;<b>Id</b>&emsp;
            <input type="text" name="id" size=14 value='''+str(sid)+''' readonly></td>
            <th rowspan=4>
            <object data="../'''+str(sid)+'''.JPG" class="profile" height=100 width=100>
            <img src="../100.JPG" alt="No image" class="profile" height=100 width=100></object></th>
        </tr>
        <tr>
            <td>&emsp;<b>Name </b></td></tr>
        <tr><td>&emsp;<input type="text" name="fname" value="'''+data[1]+'''" autocomplete="off"></td>
        </tr>
        <tr>
            <td>&emsp;<b>Address </b></td></tr>
        <tr><td colspan=2>&emsp;<textarea name="addr" cols=47 rows=3>'''+data[4]+'''</textarea>&emsp;</td>
        </tr>
        <tr>
            <td>&emsp;<b>Email </b></td>
            <td><b>Mobile </b></td></tr>
        <tr><td>&emsp;<input type="email" name="email" value='''+data[6]+''' autocomplete="off"></td>
            <td><input type="tel" name="mob" value='''+data[5]+''' autocomplete="off" pattern={pat}>&emsp;</td>
        </tr>
        <tr>
            <td>&emsp;<b>Department </b></td>
            <td><b>Designation </b></td></tr>
        <tr><td>&emsp;<input type="text" name="dept" list="dept-list" value='''+data[2]+''' autocomplete="off"></td>
            <td><input type="text" name="desg" list="desg-list" value='''+data[3]+''' autocomplete="off">&emsp;</td>
        </tr>
        <tr>
            <td>&emsp;<b>Qualification </b></td>
            <td><b>Role </b></td></tr>
        <tr><td>&emsp;<input type="text" name="qual" list="qual-list" value='''+data[7]+''' autocomplete="off"></td>
            <td><input type="text" name="role" list="role-list" value='''+data[8]+''' autocomplete="off">&emsp;</td>
        </tr>
        <tr>
            <td>&emsp;<b>Co-ordinator </b></td>
            <td><b>Year of join </b></td></tr>
        <tr><td>&emsp;<input type="text" name="cord" list="cord-list" value='''+str(data[9])+''' autocomplete="off"></td>
            <td><input type="text" name="yr" list="yr-join" value='''+data[11]+''' autocomplete="off">&emsp;</td>
        </tr>
        <tr>
            <td colspan=2 align="center"><input type="submit" name="sub1" value="Save Changes"></td>
        </tr>
    </table>
    </form><br><br><br><br><br>
        '''
    if "sub1" in form:#to save changes in get details form
        cur.execute('update staff_det set name="'+str(form.getvalue('fname')).capitalize()+'" ,lastname="'+str(form.getvalue('lname')).capitalize()+'" ,addr="'+str(form.getvalue('addr'))+'"'
        ' ,mob="'+str(form.getvalue('mob'))+'" ,email="'+str(form.getvalue('email'))+'" ,dept="'+str(form.getvalue('dept'))+'" ,desgn="'+str(form.getvalue('desg'))+'"'
        ' ,qual="'+str(form.getvalue('qual'))+'" ,role="'+str(form.getvalue('role'))+'" ,cord="'+str(form.getvalue('cord'))+'" ,entry="'+str(form.getvalue('yr'))+'"'
        ' where id='+str(form.getvalue('id')))
        con.commit()

    print((ht1+ht2).format(**locals()))


except Exception as err:
    html='''
    <html>
        <body onload="window.location='http://localhost:8080/test/cgi-bin/staff_err.py'"></body>
    </html>
    '''
    print(html.format(**locals()))
    print(err)