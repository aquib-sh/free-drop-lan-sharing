""" AUTHOR: SHAIKH AQUIB
    This is the main server file """

import sys
import os
import mysql.connector
from flask_restful import Resource, Api, reqparse 
from flask import Flask
from flask_cors import CORS
sys.path.append(os.path.abspath(
    os.path.join(os.getcwd(), os.pardir)
    ))
from freedrop.common.test_api import TestAPI
from freedrop.common.file_api import FileAPI
from freedrop.resources.db_helper import DBHelper

app = Flask(__name__)
api = Api(app)

# Setting CORS policy to allow requests from all origins
cors = CORS(app, resources={r"/*":{"origins":"*"}})

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

api.add_resource(FileAPI, 
    "/file", 
    "/file/<string:want>", 
    "/file/<string:want>/<string:filename>", 
    resource_class_kwargs={'cursor':cursor, 'helper':helper, 'db':db}
    )
api.add_resource(TestAPI, "/test")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')



