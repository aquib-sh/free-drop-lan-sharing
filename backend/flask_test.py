from flask_restful import Resource, Api, reqparse
from flask import Flask
import datetime
import werkzeug


app = Flask(__name__)
api = Api(app)

image_dir = "images"
video_dir = "videos"

class UploadImageAPI(Resource):
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('image', type=werkzeug.datastructures.FileStorage, location='files')
        args = parse.parse_args()        

        # Get current date for naming the file
        date = datetime.datetime.now().date()
        formatted_date = str(date.day)+"-"+str(date.month)+"-"+str(date.year)
        
        # Image name
        base_name = "Upload"+formatted_date+"jpg"
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



