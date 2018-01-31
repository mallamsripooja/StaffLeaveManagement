import sqlite3
import os
import cgi
import class_GetBillNo as b
import datetime
try:
	global con
	global cur
	bno=b.Bill()
	con=sqlite3.connect("F:\Tom\sh.db")
	cur=con.cursor()
	print('Content-Type:text/html\n\n')
	#datetime.date.today().strftime('%d %b %Y') 
	#%d is the day number
	#%m is the month number
	#%b is the month abbreviation
	#%y is the year last two digits
	#%Y is the all year
	form=cgi.FieldStorage()
	#print(bno.getBillNo()) -- gets the new bill no to add to db
	pattern_tel='[234][0-9]{7}'
	pattern_mob='[789][0-9]{9}'
	ht1='''
		<html>
			<meta http-equiv="refresh">
			<head><title>Home</title></head>
			<body>
				<div>
					<ul>
					<li><a href="shop_home.py">Home</a></li>
					<li><a href="#">Link 2</a></li>
					<li><a href="#">Link 3</a></li>
					</ul>
				</div>
				<form method=POST>
				<table align="center" border=1 id="b1">
					<tr>
						<td>Bill no - '''+str(bno.getBillNo())+'''</td>
						<td>Date - '''+datetime.date.today().strftime('%d %b %Y')+'''</td>
					</tr>
					<tr>
						<td>Name - <input type="text" name="name" autocomplete="off" autofocus></td>
					</tr>
					<tr>
						<td>Contact no - <input type="tel" name="tel" pattern={pattern_tel}
						autocomplete="off" placeholder="Landline"></td>
						<td><input type="text" name="mobile" pattern={pattern_mob}
						autocomplete="off" placeholder="Mobile"></td>
					</tr>
					<tr>
						<td>Care of - <input type="text" name="careof_name"></td>
					</tr>
					<tr>
						<td>No. of Blouses - <input type="number" name="no_blouses" value=0 min=0 max=100></td>
						<td>No. of Dresses - <input type="number" name="no_dresses" value=0 min=0 max=100></td>
					</tr>
				</table>
				</form>
				<table>
					<tr>
						<td align="center" colspan=2><button onclick="b1()">Done</button></td>
					</tr>
				</table>
			</body>
		</html>
		'''
	print(ht1.format(**locals()))
	
except Exception as e:
	print(e)