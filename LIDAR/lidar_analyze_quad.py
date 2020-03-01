
# breaks scan into four quadrants
# passes array [left, back, right, front]

from numpy import *
from math import *
import time
from matplotlib import pyplot as plt

# call specific laser scan file
scan_data = 'LIDAR/lidar_sample_scan.txt'

# CHOOSE ANALYSIS METHOD as "quadrant" or "intensity"
# quandrant: # checks for obst_size (number of consecutive dots) within safe_range
# intensity: calculate obst_intensity (percentage of obstacles in that quadrant)
method = "intensity"


# --- PROCESS SCAN DATA ---

angles = arange(-pi, pi, pi/180)

distances = zeros(len(angles))
with open(scan_data) as f:
    distances = f.read().split(', ')

for i in range(0,len(angles)):
    distances[i] = round(float(distances[i]),5)


# --- ANALYZE SCAN ---

obst_size = 4           # number of consecutive dots
safe_range = 0.5        # search ranges for obstacles

quad_obstacles = [0,0,0,0]
obst_intensity = [0.,0.,0.,0.]

for i in range(0,360):
    if distances[i] > safe_range: distances[i] = 0
    else: distances[i] = 1

# reorder distances vector to reflect quadrants of interest

distances[0:45] = distances[315:360]
distances[46:360] = distances[0:314]


if method == "quadrant":

    for quad in range(0,4):
        quad_check = zeros((90-obst_size,1))

        for j in range(90*quad, 90*(quad+1) - obst_size):
            scan_obst_size = 0

            for k in range(0,obst_size):
                if distances[j+k] == 1: scan_obst_size = scan_obst_size + 1

            if scan_obst_size == obst_size: quad_check[j-90*quad] = 1

        if sum(quad_check >= 1): quad_obstacles[quad] = 1

    print(quad_obstacles)


elif method == "intensity":

    quad_points = [0.,0.,0.,0.]
    for quad in range(0,4):
        for j in range(90*quad, 90*(quad+1)):
            if distances[j] == 1: quad_points[quad] = quad_points[quad] + 1

    obst_intensity = quad_points/sum(quad_points)

    print(obst_intensity)
