from flask import Flask, request, render_template, redirect, url_for
import json


# Set project directory as static directory
app = Flask(__name__, template_folder = "templates")

 

count = 0
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

		# Get credentials given by user
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


# Add new questions
@app.route("/questions", methods = ["GET", "POST"])
def add_questions():
	if request.method == "POST":
		# Set default name to avoid 404
		default_name = "0"

		# Get question details
		question = request.form.get("new_question", default_name)
		count = 1
		a = request.form.get("a")
		b = request.form.get("a")
		c = request.form.get("a")
		d = request.form.get("a")
		answer = request.form.get("answer")

		# Construct dictionary for new question
		new_question = {
			"number" : count,
			"question" : question,
			"a" : a,
			"b" : b,
			"c" : c,
			"d" : d,
			"answer" : answer
		}

		# Dump the constructed dictionary to JSON database
		with open("questions.json", "a") as f:
			json.dump(new_question, f)
			f.write("\n")

		# Redirect back to new question page
		return redirect(url_for("questions"))


# Show test taking page
@app.route("/test")
def test():
	# TODO: dump answers to database
	with open("questions.json", "r") as f:
		questions = json.load(f)
	for i in range(count):
		for key, value in questions.items():
			if key == "question":
				question = value
			if key == "a":
				a = value
			if key == "b":
				b = value
			if key == "c":
				c = value
			if key == "d":
				d = value

		return render_template("test.html", question = question, a = a, b = b, c = c, d = d)


# Handle form for test taking page
@app.route("/test", methods = ["GET", "POST"])
def test_form():
	return render_template("test.html")

# TODO: add scoring mechanism