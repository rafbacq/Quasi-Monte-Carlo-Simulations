import pandas as pd
import matplotlib.pyplot as plt

# Load the Sobol sequence CSV output
df = pd.read_csv("200sobolpoints.csv")

# Plot Sobol points (assuming 2D: x1 and x2)
plt.scatter(df['x'], df['y'], s=5)
plt.title("20 Quasi-Random Points (2D)")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)
plt.axis('square')  # keep aspect ratio square
plt.tight_layout()
plt.show()
