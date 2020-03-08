from flask import Flask, request, render_template, redirect, url_for
import json


# Set project directory as static directory
app = Flask(__name__, template_folder = "templates")

 
lines = 1
# Set app routes

@app.route("/")
def root():
	"""Homepage"""

	return render_template("index.html")


@app.route("/", methods = ["GET", "POST"])
def mode_redirect():
	"""Redirect user as candidate or administrator"""

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


@app.route("/admin")
def admin_show():
	"""Show admin login"""

	return render_template("admin.html")


@app.route("/questions")
def questions():
	"""Show page to add questions"""

	return render_template("questions.html")


@app.route("/invalid")
def invalid():
	"""Show invalid login attempt"""

	return render_template("invalid.html")


# TODO: add real authentication
@app.route("/admin", methods = ["GET", "POST"])
def admin_handle():
	"""Handle admin login"""

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


@app.route("/questions", methods = ["GET", "POST"])
def add_questions():
	"""Add new questions"""

	if request.method == "POST":
		# Set default name to avoid 404
		default_name = "0"

		# Get question details
		question = request.form.get("new_question", default_name)
		count = 1
		a = request.form.get("a", default_name)
		b = request.form.get("a", default_name)
		c = request.form.get("a", default_name)
		d = request.form.get("a", default_name)
		answer = request.form.get("answer", default_name)

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


@app.route("/test")
def test():
	"""Show test taking page"""

	# TODO: dump answers to database
	with open("questions.json", "r") as f:
		questions = json.load(f)
	for i in range(lines):
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


answer_count = 1
@app.route("/test", methods = ["GET", "POST"])
def test_form():
	"""Handle form for test taking page"""

	if request.method == "POST":
		# Set default name to avoid 404
		default_name = "0"

		# Get answer
		answer = request.form.get("answer", default_name)
		response = {
			"number" : count,
			"answer" : answer
		}
		with open("answers.json", "w") as f:
			json.dump(response, f)
			f.write("\n")
		answer_count += 1
	return render_template("test.html")

# TODO: add scoring mechanism