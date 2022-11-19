import pandas as pd
import json
from tile_longlat import deg2num


def issues_csv_to_json():
    df = pd.read_csv('./issues.csv')
    issues = []
    for idx, row in df.iterrows():
        curr_issue = {
            'longitude': row.longitude,
            'latitude': row.latitude,
            'image_id': row.image_id,
            'submissions': [],
            'modifier': 1
        }
        issues.append(curr_issue)
    with open("data/issues.json", "w") as f:
        json.dump(issues, f)


def get_neigh_dist(center):
    """
    center: (x,y) coordinate
    """
    neighbors = []
    x, y = center
    for i in range(-2, 3):
        for j in range(-2, 3):
            neighbors.append((x + i, y + j, max(abs(i), abs(j))))

    return neighbors


def update_scores(issue, user_id):
    grid_location = deg2num(issue["latitude"], issue["longitude"], 16)
    neighbors = get_neigh_dist(grid_location)
    stored_tiles = []
    new_tiles = []
    with open('data/tiles.json') as f:
        try:
            stored_tiles = json.load(f)
        except:
            print("No tiles yet. File empty")
    for x, y, dist in neighbors:
        base_score = 10 - len(issue['submissions'])
        add_score = base_score - 2 * dist
        new_tile = {
            "x": x,
            "y": y,
            "scores": {
                user_id: add_score
            }
        }
        if len(stored_tiles) != 0:
            for tile in stored_tiles:
                if (x, y) == (tile["x"], tile["y"]):
                    if user_id in tile["scores"].keys():
                        tile["scores"][user_id] += add_score
                    else:
                        tile["scores"][user_id] = add_score
                    new_tile = tile
        new_tiles.append(new_tile)
    print(len(new_tiles))
    with open('data/tiles.json', "w") as f:
        json.dump(new_tiles, f)


if __name__ == '__main__':
    test_issue = {
        "longitude": 11.527965543942017,
        "latitude": 48.14774795111176,
        "image_id": 2947015848899610,
        "submissions": [],
        "modifier": 1
    }
    update_scores(test_issue, "1")
