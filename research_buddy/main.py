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
# projects_students (Holds all projects that a student is part of) - 
# (PK, FK projectsrel_student_id REFERENCES students.id, INT) student_id
# (PK, FK projectsrel_project_id REFERENCES projects.id, INT) project_id
# 
# requirements (For all the possible requirements a student/project can have) - index[id]
# (PK, INT) id
# (NOT NULL, VARCHAR(35)) title
# (NOT NULL, VARCHAR(35)) description
#
# students_requirements (For all the requirements a student has; implement that all students are at least a student) -
# (PK, FK student_requirements_requirement_id REFERENCES requirements.id, INT) requirement_id
# (PK, FK student_requirements_student_id REFERENCES students.id, INT) student_id
# 
# projects_requirements (For all the requirements a project has) -
# (PK, FK project_requirements_requirement_id REFERENCES requirements.id, INT) requirement_id
# (PK, FK project_requirements_project_id REFERENCES projects.id, INT) project_id
# 
# status_codes - index[id]
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

import re
from flask import Flask, request, redirect, url_for, session, Response
import mysql.connector
import json
import csv
import io

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
        query = "SELECT name FROM departments ORDER BY id ASC"
        cursor.execute(query)
        responses = cursor.fetchall()
        html = f"<link rel='stylesheet' href='{url_for('static', filename='styles.css')}'><title>Sign Up</title>" \
        "<main><div class='content-container'><h1>Sign Up</h1><p>Fields marked with an asterisk (*) are required.</p>" \
        "<p>All fields have a character limit of 35.</p><form method='POST'>*Username: " \
        "<input type='text' name='username' maxlength='35'>" \
        "<br><br>*Password: <input type='password' name='password' maxlength='35' required>" \
        "<br><br>*Confirm password: <input type='password' name='password2' maxlength='35' required>" \
        "<br><br>*First name: <input type='text' name='first' maxlength='35' required>" \
        "<br><br>*Last name: <input type='text' name='last' maxlength='35' required>" \
        "<br><br>*Email: <input type='text' name='email' maxlength='35' required>" \
        "<br><br>Resume: <input type='text' maxlength='35' name='resume'>" \
        "<br><br>LinkedIn: <input type='text' maxlength='35' name='linkedin'>" \
        "<br><br>*Department: <select name='dpt' id='dpt'>"

        for row in responses:
            html += f"<option value='{row[0]}'>{row[0]}</option>"

        html += f"</select><br><br>Account Type: <select><option name='admin'>Admin</option>" \
        "<option name='student'>Student</option><option name='professor'>Professor</option></select>" \
        "<br><br><div class='content-buttons'>" \
        "<button type='button' class='back-button' onclick=\"window.location.href='/home';\">Back</button> " \
        "<button type='submit'>Sign Up</button></div></form></div></main><footer>Research Buddy v1.0a</footer>"

        return html
    
    elif request.method == "POST":
        return "POST ON SIGNUP"

