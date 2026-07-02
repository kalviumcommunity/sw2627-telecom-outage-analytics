import numpy as np
import pandas as pd
import time

# Generate dummy data (100k rows) so the script runs
np.random.seed(42)
df = pd.DataFrame({'revenue': np.random.randint(100, 10000, size=100000)})

# --- Task 1: Replace Loop with NumPy Vectorization ---
revenue_array = df['revenue'].values
normalized_np = (revenue_array - revenue_array.min()) / (revenue_array.max() - revenue_array.min())

# --- Task 2: Z-Score Normalization ---
z_scores = (revenue_array - revenue_array.mean()) / revenue_array.std()

# --- Task 3: Bulk Ranking/Scoring ---
rankings = np.argsort(-revenue_array)  # Negative for descending
revenue_rank = np.empty_like(rankings)
revenue_rank[rankings] = np.arange(1, len(rankings) + 1)

# --- Task 4: Time Performance Comparison ---
print("Running performance comparison...")
# Time loop version
start = time.time()
result_loop = []
for val in df['revenue']:
    result_loop.append(val * 1.1)
loop_time = time.time() - start

# Time NumPy version
start = time.time()
result_np = df['revenue'].values * 1.1
np_time = time.time() - start

print(f"Loop: {loop_time:.4f}s")
print(f"NumPy: {np_time:.4f}s")
print(f"Speedup: {loop_time/np_time:.0f}x\n")

# --- Task 5: Integrate Back to DataFrame ---
df['revenue_normalized'] = normalized_np
df['revenue_zscore'] = z_scores
df['revenue_rank'] = revenue_rank

# Verify types and shapes
print(f"Final Data Shape: {df.shape}")
print(f"Dtypes:\n{df.dtypes}")