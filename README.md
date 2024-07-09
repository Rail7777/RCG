# RCG

Random Cubes Growing (RCG) algorithm for determining the representative elementary volume (REV) of pore space in a binarized image stack.

RCG algorithm randomly selects seed points within the 3D stack and grows cubic regions around them and systematically computes porosity for various cube sizes, determining the average porosity and standard deviation for each extent

Install Jupyter Notebook or Python 3.9.16 for work.

Use TIF or PNG format for the image stack. The pores should be white (1) on binarized images.

Cite the work: Kadyrov, R. I. (2024). Multiple Cubes Growth Algorithms for Simple Representative Elementary Volume Determination on 3D Binary Images. Scientific Visualization, 16(50), 124–135. https://doi.org/10.26583/sv.16.1.11
