# Database Design (name: research_buddy)
# accounts (Holds all accounts) - unique_index[username, password], index[id]
# (PK, INT) id
# (NOT NULL, UNIQUE, VARCHAR(255)) username
# (NOT NULL, VARCHAR(255)) password
# (NOT NULL, VARCHAR(255)) first
# (NOT NULL, VARCHAR(255)) last
# (NOT NULL, VARCHAR(255)) email 
# (VARCHAR(255)) resume
# (VARCHAR(255)) linkedin
# (FK departments_id REFERENCES departments.id, INT) department_id
# (NOT NULL, CONSTRAINT CHK_STATUS CHECK (status='admin' OR status='professor' OR status='student'), VARCHAR(9)) status
#
# admin (Has master control over accounts, projects, and departments) - 
# (PK, FK admin_id REFERENCES accounts.id, INT) id
# 
# professors (Puts up projects) - index[id]
# (PK, FK professor_id REFERENCES accounts.id, INT) id
# (VARCHAR(255)) website
# (NOT NULL, CONSTRAINT CHK_STATUS CHECK (status='assistant' OR status='associate' OR status='full'), VARCHAR(9)) status
#
# students (Signs up for projects) - index[id]
# (PK, FK student_id REFERENCES accounts.id, INT) id
# (NOT NULL, CONSTRAINT CHK_STATUS CHECK (status='undergraduate' OR status='graduate'), VARCHAR(13)) status
# 
# departments (Holds all departments (majors), editable by the admin) - index[id]
# (PK, INT) id
# (NOT NULL, UNIQUE, VARCHAR(255)) name
# 
# projects (Holds all projects) - index[id]
# (PK, INT) id
# (NOT NULL, UNIQUE, VARCHAR(255)) title
# (NOT NULL, VARCHAR(255)) description
# (NOT NULL, FK projects_department_id REFERENCES departments.id, INT) department_id
# (NOT NULL, VARCHAR(255)) link
# (NOT NULL, FK projects_professor_id REFERENCES professors.id, INT) professor_id
# (NOT NULL, CONSTRAINT CHK_STATUS CHECK (status='open' OR status='closed' OR status='paused'), VARCHAR(9)) status
# 
# projectsrel (Holds all projects that a student is part of) - 
# (PK, FK projectsrel_student_id REFERENCES students.id, INT) student_id
# (PK, FK projectsrel_project_id REFERENCES projects.id, INT) project_id
# 
# accounts_departments (For referencing users and the departments that they are a part of) - 
# (PK, FK accounts_departments_department_id REFERENCES departments.id, INT) department_id
# (PK, FK accounts_departments_account_id REFERENCES accounts.id, INT) account_id
#
# projects_departments (For referencing projects and the departments that it is a part of) - 
# (PK, FK projects_departments_department_id REFERENCES departments.id, INT) department_id
# (PK, FK projects_departments_projects_id REFERENCES projects.id, INT) projects_id
# 
# requirements (For all the possible requirements a student/project can have) - index[id]
# (PK, INT) id
# (NOT NULL, VARCHAR(255)) title
# (NOT NULL, VARCHAR(255)) description
# (FK requirements_department_id REFERENCES departments.id, INT) department_id
#
# student_requirements (For all the requirements a student has; implement that all students are at least a student) -
# (PK, FK student_requirements_requirement_id REFERENCES requirements.id, INT) requirement_id
# (PK, FK student_requirements_student_id REFERENCES students.id, INT) student_id
# 
# project_requirements (For all the requirements a project has) -
# (PK, FK project_requirements_requirement_id REFERENCES requirements.id, INT) requirement_id
# (PK, FK project_requirements_project_id REFERENCES projects.id, INT) project_id
# 
# status_code - index[id]
# (PK, INT) id
# (NOT NULL, INT) admin
# (NOT NULL, INT) professor
# (NOT NULL, INT) student

# TODO: Get screenshots for each demo
# TODO: User interface must populate data from the database dynamically (e.g., cannot just hardcode the data) 
# and must show in demo
# TODO: Use valid indices (with queries and must be meaningful with valid justification) and create index report
# TODO: Use two database access methods
# TODO: Allow for users/projects to be part of multiple departments
# TODO: Discussion of transactions, concurrent access to data, and choice of isolation levels
# TODO: Requirement 1: An interface that allows users to add, edit, and delete data in one main table (edit account)
# TODO: Requirement 2: A report interface that allows a user (admin) to select which data to 
# display in report (admin: report all users, professors: report all projects)
# TODO: Use session.pop('username', None); if 'user_id' in session:; return redirect(url_for('signin'))

from flask import Flask, request, render_template, redirect, url_for, session
import mysql.connector
import json

with open('research_buddy/config.json') as config_file:
    db_config = json.load(config_file)
cnx = mysql.connector.connect(**db_config)
cursor = cnx.cursor()

app = Flask(__name__)

@app.route("/")
def main():
    return redirect(url_for('home'))

@app.route("/home")
def home():
    return "<title>Home</title>" \
    "<center><h1>Research Buddy</h1>" \
    "<p>Please <a href='/signin'>sign in</a> to continue or " \
    "<a href='/signup'>create an account</a>.</p></center>"
    
@app.route("/signin", methods=['GET', 'POST'])    
def signin():
    if request.method == 'GET':
        return "<title>Sign In</title><button onclick='history.back()'><<</button>" \
        "<center><h1>Sign In</h1><p><form method='POST'>Username: <input type='text' name='username'>" \
        "<br><br>Password: <input type='password' name='password' required>" \
        "<br><br><button type='submit'>Submit</button></form></p></center>"
    
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        session['username'] = username
        return f"({username}, {password})"
    

@app.route("/signup", methods=['GET', 'POST'])    
def signup():
    return "<title>Sign Up</title><button onclick='history.back()'><<</button><h1>Sign Up</h1>"

if __name__=="__main__":
    app.run(debug=True)