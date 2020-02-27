from flask import Flask, request, render_template, redirect, url_for
import json


# Set project directory as static directory
app = Flask(__name__, template_folder = "templates")

 
# Set app routes

# Homepage
@app.route("/")
def root():
	return render_template("index.html")


# Redirect user as candidate or administrator
@app.route("/", methods = ["GET", "POST"])
def mode_redirect():
	if request.method == "POST":
		# Set default value to avoid 404
		default_name = "0"

		selected = request.form.get("mode", default_name)

		# Redirect candidates to test taking page
		if selected == "candidate":
			return redirect(url_for("test"))
		# Redirect administrators to admin page
		elif selected == "admin":
			return redirect(url_for("admin_show"))


# Show admin login
@app.route("/admin")
def admin_show():
	return render_template("admin.html")


# Show page to add questions
@app.route("/questions")
def questions():
	return render_template("questions.html")


# Show invalid login attempt
@app.route("/invalid")
def invalid():
	return render_template("invalid.html")


# Handle admin login
# TODO: add real authentication
@app.route("/admin", methods = ["GET", "POST"])
def admin_handle():
	if request.method == "POST":
		# Set default name to avoid 404
		default_name = "0"

		username = request.form.get("username", default_name)
		password = request.form.get("password", default_name)

		with open("creds.json", "r") as f:
			creds = json.load(f)
		username_real = creds["admin"][0]
		password_real = creds["admin"][1]

		if username == username_real and password == password_real:
			return redirect(url_for("questions"))
		else:
			return redirect(url_for("invalid"))