# Data Dictionary

## Dataset Overview
This dataset contains customer and transaction records ingested from source systems and internal quality files. It is maintained as the single source of truth for customer acquisition, revenue, and transaction health reporting.

Last Updated: 2026-06-10
Maintained By: Data Engineering Team

## Columns

### id
- **Type**: Integer
- **Business Meaning**: Unique identifier for each transaction record in ingestion.
- **Example**: 1
- **Null Handling**: Never null for ingested transactions.
- **Related KPI**: Transaction volume, ingestion completeness
- **Updates**: Assigned when the transaction record is created in ingestion.

### customer_id
- **Type**: Integer
- **Business Meaning**: Unique customer identifier used across CRM and billing.
- **Example**: 1
- **Null Handling**: Never null in source files.
- **Related KPI**: Customer retention, churn rate, revenue per customer
- **Updates**: Set when customer is created in CRM.

### customer_name
- **Type**: String
- **Business Meaning**: Full customer name for relationship and support context.
- **Example**: Alice Smith
- **Null Handling**: May be null only when the customer record is incomplete.
- **Related KPI**: Customer segmentation, customer experience analysis
- **Updates**: Updated from source customer profile.

### name
- **Type**: String
- **Business Meaning**: Alternate customer display name used in some source files.
- **Example**: Alice
- **Null Handling**: May be null if not provided.
- **Related KPI**: Customer identity matching
- **Updates**: Used to unify customer names when customer_name is not present.

### email
- **Type**: String
- **Business Meaning**: Primary customer contact email address.
- **Example**: alice@example.com
- **Null Handling**: If null, evaluate for missing contact information.
- **Related KPI**: Retention outreach, customer communication effectiveness
- **Updates**: Sourced from customer records.

### signup_date
- **Type**: Datetime
- **Business Meaning**: Date the customer signed up or was onboarded.
- **Example**: 2025-01-15
- **Null Handling**: Should be present for all active customers.
- **Related KPI**: Customer acquisition rate, cohort analysis
- **Updates**: Set at customer creation.

### transaction_amount
- **Type**: Float
- **Business Meaning**: Revenue earned from a single transaction.
- **Example**: 150.50
- **Unit**: USD
- **Null Handling**: Very rare; investigate if found.
- **Related KPI**: Monthly revenue, average transaction value, revenue velocity
- **Updates**: Set when transaction completes.

### amount
- **Type**: Float
- **Business Meaning**: Alternate transaction revenue field from source systems.
- **Example**: 100.00
- **Unit**: USD
- **Null Handling**: Should be normalized to transaction_amount for analytics.
- **Related KPI**: Monthly revenue, transaction revenue consistency
- **Updates**: Mapped to transaction_amount during ingestion.

### transaction_date
- **Type**: Datetime
- **Business Meaning**: Date when the customer made the purchase.
- **Example**: 2025-01-15
- **Null Handling**: Required for time-series KPIs.
- **Related KPI**: Sales velocity, revenue trend analysis
- **Updates**: Recorded from transaction event date.

### status
- **Type**: String
- **Business Meaning**: Current lifecycle state of the transaction.
- **Example**: completed
- **Null Handling**: If null, treat as unknown transaction state.
- **Related KPI**: Order completion rate, failed transaction rate
- **Updates**: Updated as transaction moves through systems.

## Column to KPI Mapping

### Monthly Revenue
- **Formula**: SUM(transaction_amount) or SUM(amount)
- **Related Columns**: transaction_amount, amount, transaction_date
- **Why It Matters**: Tracks total company revenue across all transactions.
- **Update Frequency**: Daily

### Transaction Volume
- **Formula**: COUNT(id)
- **Related Columns**: id, transaction_date
- **Why It Matters**: Measures total number of transactions processed.
- **Update Frequency**: Daily

### Sales Velocity
- **Formula**: COUNT(id) / days
- **Related Columns**: transaction_date, id
- **Why It Matters**: Measures rate of sales activity and business momentum.
- **Update Frequency**: Weekly

### Revenue per Customer
- **Formula**: SUM(transaction_amount) grouped by customer_id
- **Related Columns**: customer_id, transaction_amount, amount
- **Why It Matters**: Identifies high-value customers and retention focus.
- **Update Frequency**: Weekly

### Customer Acquisition
- **Formula**: COUNT(customer_id) filtered by signup_date in range
- **Related Columns**: customer_id, signup_date
- **Why It Matters**: Tracks new customer growth and acquisition campaigns.
- **Update Frequency**: Monthly

### Order Completion Rate
- **Formula**: COUNT(status='completed') / COUNT(id)
- **Related Columns**: status, id
- **Why It Matters**: Shows how many transactions successfully closed.
- **Update Frequency**: Daily

## Ambiguous Columns & Resolutions

### Column: status
- **Original Ambiguity**: Is this the transaction outcome, customer state, or processing stage?
- **Resolved Meaning**: Transaction lifecycle state for the order record.
- **Business Interpretation**: Shows whether the transaction was completed, pending, or failed.
- **Proposed Rename**: transaction_status
- **Risk If Misunderstood**: Misclassifying transactions could distort revenue, completion rate, and refund analysis.

### Column: amount
- **Original Ambiguity**: Does this refer to payment amount, invoice amount, or discount-adjusted amount?
- **Resolved Meaning**: Alternate transaction amount field equivalent to transaction_amount in this dataset.
- **Business Interpretation**: Revenue captured for the transaction.
- **Proposed Rename**: transaction_amount_usd
- **Risk If Misunderstood**: Using the wrong amount field could overstate or understate revenue.

### Column: name
- **Original Ambiguity**: Is this customer name, product name, or account name?
- **Resolved Meaning**: Customer display name from some source files.
- **Business Interpretation**: Used for customer identity matching.
- **Proposed Rename**: customer_display_name
- **Risk If Misunderstood**: Mixing it with other entity names could lead to incorrect customer-level joins.

## Column Relationships

### Revenue per Customer
- **Definition**: SUM(transaction_amount) grouped by customer_id
- **How It Matters**: Identifies customers with the highest revenue contribution and supports upsell/retention decisions.
- **Example**: "Top 10% of customers account for the majority of revenue."
- **Related Columns**: customer_id, transaction_amount, amount

### Customer Acquisition Trend
- **Definition**: COUNT(customer_id) over new signup_date periods
- **How It Matters**: Measures how quickly new customers enter the business pipeline.
- **Example**: "March saw 25 new customers, up 20% from February."
- **Related Columns**: customer_id, signup_date

### Order Completion by Status
- **Definition**: COUNT(status='completed') / COUNT(id)
- **How It Matters**: Reveals transaction quality and execution success.
- **Example**: "90% of orders are completed, 10% are pending or failed."
- **Related Columns**: status, id, transaction_date

### Revenue Velocity
- **Definition**: Rolling sum of transaction_amount over 30-day windows
- **How It Matters**: Tracks sales momentum and trend direction.
- **Example**: "Revenue velocity increased 15% quarter-over-quarter."
- **Related Columns**: transaction_amount, transaction_date

### Customer Identity Match
- **Definition**: Join customer_id with customer_name/email to validate customer records
- **How It Matters**: Ensures the same customer is tracked consistently across systems.
- **Example**: "Customer 1 appears with email alice@example.com in both customer and transaction sources."
- **Related Columns**: customer_id, customer_name, name, email
