import cgi
import os
from http.cookies import *
import sqlite3
import datetime
import msvcrt
#http://localhost:8080/test/cgi-bin/admin.py
try:
    global form
    form=cgi.FieldStorage()
    print("Content-Type:text/html\n\n")
    con=sqlite3.connect('F:\Tom\staffapp.db')
    cur=con.cursor()
    c=SimpleCookie()
    b=SimpleCookie()
    msvcrt.setmode(0, os.O_BINARY)
    msvcrt.setmode(1, os.O_BINARY)
    global sid
    ht2=''
    hexp=''
    ht='''
    <html>
        <head>
            <link rel="icon" href="../favicon.ico" type="image/x-icon">
            <link rel="stylesheet" type="text/css" href="../style.css" />
            <title>Admin Page</title>
            <table width="100%" bgcolor="black">
                <tr>
                    <td width="10%"><img src="../logo.jpg" alt="img" height="130" width="148" ></td>
                    <td width="90%"><img src="../clg4.jpg" alt="img" height="130" width="1180" ></td>
                </tr>
            </table>
            <form enctype="multipart/form-data" action="admin.py" method="post">
            <table class="top" width="100%">
                <tr>
                    <td>
                        <input type="submit" name="sub3" style="font-size:16px;font-family:verdana;font-weight:bold;color:green;border-color:green;background-color:lightyellow;" value="Add a new record" />&emsp;
                        <input type="submit" name="sub4" style="font-size:16px;font-family:verdana;font-weight:bold;color:green;border-color:green;background-color:lightyellow;" value="Delete a record" />&emsp;
                        <input type="submit" name="sub7" style="font-size:16px;font-family:verdana;font-weight:bold;color:green;border-color:green;background-color:lightyellow;" value="Fetch a record" />
                    </td>
                    <td align="right">
                    <input type="submit" name="logout" style="font-size:16px;font-family:verdana;font-weight:bold;color:green;border-color:green;background-color:lightyellow;" value="Logout"/></td>
                </tr>
            </table>
            </form>
            <table align="center">
                <tr>
                    <td style="font-family:tahoma;font-size:26px;">Admin Page</td>
                </tr>
            </table>
        </head>'''
    ht1='''
        <body>
            <form method="POST">
                <table align="center" class="login" width="22%">
                    <tr height=20><td></td></tr>
                    <tr height=30>
                        <td align="center">&nbsp;Staff Id:</td>
                        <td align="center"><input type="text" name="username" placeholder="Enter ID" /></td>
                    </tr>
                    <tr height=20>
                        <td></td>
                        <td><br>&emsp;
                            <input type="submit" name="sub1" value="Fetch Details" style="font-size:11pt;font-family:tahoma;font-weight:500"/>
                        </td>
                    </tr>
                </table>
    '''
    
    if "logout" in form:
        htl='''
        <html>
        <body onload="window.location='http://localhost:8080/test/cgi-bin/stafflogin.py'">
        </body>
        </html>
        '''
        print(htl)

    if "sub1" in form:
        sid=str(form.getvalue('username'))
        #print("hi")
        i=0
        cur.execute('select id from staff_det')
        #print("hiiiii")
        d=cur.fetchall()
        lst=[]
        for nm in d:
            lst.append(d[i][0])
            i+=1
            #print("hello")
        if (int(sid) in lst)==False:
            hexp='<br><table align="center" style="text-align=center;color:red;font-family:tahoma;font-size:18px;"><tr><td>&emsp;&emsp;'+sid+' - Id does not exist !</td><tr><table>'
        else:
            cur.execute('select * from staff_det where id='+sid)
            data=cur.fetchall()
            #print(data)
            ht2='''
                <br><br><br>
                <form enctype="multipart/form-data" action="test.py" method="post">
                <table align="center" class="detail" cellspacing="10" border="0">
                    <caption><b>Following Details can be modified:</caption>
                    <tr>
                        <td align="center"><b>Staff Id</td>
                    <td align="center"><b>First Name</td>
                    <td align="center"><b>Last Name</td>
                        <td align="center"><b>Address</td>
                        <td align="center"><b>Mobile No.</td>
                        <td align="center"><b>Email</td>
                        <td align="center"><b>Qualification</td>
                        <td align="center"><b>Role</td>
                        <td align="center"><b>Department</td>
                        <td align="center"><b>Designation</td>
                        <td align="center"><b>Co-ordinator</td>
                    </tr>
                    <tr>
                        <td align="center">'''+str(data[0][0])+'''</td>
                    <td align="center"><input type="text" name="fnm" size="8" value='''+data[0][1]+''' /></td>
                    <td align="center"><input type="text" name="lnm" size="8" value='''+data[0][12]+''' /></td>
                        <td align="center"><input type="text" name="addr" size="20" value='''+data[0][4]+''' /></td>
                        <td align="center"><input type="text" name="mob" size="8" value='''+data[0][5]+''' /></td>
                        <td align="center"><input type="text" name="email" size="15" value='''+data[0][6]+''' /></td>
                        <td align="center"><input type="text" name="qual" size="5" value='''+data[0][7]+''' /></td>
                        <td align="center"><input type="text" name="role" size="5" value='''+data[0][8]+''' /></td>
                        <td align="center"><input type="text" name="dept" size="5" value='''+data[0][2]+''' /></td>
                        <td align="center"><input type="text" name="desgn" size="8" value='''+data[0][3]+''' /></td>
                        <td align="center"><input type="text" name="crd" size="5" value='''+str(data[0][9])+''' /></td>
                    </tr>
                    <tr>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td align="right"><input type="submit" name="sub2" value="Save Changes" style="font-size:11pt;font-family:tahoma;font-weight:500"/></td>
                    </tr>
                </table>
                </form>
            '''
            c['admin_id']=data[0][0]
            print(c.js_output());
    
    if "sub2" in form:
        if 'HTTP_COOKIE' in os.environ:
            cookie_string=os.environ.get('HTTP_COOKIE')
            c=SimpleCookie()
            c.load(cookie_string)
            if 'admin_id' in cookie_string:
                sid=c['admin_id'].value
            else:
                sid="Nil"
        else:
            sid="None"
        replace=[]
        replace=[form.getvalue('fnm'),form.getvalue('addr'),form.getvalue('mob')
                 ,form.getvalue('email'),form.getvalue('qual'),form.getvalue('role')
                 ,form.getvalue('dept'),form.getvalue('desgn'),str(form.getvalue('crd')),str(form.getvalue('lnm'))]
        print(type(replace[0]))
        cur.execute('update staff_det set name="'+replace[0]+'",addr="'+replace[1]+'",mob="'+replace[2]+'",email="'+replace[3]+'",qual="'+replace[4]+'",role="'+replace[5]+'",dept="'+replace[6]+'",desgn="'+replace[7]+'",cord="'+replace[8]+'",lastname="'+replace[9]+'" where id='+sid)
        con.commit()
        ht2=''

    if "sub3" in form:
        ht2='''
            <br><br><br>
             <form enctype="multipart/form-data" action="admin.py" method="post">
            <table align="center" class="detail" cellspacing="10" border="0">
                <caption align="center"><b>Enter the following details:</caption>&ensp;
                <tr>
                    <td align="center"><b>Staff Id</td>
                    <td align="center"><b>First Name</td>
                    <td align="center"><b>Last Name</td>
                    <td align="center"><b>Address</td>
                    <td align="center"><b>Mobile No.</td>
                    <td align="center"><b>Email</td>
                    <td align="center"><b>Qualification</td>
                    <td align="center"><b>Role</td>
                    <td align="center"><b>Department</td>
                    <td align="center"><b>Designation</td>
                    <td align="center"><b>Co-ordinator</td>
                    <td align="center"><b>Upload Image</td>
                </tr>
                <tr>
                    <td align="center"><input type="text" name="id" size="1" autofocus /></td>
                    <td align="center"><input type="text" name="fnm" size="8" /></td>
                    <td align="center"><input type="text" name="lnm" size="8" /></td>
                    <td align="center"><input type="text" name="addr" size="20" /></td>
                    <td align="center"><input type="text" name="mob" size="8" /></td>
                    <td align="center"><input type="text" name="email" size="15" /></td>
                    <td align="center"><input type="text" name="qual" size="5" /></td>
                    <td align="center"><input type="text" name="role" size="5" /></td>
                    <td align="center"><input type="text" name="dept" size="5" /></td>
                    <td align="center"><input type="text" name="desgn" size="8" /></td>
                    <td align="center"><input type="text" name="crd" size="5" /></td>
                    <td align="center"><input name="file_img" type="file" ></td>
                </tr>
                <tr>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td align="right"><input type="submit" name="sub5" value="Add record" style="font-size:11pt;font-family:tahoma;font-weight:500"/></td>
                </tr>
            </table>
            </form>'''

    if "sub4" in form:
        ht1=''
        ht2='''
            <br>
            <form method="post">
                <table align="center" class="login" height="30%" width="23%" border="0">
                    
                    <tr height=20>
                        <td align="center">&nbsp;Staff Id:</td>
                        <td align="center"><input type="text" name="del_unm" placeholder="Enter ID to delete" /></td>
                    </tr>
                    
                    <tr height=20>
                        <td align="center">&nbsp;Reason:</td>
                        <td align="center"><textarea name="lrsn" rows=3 cols=22 maxlength=50 placeholder="Reason for leaving"></textarea></td>
                    </tr>
                    <tr height=20>
                        <td></td>
                        <td>&nbsp;
                            <input type="submit" name="sub6" value="Delete record" style="font-size:11pt;font-family:tahoma;font-weight:500"/>
                        </td>
                    </tr>
                </table>
                </form>
                '''
    if "sub5" in form:
        y=datetime.date.today()
        y=str(y.year)
        cid=form.getvalue('id')
        i=0
        cur.execute('select id from staff_det')
        d=cur.fetchall()
        lst=[]
        for nm in d:
            lst.append(d[i][0])
            i+=1
        if (int(cid) in lst)==True:
            hexp='<br><table align="center" style="text-align=center;color:red;font-family:tahoma;font-size:18px;"><tr><td>&emsp;&emsp;'+cid+' - Id already exists !</td><tr><table>'
        else:
            cur.execute('insert into staff_det values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(form.getvalue('id'),str(form.getvalue('fnm')).capitalize(),str(form.getvalue('dept')).upper(),str(form.getvalue('desgn')).capitalize(),
                                                                               str(form.getvalue('addr')).capitalize(),form.getvalue('mob'),form.getvalue('email'),str(form.getvalue('qual')).capitalize()
                                                                               ,form.getvalue('role'),form.getvalue('crd'),0,y,str(form.getvalue('lnm')).capitalize(),0))
            cur.execute('insert into login_tab values(?,?)',(form.getvalue('id'),form.getvalue('id')))
            con.commit()
    
            if 'file_img' in form:

                fileitem = form['file_img']
            
