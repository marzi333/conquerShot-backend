from flask import Flask
from flask import request, jsonify
from database_utils import get_user, update_user, add_user, get_all_issues
from evaluate_single import evaluate_single_img
import json
import os

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/issues', methods=['GET'])
def get_issues():
    issues = get_all_issues()
    return jsonify(issues)


@app.route('/users', methods=['GET', 'POST', 'PUT'])
def user():
    user_id = request.args.get('user_id')
    if request.method == 'GET':
        user = get_user(user_id)
        return jsonify(user)
    elif request.method == 'POST':
        new_user = request.form
        add_user(new_user)
    elif request.method == 'PUT':
        updated_user = request.form
        update_user(updated_user)
    else:
        # POST Error 405 Method Not Allowed
        pass


@app.route('/image/upload', methods=['POST'])
def image_upload():
    files = request.files
    file = files.get('image')
    path = os.path.join('IMAGES_TO_EVAL/', file.filename)
    file.save(path)
    prediction = evaluate_single_img(path)
    return jsonify({
        'success': True,
        'file': 'Received'
    })


if __name__ == '__main__':
    app.run(debug=False)
