import sqlite3
import requests
import time

'''begin = time.perf_counter()
requests.post('https://robotsbyryan.com/Cookies/cookiechoice/Oatmeal_Raisin')
requests.post('https://robotsbyryan.com/Cookies/cookiechoice/Candy')
requests.post('https://robotsbyryan.com/Cookies/cookiechoice/Chocolate_Chip')
end = time.perf_counter()
print(f"Done! Time taken: {end-begin:.4f} seconds") #https://realpython.com/python-timer/
'''
connection = sqlite3.connect("CookieCount.db")
cursor=connection.cursor()
'''list = ['Oreo']#["Strawberry", "Falafel", "MandM", "Reeses", "Chocolate Chip"]
for cookie in list:
	cursor.execute("DELETE FROM CookieSheet WHERE species = ?", [cookie]) 
'''
shouldbe50 = cursor.execute("SELECT * FROM CookieSheet").fetchall()
connection.commit()
connection.close()
print(shouldbe50)
