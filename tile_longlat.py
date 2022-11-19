import math

"""
Reference for deg2num and num2deg:
https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Mathematics
"""

def deg2num(lat_deg, lon_deg, zoom):
  lat_rad = math.radians(lat_deg)
  n = 2.0 ** zoom
  xtile = int((lon_deg + 180.0) / 360.0 * n)
  ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
  return (xtile, ytile)

def num2deg(xtile, ytile, zoom):
  n = 2.0 ** zoom
  lon_deg = xtile / n * 360.0 - 180.0
  lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
  lat_deg = math.degrees(lat_rad)
  return (lat_deg, lon_deg)



def tilecorner_longlat(issue_latitude, issue_longitude):
   [xtile,ytile] = deg2num(48.111355593621, 11.61430161647960, 16)
   [lat_corner,long_corner] = num2deg(xtile, ytile, 16)
   return (lat_corner, long_corner)


