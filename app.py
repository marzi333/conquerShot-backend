from flask import Flask
from flask import request, jsonify
from database_utils import get_user, update_user, add_user, get_all_issues, update_issue, get_all_tiles
from evaluate_single import evaluate_single_img
from utils import update_scores
from flask_cors import cross_origin
from tile_longlat import num2deg
import os

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/issues', methods=['GET'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def get_issues():
    issues = get_all_issues()
    return jsonify(issues)


@app.route('/tiles', methods=['GET'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def get_tiles():
    tiles = get_all_tiles()
    to_send = [
        {
            "bounds": [
                num2deg(tile["x"], tile["y"], 16),
                num2deg(tile["x"] + 1, tile["y"] + 1, 16)
            ],
            "user_id": max(tile["scores"], key=tile["scores"].get)
        } for tile in tiles
    ]
    return jsonify(to_send)


@app.route('/users', methods=['GET', 'POST', 'PUT'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
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
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def image_upload():
    user_id = request.form["user_id"]
    issue_id = request.form["issue_id"]
    file = request.files.get('image')
    path = os.path.join('IMAGES_TO_EVAL/', file.filename)
    file.save(path)
    if evaluate_single_img(path, 'road-cls') == 'road':
        issue = update_issue(int(issue_id), user_id)
        update_scores(issue, user_id)
        prediction = evaluate_single_img(path)
        return jsonify(get_all_tiles())
    else:
        return {'message': 'not a road'}, 400


if __name__ == '__main__':
    app.run(debug=False)
