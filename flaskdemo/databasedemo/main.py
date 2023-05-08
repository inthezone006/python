from flask import Flask, render_template
from flask_restful import Api, Resource
import sqlite3

app = Flask(__name__)

api = Api(app)

class Account(Resource):
    def get(self, number, name):
        connection = sqlite3.connect('accounts.db')
        cursor = connection.cursor()

        get_query = "SELECT * FROM accounts WHERE id = ? AND username = ?"

        result = cursor.execute(get_query, (number, name))
        row = result.fetchone()
        connection.close()

        if row:
            return {'account': {'name': row[1], 'number': row[0]}}
        else:
            return "account not found!"
        
    def post(self, number, name):
        connection = sqlite3.connect('accounts.db')
        cursor = connection.cursor()

        push_query = "INSERT INTO accounts VALUES (?, ?)"
        data_to_insert = (number, name)

        cursor.execute(push_query, data_to_insert)
        connection.commit()
        connection.close()

        return {'successfully added': {'number': number, 'name': name}}
        
api.add_resource(Account, '/account/<int:number>/<string:name>')

@app.route("/", methods=['GET'])
def home_page():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)