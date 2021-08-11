import time
import numpy as np
import laspy as lp
import pptk
import os
import open3d as o3d

path = "YOUR PATH"  # Path of the folder where your .las files were chosen
files_name = []

files = os.listdir(path)

# Read all files names
for file in files:
    if file.endswith(".las"):
        files_name.append(path + file)

points = np.array([])
colors = np.array([])

# Loop through a number of files
for file in files_name[0:1]:

    point_cloud = lp.read(file)
    
    # Extract all points in the file (x, y, z) and the colors
    file_points = np.vstack((point_cloud.x, point_cloud.y, point_cloud.z)).transpose()
    file_colors = np.vstack((point_cloud.red, point_cloud.green, point_cloud.blue)).transpose()

    points = np.append(points, file_points)
    colors = np.append(colors, file_colors)

# Create the visualization screen
v = pptk.viewer(file_points)
v.wait() # Waits for the user to select 
selection = v.get("selected")

# Apply a filter to extract the principal components in the selected area
normals = pptk.estimate_normals(file_points[selection], k=5, r=np.inf)
idx_normals = np.where(abs(normals[...,2]) < 0.9)

# Viewer with the principal components
viewer = pptk.viewer(file_points[idx_normals], colors[idx_normals])
