import pandas as pd
import json
from database_utils import get_all_tiles, save_tiles
from tile_longlat import deg2num


def issues_csv_to_json() -> None:
    """
    convert the issues in the csv file to json objects
    and write it to a file
    """
    df = pd.read_csv('./issues.csv')
    issues = []
    for idx, row in df.iterrows():
        curr_issue = {
            'longitude': row.longitude,
            'latitude': row.latitude,
            'image_id': str(row.image_id),
            'submissions': []
        }
        issues.append(curr_issue)
    with open("data/issues.json", "w") as f:
        json.dump(issues, f)


def get_neighbour_tiles(center: (int, int)) -> [(int, int, int)]:
    """
    center: (x,y) coordinate
    :return a list of neighbour tuples of shape (x,y,dist_to_center)
    """
    neighbors = []
    x, y = center
    for i in range(-2, 3):
        for j in range(-2, 3):
            # (x, y coordinate of neighbour, distance to center)
            neighbors.append((x + i, y + j, max(abs(i), abs(j))))
    return neighbors


def eval_tile_winner(tile: {}) -> [str]:
    """
    takes the user tile scores and returns the winner/tiles
    :param tile: the tile object
    :return: a list of winners (one if there is no tie)
    """
    max_score = tile["scores"].values()
    if tile["scores"].values().count(max_score) > 1:
        ties = []
        for user_id, score in tile["scores"].items():
            if score == max_score:
                ties.append(user_id)
        return ties
    else:
        return [max(tile["scores"], key=tile["scores"].get)]


def update_scores(issue: {}, user_id: str) -> None:
    """
    for a given issue, updates all relevant tiles if a new user submits an image
    :param issue: the issue object
    :param user_id: the id of the user
    updates are directly saved to the database
    """
    grid_location = deg2num(issue["latitude"], issue["longitude"], 16)
    neighbours = get_neighbour_tiles(grid_location)
    stored_tiles = get_all_tiles()
    new_tiles = []
    for x, y, dist in neighbours:
        base_score = 10 - len(issue['submissions'])
        add_score = base_score - 2 * dist
        new_tiles.append({
            "x": x,
            "y": y,
            "scores": {
                user_id: add_score
            }
        })
    final_tiles = []
    for new_tile in new_tiles:
        found_duplicate = False
        if len(stored_tiles) != 0:
            for old_tile in stored_tiles:
                if (new_tile["x"], new_tile["y"]) == (old_tile["x"], old_tile["y"]):
                    old_tile["scores"] = {k: new_tile["scores"].get(k, 0) + old_tile["scores"].get(k, 0) for k in
                                          set(new_tile["scores"]) | set(old_tile["scores"])}
                    found_duplicate = True
                    break
            if not found_duplicate:
                final_tiles.append(new_tile)
    save_tiles(stored_tiles + final_tiles)
