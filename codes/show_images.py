import time
import numpy as np
import laspy as lp
import pptk
import os
import open3d as o3d

path = "YOUR PATH"  #path of the folder where your .las files were chosen
files_name = []

files = os.listdir(path)

for file in files:
    if file.endswith(".las"):
        files_name.append(path + file)

points = np.array([])
colors = np.array([])

for file in files_name[0:1]:

    point_cloud = lp.read(file)

    file_points = np.vstack((point_cloud.x, point_cloud.y, point_cloud.z)).transpose()
    file_colors = np.vstack((point_cloud.red, point_cloud.green, point_cloud.blue)).transpose()

    points = np.append(points, file_points)
    colors = np.append(colors, file_colors)

v = pptk.viewer(file_points)
v.wait()
selection = v.get("selected")

normals = pptk.estimate_normals(file_points[selection], k=5, r=np.inf)
idx_normals = np.where(abs(normals[...,2]) < 0.9)

viewer = pptk.viewer(file_points[idx_normals], colors[idx_normals])

idx_ground = np.where(file_points[...,2]>np.min(file_points[...,2]+0.3))
idx_wronglyfiltered = np.setdiff1d(idx_ground, idx_normals)
idx_retained = np.append(idx_normals, idx_wronglyfiltered)
viewer2 = pptk.viewer(file_points[idx_retained],colors[idx_retained])

