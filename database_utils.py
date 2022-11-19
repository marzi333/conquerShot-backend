import json
import time


def update_user(updated_user: {}):
    with open('data/users.json', "w") as f:
        users = json.load(f)
        users = [u for u in users if u['id'] != updated_user["id"]]
        users.append(updated_user)
        json.dump(users, f)


def update_issue(issue_id, user_id):
    with open('data/issues.json', "r") as f:
        issues = json.load(f)
    print(type(issues[0]['image_id']))
    old_issues = [i for i in issues if i['image_id'] != issue_id]
    to_update = [i for i in issues if i['image_id'] == issue_id][0]
    to_update["submissions"].append({
        "user_id": user_id,
        "timestamp": int(time.time())
    })
    old_issues.append(to_update)
    with open('data/issues.json', "w") as f:
        json.dump(old_issues, f)
    return to_update


def add_user(new_user: {}):
    with open('data/users.json') as f:
        users = json.load(f)
        users.append(new_user)
        json.dump(users, f)


def get_user(user_id):
    with open('data/users.json') as f:
        users = json.load(f)
    user = list(filter(lambda u: u['id'] == int(user_id), users))[0]
    return user


def get_all_issues():
    with open('data/issues.json') as f:
        issues = json.load(f)
    return issues


def get_all_tiles():
    with open('data/tiles.json') as f:
        tiles = json.load(f)
    return tiles
