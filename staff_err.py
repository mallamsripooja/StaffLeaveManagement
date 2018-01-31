import cgi
import math
import sqlite3
import datetime
import os
import calendar
from http.cookies import *
from datetime import timedelta, date
print("Content-Type:text/html\n\n")
ht1='''
                <html>
                    <head>
        <link rel="icon" href="../favicon.ico" type="image/x-icon">
                    <link rel="stylesheet" type="text/css" href="../style.css" />
                    <title>Leave Form</title>
                    <table width="100%" bgcolor="black">
                        <tr>
                        <td width="10%"><img src="../logo.jpg" alt="img" height="130" width="148" ></td>
                        <td width="90%"><img src="../clg4.jpg" alt="img" height="130" width="1170" ></td>
                    </tr>
                    </table>
                    </head>
                    <body><br><br><br><br><br><br><br>
            <table align="center" height=30%>
                <tr>
                    <td style="font-family:Tahoma;font-size:24px;">Oops! Seems like something is wrong</td>
                </tr>
                <tr>
                    <td align="center"><a href="stafflogin.py" style="text-decoration: none;font-family:Tahoma;font-size:24px;">Login Again</a></td>
                </tr>
                </table>
                    </body><br><br><br><br><br><br><br><br>
      <footer>
            <table style="width:100%;" align="center">
                <tr>
                    <td style="width:33%;text-align:center;font-size:18px;">3-5-1026, Narayanguda, Hyderabad, Telangana -500029</td>
                    <td style="width:33%;text-align:center;font-size:18px;">&emsp;&emsp;&emsp;Copyright &#169; KMIT</td>
                    <td style="width:33%;text-align:center;font-size:18px;">&emsp;&emsp;&emsp;Website:    <a href="http://www.kmit.in/" style="text-decoration:none"/>kmit.in</td>
                </tr>
            </table>
        </footer>
    </html>'''
print(ht1.format(**locals()))
