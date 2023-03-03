import os
from datetime import datetime
from flask import request, current_app, jsonify
from flask_restful import Resource
from flask_security import current_user, auth_required
from werkzeug.utils import secure_filename
from application.backend_jobs.import_task_list import import_task_list





def correct_file_extension(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config["UPLOAD_ALLOWED_EXTENSIONS"]

class ImportTaskListAPI(Resource):
    @auth_required('token')
    def post(self):

        try:
            current_app.logger.info("Entered Function")
            uploaded_file = request.files['file']
            current_app.logger.info(uploaded_file.filename)
            current_app.logger.info("File parsed")
        
            if uploaded_file and correct_file_extension(uploaded_file.filename):
                file_name=secure_filename(uploaded_file.filename).split('.')[0]+"__"+datetime.now().strftime("%Y_%m_%d")+".csv"
                file_path = os.path.join(current_app.config['UPLOAD_SAVE_FOLDER'], file_name)
                uploaded_file.save(file_path)
                import_task_list.apply_async([current_user.id,file_path])
                return jsonify({"response":"CSV File successfully uploaded. Task Lists should be successfully imported shortly!"})
            else:
                return jsonify({"response":"CSV File has some error in file name!"})
        except Exception as e:
            return jsonify({"response":e})


