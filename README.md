# Telecom Outage Analytics

# Analytics Workspace Setup

## Project Description

This repository provides a standardized analytics development environment for data product teams. It establishes a consistent project structure, dependency management process, environment configuration strategy, and collaboration workflow that can be used across different analytics and business intelligence projects.

---

## Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd analytics-workspace-setup
```

### 2. Create Virtual Environment

#### macOS/Linux

```bash
python3 -m venv venv
```

#### Windows

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

#### macOS/Linux

```bash
source venv/bin/activate
```

#### Windows

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Copy the example file:

```bash
cp .env.example .env
```

Windows:

```powershell
copy .env.example .env
```

Update the values in `.env` with your own credentials.

---

## Project Structure

```text
analytics-workspace-setup/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── scripts/
├── output/
├── requirements.txt
├── .gitignore
├── .env.example
└── README.md
```

### Directory Purpose

- data/raw → Stores original source data.
- data/processed → Stores cleaned and transformed data.
- notebooks → Contains Jupyter notebooks for analysis.
- scripts → Contains reusable Python scripts.
- output → Stores reports, charts, and exports.

---

## Notes

- Environment variables are stored in `.env`.
- Never commit the `.env` file to Git.
- Copy `.env.example` to `.env`.
- Replace placeholder values with your own credentials.
- Dependencies are managed through `requirements.txt`.