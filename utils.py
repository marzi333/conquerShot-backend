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
    neighbours = get_neigh_dist(grid_location)

    stored_tiles = []
    with open('data/tiles.json') as f:
        try:
            stored_tiles = json.load(f)
        except:
            print("No tiles yet. File empty")

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
        for old_tile in stored_tiles:
            if (new_tile["x"], new_tile["y"]) == (old_tile["x"], old_tile["y"]):
                old_tile["scores"] = {k: new_tile["scores"].get(k, 0) + old_tile["scores"].get(k, 0) for k in
                                      set(new_tile["scores"]) | set(old_tile["scores"])}
                found_duplicate = True
                break
        if not found_duplicate:
            final_tiles.append(new_tile)
    final_tile_set = stored_tiles + final_tiles
    print(len(final_tile_set))
    with open('data/tiles.json', "w") as f:
        json.dump(final_tile_set, f)


# if __name__ == '__main__':
#     test_issue = {
#         "longitude": 11.613106928911195,
#         "latitude": 48.17299008497127,
#         "image_id": 2096254440714769,
#         "submissions": [],
#         "modifier": 1
#     }
#     update_scores(test_issue, "2")
