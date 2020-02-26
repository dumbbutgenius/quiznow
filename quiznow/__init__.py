 from flask import Flask, request


 # Set project directory as static directory
 app = Flask(__name__)

 
 # Set app routes

 # Homepage
 @app.route("/")
 def root():
	 return render_template("index.html")


# Redirect user as candidate or administrator
@app.route("/handle_mode", methods = ["POST"])
def mode():