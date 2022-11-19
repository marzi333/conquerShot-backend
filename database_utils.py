import json
import time


def update_user(updated_user: {}) -> None:
    """
    updates a users properties in the database
    :param updated_user: the user with the updated properties
    """
    with open('data/users.json', "w") as f:
        users = json.load(f)
        users = [u for u in users if u['id'] != updated_user["id"]]
        users.append(updated_user)
        json.dump(users, f)
    return None


def update_issue(issue_id: str, user_id: str) -> {}:
    """
    updates an issues properties in the database
    :param issue_id: the id of the issue
    :param user_id:
    :return: the updated issue object
    """
    with open('data/issues.json', "r") as f:
        issues = json.load(f)
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


def get_user_by_id(user_id: str) -> {}:
    """
    given a user_id queries the user from the database
    :param user_id: the id of the desired user
    :return: the user object
    """
    with open('data/users.json') as f:
        users = json.load(f)
    user = list(filter(lambda u: u['id'] == int(user_id), users))[0]
    return user


def get_all_issues() -> [{}]:
    """
    queries  of all existing issues
    :return: a list of issue objects
    """
    with open('data/issues.json') as f:
        issues = json.load(f)
    return issues


def get_all_tiles() -> [{}]:
    """
    queries all conquered tiles
    :return: a list of tile objects
    """
    with open('data/tiles.json') as f:
        try:
            tiles = json.load(f)
            return tiles
        except:
            print("No tiles yet. File empty")
            return []


def save_tiles(tiles: [{}]) -> None:
    """
    updates the tiles
    :param tiles: a list of tile objects to persist
    """
    with open('data/tiles.json', "w") as f:
        json.dump(tiles, f)
