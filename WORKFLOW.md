# Telecom Outage Analytics Workflow
## Branching Strategy

- Main branch contains stable code.
- Feature branches follow feature/[description].
- Branches are deleted after merge.


## Commit Message Convention

Format:
[type]: [description]

Types:
- feat
- fix
- docs
- refactor
- chore


## Python Workflow Script

### How to Execute

Run from the repository root:

python scripts/data_workflow.py

### Functions

#### ingest_data(filepath)

Reads raw telecom outage data from a CSV file and returns a Pandas DataFrame.

#### process_data(df)

Removes duplicate records and calculates an operational impact score using outage alerts, customer complaints, and regional usage metrics.

#### output_results(df, output_path)

Writes processed results to a CSV file and prints execution statistics.

### Modifying for New Datasets

1. Replace the input CSV file in data/raw.
2. Update column names inside process_data if the schema changes.
3. Add new transformation logic as required.
4. Execute the script again to generate updated output.
