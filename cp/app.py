import pymysql.cursors
from flask import Flask, render_template, request, redirect, flash
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def goHome():
    usersArray = []
    if request.method == "GET":
        connection = pymysql.connect(host=os.environ.get("hostname"),
                     user=os.environ.get("user"),
                     password=os.environ.get("password"),
                     database=os.environ.get("database"),
                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                sql = "SELECT Username FROM Accounts"
                cursor.execute(sql)
                result = cursor.fetchall()
                for entry in result:
                    usersArray.append(entry['Username'])
        except:
            return render_template('index.html', status="Error", usersList=usersArray)
        finally:
            connection.close()
            return render_template('index.html', status="Success", usersList=usersArray)
    
    if request.method=="POST":
        connection = pymysql.connect(host='10.0.0.208',
                     user='remote',
                     password='Pencil1',
                     database='FlaskApp',
                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                un = request.form['selectUser']
                pw = request.form['pass']
                sql = "SELECT Password FROM Accounts WHERE USERNAME=%s"
                cursor.execute(sql, (un))
                result = cursor.fetchone()
                if pw == result['Password']:
                    return render_template('account.html', user=un, status="Success")
                else:
                    return render_template('index.html', status="Success", usersList=usersArray)
        except:
            return render_template('index.html', status="Error", usersList=usersArray)
        finally:
            connection.close()
        
@app.route('/create', methods=['POST', 'GET'])
def createAccount():
    if request.method=="GET":
        return render_template('creation.html')
    else:
        return "POST request recieved."

if __name__ == "__main__":
    app.run(debug=True)