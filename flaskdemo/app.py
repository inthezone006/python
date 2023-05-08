from flask import Flask, render_template, request, jsonify
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

#@app.route("/signup")
#def signedIn():
#    return "user successfully created!"

@app.route("/signup", methods=['PUT'])
def createUser():
    request_body = request.get_json()

    newUser = {
        'name': request_body['name'],
        'age': request_body['age'],
        'job': request_body['job']
    }

    return jsonify(newUser)


if __name__ == "__main__":
    app.run(debug=True)