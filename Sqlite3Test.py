import sqlite3

connection = sqlite3.connect("CookieCount.db")
cursor=connection.cursor()
CookieList = ["Oatmeal_Raisin", "Chocolate_Chip", "Candy"]
cursor.execute("CREATE TABLE IF NOT EXISTS CookieSheet (species TEXT NOT NULL PRIMARY KEY, current_votes INTEGER, UNIQUE(species, current_votes))")
#for cookie in CookieList:
#	cursor.execute("INSERT OR IGNORE INTO CookieSheet VALUES (?, '1')", [cookie])
#	for x in range(50):
#		cursor.execute(f"UPDATE CookieSheet SET current_votes = current_votes + 100 WHERE species = '{cookie}'")
cursor.execute("UPDATE CookieSheet SET current_votes = 10000 WHERE species = 'Candy'")
shouldbe50 = cursor.execute("SELECT * FROM CookieSheet").fetchall()
print(shouldbe50[0][0])
print(shouldbe50)
c = cursor.execute("SELECT species, current_votes FROM CookieSheet ORDER BY current_votes DESC").fetchall()
print(c)
print(c[0][1])
connection.commit()
connection.close()
