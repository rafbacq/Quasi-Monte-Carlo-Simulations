import numpy as np
import pandas as pd
from scipy.stats.qmc import Sobol

# Step 1: Initialize Sobol generator for 2 dimensions
sobol_engine = Sobol(d=2, scramble=False)

# Step 2: Generate 1000 Sobol points
n_points = 20
points = sobol_engine.random(n=n_points)  # shape: (1000, 2)

# Step 3: Save to CSV using pandas
df = pd.DataFrame(points, columns=["x", "y"])
df.to_csv("20sobolpoints.csv", index=False)

print("Saved 20 Sobol (x, y) points to 'sobol_points.csv'")
