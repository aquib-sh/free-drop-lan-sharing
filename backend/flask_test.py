from flask_restful import Resource, Api, reqparse
from flask import Flask
import datetime
import werkzeug
import mysql.connector


app = Flask(__name__)
api = Api(app)

image_dir  = "images"
video_dir  = "videos"
pdf_dir    = "pdf_documents"
others_dir = "others"

# Create connection with MySQL server
db = mysql.connector.connect(
        host     = "localhost",
        user     = "aquib",
        password = "admin@7977"
        )

# Create cursor for MySQL 
cursor = db.cursor() 

# If database doesn't exist then create one
database = "freedrop"
cursor.execute("SHOW DATABASES;")

if database in cursor:
    cursor.execute("CONNECT {};".format(database)) 
else:
    cursor.execute("CREATE DATABASE {};".format(database))
    cursor.execute("CONNECT {};".format(database))


class UploadImageAPI(Resource):
    def __init__(self):
        self.table = "images" 
        cursor.execute("SHOW TABLES;")

        if self.table not in cursor:
            cursor.execute("""CREATE TABLE {0}
                (
                    id INT AUTO_INCREMENT PRIMARY_KEY,
                    path VARCHAR(500),
                    format VARCHAR(20),
                    creation VARCHAR(50)
                )
                """)
 
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("image", type = werkzeug.datastructures.FileStorage, location = "files", help = "Attach an image file")
        parser.add_argument("format", help = "Specify file format for image") 
        args = parser.parse_args()        

        # Get current date for naming the file
        date = datetime.datetime.now().date()
        formatted_date = str(date.day) + "-" + str(date.month) + "-" + str(date.year)
        
        # Image name
        base_name = "Upload" + formatted_date + "jpg"
        # Check if the image already exists if it exists then put a number on it.
        

        image_name = os.path.join(image_dir, base_name)

    
        image_file = args['image']
        image_file.save("image.jpg") 


class TestAPI(Resource):
    def get(self):
        return {"status":"successful"}


api.add_resource(UploadImageAPI,"/")
api.add_resource(TestAPI,"/test")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')



