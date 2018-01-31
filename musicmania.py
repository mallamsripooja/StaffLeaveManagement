import cgi
from musicmaniaClass import MusicClass as mc
from spreadsheetsCustomizePg import CustomPg as cp
'''<!DOCTYPE html>
<html>
<body>

<audio controls>
  <source src="horse.mp3" type="audio/mpeg">
Your browser does not support the audio element.
</audio>

</body>
</html>
<iframe width="420" height="315"
src="http://www.youtube.com/embed/XGSy3_Czz8k?autoplay=1">
</iframe>
os.listdir('E:\\SONGS\\')#to get songs list'''
#FOR SG SONGS ONLY
try:
    form=cgi.FieldStorage()
    print("Content-Type:text/html\n\n")
    ht='<html><link rel="icon" href="../music.ico" type="image/x-icon">'
    ht+='<script type="text/javascript" src="../main.js" charset="UTF-8"></script>'
    ht+=cp.head1('Music Mania','')
    ht+=cp.heading('Just Music or Nothing')
    ht+='''<div align="center">
    <iframe src="../music.jpg" width="800" height="500" name="iframe_top" frameborder="none" scrolling="no">
    </iframe></div>'''
    #ht+='<audio controls><source src="../SONGS/Malhari.mp3"></audio>'
    ht+=mc.createList('F:\\Tomcat\\apache-tomcat-8.0.26\\webapps\\test\\SG-songs')
    ht+=cp.footer1('footer part')
    ht+='</html>'
    
    print(ht.format(**locals()))
except exception as err:
    print('Found Error in musicmania',err)
