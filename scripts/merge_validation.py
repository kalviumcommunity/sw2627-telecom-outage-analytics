import pandas as pd
import numpy as np
import json
import os

# Create output directory if it doesn't exist
os.makedirs('output', exist_ok=True)

# ==========================================
# Setup: Generate Mock Data
# ==========================================
# 1000 Customers (IDs 1 to 1000)
df_customers = pd.DataFrame({
    'customer_id': range(1, 1001),
    'name': [f"Customer_{i}" for i in range(1, 1001)]
})

# 5000 Orders (Simulating orphaned orders and customers with no orders)
# Let's say 4900 orders belong to customers 1-900, and 100 are orphaned (IDs 1001+)
np.random.seed(42)
customer_ids_with_orders = list(np.random.choice(range(1, 901), size=4900))
orphaned_customer_ids = list(np.random.choice(range(1001, 1100), size=100))

df_orders = pd.DataFrame({
    'order_id': range(1, 5001),
    'customer_id': customer_ids_with_orders + orphaned_customer_ids,
    'amount': np.random.uniform(15, 250, size=5000).round(2)
})

print("=" * 50)
print("Task 1: Explicit Join with Row Count Validation")
print("=" * 50)
print(f"Left: {len(df_customers)}")
print(f"Right: {len(df_orders)}")

df_merged = pd.merge(df_customers, df_orders, on='customer_id', how='left')

print(f"Merged: {len(df_merged)}")
print(f"Change: {len(df_merged) - len(df_customers)}")


print("\n" + "=" * 50)
print("Task 2: Detect Unmatched Keys")
print("=" * 50)
unmatched_customers = df_customers[~df_customers['customer_id'].isin(df_orders['customer_id'])]
unmatched_orders = df_orders[~df_orders['customer_id'].isin(df_customers['customer_id'])]

print(f"Customers without orders: {len(unmatched_customers)}")
print(f"Orphaned orders: {len(unmatched_orders)}")

# Export anomalies for auditing
unmatched_customers.to_csv('output/unmatched_customers.csv', index=False)
unmatched_orders.to_csv('output/unmatched_orders.csv', index=False)


print("\n" + "=" * 50)
print("Task 3: Compare Join Types")
print("=" * 50)
inner = pd.merge(df_customers, df_orders, on='customer_id', how='inner')
left = pd.merge(df_customers, df_orders, on='customer_id', how='left')
outer = pd.merge(df_customers, df_orders, on='customer_id', how='outer')

print(f"Inner: {len(inner)}, Left: {len(left)}, Outer: {len(outer)}")


print("\n" + "=" * 50)
print("Task 4: Validate No Unexpected Duplication")
print("=" * 50)
# Check for unexpected column conflicts
print("Columns in merged dataset:", df_merged.columns.tolist())

# If customer_id appears in both, verify merge key behavior
key_counts = df_merged['customer_id'].value_counts()
print(f"Max orders per customer: {key_counts.max()}")


print("\n" + "=" * 50)
print("Task 5: Document Join Decision")
print("=" * 50)
join_report = {
    'join_type': 'left',
    'left_table': 'customers',
    'right_table': 'orders',
    'join_key': 'customer_id',
    'left_rows': len(df_customers),
    'right_rows': len(df_orders),
    'result_rows': len(df_merged),
    'unmatched_left': len(unmatched_customers),
    'unmatched_right': len(unmatched_orders),
    'reasoning': 'Left join preserves all customers; unmatched customers have no orders'
}

# Print nicely formatted JSON to standard output
print(json.dumps(join_report, indent=2))

# Optionally save the report to disk
with open('output/join_decision.json', 'w') as f:
    json.dump(join_report, f, indent=2)