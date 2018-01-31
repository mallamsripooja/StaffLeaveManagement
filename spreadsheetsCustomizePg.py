import cgi
import math
import sqlite3
import datetime
import numpy as np
import matplotlib.pyplot as plt
class CustomPg:
    
    #only head tags
    def head():
        ht='''<head></head>'''
        return ht

    #only footer tags
    def footer():
        ht='''<footer></footer>'''
        return ht
    
    #head tags with content
    def head1(title,content):
        ht='''<head>
        <title>
        '''+title+'''
        </title>
        '''+content+'''
        </head>'''
        return ht

    #footer tags with content -- CLOSES BODY,FORM TAG
    def footer1(content):
        ht='''</form></body><footer>'''+content+'''</footer>'''
        return ht

    #Page Heading -- OPENS BODY,FORM TAG
    def heading(heading):
        ht='''<body><div align="center"><h1>
        '''+heading+'''
        </h1></div><form method=POST>'''
        return ht

    #Add a line
    def addALine(content,align,font):
        ht='''<div align="'''+align+'''"><'''+font+'''>'''+content+'''</'''+font+'''></div>'''
        return ht

    #Adding tables
    def addTable_ss(name,color):
        ht='''<table width=70% align="center" border=0>
        <tr>
        <td bgcolor="'''+color+'''" width=60%>&emsp;'''+name+'''</td>
        <td>
             Rupees&nbsp;:&nbsp;<input type="number" value=0 min=0 name="'''+name+'''">
             &emsp;
             <input type="submit" name="addAmt" value="Add">
        </td>
        </tr> 
        </table>'''
        return ht

    #Getting fields from a particular table in DATABASE
    def getFieldsfromTable_ss(filePath,tableName):
        con=sqlite3.connect(filePath)
        cur=con.cursor()
        cur.execute('select * from "'+tableName+'" where id>100')
        data=cur.fetchall()
        con.close()
        return data

    #Initialize amt=0 in the table
    def initializeByChecking(filePath,tableName,date):
        con=sqlite3.connect(filePath)
        cur=con.cursor()
        #checking if a date is already there or not
        cur.execute('select date from "'+tableName+'" where date="'+date+'"')
        data=cur.fetchall()
        
        if len(data)==0:#if that date is NOT there
            cur.execute('insert into "'+tableName+'" values("'+date+'",0)')

        #there is no else as the requirement is satisfied
        con.commit()
        con.close()
        
    #Adding amt to a particular table
    def addAmt(filePath,tableName,date,amt):
        con=sqlite3.connect(filePath)
        cur=con.cursor()
        cur.execute('update "'+tableName+'" set amt=amt+'+str(amt)+' where date="'+date+'"')
        con.commit()
        con.close()

    #Add a new category
    def addNewCat(filePath,tableName,catName,catColor):
        con=sqlite3.connect(filePath)
        cur=con.cursor()
        cur.execute('select max(id) from genre')
        data=int(cur.fetchall()[0][0])+1
        cur.execute('insert into "'+tableName+'" values ('+str(data)+',"'+catName+'","'+catColor+'")')
        con.commit()
        con.close()

    #Del an existing category    
    def delExistCat(filePath,tableName,catName):
        con=sqlite3.connect(filePath)
        cur=con.cursor()
        cur.execute('drop table "'+catName+'"')
        cur.execute('delete from "'+tableName+'" where category="'+catName+'"')
        con.commit()
        con.close()

    #Aggregate of each category
    def aggrAllCat(filePath,tableName,yearMonth):
        con=sqlite3.connect(filePath)
        cur=con.cursor()
        data=CustomPg.getFieldsfromTable_ss(filePath,tableName)
        catNames=[cat[1] for cat in data]#linear expressions
        catColors=[cat[2] for cat in data]
        aggrData=[]
        for cat in data:
            cur.execute('select sum(amt) from "'+cat[1]+'" where strftime("%Y-%m",date)="'+yearMonth+'"')
            amt=cur.fetchall()[0][0]
            aggrData.append(amt)
        con.close()
        y_pos=np.arange(len(catNames))
        plt.xticks(y_pos,catNames)#, ha='right', rotation=45--to rotate the labels
        plt.xlabel('Categories')
        plt.ylabel('Rupees')
        plt.title(yearMonth+' view of all categories')
        plt.bar(y_pos,aggrData,width=.3,color=catColors,align='center')
        for i in range(len(catNames)):
            if aggrData[i]!=0:
                plt.text(i,aggrData[i]+50,int(aggrData[i]),ha='center',va='bottom')
        plt.savefig("../../myMonthlyPythonPlot.png")#everytime this function is called the plt.savefig() REPLACES the old image
        ht='<div align="center" style="width:700px height:700px; overflow:hidden;">'
        ht+='<img src="../myMonthlyPythonPlot.png" alt="No image" width="700px" height="auto">'
        ht+='</div>'#returning IMAGE from here
        plt.close()
        return ht

    #months vs amt for each category
    def iterEachCatInAMonth(filePath,tableName):
        date=datetime.date.today()
        con=sqlite3.connect(filePath)
        cur=con.cursor()
        data=CustomPg.getFieldsfromTable_ss(filePath,tableName)
        months=['01','02','03','04','05','06','07','08','09','10','11','12']
        m=['Jan','Feb','Mar','Apr','May','June','July','Aug','Sept','Oct','Nov','Dec']
        M=[1,2,3,4,5,6,7,8,9,10,11,12]
        ht=''
        for cat in data:
            Data=[]
            for month in months:
                cur.execute('select sum(amt) from "'+cat[1]+'" where strftime("%m-%Y",date)="'+month+'-'+str(date.year)+'"')
                d2=cur.fetchall()[0][0]
                #print(cat[1],month+'-'+str(date.year),d2)
                #print("\n")
                if d2!=None:
                    Data.append(math.ceil(d2))
                else:
                    Data.append(0)
            #print(cat[1],Data,print(type(Data)))
            plt.title(cat[1])
            plt.ylabel('Rupees')
            plt.ylim([0,5000])
            plt.xticks(M,m)
            plt.bar(M,Data,color=cat[2],align='center')
            #u"\u20B9" -- code for indian rupee
            for i in range(12):
                if Data[i]!=0:
                    plt.text(M[i],Data[i]+50,Data[i],ha='center',va='bottom')
            plt.savefig('../../'+cat[1]+'.png')
            ht+='<div align="center" style="width:660px height:660px; overflow:hidden; float:left;">'
            ht+='<img src="../'+cat[1]+'.png" alt="No image" width="660px" height="auto">'
            ht+='</div>'
            plt.close()
        con.close()
        return ht

    def getCompareGraph(filePath,tableName):
        date=datetime.date.today()
        con=sqlite3.connect(filePath)
        cur=con.cursor()
        data=CustomPg.getFieldsfromTable_ss(filePath,tableName)
        months=['01','02','03','04','05','06','07','08','09','10','11','12']
        m=['Jan','Feb','Mar','Apr','May','June','July','Aug','Sept','Oct','Nov','Dec']
        M=[1,2,3,4,5,6,7,8,9,10,11,12]
        ht=''
        X=[]
        for cat in data:
            x=[]
            for month in months:
                cur.execute('select sum(amt) from "'+cat[1]+'" where strftime("%m-%Y",date)="'+month+'-'+str(date.year)+'"')
                d2=cur.fetchall()[0][0]
                if d2!=None:
                    x.append(math.ceil(d2))
                else:
                    x.append(0)
            X.append(x)
            
        for i in range(len(X)):
            plt.plot(M,X[i],data[i][2],marker='o')
        
        plt.xticks(M,m)
        plt.legend([cat[1] for cat in data])#linear expression
        plt.savefig('../../myCompareGraph.png')
        ht+='<div align="center" style="width:660px height:660px; overflow:hidden;">'
        ht+='<img src="../myCompareGraph.png" alt="No image" width="660px" height="auto">'
        ht+='</div>'
        plt.close()
        con.close()
        return ht
        
'''
    first_day = date.replace(day = 1)
    last_day = date.replace(day = calendar.monthrange(date.year, date.month)[1])
    return first_day, last_day
'''

            
