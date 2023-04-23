from flask import Flask, render_template, request
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/user/<username>")
def account(username):
    return render_template('account.html', username = username)

@app.route("/<code>")
def codeError(code):
    return f"Invalid location \'{code}\'"

@app.get("/signin")
def signin():
    return "<script>var test = window.prompt(\'input something\')</script>"

@app.post("/signin")
def signedIn():
    return "signed in!"
