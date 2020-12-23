import os
import sys
import werkzeug
from flask_restful import Resource, reqparse
from flask import make_response, send_file, jsonify
from freedrop.resources.util import set_table_structure, get_formatted_date, format_path
import freedrop.resources.configuration as config

class FileAPI(Resource):
    """ 
        FileAPI
        Author: Shaikh Aquib
        methods: get, post, delete, patch 
    """


    def __init__(self, cursor, helper, db):
        self.table  = "files"
        self.cursor = cursor
        self.helper = helper
        self.db     = db 
        self.cursor.execute("SHOW TABLES;")

        if self.table not in self.helper.fetch_list():
            self.cursor.execute(set_table_structure(self.table))

    def custom_error(self, message, status_code):
        """ Sending error codes with custom messages. """
        return make_response(jsonify(message), status_code)

    def post(self):
        """For uploading file."""
        parser = reqparse.RequestParser()
        parser.add_argument("file", type = werkzeug.datastructures.FileStorage, location = "files", help = "Attach an file", required=True)
        parser.add_argument("format", help = "Specify file format for file", required=True)
        parser.add_argument("filename", help = "Specify the name you want to put on file", default=None)
        args = parser.parse_args()

        # If name argument is given in the request then name it as according to it
        # else name it defaultly by giving Upload and current date
        if args["filename"] == None:        
            base_name = "FreeDrop" + get_formatted_date()         # File name
        else:
            base_name = args["filename"]
            extension = ("." + args['format'])
            if extension in base_name:
                base_name = base_name.replace(extension, "")

        # If files folder does not exists then create it
        parent_path = os.path.abspath(
            os.path.join(os.getcwd(), os.pardir)
        )
        files_dir = config.files_dir
        temp = files_dir
        files_dir = os.path.join(parent_path, temp)

        if temp not in os.listdir(parent_path):
            os.mkdir(files_dir)
        del parent_path
        del temp


        # Check if the file already exists if it exists then put a number on it.
        file_name   = os.path.abspath(os.path.join(files_dir, base_name))
        to_check    = format_path(file_name)
        matches     = self.helper.search_path(to_check, self.table)
        total_match = len(matches)  
        
        if total_match == 0:
            # If the path with same name does not exist then insert the current file_name.
            #print("[+] entered new file phase")
            file_name += ".{}".format(args['format'])
            self.helper.insert_value(table=self.table, path=file_name, file_format=args['format'])
        else:
            # Append the name with a numeral depending upon the total matches present.
            file_name += ("(" + str(total_match) + ")" + ".{}".format(args['format']))
            self.helper.insert_value(table=self.table, path=file_name, file_format=args['format'])
        
        self.db.commit()
        file_file = args['file']
        file_file.save(file_name)
        return {"status":"file uploaded successfully"} 

    def get(self, want, filename):
        """ For sending file to client. """
        args = {}

        args['filename'] = filename
        args['type']     = want 
        #parser = reqparse.RequestParser()
        #parser.add_argument("filename", type=str, help="Specify name of the file", default="null")
        #parser.add_argument("type",type=str,help="Use file_req for receiving a file from server\nUse list_files for getting list of all files present ", required=True)
        #args = parser.parse_args()

        print("Got type as {}".format(args['type']))

        if args['type'] == "file_req" and filename != "all":
            # Send specific file file
            result = self.helper.get_path(args['filename'], self.table)
            # If file not found return 404
            if len(result) == 0:
                return self.custom_error("file not found", 404)

            img_path = result[0]
            file_format = self.helper.get_format(img_path, self.table)[0]

            # Using make_response to include headers with the file
            # Would be used to determine file format
            response = make_response(send_file(img_path))
            response.headers['File-Format'] = file_format
            return response        

        elif args['type'] == "list_files" and args['filename'] == "all":
            # Send list of all file files present on the server
            all_files = self.helper.get_full_list("filename", self.table)
            resp = {"present files":all_files}
            return resp
        
    def delete(self):
        """ For removing files from server."""
        parser = reqparse.RequestParser()
        parser.add_argument("filename", help="Specify name of the file", required=True)
        args = parser.parse_args()
        filename = args['filename']

        # Get the path for file and check if it exists
        self.cursor.execute('SELECT path FROM {} WHERE filename="{}"'.format(self.table, filename))
        db_res = self.helper.fetch_list()
        # If no results were found then return 404
        if len(db_res) == 0:
            return self.custom_error("file not found", 404)

        # Now remove the file from server
        path = db_res[0]
        os.remove(path)
        
        # Delete record from database as well
        self.helper.delete_value(self.table, args['filename'])
        self.db.commit()
        return {"status":"file deleted sucessfully"}

    def patch(self):
        """ For renaming files on server. """
        parser = reqparse.RequestParser()
        parser.add_argument("current", help="Specify the current name of the file", required=True)
        parser.add_argument("new", help="Specify the new name of the file", required=True)
        args = parser.parse_args()

        # First check if the file even exists or not
        self.cursor.execute('SELECT path FROM {} WHERE filename="{}"'.format(self.table, args['current']))
        db_res = self.helper.fetch_list()
        # If no results were found then return 404
        if len(db_res) == 0:
            return self.custom_error("file not found", 404)
    
        format = self.helper.get_format(path_name=db_res[0], table_name=self.table)
        
        par_dir  = os.path.abspath(os.path.join(db_res[0], os.pardir))
        
        new_filename = None
        if not format[0] in args['new']:
            new_filename = args['new'] + "." + format[0]
        else:
            new_filename = args['new']

        new_path = os.path.join(par_dir, new_filename)

        #  Update filename
        self.helper.update_value(
            table         = self.table,
            column        = "filename",
            current_value = args['current'],
            new_value     = args['new']
        )
        # Update path
        self.helper.update_value(
            table         = self.table,
            column        = "filename",
            current_value = db_res[0],
            new_value     = new_path
        )
        self.db.commit()
        os.rename(db_res[0], new_path)
