import json

def update_user(updated_user: {}):
    with open('data/users.json', "w") as f:
        users = json.load(f)
        users = [u for u in users if u['id'] != updated_user["id"]]
        users.append(updated_user)
        json.dump(users, f)


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