@app.route("/dashboard")    
def dashboard():
    if 'id' in session:
        status_buttons = ""
        if session['status'] == 'admin':
            status_buttons = "<div class='flex-container'><div class='flex-item'><fieldset class='fieldset-style'>" \
            "<legend>View:</legend><button class='btn-view' onclick=\"window.location.href='/accounts';\">" \
            "Accounts Report</button><br><br>" \
            "<button class='btn-view' onclick=\"window.location.href='/departments';\">" \
            "Departments Report</button><br><br>" \
            "<button class='btn-view' onclick=\"window.location.href='/projects';\">" \
            "Projects Report</button><br><br" \
            "><button class='btn-view' onclick=\"window.location.href='/requirements';\">" \
            "Requirements Report</button><br><br>" \
            "<button class='btn-view' onclick=\"window.location.href='/status-codes';\">Status Codes Report</button>" \
            "<br><br></fieldset></div><div class='flex-item'><fieldset class='fieldset-style'>" \
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
            "<button class='btn-view' onclick=\"window.location.href='/projects';\">Projects Report</button><br><br> " \
            "<button class='btn-view' onclick=\"window.location.href='/profile';\">Profile Report</button> " \
            "</fieldset></div><div class='flex-item'><fieldset class='fieldset-style custom-fieldset'>" \
            "<legend>Edit:</legend><button class='btn-edit' onclick=\"window.location.href='/edit/projects';\">" \
            "Owned Projects</button><br><br>" \
            "<button class='btn-edit' onclick=\"window.location.href='/new/projects';\">Create New Project</button>" \
            "</fieldset></div><div class='flex-item'><fieldset class='fieldset-style custom-fieldset'><legend>" \
            "Account:</legend><button class='btn-account' onclick=\"window.location.href='/edit';\">" \
            "Account Settings</button><br><br><button class='back-button' onclick=\"window.location.href='/logout';\">" \
            "Sign Out</button></fieldset></div></div><br><br>"
        
        elif session['status'] == 'student':
            status_buttons = "<div class='flex-container'><div class='flex-item'>" \
            "<fieldset class='fieldset-style custom-fieldset'><legend>View:</legend>" \
            "<button class='btn-view' onclick=\"window.location.href='/projects';\">Projects Report</button><br><br> " \
            "<button class='btn-view' onclick=\"window.location.href='/profile';\">Profile Report</button> " \
            "</fieldset></div><div class='flex-item'><fieldset class='fieldset-style custom-fieldset'>" \
            "<legend>Edit:</legend><button class='btn-edit' onclick=\"window.location.href='/edit/projects';\">" \
            "Current Projects</button><br><br>" \
            "<button class='btn-edit' onclick=\"window.location.href='/new/projects';\">Join New Project</button>" \
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

@app.route("/profile", methods=['GET', 'POST'])
def view_profile():
    if session['status'] == 'student' or session['status'] == 'professor':

        if request.method == "GET":
            query = "SELECT a.id, a.username, a.password, a.first, a.last, a.email, a.resume," \
            " a.linkedin, d.name AS department_name, a.status, p.website AS professor_website, p.status " \
            "AS professor_status, s.status AS student_status FROM accounts a LEFT JOIN departments d ON " \
            "a.department_id = d.id LEFT JOIN professors p on a.id = p.id LEFT JOIN students s on a.id = s.id" \
            " WHERE a.id = %s;"
            cursor.execute(query, (session['id'], ))
            response = cursor.fetchone()

            html = f"<link rel='stylesheet' href='{url_for('static', filename='styles.css')}'> \
            <title>Profile Report</title><body><main><div class='viewer-container'><h1>Profile Report</h1> \
            <div class='content-field'><span class='viewer-label'>Username:</span> \
            <span>{response[1]}</span></div><div class='content-field'><span class='viewer-label'>Password:</span> \
            <span>{response[2]}</span></div><div class='content-field'><span class='viewer-label'>First Name:</span> \
            <span>{response[3]}</span></div><div class='content-field'><span class='viewer-label'>Last Name:</span> \
            <span>{response[4]}</span></div><div class='content-field'><span class='viewer-label'>Email:</span> \
            <span>{response[5]}</span></div><div class='content-field'><span class='viewer-label'>Resume:</span> \
            <span>{response[6]}</span></div><div class='content-field'><span class='viewer-label'>LinkedIn:</span> \
            <span>{response[7]}</span></div><div class='content-field'><span class='viewer-label'>Department:</span> \
            <span>{response[8]}</span></div><div class='content-field'><span class='viewer-label'>Status:</span> \
            <span>{response[9].capitalize()}</span></div>"
            
            if session['status'] == 'student':
                html += f"<div class='content-field'><span class='viewer-label'>Student Status:</span> \
                <span>{response[12].capitalize()}</span></div>"

            elif session[session] == 'professor':
                html += f"<div class='content-field'><span class='viewer-label'>Professor Website:</span> \
                <span>{response[10]}</span></div><div class='content-field'> \
                <span class='viewer-label'>Professor Status:</span> \
                <span>{response[11].capitalize()}</span></div>"

            html += f"<div class='content-buttons'><form method='POST'> \
            <button>Export to CSV</button> \
            <br><button type='button' class='back-button' onclick=\"window.location.href='/home';\">Back</button><br> \
            </form></div></div></main><footer>Account Status: {session['status'].capitalize()}</footer></body>"

            return html
        
        elif request.method == "POST":
            si = io.StringIO()
            cw = csv.writer(si)

            if session['status'] == 'student':
                query = "SELECT a.id, a.username, a.password, a.first, a.last, a.email, a.resume, " \
                "a.linkedin, d.name AS department_name, a.status, s.status AS student_status FROM accounts a " \
                "LEFT JOIN departments d ON a.department_id = d.id LEFT JOIN students s on a.id = s.id " \
                "WHERE a.id = %s;"
                cursor.execute(query, (session['id'], ))
                response = cursor.fetchall()

                cw.writerow(['id', 'username', 'password', 'first', 'last', 'email', 'resume', 
                         'linkedin', 'department', 'status', 'student_status'])


            elif session['status'] == 'professor':
                query = "SELECT a.id, a.username, a.password, a.first, a.last, a.email, a.resume," \
                " a.linkedin, d.name AS department_name, a.status, p.website AS professor_website, p.status " \
                "AS professor_status FROM accounts a LEFT JOIN departments d ON a.department_id = d.id " \
                "LEFT JOIN professors p on a.id = p.id WHERE a.id = %s;"
                cursor.execute(query, (session['id'], ))
                response = cursor.fetchall()

                cw.writerow(['id', 'username', 'password', 'first', 'last', 'email', 'resume', 
                         'linkedin', 'department', 'status', 'professor_website', 'professor_status'])


            for row in response:
                cw.writerow(row)

            output = si.getvalue()

            response = Response(output, mimetype="text/csv")
            response.headers["Content-Disposition"] = "attachment; filename=profile.csv"
            return response
    
    else:
        if 'id' in session:
            return "<script>window.alert('You are not authorized to view this page.');" \
            "window.location.href = '/dashboard';</script>"

        else:
            return redirect(url_for('home'))

