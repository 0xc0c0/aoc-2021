alg:
- init risk grid of same size as orig
- start at end
- repeat
  - add all points accessible from end
  - find lowest risk total among those points
  - populate risk grid
  - ...until 'start' is populated
- return grid[start]
