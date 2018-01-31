#!/usr/bin/env python3

import cgi
import sqlite3
import datetime

try:
        
        
    print("Content-Type:text/html\n\n")
    form=cgi.FieldStorage()
    con=sqlite3.connect("F:\Tom\staffapp.db")
    cur=con.cursor()
    def weekday1(date):
        if(date==0):
            return 'Monday'
        elif (date==1):
            return 'Tuesday'
        elif (date==2):
            return 'Wednesday'
        elif (date==3):
            return 'Thursday'
        elif (date==4):
            return 'Friday'
        elif (date==5):
            return 'Saturday'
        else:
            return 'Sunday'
    def day(date):
        cur.execute('select id,fdt,tdt,type from leave_tab where approv=3 and tdt >="'+str(date)+'"')
        data=cur.fetchall()
        dte=date
        dte=str(dte).split('-')
        week=datetime.date(int(dte[0]),int(dte[1]),int(dte[2])).weekday()
       
        h22='''
           <table width="100%" border="0"><tr><td width="60%"><b>'''+str(dte[2])+'-'+str(dte[1])+'-'+str(dte[0])+''' - '''+str(weekday1(week))+'''</b></td></tr>
'''
        h2=''
        for tup in data:
            f=tup[1]
            h3=''
            t=tup[2]
            fd=f.split('-')
            fd=datetime.date(int(fd[0]),int(fd[1]),int(fd[2]))
            td=t.split('-')
            td=datetime.date(int(td[0]),int(td[1]),int(td[2]))
            a=fd
            if(fd==td and td==date):
                cur.execute('select name from staff_det where id='+str(tup[0]))
                name=cur.fetchone()
                h4='''<tr><td>'''+str(name[0])+'''</td><td>'''+str(tup[3])+'''</td></tr>'''
                h3=h3+h4
            else:
                while(fd<=td):
                   if fd==date:
                        cur.execute('select name from staff_det where id='+str(tup[0]))
                        name=cur.fetchone()
                        h4='''<tr><td>'''+str(name[0])+'''</td><td>'''+str(tup[3])+'''</td></tr>'''
                        h3=h3+h4

                   fd=fd+datetime.timedelta(1)
            h2=h2+h3
        if h2=='':
            h22=h22+'''<tr><td>Nobody is on leave</td></tr>'''
        return h22+h2+'''</table><br>'''

    tody=datetime.date.today()
    #tody=datetime.date(2015,12,22)
    tmrw=tody+datetime.timedelta(1)
    ttmrw=tody+datetime.timedelta(2)

    h1='''
<html>
            <link rel="icon" href="../favicon.ico" type="image/x-icon">
                        <title>Notify</title>
<link rel="stylesheet" type="text/css" href="../style-c.css"/>
<body>
<form>
'''

    if(tody.isoweekday()!=7):
        ho=day(tody)
        h1=h1+ho
    else:
        dte=tody
        dte=str(dte).split('-')
        h1=h1+'''<table><tr><td><b>'''+str(dte[2])+'-'+str(dte[1])+'-'+str(dte[0])+''' - Sunday</b></td></tr></table><br>'''
    if(tmrw.isoweekday()!=7):
        ht=day(tmrw)
        h1=h1+ht
    else:
        dte=tmrw
        dte=str(dte).split('-')
        h1=h1+'''<table><tr><td><b>'''+str(dte[2])+'-'+str(dte[1])+'-'+str(dte[0])+''' - Sunday</b></td></tr></table><br>'''
        
    if(ttmrw.isoweekday()!=7):
        htt=day(ttmrw)
        h1=h1+htt
    else:
        dte=ttmrw
        dte=str(dte).split('-')
        h1=h1+'''<table><tr><td><b>'''+str(dte[2])+'-'+str(dte[1])+'-'+str(dte[0])+''' - Sunday</b></td></tr></table><br>'''
        
    hh=h1+'''</form></body></table>'''

    print(hh.format(**locals()))               
        
except Exception as e:
    print(e)
