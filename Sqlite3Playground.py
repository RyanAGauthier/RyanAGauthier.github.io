import sqlite3
import requests
import time

begin = time.perf_counter()
for i in range (500):
    requests.get('http://54.176.96.251/cookiechoice/Oreo')
end = time.perf_counter()
print(f"Done! Time taken: {end-begin:.4f} seconds") #https://realpython.com/python-timer/
connection = sqlite3.connect("CookieCount.db")
cursor=connection.cursor()
cursor.execute("UPDATE CookieSheet SET current_votes = 0 WHERE species = 'MandM'") 
shouldbe50 = cursor.execute("SELECT * FROM CookieSheet").fetchall()
connection.commit()
connection.close()
print(shouldbe50)
