""" AUTHOR: SHAIKH AQUIB
    This is the main server file """

import mysql.connector
from flask_restful import Resource, Api, reqparse
from flask import Flask
import sys
import os
sys.path.append(os.getcwd())

from backend.common.image_api import ImageAPI
from backend.common.test_api import TestAPI
from backend.resources.db_helper import DBHelper

app = Flask(__name__)
api = Api(app)

# Create connection with MySQL server
db = mysql.connector.connect(
        host     = "localhost",
        user     = "aquib",
        password = "admin@7977",
        database = "freedrop"        
        )

# Create cursor for MySQL
cursor = db.cursor(buffered = True) 
helper = DBHelper(cursor)

api.add_resource(ImageAPI, "/image", resource_class_kwargs={'cursor':cursor, 'helper':helper, 'db':db})
api.add_resource(TestAPI, "/test")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')



