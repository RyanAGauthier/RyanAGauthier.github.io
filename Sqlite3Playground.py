import sqlite3
import requests
import time

begin = time.perf_counter()
requests.post('http://54.176.96.251/Cookies/cookiechoice/Oatmeal_Raisin')
requests.post('http://54.176.96.251/Cookies/cookiechoice/Candy')
requests.post('http://54.176.96.251/Cookies/cookiechoice/Chocolate_Chip')
end = time.perf_counter()
print(f"Done! Time taken: {end-begin:.4f} seconds") #https://realpython.com/python-timer/
connection = sqlite3.connect("CookieCount.db")
cursor=connection.cursor()
#cursor.execute("UPDATE CookieSheet SET current_votes = 0 WHERE species = 'MandM'") 
shouldbe50 = cursor.execute("SELECT * FROM CookieSheet").fetchall()
connection.commit()
connection.close()
print(shouldbe50)
