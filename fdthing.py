from tkinter import *#for gui
import cgi
import sqlite3
import datetime
from dateutil.relativedelta import relativedelta
from spreadsheetsCustomizePg import CustomPg as cp
try:
    #http://localhost:8080/test/cgi-bin/fdthing.py
    def fetch():
        #print('Input -> '+ent.get())
        if (ent.get()=='6656'):#correct password
            root.destroy()
            
            con=sqlite3.connect("F:\Tom\post.db")
            cur=con.cursor()

            form=cgi.FieldStorage()
            print('Content-Type:text/html\n\n')
            #<HEAD part>
            headPart='<link rel="icon" href="../spreadsheet.ico" type="image/x-icon">'#did not link a stylesheet
            headPart+='<script type="text/javascript" src="../fdthing.js" charset="UTF-8"></script>'
            ht=cp.head1('FD-Details',headPart)#HEAD
            
            ht+=cp.heading('Your information is safe here!')#PAGE TITLE-BODY tag opening

            ht+='''<br><table align="center" border=1 width="90%">'''#starting table
            #can also use- PRAGMA table_info(table_name) to fetch column names
            ht+='''<tr>
            <td align="center"><b>S.No</b></td>
            <td align="center"><b>Deposited Amount</b></td>
            <td align="center"><b>Years</b></td>
            <td align="center"><b>Names</b></td>
            <td align="center"><b>Deposit date</b></td>
            <td align="center"><b>Interest Amount</b></td>
            <td align="center"><b>A/C no.</b></td>
            <td align="center"><b>No. of books</b></td>
            <td align="center"><b>Area</b></td>
            <td align="center"><b>Deposit type</b></td>
            <td align="center"><b>Agent Bonus</b></td>
            <td align="center"><b>Postoffice bonus</b></td>
            <td align="center"><b>Maturity date</b></td>
            </tr>'''
            #fetching data from deposit table
            cur.execute('select * from fddetails')
            lst=cur.fetchall()
            #print(lst)
            for row in lst:
                if row[9]=='r':#if deposit type is 'r' - change row color
                    ht+='''
                    <tr bgcolor="#00FF00">'''
                else:
                    ht+='''
                    <tr>'''
                #calculating maturity date
                todt=datetime.datetime.strptime(row[4],'%Y-%m-%d')+relativedelta(years=int(row[2]))
                fromdt=datetime.datetime.strptime(row[4],'%Y-%m-%d')

                #displaying details in a table
                for i in range(12):
                    if i==4:#only to change format of deposit date
                        ht+='''<td align="center">'''+str(fromdt.strftime('%d-%m-%Y'))+'''</td>'''
                    else:
                        ht+='''<td align="center">'''+str(row[i])+'''</td>'''
                ht+='''<td align="center">'''+str(todt.strftime('%d-%m-%Y'))+'''</td>'''
                ht+='''
                </tr>
                '''
            ht+='''</table>'''#end of table

            ht+='''<br><br><div align="center"><button onclick="createTable()">+ New Entry</button></div>'''

            if "add_entry" in form:
                print('hi')
            
            ht+=cp.footer1('')#FOOTER  
            print('<html>'+ht+'</html>'.format(**locals()))
            #END of HTML
            
        else:#Incorrect password
            root.destroy()
            print('Content-Type:text/html\n\n')
            #<HEAD part>
            headPart='<link rel="icon" href="../spreadsheet.ico" type="image/x-icon">'#did not link a stylesheet
            headPart+='<script type="text/javascript" src="../fdthing.js" charset="UTF-8"></script>'
            ht=cp.head1('FD-Details',headPart)#HEAD

            ht+=cp.heading('Incorrect password<br><a href="fdthing.py" style="text-decoration:none;">Try again</a>')#PAGE TITLE-BODY tag opening
            
            ht+=cp.footer1('')#FOOTER  
            print('<html>'+ht+'</html>'.format(**locals()))
            #END of HTML

    #Displaying login window before displaying HTML content (SECURITY-LOGIN)
    root=Tk()
    lab=Label(root,text="Enter password")
    ent=Entry(root,show="*")
    #ent.insert(0,'Type words here')
    lab.pack()
    ent.pack(side=TOP,fill=X)
    ent.focus()
    ent.bind('<Return>',(lambda event: fetch()))
    btn=Button(root,text='Verify',command=fetch)
    btn.pack(side=BOTTOM)
    
    #to display the window above all other windows
    root.attributes("-topmost", True)

    #setting window postion - where it should open
    w = 300 # width for the Tk root
    h = 80 # height for the Tk root

    # get screen width and height
    ws = root.winfo_screenwidth() # width of the screen
    hs = root.winfo_screenheight() # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    # set the dimensions of the screen 
    # and where it is placed
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    root.title('Verification')
    root.mainloop()

except Exception as err:
    print(err)
