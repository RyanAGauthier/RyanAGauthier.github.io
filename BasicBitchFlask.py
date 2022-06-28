from flask import Flask, send_from_directory, request, send_file, jsonify, make_response, redirect
from markupsafe import escape
import sqlite3

#connection = sqlite3.connect(":memory:")
app = Flask(__name__)
connection = sqlite3.connect("CookieCount.db")
cursor=connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS CookieSheet (species TEXT NOT NULL PRIMARY KEY, current_votes INTEGER, UNIQUE(species, current_votes))")

#@app.route("/")
#def hello():
#	return redirect("https://robotsbyryan.com/Cookies", code=302)

@app.route("/")
def hello_world():
	return send_from_directory('static/', 'index.html')

@app.route("/Cookies/")
def cookies():
	return send_from_directory('static/Cookies', 'index.html');

@app.route("/cookies")
def display_cookies():
	return "Delicious cookies here soon!"

@app.route("/assets/<path:subpath>")
def return_assets(subpath):
	return send_from_directory('static/assets', escape(subpath))

#@app.route("/images/<path:subpath>")
#def temp_return_images(subpath):
#	pass

@app.route("/Cookies/<path:subpath>")
def return_file(subpath):
	#return "COOKIE PLZ"
	#return send_file('static/Cookies/cookie300.png')
	return send_from_directory('static/Cookies', escape(subpath))

@app.route('/Cookies/cookiechoice/', methods=['POST'])
def submit_cookie_choice():
        if "cookie" in request.headers:
                if "cookiechoice" in request.headers['cookie']:
                        if request.cookies.get('cookiechoice') in ["Chocolate_Chip", "Candy", "Oatmeal_Raisin"]:
                                cursor.execute("UPDATE CookieSheet SET current_votes = current_votes + 1 WHERE species = ?", [request.cookies.get('cookiechoice')])
                                connection.commit()                                                                                                                                                                                                
                                response = make_response()                                                                                                                                                                                         
                                response.status_code = 200
                                return response
        return make_response('failed', 400)


@app.route('/Cookies/cookiechoice/<string:cookiechoice>', methods=['POST'])
def update_baking_sheet(cookiechoice):
	if cookiechoice in ["Chocolate_Chip", "Candy", "Oatmeal_Raisin"]:
		cursor.execute("INSERT OR IGNORE INTO CookieSheet VALUES (?, '1')", [cookiechoice])
		cursor.execute("UPDATE CookieSheet SET current_votes = current_votes + 1 WHERE species = ?", [cookiechoice])
		connection.commit()
		response = make_response()
		response.status_code = 200
		return response #https://stackoverflow.com/questions/26079754/flask-how-to-return-a-success-status-code-for-ajax-call

@app.route("/Cookies/topcookies")
def current_favorites():
	#print("Forwarded IPS: " + request.headers['X-Forwarded-For'])
	#print("Connecting IPS: " + request.headers['CF-Connecting-IP'])
	c = cursor.execute("Select species, current_votes FROM CookieSheet ORDER BY current_votes DESC").fetchall()
	_cookie1 = c[0][0]
	_cookie1count = c[0][1]
	_cookie2 = c[1][0]
	_cookie2count = c[1][1]
	_cookie3 = c[2][0]
	_cookie3count = c[2][1]
	bigdict = {"cookie1":{"name":_cookie1,"count":_cookie1count},"cookie2":{"name":_cookie2,"count":_cookie2count},"cookie3":{"name":_cookie3,"count":_cookie3count}}
	return make_response(jsonify(rankedcookies=bigdict), 200)

if __name__ == "__main__":
    app.run()
