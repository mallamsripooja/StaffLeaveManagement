import cgi
import sqlite3
import datetime
import os
from http.cookies import *
from datetime import timedelta, date
import msvcrt
try:
    con=sqlite3.connect("F:\Tom\pic.db")
    cur=con.cursor()
    form=cgi.FieldStorage()
    data=[]
    msvcrt.setmode(0,os.O_BINARY)
    msvcrt.setmode(1,os.O_BINARY)
    print("Content-Type:text/html\n\n")
    def save_uploaded_file (form_field, upload_dir):
        """This saves a file uploaded by an HTML form.
           The form_field is the name of the file input field from the form.
           For example, the following form_field would be "file_1":
               <input name="file_1" type="file">
           The upload_dir is the directory where the file will be written.
           If no file was uploaded or if the field does not exist then
           this does nothing.
        """
        if not form[form_field]:
            return
        fileitem = form[form_field]
        if not fileitem.file:
            return
        fout = file (os.path.join(upload_dir, fileitem.filename), 'wb')
        while 1:
            chunk = fileitem.file.read(100000)
            if not chunk:
                break
            fout.write (chunk)
        fout.close()
    ht1='''
    <html>
        <body>
        <form method=POST  action="picup.py" enctype="multipart/form-data">
        <input type="text" name="d1" >
        <input type="text" name="d2" >
        <input type="file" name="form_field" accept="image/gif,image/png,image/jpeg" >
        <input type="submit" name="sub" value="Submit" >
        '''
    ht2='''
            </form>
        </body>
    </html>
    '''
    if "sub" in form:
        data=[form.getvalue('d1'),form.getvalue('d2'),form.getvalue('form_field')]
        #print(data)
        cur.execute('insert into pic values(?,?,?)',(form.getvalue('d1'),form.getvalue('d2'),form.getvalue('form_field')))
        con.commit()
        save_uploaded_file ('form_field','F:\Tomcat\apache-tomcat-8.0.26\webapps\test')

    print((ht1+ht2).format(**locals()))
except Exception as err:
    print(err)
