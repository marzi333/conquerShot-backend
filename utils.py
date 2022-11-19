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


if __name__ == '__main__':
    issues_csv_to_json()
