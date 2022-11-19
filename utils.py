import pandas as pd
import json


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


def get_grid_location():
    return (0, 0)


def update_scores(issue):
    grid_location = get_grid_location()
    # stored_tiles = []
    # base_score = 0
    # for x, y, dist in tiles:
    #     score = base_score - (2 * dist)
    #     for stored_tile in stored_tiles:
    #         pass


if __name__ == '__main__':
    issues_csv_to_json()
