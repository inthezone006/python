from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from example_blueprint import example_blueprint

app = Flask(__name__)
app.register_blueprint(example_blueprint)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://remote:Pencil1@10.0.0.208:3306/FlaskApp'
db=SQLAlchemy(app)


@app.route('/test/')
def getTest():
    return "It works!"

@app.route('/dbtest')
def getDbData():
    result = db.session.execute(text('SELECT * FROM Calendars')).fetchall()
    results = []
    for row in result:
        results.append(row.Name)
    return str(results)

if __name__ == "__main__":
    app.run(debug=True)