# Database Design (name: research_buddy)
# accounts (Holds all accounts) - unique_index[username, password], index[id]
# (PK, INT) id
# (NOT NULL, UNIQUE, VARCHAR(35)) username
# (NOT NULL, VARCHAR(35)) password
# (NOT NULL, VARCHAR(35)) first
# (NOT NULL, VARCHAR(35)) last
# (NOT NULL, VARCHAR(35)) email 
# (VARCHAR(35)) resume
# (VARCHAR(35)) linkedin
# (FK departments_id REFERENCES departments.id, INT) department_id
# (NOT NULL, CONSTRAINT CHK_STATUS CHECK (status='admin' OR status='professor' OR status='student'), VARCHAR(9)) status
#
# admin (Has master control over accounts, projects, and departments) - 
# (PK, FK admin_id REFERENCES accounts.id, INT) id
# 
# professors (Puts up projects) - index[id]
# (PK, FK professor_id REFERENCES accounts.id, INT) id
# (VARCHAR(35)) website
# (NOT NULL, CONSTRAINT CHK_STATUS CHECK (status='assistant' OR status='associate' OR status='full'), VARCHAR(9)) status
#
# students (Signs up for projects) - index[id]
# (PK, FK student_id REFERENCES accounts.id, INT) id
# (NOT NULL, CONSTRAINT CHK_STATUS CHECK (status='undergraduate' OR status='graduate'), VARCHAR(13)) status
# 
# departments (Holds all departments/majors) - index[id]
# (PK, INT) id
# (NOT NULL, UNIQUE, VARCHAR(35)) name
# 
# projects (Holds all projects) - index[id]
# (PK, INT) id
# (NOT NULL, UNIQUE, VARCHAR(35)) title
# (NOT NULL, VARCHAR(35)) description
# (NOT NULL, FK projects_department_id REFERENCES departments.id, INT) department_id
# (NOT NULL, VARCHAR(35)) link
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
# (NOT NULL, VARCHAR(35)) title
# (NOT NULL, VARCHAR(35)) description
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
# TODO: New user creation must add to both accounts and the appropriate table (admin/professor/student)

from flask import Flask, request, redirect, url_for, session
import mysql.connector
import json

with open('research_buddy/config.json') as config_file:
    db_config = json.load(config_file)

cnx = mysql.connector.connect(**db_config)
cursor = cnx.cursor()

app = Flask(__name__)
app.config.from_pyfile('config.py')

@app.route("/")
def main():
    return redirect(url_for('home'))

@app.route("/home")
def home():
    if 'id' in session:
        return redirect(url_for('dashboard'))
    
    else:
        return f"<link rel='stylesheet' href='{url_for('static', filename='styles.css')}'> \
        <title>Research Buddy</title><main><h1>Home</h1><button onclick=\"window.location.href='/signin';\"> \
        Sign In</button> <button onclick=\"window.location.href='/signup';\">Create Account</button> \
        </main><footer>Research Buddy v1.0a</footer>"
    
@app.route("/signin", methods=['GET', 'POST'])    
def signin():
    if request.method == 'GET':
        return f"<link rel='stylesheet' href='{url_for('static', filename='styles.css')}'><title>Sign In</title> \
        <main><div class='content-container'><h1>Sign In</h1><form method='POST'> Username: \
        <input type='text' maxlength='35' name='username' required><br><br>Password: \
        <input type='password' maxlength='35' name='password' required> \
        <br><br><div class='content-buttons'> \
        <button type='button' class='back-button' onclick=\"window.location.href='/home';\">Back</button> \
        <button type='submit'>Sign In</button></div></form></div></main><footer>Research Buddy v1.0a</footer>"
    
    elif request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        query = "SELECT * FROM accounts WHERE username = %s AND password = %s ORDER BY id ASC"
        cursor.execute(query, (username, password))
        response = cursor.fetchone()
        
        if not response:
            return "<script>window.alert('Invalid username or password! Please try again.');" \
            "window.location.href = '/signin';</script>"
    
        session['id'] = response[0]
        session['username'] = response[1]
        session['password'] = response[2]
        session['first'] = response[3]
        session['last'] = response[4]
        session['email'] = response[5]
        session['resume'] = response[6]
        session['linkedin'] = response[7]
        session['department_id'] = response[8]
        session['status'] = response[9]

        return redirect(url_for('dashboard'))
    

