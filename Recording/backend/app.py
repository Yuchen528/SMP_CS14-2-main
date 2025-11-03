import json
import traceback
import datetime

import boto3
from botocore.exceptions import NoCredentialsError
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from s3_client import s3

S3_BUCKET = "cs14-2-recordingtool"

S3_PROJECTTASK_FOLDER = 'CMSContent/'

S3_INPUT_FOLDER = 'recording_results/'

S3_OUTPUT_FOLDER = 'Output/'

def create_app(config_name='development'):
    app = Flask(__name__)
    # 测试时用的配置
    app.config['TESTING'] = (config_name == 'testing')
    app.config['S3_BUCKET'] = os.environ.get('S3_BUCKET', 'cs14-2-recordingtool')
    CORS(app)

    # API for projectTask
    @app.route('/api/projectTask/upload', methods=['POST'])
    def upload_projectTask():
        file = request.files['file']
        s3.upload_fileobj(file, S3_BUCKET, f"{S3_PROJECTTASK_FOLDER}{file.filename}")
        return 'Upload projectTask.json Successfully!', 200

    @app.route('/api/projectTask/get_projectTask_list', methods=['GET'])
    def list_project_tasks():
        try:
            response = s3.list_objects(Bucket=S3_BUCKET, Prefix=S3_PROJECTTASK_FOLDER)
            result = []
            for obj in response.get('Contents', []):
                key = obj['Key']
                if key.endswith('.json'):
                    file_name = key.split('/')[-1]
                    obj_data = s3.get_object(Bucket=S3_BUCKET, Key=key)
                    content = obj_data['Body'].read().decode('utf-8')
                    json_data = json.loads(content)
                    name = json_data.get('projectName', '(Unnamed)')
                    result.append({'filename': file_name, 'name': name})
            return jsonify(result), 200
        except Exception as e:
            print("List Acquisition Failed:", e)
            return f'List Acquisition Failed: {str(e)}', 500

    @app.route('/api/projectTask/get_projectTask', methods=['GET'])
    def get_project_task():
        try:
            file_name = request.args.get('file')
            if not file_name:
                return 'Missing File Name', 400
            key = f'{S3_PROJECTTASK_FOLDER}{file_name}'
            obj = s3.get_object(Bucket=S3_BUCKET, Key=key)
            content = obj['Body'].read().decode('utf-8')
            return jsonify(json.loads(content)), 200
        except Exception as e:
            return f'Read Failed: {str(e)}', 500

    @app.route('/api/projectTask/update', methods=['PUT'])
    def update_projectTask():
        file = request.files.get('file')
        if not file:
            return 'Missing file to update', 400

        filename = secure_filename(file.filename)
        key = f"{S3_PROJECTTASK_FOLDER}{filename}"
        try:
            s3.upload_fileobj(file, S3_BUCKET, key)
            return f'Updated {filename} Successfully!', 200
        except Exception as e:
            return f'Update Failed: {str(e)}', 500

    @app.route('/api/projectTask/delete', methods=['DELETE'])
    def delete_projectTask():
        file_name = request.args.get('file')
        if not file_name:
            return 'Missing file name to delete', 400

        key = f"{S3_PROJECTTASK_FOLDER}{secure_filename(file_name)}"
        try:
            s3.delete_object(Bucket=S3_BUCKET, Key=key)
            return f'Deleted {file_name} Successfully!', 204
        except Exception as e:
            print(e)
            return f'Delete Failed: {str(e)}', 500


    # API for recording result
    @app.route('/api/recording/upload', methods=['POST'])
    def upload_recording():
        try:
            form = request.form
            files = request.files
            project_name = form.get('projectName', '').strip()
            first_name = form.get('firstName', '').strip()
            last_name = form.get('lastName', '').strip()
            email = form.get('email', '')
            uuid = form.get('uuid', '')
            # task_title = form.get('taskTile')
            task_index = form.get('taskIndex')

            base_prefix = f"recording_results/{secure_filename(project_name)}/{secure_filename(uuid)}/"
            recording_prefix = base_prefix + f"task_{task_index}/"
            saved_keys = {}
            for field in ['recordedScreen', 'recordedCamera', 'recordedAudio']:
                file = files.get(field)
                if file and task_index is not None:
                    name = secure_filename(file.filename)
                    key = recording_prefix + name
                    s3.upload_fileobj(file, S3_BUCKET, key)
                    saved_keys[field] = key
            if first_name or last_name or email:
                metadata = {
                    "firstName": first_name,
                    "lastName": last_name,
                    "email": email,
                    "timestamp": datetime.datetime.now().isoformat()
                }
                body = json.dumps(metadata, ensure_ascii=False, indent=2)
                ts = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                filename = secure_filename(f"{ts}_user_data.json")
                key = base_prefix + filename
                s3.put_object(Bucket=S3_BUCKET, Key=key, Body=body, ContentType='application/json')
                saved_keys['metadata'] = key
            return jsonify({"status": "success", "keys": saved_keys}), 200
        except Exception as e:
            traceback.print_exc()
            return jsonify({"status": "error", "message": str(e)}), 500

    @app.route('/api/recording/get_recording', methods=['GET'])
    def get_recording():
        # to do
        return

    @app.route('/api/recording/delete_recording', methods=['DELETE'])
    def delete_recording():
        # to do
        return

    # API for visualization
    @app.route('/api/visualization/get_project_list', methods=['GET'])
    def get_output_project_list():
        try:
            response = s3.list_objects_v2(Bucket=S3_BUCKET, Prefix=S3_OUTPUT_FOLDER, Delimiter='/')
            projects = [prefix['Prefix'].split('/')[-2] for prefix in response.get('CommonPrefixes', [])]
            return jsonify(projects), 200
        except NoCredentialsError:
            return jsonify({"error": "S3 credentials not found"}), 500
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/api/visualization/get_heatmap_list/<project_name>', methods=['GET'])
    def get_output_result(project_name):
        try:
            prefix = f"{S3_OUTPUT_FOLDER}{project_name}/"
            response = s3.list_objects_v2(Bucket=S3_BUCKET, Prefix=prefix)
            images = [
                {
                    'url': f"https://{S3_BUCKET}.s3.amazonaws.com/{obj['Key']}",
                    'name': obj['Key'].split('/')[-1]
                }
                for obj in response.get('Contents', [])
                if obj['Key'].lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))
            ]
            return jsonify(images), 200
        except NoCredentialsError:
            return jsonify({"error": "S3 credentials not found"}), 500
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    # API for analysis
    ##❗The analysis group has already implemented the analysis code❗##
    ##❗But we do not have enough time to implement those API from Week 11❗##

    return app


if __name__ == '__main__':
    app = create_app('development')
    app.run(host='0.0.0.0', port=5000, debug=app.config.get('DEBUG', False))
