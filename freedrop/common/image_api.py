import os
import werkzeug
from flask_restful import Resource, reqparse
from flask import make_response, send_file
from backend.resources.util import set_table_structure, get_formatted_date
from backend.resources.configuration import image_dir

class ImageAPI(Resource):
    """ ImageAPI
    methods: get, post, delete 
    """


    def __init__(self, cursor, helper, db):
        self.table  = "images"
        self.cursor = cursor
        self.helper = helper
        self.db     = db 
        self.cursor.execute("SHOW TABLES;")

        if self.table not in self.helper.fetch_list():
            self.cursor.execute(set_table_structure(self.table))
 
    def post(self):
        """For uploading image."""

        parser = reqparse.RequestParser()
        parser.add_argument("image", type = werkzeug.datastructures.FileStorage, location = "files", help = "Attach an image file", required=True)
        parser.add_argument("format", help = "Specify file format for image", required=True) 
        args = parser.parse_args()        
        base_name = "Upload" + get_formatted_date()         # Image name

        # Check if the image already exists if it exists then put a number on it.
        image_name  = os.path.join(image_dir, base_name)
        matches     = self.helper.search_path(image_name, self.table)
        total_match = len(matches)  
        
        if total_match == 0:
            # If the path with same name does not exist then insert the current image_name.
            image_name += ".{}".format(args['format'])
            self.helper.insert_value(table=self.table, path=image_name, file_format=args['format'])
        else:
            # Append the name with a numeral depending upon the total matches present.
            image_name += ("(" + str(total_match) + ")" + ".{}".format(args['format']))
            self.helper.insert_value(table=self.table, path=image_name, file_format=args['format'])
        
        self.db.commit()
        image_file = args['image']
        image_file.save(image_name)
        return {"status":"image uploaded successfully"} 

    def get(self):
        """ For sending image to client. """

        parser = reqparse.RequestParser()
        parser.add_argument("filename", help="Specify name of the file", default="null")
        parser.add_argument("type",help="Use file_req for receiving a file from server\nUse list_files for getting list of all files present ", required=True)
        args = parser.parse_args()

        if args['type'] == "file_req":
            # Send specific image file
            result = self.helper.get_path(args['filename'], self.table)
            # If results were not found then simply return this message
            if len(result) == 0:
                message = "No matching file found"
                return {"status":message}
            # Else return the file
            img_path = result[0]
            image_format = self.helper.get_format(img_path, self.table)[0]

            # Using make_response to include headers with the file
            # Would be used to determine image format
            response = make_response(send_file(img_path, mimetype="image/"+image_format))
            response.headers['File-Format'] = image_format
            return response        

        elif args['type'] == "list_files":
            # Send list of all image files present on the server
            all_files = self.helper.get_full_list("filename", self.table)
            return {"list":all_files}
        
    def delete(self):
        """For removing files from server."""
        
        parser = reqparse.RequestParser()
        parser.add_argument("filename", help="Specify name of the file", required=True)
        args = parser.parse_args()

        filename = args['filename']

        # Get the path for file and delete it
        self.cursor.execute('SELECT path FROM {} WHERE filename="{}"'.format(self.table, filename))
        path = self.helper.fetch_list()[0]
        os.remove(path)

        # Delete record from database as well
        self.helper.delete_value(self.table, args['filename'])

        return {"status":"file deleted sucessfully"}