@app.route("/accounts", methods=['GET', 'POST'])
def view_accounts():
    if session['status'] == 'admin':
        query = "SELECT a.id, a.username, a.password, a.first, a.last, a.email, a.resume," \
        " a.linkedin, d.name, a.status, p.website AS professor_website, p.status AS professor_status," \
        " s.status AS student_status FROM accounts a LEFT JOIN departments d ON a.department_id = d.id" \
        " LEFT JOIN professors p on a.id = p.id LEFT JOIN students s on a.id = s.id ORDER BY a.id ASC;"
        if request.method == "GET":
            cursor.execute(query)
            response = cursor.fetchall()

            html = f"<link rel='stylesheet' href='{url_for('static', filename='styles.css')}'> \
            <title>Accounts Report</title><body><main><div class='viewer-container'><h1>Accounts Report</h1>"

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
                <div class='content-field'><span class='viewer-label'>Status:</span><span>{row[9].capitalize()}</span>"
                if row[9] == 'professor':
                    html += f"<div class='content-field'><span class='viewer-label'>Professor Website:</span><span>{row[10]}</span></div> \
                    <div class='content-field'><span class='viewer-label'>Professor Status:</span><span>{row[11].capitalize()}</span></div>"
                
                elif row[9] == 'student':
                    html += f"<div class='content-field'><span class='viewer-label'>Student Status:</span><span>{row[12].capitalize()}</span></div>"
                
                html += "</div>"

            html += f"<div class='content-buttons'> \
            <form method='POST'><button type='submit'>Export to CSV</button><br> \
            <button type='button' class='back-button' onclick=\"window.location.href='/home';\">Back</button> \
            </form></div></div></main><footer>Account Status: {session['status'].capitalize()}</footer></body>"

            return html
        
        elif request.method == "POST":
            cursor.execute(query)
            response = cursor.fetchall()

            si = io.StringIO()
            cw = csv.writer(si)

            cw.writerow(['id', 'username', 'password', 'first', 'last', 'email', 'resume', 
                         'linkedin', 'department', 'status', 'professor_website', 'professor_status', 'student_status'])

            for row in response:
                cw.writerow(row)

            output = si.getvalue()

            response = Response(output, mimetype="text/csv")
            response.headers["Content-Disposition"] = "attachment; filename=accounts.csv"
            return response
            
    else:
        if 'id' in session:
            return "<script>window.alert('You are not authorized to view this page.');" \
            "window.location.href = '/dashboard';</script>"

        else:
            return redirect(url_for('home'))
        
