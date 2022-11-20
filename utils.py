import random

import pandas as pd
import json
import math
from database_utils import get_all_tiles, save_tiles

"""
Reference for deg2num and num2deg:
https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Mathematics
"""


def deg2num(lat_deg: float, lon_deg: float, zoom: int) -> (int, int):
    """
    computes the (x,y) grid index in the OSM map for a given point
    :param lat_deg: the latitude of a point
    :param lon_deg: the longitude of a point
    :param zoom: the zoom level of the map
    :return: the gird indices
    """
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return xtile, ytile


def num2deg(x_tile: int, y_tile: int, zoom: int) -> (float, float):
    """
    computes the inverse of the above. Given the (x,y) grid indeces of a OSM map tile, the corersponding latidue and
    longitude of the top-left tile-corner are computed
    :param x_tile: the x index of the tile in the tile-grid
    :param y_tile: the y index of the tile in the tile-grid
    :param zoom: the zoom level of the map
    :return: the latitude and longitude of the top-left corner of the tile cell
    """
    n = 2.0 ** zoom
    lon_deg = x_tile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * y_tile / n)))
    lat_deg = math.degrees(lat_rad)
    return lat_deg, lon_deg


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
            'submissions': [],
            'icon': random.choice(['tower', 'castle', 'village'])
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
    max_score = max(tile["scores"].values())
    if list(tile["scores"].values()).count(max_score) > 1:
        ties = []
        for user_id, score in tile["scores"].items():
            if score == max_score:
                ties.append(user_id)
        return ties
    else:
        return [max(tile["scores"], key=tile["scores"].get)]


def compute_user_total_score(user_id: str) -> int:
    """
    computes the users global overall score
    :param user_id: the id of the user
    :return: the total score
    """
    tiles = get_all_tiles()
    total_score = 0
    for tile in tiles:
        if user_id in tile["scores"].keys():
            total_score += tile["scores"][user_id]
    return total_score


def compute_user_min_max_tile_score(user_id: str) -> (int, int):
    """
    gets a users min and max value of all his tiles
    :param user_id: the user id
    :return: the min and max scores overall the users tiles
    """
    tiles = get_all_tiles()
    min_score = 999999
    max_score = 0
    for tile in tiles:
        if user_id in tile["scores"].keys():
            if tile["scores"][user_id] < min_score:
                min_score = tile["scores"][user_id]
            if tile["scores"][user_id] > max_score:
                max_score = tile["scores"][user_id]
    return min_score, max_score


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
        for old_tile in stored_tiles:
            if (new_tile["x"], new_tile["y"]) == (old_tile["x"], old_tile["y"]):
                old_tile["scores"] = {k: new_tile["scores"].get(k, 0) + old_tile["scores"].get(k, 0) for k in
                                      set(new_tile["scores"]) | set(old_tile["scores"])}
                found_duplicate = True
                break
        if not found_duplicate:
            final_tiles.append(new_tile)
    save_tiles(stored_tiles + final_tiles)


if __name__ == '__main__':
    issues_csv_to_json()
