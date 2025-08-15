import numpy as np
import pandas as pd
from scipy.stats import qmc
import argparse
import sys

def star_discrepancy(points: np.ndarray, num_test: int = 1024, method: str = "sobol", seed: int | None = None) -> float:
    """
    Approximate the star discrepancy of a point set P in [0,1]^d:
        D_N(P) = sup_{x in [0,1]^d} | N(P, x)/N - Vol([0, x]) |
    by sampling candidate x's (axis-aligned boxes [0, x]).

    Args:
        points: (N, d) array with all coordinates assumed in [0,1].
        num_test: number of test box corners to sample for approximating the supremum.
        method: "sobol" or "random" for how to choose test x's.
        seed: random seed for reproducibility (affects "random" and scrambled Sobol).

    Returns:
        Approximated star discrepancy (float).
    """
    n, d = points.shape
    # Generate test x's
    if method == "sobol":
        # Sobol requires a power-of-two base if using random_base2.
        # We'll pick m such that 2^m >= num_test and then truncate.
        m = int(np.ceil(np.log2(num_test)))
        sampler = qmc.Sobol(d=d, scramble=True, seed=seed)
        test_pts = sampler.random_base2(m)  # produces 2^m points
        if test_pts.shape[0] > num_test:
            test_pts = test_pts[:num_test]
    elif method == "random":
        rng = np.random.default_rng(seed)
        test_pts = rng.random((num_test, d))
    else:
        raise ValueError(f"Unknown method '{method}'; choose 'sobol' or 'random'.")

    # Always include the sample point coordinates themselves as candidate x's,
    # since they often are informative for the sup, and also include the upper corner [1,...,1].
    extra = points.copy()
    upper = np.ones((1, d), dtype=float)
    combined = np.vstack([test_pts, extra, upper])

    max_diff = 0.0
    # Precompute: for efficiency we can sort if needed, but we'll do the straightforward loop.
    for x in combined:
        # Count of points in [0, x] (inclusive)
        inside = np.all(points <= x, axis=1)
        N_P_x = np.sum(inside)
        empirical = N_P_x / n
        volume = np.prod(x)
        diff = abs(empirical - volume)
        if diff > max_diff:
            max_diff = diff
    return max_diff

def main():
    parser = argparse.ArgumentParser(description="Approximate star discrepancy of a point set CSV in [0,1]^d.")
    parser.add_argument("csv_path", help="Path to CSV. Each row should be a point; columns are coordinates (no header required).")
    parser.add_argument("--num-test", type=int, default=2048, help="Number of test boxes to sample (default: 2048).")
    parser.add_argument("--method", choices=["sobol", "random"], default="sobol", help="Sampling method for test x's (default: sobol).")
    parser.add_argument("--seed", type=int, default=42, help="Random seed (affects random or scrambled Sobol).")
    parser.add_argument("--clip", action="store_true", help="Clip input points to [0,1] if they slightly exceed due to numerical issues.")
    args = parser.parse_args()

    # Load CSV (handles a header row and non-numeric debris)
    try:
        df = pd.read_csv(args.csv_path)  # lets pandas infer header
    except Exception as e:
        print(f"Failed to read CSV '{args.csv_path}': {e}", file=sys.stderr)
        sys.exit(1)

    # Coerce all columns to numeric, turning bad entries into NaN
    df = df.apply(pd.to_numeric, errors="coerce")

    # Drop rows with any non-numeric / missing values
    if df.isna().any().any():
        dropped = df.isna().any(axis=1).sum()
        print(f"Warning: dropped {dropped} rows due to non-numeric values.", file=sys.stderr)
        df = df.dropna()

    points = df.to_numpy(dtype=float)
    if args.clip:
        points = np.clip(points, 0.0, 1.0)

    if np.any(points < 0.0) or np.any(points > 1.0):
        print("Warning: some points fall outside [0,1]^d. Star discrepancy assumes points in the unit cube.", file=sys.stderr)

    discrepancy = star_discrepancy(points, num_test=args.num_test, method=args.method, seed=args.seed)
    n, d = points.shape
    print(f"Loaded {n} points in {d} dimensions from '{args.csv_path}'.")
    print(f"Approximated star discrepancy (method={args.method}, num_test={args.num_test}): {discrepancy:.8f}")

if __name__ == "__main__":
    main()
