import numpy as np
import pandas as pd

# Step 1: Initialize Xoroshiro128++ RNG with a fixed seed for reproducibility
bitgen = np.random.Xoroshiro128(seed=42)
rng = np.random.Generator(bitgen)

# Step 2: Generate 200 uniform random points in 2D
n_points = 200
points = rng.random((n_points, 2))  # shape: (200, 2)

# Step 3: Save to CSV using pandas
df = pd.DataFrame(points, columns=["x", "y"])
df.to_csv("200GENERATEDxoroshiropoints.csv", index=False)

print("Saved 200 Xoroshiro (x, y) points to '200xoroshiropoints.csv'")
