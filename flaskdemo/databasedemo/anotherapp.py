from flask import Flask
from flask_restful import Api, Resource
import sqlite3

app = Flask(__name__)

api = Api(app)

class Account(Resource):
    def getAcct(self, name):
        connection = sqlite3.connect('accounts.db')

