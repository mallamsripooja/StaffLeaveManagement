import os
import cgi
import sqlite3
import datetime
import numpy as np
import matplotlib.pyplot as plt
from spreadsheetsCustomizePg import CustomPg as cp
#<script type="text/javascript" src="http://gc.kis.scr.kaspersky-labs.com/1B74BD89-2A22-4B93-B451-1C9E1052A0EC/main.js" charset="UTF-8"></script>
#try using this
try:
#sqlite connection
    con=sqlite3.connect("F:\Tom\spreadsheet.db")
    cur=con.cursor()
    date=str(datetime.date.today())#typecasting
    
#HTML content starts here
    form=cgi.FieldStorage()
    print("Content-Type:text/html\n\n")
    headPart='<link rel="icon" href="../spreadsheet.ico" type="image/x-icon">'#did not link a stylesheet
    headPart+='<script type="text/javascript" src="../main.js" charset="UTF-8"></script>'
    ht=cp.head1('RecordMyRupee',headPart)#HEAD

    ht+=cp.heading('Record My Rupee App')#PAGE TITLE

#Getting fields from a table
    lst=cp.getFieldsfromTable_ss("F:\Tom\spreadsheet.db","genre")
    #print(lst)


#Initialize amt=0 in all tables for A DAY
    for cat in lst:
        dates=cp.initializeByChecking("F:\Tom\spreadsheet.db",cat[1],str(date))
        #print(dates)

#Adding diff categories as tables i.e., entertainment etc
    for cat in lst:
        ht+=cp.addTable_ss(cat[1],cat[2])
    
#Option to add/delete a category --this is inside form
    ht+='''
    <div align="center">
        <input type="submit" name="addcat" value="+ Add a new category" autocomplete="off">
        <input type="submit" name="delcat" value="- Delete an existing category" autocomplete="off">
    </div>
    '''
#AddAmt to db table [Add]
    if "addAmt" in form:
        for cat in lst:
            amt=int(form.getvalue(cat[1]))
            cp.addAmt("F:\Tom\spreadsheet.db",cat[1],str(date),amt)

#Adding a new category by clicking [+ Add]
    if "addcat" in form:
        ht+='''
        <div align="center"><h3>New Category Details</h3>
        <input type="text" autocomplete="off" name="addcatname" placeholder="Enter category name">
        <br><br>
        Choose a color:<input type="color" name="addcatcolor" placeholder="Enter category color">
        <br><br>
        <input type="submit" name="addcatname_save" value="Save Changes">
        </div>
        '''
        
    if "addcatname_save" in form:
        catName=str(form.getvalue('addcatname')).upper()#making uppercase so that data is not case sensitive
        catColor=str(form.getvalue('addcatcolor'))
        cp.addNewCat("F:\Tom\spreadsheet.db","genre",catName,catColor)
        cur.execute('create table "'+catName+'" (date date,amt float)')
        con.commit()
        ht+=cp.addALine("<a href='spreadsheethome.py'>Click here</a> to apply changes","center","h3")
        
#Deleting an existing category
    if "delcat" in form:
        ht+='''
        <div align="center"><h3>Existing Category Details</h3>
        <input type="text" autocomplete="off" name="delcatname" size="23" placeholder="Enter category name to delete">
        <br><br>
        <input type="submit" name="delcatname_save" value="Save Changes">
        </div>
        '''
    if "delcatname_save" in form:
        catName=str(form.getvalue('delcatname')).upper()#making uppercase so that data is not case sensitive
        cp.delExistCat("F:\Tom\spreadsheet.db","genre",catName)
        con.commit()
        ht+=cp.addALine("<a href='spreadsheethome.py'>Click here</a> to apply changes","center","h3")

#Adding a NOTE line
    ht+=cp.addALine('Click anyone "Add" button to add amount to respective categories','center','h3')

#1-Get All Graphs  2-Scatter graph
    ht+='<div align="center"><input type="submit" name="getallgraphs" value="Get All Graphs">'
    ht+='&emsp;<input type="submit" name="comparegraphs" value="Compare"></div>'

#JS testing -- click1()
    ht+='<div id="test" onclick="click1()">Click to change</div>'
    d=str(datetime.date.today()).split('-')
    yearMonth=d[0]+'-'+d[1]#this will be of the form strftime("%Y-%m")
    
#To display graph -- Get All Graphs clicked
    if "getallgraphs" in form:
        ht+=cp.aggrAllCat("F:\Tom\spreadsheet.db","genre",yearMonth)
        ht+='<div align="center">'
        ht+=cp.iterEachCatInAMonth("F:\Tom\spreadsheet.db","genre")
        ht+='</div>'

#To display scatter graph -- COMPARE clicked
    if "comparegraphs" in form:
        ht+=cp.getCompareGraph("F:\Tom\spreadsheet.db","genre")
        
    ht+=cp.footer1('')#FOOTER  
    print(("<html>"+ht+"</html>").format(**locals()))
#END of HTML
        
except Exception as e:
    print('Error in sshome')
    print(e,e.args)
