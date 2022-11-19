from flask import Flask
from flask import request, jsonify
import json
import os

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/issues', methods=['GET'])
def get_all_issues():
    with open('issues.json') as f:
        issues = json.load(f)
    return jsonify(issues)


@app.route('/users', methods=['GET', 'POST'])
def user():
    user_id = request.args.get('user_id')
    if request.method == 'GET':
        with open('users.json') as f:
            users = json.load(f)
        print(users)
        user = list(filter(lambda u: u['id'] == int(user_id), users))[0]
        return jsonify(user)
    if request.method == 'POST':
        updated_user = request.form
        with open('users.json') as f:
            users = json.load(f)
        users = [u for u in users if u['id'] != updated_user["id"]]
        users.append(updated_user)
        with open("users.json", "w") as f:
            json.dump(users, f)
    else:
        # POST Error 405 Method Not Allowed
        pass


@app.route('/image/upload', methods=['POST'])
def image_upload():
    files = request.files
    file = files.get('image')
    path = os.path.join('IMAGES_TO_EVAL/', file.filename)
    file.save(path)
    # TODO: call model with path
    return jsonify({
        'success': True,
        'file': 'Received'
    })


if __name__ == '__main__':
    app.run(debug=False)
