import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/raw/transactions.csv")

# Parse timestamp strings
df['transaction_date'] = pd.to_datetime(
    df['transaction_date'],
    format='%Y-%m-%d %H:%M:%S'
)

print("Datatype:")
print(df['transaction_date'].dtype)

print("\nMin date:", df['transaction_date'].min())
print("Max date:", df['transaction_date'].max())

df['day_of_week'] = df['transaction_date'].dt.day_name()
df['hour'] = df['transaction_date'].dt.hour

print("\nDay and Hour Features:")
print(df[['transaction_date', 'day_of_week', 'hour']])

hourly_volume = df.groupby('hour').size()

print("\nHourly Volume:")
print(hourly_volume)

plt.figure(figsize=(8,5))
df['hour'].hist(bins=24)

plt.title("Transaction Distribution by Hour")
plt.xlabel("Hour")
plt.ylabel("Frequency")

plt.savefig("output/hourly_distribution.png")
plt.show()

df['week_num'] = df['transaction_date'].dt.isocalendar().week

print("\nWeek Numbers:")
print(df[['transaction_date', 'week_num']])

df_ts = df.set_index('transaction_date')

weekly_revenue = df_ts['amount'].resample('W').sum()

print("\nWeekly Revenue:")
print(weekly_revenue)

weekly_revenue.plot()

plt.title("Weekly Revenue Trend")
plt.ylabel("Revenue")

plt.savefig("output/weekly_revenue.png")
plt.show()

today = pd.Timestamp.now()

customer_last_purchase = (
    df.groupby('customer_id')['transaction_date']
    .max()
)

recency_df = customer_last_purchase.reset_index()

recency_df['days_since_last_purchase'] = (
    today - recency_df['transaction_date']
).dt.days

print("\nRecency Data:")
print(recency_df)

print("\nRecency Statistics:")
print(
    recency_df['days_since_last_purchase']
    .describe()
)

inactive_customers = recency_df[
    recency_df['days_since_last_purchase'] > 30
]

print("\nInactive Customers:")
print(inactive_customers)

hourly_daily = df.groupby(
    ['day_of_week', 'hour']
).agg({
    'amount': ['sum', 'count', 'mean']
})

print("\nHourly Daily Aggregation:")
print(hourly_daily)

pivot_table = pd.pivot_table(
    df,
    values='amount',
    index='hour',
    columns='day_of_week',
    aggfunc='sum'
)

print("\nPivot Table:")
print(pivot_table)


import seaborn as sns

plt.figure(figsize=(10,6))

sns.heatmap(
    pivot_table,
    annot=True,
    cmap='YlGnBu'
)

plt.title("Hour vs Day Activity Heatmap")

plt.savefig("output/activity_heatmap.png")
plt.show()

peak = hourly_daily['amount']['count'].idxmax()

print("\nPeak Activity Window:")
print(peak)

print("\n===== TESTING =====")

print(
    f"Days in dataset: "
    f"{(df['transaction_date'].max() - df['transaction_date'].min()).days}"
)

print(
    f"Hours with data: "
    f"{df['hour'].unique()}"
)

print(
    f"Weeks in dataset: "
    f"{df['week_num'].nunique()}"
)

print(
    f"Min days since purchase: "
    f"{recency_df['days_since_last_purchase'].min()}"
)

print(
    f"Max days since purchase: "
    f"{recency_df['days_since_last_purchase'].max()}"
)   


df['week_num'] = df['transaction_date'].dt.isocalendar().week

print(df[['transaction_date', 'week_num']])


df_ts = df.set_index('transaction_date')

weekly_revenue = df_ts['amount'].resample('W').sum()

print(weekly_revenue)

peak = hourly_daily['amount']['count'].idxmax()

print(f"\nPeak Activity Window: {peak}")