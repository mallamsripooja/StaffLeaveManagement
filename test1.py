#!/usr/bin/env python
import cgi, os
import cgitb; cgitb.enable()

try:
    # Windows needs stdio set for binary mode. 
    import msvcrt
    msvcrt.setmode (0, os.O_BINARY) # stdin  = 0
    msvcrt.setmode (1, os.O_BINARY) # stdout = 1
except ImportError:
    pass

form = cgi.FieldStorage()

print("Content-Type: text/html\n");
h1='''
<html><body>
<form enctype="multipart/form-data" action="test.py" method="post">
<p>File: <input type="file" name="file_img"></p>
<p><input type="submit" value="Upload"></p>
</form>
</body></html>'''

print(h1.format(**locals()))

# A nested FieldStorage instance holds the file

if 'file_img' in form:

    fileitem = form['file_img']

# Test if the file was uploaded
    if fileitem.filename:
     
   
   # strip leading path from file name to avoid directory traversal attacks
        fn = os.path.basename(fileitem.filename)
        open('../../' + fn, 'wb').write(fileitem.file.read())
        message = 'The file "' + fn + '" was uploaded successfully'
   
    else:
        message = 'No file was uploaded'
   

print("""
<p>%s</p>
"""% (message))

'''
   # strip leading path from file name to avoid directory traversal attacks
        fn = os.path.basename(fileitem.filename)
        open('files/' + fn, 'wb').write(fileitem.file.read())
        message = 'The file "' + fn + '" was uploaded successfully'''

