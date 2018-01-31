import sqlite3
class Bill:
	def __init__(self):
		self.con=sqlite3.connect("F:\Tom\sh.db")
		self.cur=self.con.cursor()
		self.cur.execute('select * from bill order by bno')
		self.bno=self.cur.fetchall()[-1][0]
	def getBillNo(self):
		return self.bno

b=Bill()
print(b.getBillNo())
