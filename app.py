from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST']='10.0.0.208'
app.config['MYSQL_USER']='app_user'
app.config['MYSQL_PASSWORD']='Pencil1'
app.config['MYSQL_DB']='FlaskApp'

mysql = MySQL(app)


@app.route('/')
def form():
    return render_template('form.html')

@app.route('/signup', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return "Please signup via the signup form."
    elif request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO Accounts VALUES (%s, %s)''', (name, password))
        mysql.connection.commit()
        cursor.close()
        return f'Done!!'
    

if __name__ == '__main__':
    app.run(debug=True)