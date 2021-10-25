from flask import Flask, send_from_directory, request, send_file, jsonify, make_response
from markupsafe import escape
import sqlite3

connection = sqlite3.connect(":memory:")
app = Flask(__name__)
connection = sqlite3.connect("CookieCount.db")
cursor=connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS CookieSheet (species TEXT NOT NULL PRIMARY KEY, current_votes INTEGER, UNIQUE(species, current_votes))")

@app.route("/")
def hello_world():
	return "<p>Hello, World!</p>"

@app.route("/cookies")
def display_cookies():
	return "Delicious cookies here soon!"

@app.route("/path/<path:subpath>")
def return_image(subpath):
	#return "COOKIE PLZ"
	#return send_file('static/Cookies/cookie300.png')
	return send_from_directory('static/Cookies', f'{escape(subpath)}')

@app.route("/cookiechoice/<string:cookiechoice>")
def update_baking_sheet(cookiechoice):
	cursor.execute("INSERT OR IGNORE INTO CookieSheet VALUES (?, '1')", [cookiechoice])
	cursor.execute("UPDATE CookieSheet SET current_votes = current_votes + 1 WHERE species = ?", [cookiechoice])
	connection.commit()
	return make_response('nice', 200) #https://stackoverflow.com/questions/26079754/flask-how-to-return-a-success-status-code-for-ajax-call

@app.route("/topcookies")
def current_favorites():
	c = cursor.execute("Select species, current_votes FROM CookieSheet ORDER BY current_votes DESC").fetchall()
	_cookie1 = c[0][0]
	_cookie1count = c[0][1]
	_cookie2 = c[1][0]
	_cookie2count = c[1][1]
	_cookie3 = c[2][0]
	_cookie3count = c[2][1]
	bigdict = {"cookie1":{"name":_cookie1,"count":_cookie1count},"cookie2":{"name":_cookie2,"count":_cookie2count},"cookie3":{"name":_cookie3,"count":_cookie3count}}
	return make_response(jsonify(rankedcookies=bigdict), 200)