@app.route("/signup", methods=['GET', 'POST'])    
def signup():
    if request.method == "GET":
        return f"<link rel='stylesheet' href='{url_for('static', filename='styles.css')}'><title>Sign Up</title>" \
        "<main><div class='content-container'><h1>Sign Up</h1><p>Fields marked with an asterisk (*) are required.</p>" \
        "<form method='POST'>*Username: <input type='text' name='username' maxlength='35'>" \
        "<br><br>*Password: <input type='password' name='password' maxlength='35' required>" \
        "<br><br>*Confirm password: <input type='password' name='password2' maxlength='35' required>" \
        "<br><br>*First name: <input type='text' name='first' maxlength='35' required>" \
        "<br><br>*Last name: <input type='text' name='last' maxlength='35' required>" \
        "<br><br>*Email: <input type='text' name='email' maxlength='35' required>" \
        "<br><br>Resume: <input type='text' maxlength='35' name='resume'>" \
        "<br><br>LinkedIn: <input type='text' maxlength='35' name='linkedin'>" \
        "<br><br>*Department: <input type='checkbox' name='cb_dpt1'>Test Department" \
        "<br><br>Account Type: <select><option name='admin'>Admin</option>" \
        "<option name='student'>Student</option><option name='professor'>Professor</option></select>" \
        "<br><br><div class='content-buttons'>" \
        "<button type='button' class='back-button' onclick=\"window.location.href='/home';\">Back</button> " \
        "<button type='submit'>Sign Up</button></div></form></div></main><footer>Research Buddy v1.0a</footer>"
    
    elif request.method == "POST":
        return "POST ON SIGNUP"

@app.route("/dashboard")    
def dashboard():
    if 'id' in session:
        status_buttons = ""
        if session['status'] == 'admin':
            status_buttons = "<div class='flex-container'><div class='flex-item'><fieldset class='fieldset-style'>" \
            "<legend>View:</legend><button class='btn-view' onclick=\"window.location.href='/accounts';\">" \
            "Accounts</button><br><br><button class='btn-view' onclick=\"window.location.href='/departments';\">" \
            "Departments</button><br><br><button class='btn-view' onclick=\"window.location.href='/projects';\">" \
            "Projects</button><br><br><button class='btn-view' onclick=\"window.location.href='/requirements';\">" \
            "Requirements</button><br><br><button class='btn-view' onclick=\"window.location.href='/status-codes';\">" \
            "Status Codes</button><br><br></fieldset></div><div class='flex-item'><fieldset class='fieldset-style'>" \
            "<legend>Edit:</legend><button class='btn-edit' onclick=\"window.location.href='/edit/accounts';\">" \
            "Accounts</button><br><br><button class='btn-edit' onclick=\"window.location.href='/edit/departments';\">" \
            "Departments</button><br><br><button class='btn-edit' onclick=\"window.location.href='/edit/projects';\">" \
            "Projects</button><br><br><button class='btn-edit' onclick=\"window.location.href='/edit/requirements';\">" \
            "Requirements</button><br><br>" \
            "<button class='btn-edit' onclick=\"window.location.href='/edit/status-codes';\">Status Codes</button>" \
            "<br><br></fieldset></div><div class='flex-item'><fieldset class='fieldset-style'><legend>Account:" \
            "</legend><button class='btn-account' onclick=\"window.location.href='/edit';\">Account Settings</button>" \
            "<br><br><button class='back-button' onclick=\"window.location.href='/logout';\">Sign Out</button>" \
            "</fieldset></div></div><br><br>"

        elif session['status'] == 'professor':
            status_buttons = "<div class='flex-container'><div class='flex-item'>" \
            "<fieldset class='fieldset-style custom-fieldset'><legend>View:</legend>" \
            "<button class='btn-view' onclick=\"window.location.href='/projects';\">Projects</button><br><br> " \
            "<button class='btn-view' onclick=\"window.location.href='/profile';\">Profile</button> " \
            "</fieldset></div><div class='flex-item'><fieldset class='fieldset-style custom-fieldset'>" \
            "<legend>Edit:</legend><button class='btn-edit' onclick=\"window.location.href='/edit/projects';\">" \
            "Projects</button></fieldset></div><div class='flex-item'>" \
            "<fieldset class='fieldset-style custom-fieldset'><legend>Account:</legend>" \
            "<button class='btn-account' onclick=\"window.location.href='/edit';\">Account Settings</button><br>" \
            "<br><button class='back-button' onclick=\"window.location.href='/logout';\">Sign Out</button>" \
            "</fieldset></div></div><br><br>"
        
        elif session['status'] == 'student':
            status_buttons = "<div class='flex-container'><div class='flex-item'>" \
            "<fieldset class='fieldset-style custom-fieldset'><legend>View:</legend>" \
            "<button class='btn-view' onclick=\"window.location.href='/projects';\">Projects</button><br><br> " \
            "<button class='btn-view' onclick=\"window.location.href='/profile';\">Profile</button> " \
            "</fieldset></div><div class='flex-item'><fieldset class='fieldset-style custom-fieldset'>" \
            "<legend>Account:</legend><button class='btn-account' onclick=\"window.location.href='/edit';\">" \
            "Account Settings</button><br><br>" \
            "<button class='back-button' onclick=\"window.location.href='/logout';\">Sign Out</button>" \
            "</fieldset></div></div><br><br>"

        return f"<link rel='stylesheet' href='{url_for('static', filename='styles.css')}'><title>Dashboard</title> \
        <main><h1>Dashboard</h1><p>Welcome, {session['first']} {session['last']}!</p> {status_buttons} </main> \
        <footer>Account Status: {session['status'].capitalize()}</footer>"
    
    else:
        return redirect(url_for('home'))