# Test if the file was uploaded
                if fileitem.filename:
   # strip leading path from file name to avoid directory traversal attacks
                    fn = os.path.basename(fileitem.filename)
                    open('files/' + fn, 'wb').write(fileitem.file.read())
                else:
                    print("hello1");
            else:
                print("hello");

    if "sub6" in form:
        did=str(form.getvalue('del_unm'))
        i=0
        cur.execute('select id from staff_det')
        d=cur.fetchall()
        lst=[]
        for nm in d:
            lst.append(d[i][0])
            i+=1
        if (int(did) in lst)==False:
            hexp='<br><table align="center" style="text-align=center;color:red;font-family:tahoma;font-size:18px;"><tr><td>&emsp;&emsp;'+did+' - Id does not exist !</td><tr><table>'
        else:
            y=datetime.date.today()
            y=str(y.year)
            cur.execute('select * from staff_det where id='+did)
            data=cur.fetchall()
            #print(data[0][1])
            cur.execute('insert into exstaff_det values(?,?,?,?,?,?,?,?,?,?,?,?)',(data[0][0],data[0][1],data[0][2],data[0][3],data[0][4],data[0][5],data[0][6]
                                                                                 ,data[0][7],data[0][8],data[0][11],y,form.getvalue('lrsn')))
            cur.execute('delete from staff_det where id='+did)
            cur.execute('delete from login_tab where id='+did)
            con.commit()

    print((ht+ht1+ht2+hexp).format(**locals()))
except Exception as err:
    print((ht+ht1+ht2+hexp).format(**locals()))
    #print('No such record !')
    print(err)
