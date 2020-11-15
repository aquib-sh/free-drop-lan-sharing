""" AUTHOR: SHAIKH AQUIB
    This is the main server file
 """

from flask_restful import Resource, Api, reqparse
from flask import Flask
import datetime
import werkzeug
import mysql.connector
from db_helper import DBHelper


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
        password = "admin@7977",
        database = "freedrop"
        )

# Create cursor for MySQL
cursor = db.cursor(buffered = True) 

helper = DBHelper(cursor)

# Creates new table structure 
def set_table_structure(table_name):
    command = """CREATE TABLE {} (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    path VARCHAR(500),
                    format VARCHAR(20),
                    creation VARCHAR(50));
                """.format(table_name)
    return command


class UploadImageAPI(Resource):
    def __init__(self):
        self.table = "images" 
        cursor.execute("SHOW TABLES;")

        if self.table not in helper.fetch_list():
            cursor.execute(set_table_structure(self.table))
 
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("image", type = werkzeug.datastructures.FileStorage, location = "files", help = "Attach an image file")
        parser.add_argument("format", help = "Specify file format for image") 
        args = parser.parse_args()        

        # Get current date for naming the file
        date_obj = datetime.datetime.now()
        date = date_obj.date()
        formatted_date = str(date.day) + "-" + str(date.month) + "-" + str(date.year)
        
        # Image name
        base_name = "Upload" + formatted_date + "jpg"

        # Check if the image already exists if it exists then put a number on it.
        image_name  = os.path.join(image_dir, base_name)
        matches     = helper.search_path(image_name, self.table)
        total_match = len(matches)  
        
        if total_match == 0:
            # If the path with same name does not exist then insert the current image_name
            helper.insert_value(table=self.table, path=image_name, file_format=args['format'], creation=formatted_date)
        else:
            # Append the name with a numeral depending upon the total matches present
            # so that there are no duplicates
            image_name += str(total_match)
            cursor.execute("""INSERT INTO {table} (path, format, creation) 
            VALUES ("{image_path}", "{format}", "{creation_date}")
            """).format(table=self.table, 
                        image_path=image_name, 
                        format=args['format'], 
                        creation_date=formatted_date)
                        )            


    
        image_file = args['image']
        image_file.save("image.jpg") 


class TestAPI(Resource):
    def get(self):
        return {"status":"successful"}


api.add_resource(UploadImageAPI,"/")
api.add_resource(TestAPI,"/test")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')