@app.route("/view")
def view_profile():
    if session['status'] == 'student' or session['status'] == 'professor':
        if session['status'] == 'student':
            return "GET ON VIEW PROFILE"
        
        elif session['status'] == 'professor':
            return "GET ON VIEW PROFILE"
    
    else:
        if 'id' in session:
            return "<script>window.alert('You are not authorized to view this page.');" \
            "window.location.href = '/dashboard';</script>"

        else:
            return redirect(url_for('home'))

@app.route("/accounts")
def view_accounts():
    if session['status'] == 'admin':
        query = "SELECT * FROM accounts ORDER BY id ASC"
        cursor.execute(query)
        response = cursor.fetchall()

        html = f"<link rel='stylesheet' href='{url_for('static', filename='styles.css')}'> \
        <title>Status Codes</title><body><main><div class='viewer-container'><h1>Accounts</h1>"

        for row in response:
            html += f"<div class='row-heading'>ID: {row[0]}</div> \
            <div class='content-field'><span class='viewer-label'>Username:</span><span>{row[1]}</span></div> \
            <div class='content-field'><span class='viewer-label'>Password:</span><span>{row[2]}</span></div> \
            <div class='content-field'><span class='viewer-label'>First name:</span><span>{row[3]}</span></div> \
            <div class='content-field'><span class='viewer-label'>Last name:</span><span>{row[4]}</span></div> \
            <div class='content-field'><span class='viewer-label'>Email:</span><span>{row[5]}</span></div> \
            <div class='content-field'><span class='viewer-label'>Resume:</span><span>{row[6]}</span></div> \
            <div class='content-field'><span class='viewer-label'>LinkedIn:</span><span>{row[7]}</span></div> \
            <div class='content-field'><span class='viewer-label'>Department:</span><span>{row[8]}</span></div> \
            <div class='content-field'><span class='viewer-label'>Status: </span><span>{row[9]}</span></div>"

        html += f"<div class='content-buttons'> \
        <button type='button' class='back-button' onclick=\"window.location.href='/home';\">Back</button> \
        </div></div></main><footer>Account Status: {session['status'].capitalize()}</footer></body>"

        return html
    
    else:
        if 'id' in session:
            return "<script>window.alert('You are not authorized to view this page.');" \
            "window.location.href = '/dashboard';</script>"

        else:
            return redirect(url_for('home'))
        
