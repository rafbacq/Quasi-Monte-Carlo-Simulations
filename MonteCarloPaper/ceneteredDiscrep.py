import numpy as np
from scipy.stats import qmc
import pandas as pd

def compute_centered_discrepancy(points, num_grid=10000):
    """
    Compute the centered discrepancy of a point set in [0,1]^d.
    
    Args:
        points (ndarray): An (n, d) array of points in [0,1]^d
        num_grid (int): Number of random test boxes (x vectors)

    Returns:
        float: The centered discrepancy D_C(P)
    """
    n, d = points.shape
    max_diff = 0.0

    # Generate random x-values in [0,1]^d to approximate the sup
    # Generate random test boxes in [0,1]^d to approximate sup
    test_points = np.random.rand(num_grid, d)

    for x in test_points:
        # Count how many points are within the box [0, x]
        inside = np.all(points <= x, axis=1)
        N_P_x = np.sum(inside)

        empirical = N_P_x / n
        volume = np.prod(x)
        diff = abs(empirical - volume)

        max_diff = max(max_diff, diff)

    return max_diff
# Generate 1024 Sobol points in 2D
df = pd.read_csv("sobol_points.csv")  # ensure it contains columns x1, x2
points = df.to_numpy()

discrepancy = compute_centered_discrepancy(points, num_grid=10000)
print(f"Centered discrepancy: {discrepancy:.6f}")