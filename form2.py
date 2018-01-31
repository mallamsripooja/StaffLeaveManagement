import cgi
import sqlite3
import datetime
import os
from http.cookies import *
from datetime import timedelta
#http://localhost:8080/test/cgi-bin/form2.py
try:
    global con
    global cur
    global td
    global fd
    global dep
    global dt
    global ht4
    global ht3
    global ht2
    global ht1
    global hsel
    global cse
    global ece
    global eie
    global it
    global data1
    con=sqlite3.connect("F:\Tom\staffapp.db")
    cur=con.cursor()
    

    form=cgi.FieldStorage()
    print('Content-Type:text/html\n\n')
    
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
    
    cur.execute('select * from leave_tab where id='+str(id))
    data=cur.fetchall()
    ex=data[-1]

    s=str(ex[3]).split('-')
    fd=datetime.date(int(s[0]),int(s[1]),int(s[2]))
    s=str(ex[4]).split('-')
    td=datetime.date(int(s[0]),int(s[1]),int(s[2]))
    
    dt=str(fd.strftime("%d-%m-%Y"))
    htf=''
    hs='''
        <option selected>H&S</option>
        <option>CSE</option>
        <option>IT</option>
        <option>ECE</option>
        <option>EIE</option></select></td>
    '''

    cse='''
        <option>H&S</option>
        <option selected>CSE</option>
        <option>IT</option>
        <option>ECE</option>
        <option>EIE</option></select></td>
    '''
    ece='''
        <option>H&S</option>
        <option>CSE</option>
        <option>IT</option>
        <option selected>ECE</option>
        <option>EIE</option></select></td>
    '''
    it='''
        <option>H&S</option>
        <option>CSE</option>
        <option selected>IT</option>
        <option>ECE</option>
        <option>EIE</option></select></td>
    '''
    eie='''
        <option>H&S</option>
        <option>CSE</option>
        <option>IT</option>
        <option>ECE</option>
        <option selected>EIE</option></select></td>
    '''
    def daterange(start_date, end_date):
        for n in range(int ((end_date - start_date).days)):
            yield start_date + timedelta(n)

    def fill_d():
        global ht4
        ht4='''
        <td>
            <select name="dropdown" required>
            <option value="" disabled selected>Date</option>
        '''
        for single_date in daterange(fd,td+timedelta(1)):
            if single_date.isoweekday()!=7:
                ht4=ht4+'''<option value="'''+single_date.strftime("%d-%m-%Y")+'''">'''+single_date.strftime("%d-%m-%Y")+'''</option>'''
        ht4=ht4+'''</select></td>'''
        return ht4
    
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
            <title>Substitution Form</title>
            <table width="100%" bgcolor="black" width="100%">
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
           <a href="stafflogin.py">Logout</a>&emsp;</td>
           </tr>
                     </table>
            <form method="POST">
                     <br><br>
                     <table  align="Center" class="lf1" bgcolor="black">
                    <tr>
                        <td><b>&nbsp;Id&emsp;&nbsp; :</b></td>
                        <td>'''+str(id)+'''</td>
                    </tr>
                    <tr>
                        <td><b>&nbsp;Date :</b></td>
                        <td>From:&nbsp;'''+str(fd.strftime("%d-%m-%Y"))+'''</td>
                    </tr>
                    <tr>
                        <td></td>
                        <td>To:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'''+str(td.strftime("%d-%m-%Y"))+'''</td>
                    </tr>
                    <tr>
                        <td><b>&nbsp;Type :</b></td>
                        <td>'''+str(ex[2]).capitalize()+'''</td>
                        <td></td>
                    </tr>
                </table>
                <br><br>
                <table height="10%" align="center">
                    <tr height="10%">
                        <td style="font-family:tahoma;font-size:20px;">Substitution Form</td>
                    </tr>
                </table>
        <table align="center" border="0" class="lf1">
        <tr><td colspan="2">&nbsp;Department:</td></tr>
            <tr>
                <td><select name="ddep">
        '''
    hsel='''
    <td><input type="submit" name="sub" value="Select" /></td>
    '''
    def check():
        global ht1
        global cse
        global ece
        global eie
        global it
        global hsel
        global upd
        #print(ht1.format(**locals()))
        dep=str(form.getvalue('ddep'))
        #print(dep)
        if dep!='ECE' and dep!='EIE' and dep!='IT' and dep!='H&S':
            ht1=ht1+cse+hsel
        if dep=='EIE':
            ht1=ht1+eie+hsel
        if dep=='ECE':
            ht1=ht1+ece+hsel
        if dep=='IT':
            ht1=ht1+it+hsel
        if dep=='H&S':
            ht1=ht1+hs+hsel

    def fill():
        global ht2
        cur.execute('select name from staff_det where dept="'+dep+'"')
        d=cur.fetchall()
        ht2='''
        <td><select name="dropdown" required>
        <option value="" disabled selected>Name</option>
        '''
        for i in d:
            a=i[0]
            ht2=ht2+'''<option value="'''+str(a)+'''">'''+str(a)+'''</option>'''
        ht2=ht2+'''</select></td>'''
        #return ht

    def gen():
        global ht3
        ht3='''
                <td><select name="dropdown" required>
                    <option value="" disabled selected>Year</option>
                    <option value="I">I</option>
                    <option value="II">II</option>
                    <option value="III">III</option>
                    <option value="IV">IV</option>
                </select></td>
                <td><select name="dropdown"  required>
                    <option value="" disabled selected>Branch</option>
                    <option value="CSE">CSE</option>
                    <option value="ECE">ECE</option>
                    <option value="EIE">EIE</option>
                    <option value="IT">IT</option>
                </select></td>
                <td><select name="dropdown" required>
                    <option value="" disabled selected>Section</option>
                    <option value="A">A</option>
                    <option value="B">B</option>
                    <option value="C">C</option>
                    <option value="D">D</option>
                    <option value="E">E</option>
                    <option value="F">F</option>
                    <option value="G">G</option>
                </select></td>
                <td><select name="dropdown" required>
                    <option value="" disabled selected>Period</option>
                    <option value="1">1</option>
                    <option value="2">2</option>
                    <option value="3">3</option>
                    <option value="4">4</option>
                    <option value="5">5</option>
                    <option value="6">6</option>
                    <option value="7">7</option>
                </select></td>
                <td><input type="submit" name="sub1" value="Submit" /></td>
            </tr>
            </table>'''
    extra='''
            <table align="center" height=60>
            <tr>
            <td height=60>Update option available, in case of error - modification can be done&emsp;<input type="submit" name="sub2" value="Done filling details" /></td>
            </tr>
            </table>
            </form>
            </body>
            </html>
        '''
        #ht3=fill()+ht3
        #print(ht4.format(**locals()))

    def updcall():
        cur.execute('select role from staff_det where id='+str(id))
        role=cur.fetchone()[0]
        approv=0
        if role=="co-ord":
            approv=1
        cur.execute('select * from leave_sub where id='+str(id)+' and approv='+str(approv)+' order by date')
        up=cur.fetchall()
        #print(up)
        upd='''<form method=POST>
        <table class='lf1' align="center">
        <tr>
        <td>Date</td><td>Name</td><td>Class</td><td>Period</td>
        </tr>
        '''
        cur.execute('select name,dept from staff_det where id>100 order by dept')
        db=cur.fetchall()
        htd='''<datalist id="catlist">'''
        for e in db:
            #dlst.append(ele[0])
            htd=htd+'''<option value="'''+e[0]+'''" >'''+e[1]+'''</option>'''
        htd=htd+'''</datalist>'''
        for ele in up:
            dt=ele[1].split('-')
            upd=upd+htd+'''
            <tr>
                <td><input type="date" name="date" size="10" value='''+dt[2]+'-'+dt[1]+'-'+dt[0]+''' min="'''+str(fd)+'''" max="'''+str(td)+'''"/></td>
                <td><input type="text" list="catlist" name="name" autocomplete="off" value="'''+ele[2]+'''"></td>
                <td><input type="text" name="class" size="10" value='''+ele[3]+''' /></td>
                <td><input type="text" name="period" size="10" value='''+ele[4]+''' /></td>
            </tr>
                '''
        upd=upd+'''
        <tr>
            <td colspan=4 align="center"><input type="submit" name="sub3" value="Updated/Ok" />
            </td>
        </tr></table></form>
        '''
        print(upd.format(**locals()))

    if "sub" in form:
        dep=str(form.getvalue('ddep'))
        gen()
        fill()
        fill_d()
        htf=ht4+ht2+ht3
    
    if "sub1" in form:
        data1=form.getvalue('dropdown')
        #print(data1[0])
        cur.execute('select role from staff_det where id='+str(id))
        role=cur.fetchone()[0]
        approv=0
        if role=="co-ord":
            approv=1
        cur.execute('insert into leave_sub values(?,?,?,?,?,?)',(str(id),data1[0],data1[1],(data1[2]+'-'+data1[3]+'-'+data1[4]),data1[5],approv))
        con.commit()

    counter=1
    check()
    print(ht1.format(**locals()))
    print((htf+extra).format(**locals()))
    
    if "sub3" in form:    
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
        place=[]
        place=[form.getvalue('date'),form.getvalue('name'),form.getvalue('class'),form.getvalue('period')]
        #print(data1)
        cur.execute('select role from staff_det where id='+str(id))
        role=cur.fetchone()[0]
        approv=0
        if role=="co-ord":
            approv=1
        cur.execute('delete from leave_sub where id='+str(id)+' and approv='+str(approv))
        #print(place)
        con.commit()
        for i in range(len(place[0])):
            #print(place[0][i],place[1][i])
            dt=place[0][i].split('-')
            cur.execute('insert into leave_sub values(?,?,?,?,?,?)',(str(id),dt[0]+'-'+dt[1]+'-'+dt[2],place[1][i],place[2][i],place[3][i],approv))
        con.commit()
        #ht2=''
        temp='''
                <html>
                    <body onload="window.location='http://localhost:8080/test/cgi-bin/form.py'"></body>
                </html>'''
        print(temp)

    if "sub2" in form:
        updcall()


except Exception as err:
    html='''
    <html>
        <body onload="window.location='http://localhost:8080/test/cgi-bin/staff_err.py'"></body>
    </html>
    '''
    #print(html.format(**locals()))
    print(err)