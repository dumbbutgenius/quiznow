from flask import Flask, request


# Set project directory as static directory
app = Flask(__name__)

 
# Set app routes

# Homepage
@app.route("/")
def root():
	return render_template("index.html")


# Redirect user as candidate or administrator
@app.route("/", methods = ["POST"])
def mode_redirect():
	if request.method == "POST":
		# Set default value to avoid 404
		default_name = '0'

		selected = request.form.get("mode", default_name)

		# Redirect candidates to test taking page
		if selected == "candidate":
			return redirect(url_for("test.html"))
		# Redirect administrators to admin page
		elif selected == "admin":
			return redirect(url_for("admin.html"))