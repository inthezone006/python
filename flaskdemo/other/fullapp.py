from flask import Flask, request, jsonify
from markupsafe import escape

app = Flask(__name__)

users = [
    {
    'name': 'Rahul',
    'birthmonth': 'May',
    'number': 1
    },
    {
    'name': 'Swathi',
    'birthmonth':'May',
    'number':2
    }
]

@app.route("/users", methods=['GET'])
def getResponse():
    return jsonify({'users':users})

@app.route('/users/<string:username>', methods=["POST"])
def returnUser(username):
    for user in users:
        if user['name'] == username:
            return jsonify(user)
        
    return jsonify({'error':'No user found'})

@app.route('/users', methods=['POST'])
def createUser():
    request_body = request.get_json()

    newUser = {
        'user': request_body['name'],
        'birthmonth': request_body['birthmonth'],
        'number': request_body['number']
    }

    users.append(newUser)
    return jsonify(newUser)

@app.route('/users/<string:username>', methods=['PUT'])
def updateUser(username):
    request_body = request.get_json()

    for user in users:
        if users['name'] == username:
            user['name'] = request_body['name']
            user['birthmonth'] = request_body['birthmonth']
            user['number'] = request_body['number']
            return jsonify(user)
        
    return jsonify({'error': 'user not found'})


@app.route('/users/<string:username>', methods=["DELETE"])
def deleteUser(username):
    request_body = request.get_json()

    for (index,user) in users:
        if user['name'] == username:
            del users[index]
            return jsonify({'success': 'user deleted'})

    return jsonify({'error': 'user not found'})

