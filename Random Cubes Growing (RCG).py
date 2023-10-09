#!/usr/bin/env python
# coding: utf-8

# In[4]:


# Random Cubes Growing algorithm © 2023 by Rail Kadyrov is licensed under CC BY-NC-ND 4.0
# Сite this work: Kadyrov, R.I., 2023. Multiple cubes growth algorithms for simple REV determination on 3D binary images. Scientific Visualization.

import numpy as np
import matplotlib.pyplot as plt
from skimage import io
from glob import glob
from scipy.spatial import distance

# Load the 3D binary image stack
folder_path = "C:/Users/.../"
file_extension = "*.tif"  # Change this to "*.png" if using PNG image stacks

# Get the paths of all image files in the folder
image_paths = glob(folder_path + file_extension)

# Read the image files and stack them
image_stack = np.stack([io.imread(image_path) for image_path in image_paths])

# Set the voxel size in mm
voxel_size = 0.001

# Set the number of random seeds
num_seeds = 25

# Define the zoom range in voxels
zoom_from = 2
zoom_to = min(image_stack.shape)     #change min(image_stack.shape) to the limit of upper size of the cubes, e.g. 100

def calculate_porosity(cube, voxel_size):
    cube_volume = np.prod(cube.shape)
    cube_pore_count = np.sum(cube)
    cube_porosity = cube_pore_count / cube_volume
    return cube_porosity

# Get the dimensions of the image stack
x, y, z = image_stack.shape

# Generate random seed points within the image volume
np.random.seed(42)  # for reproducibility
seed_points = np.random.randint(0, min(x, y, z), size=(num_seeds, 3))

# Calculate porosity for each seed point and cube size within the zoom range
all_porosity_values = np.zeros((num_seeds, zoom_to - zoom_from + 1))

for i, seed in enumerate(seed_points):
    for j, cube_size in enumerate(range(zoom_from, zoom_to + 1)):
        cube = np.zeros((cube_size, cube_size, cube_size), dtype=int)
        cube_start = np.array(seed) - cube_size
        cube_end = cube_start + cube_size

        for dim in range(3):
            if cube_start[dim] < 0:
                cube_start[dim] = 0
                cube_end[dim] = cube_size

            if cube_end[dim] > [x, y, z][dim]:
                cube_start[dim] = [x, y, z][dim] - cube_size
                cube_end[dim] = [x, y, z][dim]

        cube[:, :, :] = image_stack[
            cube_start[0]:cube_end[0], cube_start[1]:cube_end[1], cube_start[2]:cube_end[2]
        ]

        porosity = calculate_porosity(cube, voxel_size)
        all_porosity_values[i, j] = porosity

# Calculate mean porosity and standard deviation for each cube size
mean_porosity = np.mean(all_porosity_values, axis=0)
std_porosity = np.std(all_porosity_values, axis=0)

# Find the cube size where standard deviation is lowest
rev_size_index = np.argmin(std_porosity)

# Calculate the REV porosity at the intersection point
rev_porosity = mean_porosity[rev_size_index]

# Calculate the cube sizes in mm
cube_sizes = np.arange(zoom_from, zoom_to + 1) * voxel_size  # Update the calculation

# Plot the results
plt.figure(figsize=(10, 6))

for i, seed in enumerate(seed_points):
    plt.plot(cube_sizes, all_porosity_values[i])

plt.plot(cube_sizes, mean_porosity, label='Mean Porosity', linestyle='dashed', color='blue')

# Use following plot elements if necessary

plt.axvline(x=cube_sizes[rev_size_index], color='r', linestyle='--', label=f'Min Std Dev: {cube_sizes[rev_size_index]:.2f} mm')

plt.scatter(cube_sizes[rev_size_index], rev_porosity, color='r', marker='o', label=f'Proposed REV Porosity: {rev_porosity:.4f}')

plt.xlabel('Cube Size (mm)')
plt.ylabel('Porosity')
plt.title(f'Porosity vs. Cube Size (Seeds = {num_seeds})')
plt.legend()
plt.grid(True)
plt.show()


# In[ ]:




