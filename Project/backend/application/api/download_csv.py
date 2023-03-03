from flask import current_app, Response
from flask_restful import Resource

class DownloadCSVTemplateAPI(Resource):
    def get(self):
        try:
            with open(current_app.config['DOWNLOADABLE_FILES_FOLDER']+'ImportFile.csv') as file_:
                return Response(file_.read(),mimetype="text/csv")
            
            
        except Exception as e:
            current_app.logger.error(e)


    


