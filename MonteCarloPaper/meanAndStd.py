import csv
import numpy as np

# Load 2D points
points = []
with open("pseudopoints200.csv", "r") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # skip header
    for row in reader:
        x, y = map(float, row)
        points.append([x, y])

points = np.array(points)

# Separate x and y
x_coords = points[:, 0]
y_coords = points[:, 1]

# Compute mean and standard deviation for x and y separately
mean_x = np.mean(x_coords)
std_x = np.std(x_coords, ddof=0)  # population std dev

mean_y = np.mean(y_coords)
std_y = np.std(y_coords, ddof=0)  # population std dev

print(f"Mean X: {mean_x:.4f}")
print(f"Standard Deviation X: {std_x:.4f}")
print(f"Mean Y: {mean_y:.4f}")
print(f"Standard Deviation Y: {std_y:.4f}")
