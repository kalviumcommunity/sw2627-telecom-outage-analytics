import pandas as pd
import numpy as np

# ==========================================
# Setup: Generate Mock Data
# ==========================================
np.random.seed(42)
n_customers = 1000

df = pd.DataFrame({
    'customer_id': range(1, n_customers + 1),
    'days_as_customer': np.random.randint(30, 1000, n_customers),
    'total_transactions': np.random.randint(1, 150, n_customers),
    'total_spent': np.random.uniform(50, 5000, n_customers),
    'days_since_last_purchase': np.random.randint(1, 365, n_customers)
})
# Alias for RFM calculation consistency
df['purchase_count'] = df['total_transactions'] 

print("=" * 50)
print("Task 1: Compute Ratio Features")
print("=" * 50)
df['transactions_per_month'] = df['total_transactions'] / (df['days_as_customer'] / 30)
df['avg_spend_per_transaction'] = df['total_spent'] / df['total_transactions']
df['lifetime_value_per_month'] = df['total_spent'] / (df['days_as_customer'] / 30)

print(df[['transactions_per_month', 'avg_spend_per_transaction']].describe())


print("\n" + "=" * 50)
print("Task 2: Binning with Equal-Width Bins (pd.cut)")
print("=" * 50)
df['engagement_tier'] = pd.cut(
    df['transactions_per_month'],
    bins=[0, 2, 10, float('inf')],
    labels=['low', 'medium', 'high']
)

print(df['engagement_tier'].value_counts())


print("\n" + "=" * 50)
print("Task 3: Binning with Quantiles (pd.qcut)")
print("=" * 50)
df['spend_quartile'] = pd.qcut(
    df['total_spent'],
    q=4,
    labels=['Q1', 'Q2', 'Q3', 'Q4']
)

print(df['spend_quartile'].value_counts())


print("\n" + "=" * 50)
print("Task 4: Composite Score (RFM)")
print("=" * 50)
# Note: For recency, lower days is better, so the labels are reversed (5 is best)
df['recency_score'] = pd.qcut(df['days_since_last_purchase'], q=5, labels=[5,4,3,2,1])
df['frequency_score'] = pd.qcut(df['purchase_count'], q=5, labels=[1,2,3,4,5])
df['monetary_score'] = pd.qcut(df['total_spent'], q=5, labels=[1,2,3,4,5])

df['rfm_score'] = (df['recency_score'].astype(int) + 
                   df['frequency_score'].astype(int) + 
                   df['monetary_score'].astype(int))

print(df[['customer_id', 'rfm_score']].head())


print("\n" + "=" * 50)
print("Task 5: Feature Validation")
print("=" * 50)
# Check ranges are sensible
print(f"Engagement tier distribution:\n{df['engagement_tier'].value_counts()}\n")
print(f"RFM score range: {df['rfm_score'].min()} - {df['rfm_score'].max()}\n")

# Ensure no NaNs introduced
print("Missing values in engineered features:")
print(df[['engagement_tier', 'spend_quartile', 'rfm_score']].isna().sum())

# Optionally save the engineered dataset
import os
os.makedirs('data/processed', exist_ok=True)
df.to_csv('data/processed/engineered_customers.csv', index=False)