@app.route("/departments", methods=['GET', 'POST'])
def view_departments():
    if session['status'] == 'admin':
        query = "SELECT * FROM departments ORDER BY id ASC"
        if request.method == "GET":
            cursor.execute(query)
            response = cursor.fetchall()

            html = f"<link rel='stylesheet' href='{url_for('static', filename='styles.css')}'> \
            <title>Departments Report</title><body><main><div class='viewer-container'><h1>Departments Report</h1>"

            for row in response:
                html += f"<div class='row-heading'>ID: {row[0]}</div> \
                <div class='content-field'><span class='viewer-label'>Department:</span><span>{row[1]}</span></div>"

            html += f"<div class='content-buttons'><form method='POST'><button type='submit'>Export to CSV</button> \
            <br><button type='button' class='back-button' onclick=\"window.location.href='/home';\">Back</button> \
            </form></div></div></main><footer>Account Status: {session['status'].capitalize()}</footer></body>"

            return html
        
        elif request.method == "POST":
            cursor.execute(query)
            response = cursor.fetchall()

            si = io.StringIO()
            cw = csv.writer(si)

            cw.writerow(['id', 'name'])

            for row in response:
                cw.writerow(row)

            output = si.getvalue()

            response = Response(output, mimetype="text/csv")
            response.headers["Content-Disposition"] = "attachment; filename=departments.csv"
            return response
    
    else:
        if 'id' in session:
            return "<script>window.alert('You are not authorized to view this page.');" \
            "window.location.href = '/dashboard';</script>"

        else:
            return redirect(url_for('home'))

@app.route("/projects", methods=['GET', 'POST'])
def view_projects():
    if 'id' in session:
        if session['status'] == 'admin':
            query = "SELECT p.id, p.title, p.description, d.name, p.link, a.first, a.last, p.status FROM projects " \
                "p LEFT JOIN departments d ON p.department_id = d.id LEFT JOIN accounts a " \
                "ON p.professor_id = a.id ORDER BY p.id ASC"
            
            cursor.execute(query)
            response = cursor.fetchall()

            if request.method == "GET":
                html = f"<link rel='stylesheet' href='{url_for('static', filename='styles.css')}'> \
                <title>Projects Report</title><body><main><div class='viewer-container'><h1>Projects Report</h1>"

                for row in response:
                    html += f"<div class='row-heading'>ID: {row[0]}</div> \
                    <div class='content-field'><span class='viewer-label'>Title:</span><span>{row[1]}</span></div> \
                    <div class='content-field'><span class='viewer-label'>Description:</span><span>{row[2]}</span></div> \
                    <div class='content-field'><span class='viewer-label'>Department:</span><span>{row[3]}</span></div> \
                    <div class='content-field'><span class='viewer-label'>Link:</span><span>{row[4]}</span></div> \
                    <div class='content-field'><span class='viewer-label'>Professor:</span><span>{row[5]} {row[6]}</span></div> \
                    <div class='content-field'><span class='viewer-label'>Status:</span><span>{row[6].capitalize()}</span></div>"

                html += f"<div class='content-buttons'><form method='POST'><button type='submit'> \
                Export to CSV</button><br> \
                <button type='button' class='back-button' onclick=\"window.location.href='/home';\">Back \
                </button></div></div></main><footer>Account Status: {session['status'].capitalize()}</footer></body>"

                return html
            
            elif request.method == "POST":
                si = io.StringIO()
                cw = csv.writer(si)

                cw.writerow(['id', 'title', 'description', 'department', 'link', 'professor', 'status'])

                for row in response:
                    row_list = list(row)
                    row_list[5] = f"{row_list[5]} {row_list[6]}"
                    del row_list[6]
                    cw.writerow(row_list)

                output = si.getvalue()

                response = Response(output, mimetype="text/csv")
                response.headers["Content-Disposition"] = "attachment; filename=projects.csv"
                return response
    
        elif session['status'] == 'professor':
            if request.method == "GET":
                return "GET ON PROJECTS - PROFESSOR"

            elif request.method == "POST":
                return "POST ON PROJECTS - PROFESSOR"
            
        elif session['status'] == 'student':
            if request.method == "GET":
                return "GET ON PROJECTS - STUDENT"

            elif request.method == "POST":
                return "POST ON PROJECTS - STUDENT"
        
    else:
        return redirect(url_for('home'))