@app.route("/departments")
def view_departments():
    if session['status'] == 'admin':
        query = "SELECT * FROM departments ORDER BY id ASC"
        cursor.execute(query)
        response = cursor.fetchall()

        html = f"<link rel='stylesheet' href='{url_for('static', filename='styles.css')}'> \
        <title>Departments</title><body><main><div class='viewer-container'><h1>Departments</h1>"

        for row in response:
            html += f"<div class='row-heading'>ID: {row[0]}</div> \
            <div class='content-field'><span class='viewer-label'>Department:</span><span>{row[1]}</span></div>"

        html += f"<div class='content-buttons'> \
        <button type='button' class='back-button' onclick=\"window.location.href='/home';\">Back</button> \
        </div></div></main><footer>Account Status: {session['status'].capitalize()}</footer></body>"

        return html
        
    else:
        if 'id' in session:
            return "<script>window.alert('You are not authorized to view this page.');" \
            "window.location.href = '/dashboard';</script>"

        else:
            return redirect(url_for('home'))

@app.route("/projects")
def view_projects():
    if 'id' in session:
        return "GET ON VIEW PROJECTS"
    
    elif request.method == "POST":
        return "POST ON VIEW PROJECTS"
    
    else:
        return redirect(url_for('home'))

@app.route("/requirements")
def view_requirements():
    if session['status'] == 'admin':
        return "GET ON VIEW REQUIREMENTS"
        
    else:
        if 'id' in session:
            return "<script>window.alert('You are not authorized to view this page.');" \
            "window.location.href = '/dashboard';</script>"

        else:
            return redirect(url_for('home'))

@app.route("/status-codes")
def view_status_codes():
    if session['status'] == 'admin':
        query = "SELECT * FROM status_code"
        cursor.execute(query)
        response = cursor.fetchone()

        return f"<link rel='stylesheet' href='{url_for('static', filename='styles.css')}'> \
        <title>Status Codes</title><body><main><div class='viewer-container'><h1>Status Codes</h1> \
        <div class='content-field'><span class='viewer-label'>Admin:</span> \
        <span>{response[1]}</span></div><div class='content-field'><span class='viewer-label'>Professor:</span> \
        <span>{response[2]}</span></div><div class='content-field'><span class='viewer-label'>Student:</span> \
        {response[3]}<span></span><div class='content-buttons'> \
        <button type='button' class='back-button' onclick=\"window.location.href='/home';\">Back</button> \
        </div></div></main><footer>Account Status: {session['status'].capitalize()}</footer></body>"
        
    else:
        if 'id' in session:
            return "<script>window.alert('You are not authorized to view this page.');" \
            "window.location.href = '/dashboard';</script>"

        else:
            return redirect(url_for('home'))

@app.route("/edit", methods=['GET', 'POST'])
def edit_profile():
    if request.method == "GET":
        return "GET ON EDIT PROFILE"
    
    elif request.method == "POST":
        return "POST ON EDIT PROFILE"
    
@app.route("/edit/accounts", methods=['GET', 'POST'])
def edit_accounts():
    if request.method == "GET":
        return "GET ON EDIT ACCOUNTS"
    
    elif request.method == "POST":
        return "POST ON EDIT ACCOUNTS"
    
@app.route("/edit/departments", methods=['GET', 'POST'])
def edit_departments():
    if request.method == "GET":
        return "GET ON EDIT DEPARTMENTS"
    
    elif request.method == "POST":
        return "POST ON EDIT DEPARTMENTS"    

@app.route("/edit/status-codes", methods=['GET', 'POST'])
def edit_status_codes():
    if 'id' in session:
        if request.method == "GET":
            return "GET ON EDIT STATUS CODES"
    
        elif request.method == "POST":
            return "POST ON EDIT STATUS CODES"  

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__=="__main__":
    app.run(debug=True)