@app.route("/requirements", methods=['GET', 'POST'])
def view_requirements():
    if session['status'] == 'admin':
        query = "SELECT * FROM requirements ORDER BY id ASC"
        if request.method == "GET":
            cursor.execute(query)
            response = cursor.fetchall()

            html = f"<link rel='stylesheet' href='{url_for('static', filename='styles.css')}'> \
            <title>Requirements Report</title><body><main><div class='viewer-container'><h1>Requirements Report</h1>"

            for row in response:
                html += f"<div class='row-heading'>ID: {row[0]}</div> \
                <div class='content-field'><span class='viewer-label'>Title:</span><span>{row[1]}</span></div> \
                <div class='content-field'><span class='viewer-label'>Description:</span><span>{row[2]}</span></div>"

            html += f"<div class='content-buttons'><form method='POST'><button type='submit'>Export to CSV</button> \
            <br><button type='button' class='back-button' onclick=\"window.location.href='/home';\">Back</button> \
            </form></div></div></main><footer>Account Status: {session['status'].capitalize()}</footer></body>"

            return html
        
        elif request.method == "POST":
            cursor.execute(query)
            response = cursor.fetchall()

            si = io.StringIO()
            cw = csv.writer(si)

            cw.writerow(['id', 'title', 'description'])

            for row in response:
                cw.writerow(row)

            output = si.getvalue()

            response = Response(output, mimetype="text/csv")
            response.headers["Content-Disposition"] = "attachment; filename=requirements.csv"
            return response
    
    else:
        if 'id' in session:
            return "<script>window.alert('You are not authorized to view this page.');" \
            "window.location.href = '/dashboard';</script>"

        else:
            return redirect(url_for('home'))

@app.route("/status-codes", methods=['GET', 'POST'])
def view_status_codes():
    if session['status'] == 'admin':
        query = "SELECT * FROM status_codes"
        if request.method == "GET":
            cursor.execute(query)
            response = cursor.fetchone()

            return f"<link rel='stylesheet' href='{url_for('static', filename='styles.css')}'> \
            <title>Status Codes Report</title><body><main><div class='viewer-container'><h1>Status Codes Report</h1> \
            <div class='content-field'><span class='viewer-label'>Admin:</span> \
            <span>{response[1]}</span></div><div class='content-field'><span class='viewer-label'>Professor:</span> \
            <span>{response[2]}</span></div><div class='content-field'><span class='viewer-label'>Student:</span> \
            {response[3]}<span></span><div class='content-buttons'><form method='POST'><button type='submit'> \
            Export to CSV</button><br> \
            <button type='button' class='back-button' onclick=\"window.location.href='/home';\"> \
            Back</button></form></div></div></main><footer>Account Status: {session['status'].capitalize()}</footer> \
            </body>"
        
        elif request.method == "POST":
            cursor.execute(query)
            response = cursor.fetchall()

            si = io.StringIO()
            cw = csv.writer(si)

            cw.writerow(['id', 'admin', 'professor', 'student'])

            for row in response:
                cw.writerow(row)

            output = si.getvalue()

            response = Response(output, mimetype="text/csv")
            response.headers["Content-Disposition"] = "attachment; filename=status_codes.csv"
            return response
        
    else:
        if 'id' in session:
            return "<script>window.alert('You are not authorized to view this page.');" \
            "window.location.href = '/dashboard';</script>"

        else:
            return redirect(url_for('home'))

@app.route("/edit", methods=['GET', 'POST'])
def edit_profile():
    if request.method == "GET":
        html = f"<link rel='stylesheet' href='{url_for('static', filename='styles.css')}'> \
        <title>Account Settings</title><body><main><div class='content-container'><h1>Account Settings</h1> \
        <form method='POST' onsubmit='return handlePrompt();'><label for='ssetting'>Account Setting to Change:</label> \
        <select name='ssetting' id='ssetting'><option value='username'>Username</option><option value='password'> \
        Password</option><option value='first'>First Name</option><option value='last'>Last Name</option> \
        <option value='email'>Email</option><option value='resume'>Resume</option><option value='linkedin'> \
        LinkedIn</option><option value='department'>Department</option>"
        
        if session['status'] == 'professor':
            html += "<option value='professor_website'>Professor Website</option> \
            <option value='professor_status'>Professor Status</option>"
        
        elif session['status'] == 'student':
            html += "<option value='student_status'>Student Status</option>"
        
        html += f"</select><input type='hidden' name='new_value' id='new_value' value=''><br><br> \
        <div class='content-buttons'><button type='submit'>Change Setting</button> \
        <button type='button' class='btn-account' onclick='window.location.href='/delete'>Delete \
        <button type='button' class='back-button' onclick=\"window.location.href='/home';\">Back</button> \
        </div></form></main><footer>Account Status: {session['status'].capitalize()}</footer><script> \
        function handlePrompt() {{ var newValue = prompt('Enter new value (limit: 35 characters): '); \
        if (newValue !== null && newValue.trim() !== '') {{ document.getElementById('new_value').value = newValue; \
        return true; }} return false; }};</script></body>"
        
        return html
    elif request.method == "POST":
        # Make specific to student and professor
        setting_type = request.form.get('ssetting')
        new_value = request.form.get('new_value')
        if len(new_value) > 35:
            return "<script>alert('Status code must be less than 35 characters.');window.location.href='/edit';" \
            "</script>"
        query = f"UPDATE accounts SET {setting_type} = %s WHERE id = %s"
        cursor.execute(query, (new_value, session['id'], ))
        cnx.commit()
        return "<script>alert('Successfully updated!'); window.location.href='/edit';</script>"
    
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
    
@app.route("/edit/projects", methods=['GET', 'POST'])
def edit_projects():
    if request.method == "GET":
        return "GET ON EDIT PROJECTS"
    
    elif request.method == "POST":
        return "POST ON EDIT PROJECTS"    

@app.route("/edit/requirements", methods=['GET', 'POST'])
def edit_requirements():
    if request.method == "GET":
        return "GET ON EDIT REQUIREMENTS"
    
    elif request.method == "POST":
        return "POST ON EDIT REQUIREMENTS"    

@app.route("/edit/status-codes", methods=['GET', 'POST'])
def edit_status_codes():
    if session['status'] == 'admin':
        if request.method == "GET":
            return f"<link rel='stylesheet' href='{url_for('static', filename='styles.css')}'> \
            <title>Edit Status Codes</title><body><main><div class='content-container'><h1>Edit Status Codes</h1> \
            <form method='POST' onsubmit='return handlePrompt();'><label for='scode'>Status Code to Change:</label> \
            <select name='scode' id='scode'><option value='admin'>Admin</option><option value='student'> \
            Student</option><option value='professor'>Professor</option></select> \
            <input type='hidden' name='new_code' id='new_code' value=''><br><br><div class='content-buttons'> \
            <button type='button' class='back-button' onclick=\"window.location.href='/home';\">Back</button> \
            <button type='submit'>Change Status Code</button></div></form></main><footer> \
            Account Status: {session['status'].capitalize()}</footer><script> \
            function handlePrompt() {{ var newCode = prompt('Enter new status code (4 digit numbers only): '); \
            if (newCode !== null && newCode.trim() !== '') {{ document.getElementById('new_code').value = newCode; \
            return true; }} return false; }};</script></body>"
        
        elif request.method == "POST":
            status_code_type = request.form.get('scode')
            new_code = request.form.get('new_code')
            if not new_code or not new_code.isdigit() or len(new_code) != 4:
                return "<script>alert('Status code must be a 4-digit number.'); " \
                "window.location.href='/edit/status-codes';</script>"
            query = f"UPDATE status_codes SET {status_code_type} = %s WHERE id = 1"
            cursor.execute(query, (new_code, ))
            cnx.commit()
            return "<script>alert('Successfully updated!'); window.location.href='/edit/status-codes';</script>"
        
    else:
        if 'id' in session:
            return "<script>window.alert('You are not authorized to view this page.');" \
            "window.location.href = '/dashboard';</script>"

        else:
            return redirect(url_for('home'))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('home'))

#TODO: Implement a delete route
@app.route("/delete")
def delete():
    session.clear()
    return redirect(url_for('home'))

if __name__=="__main__":
    app.run(debug=True)