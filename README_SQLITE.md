# Personal Finance Dashboard - SQLite Version

This is a modified version of the Personal Finance Dashboard that uses SQLite instead of PostgreSQL for easier local setup.

## Prerequisites

1. **Python 3.7+** - Make sure Python is installed and accessible in your PATH
2. **pip** - Python package manager

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install pandas sqlalchemy streamlit plotly pillow
   ```

2. **Verify installation:**
   ```bash
   python --version
   pip list
   ```

## Running the Application

1. **Navigate to the scripts directory:**
   ```bash
   cd scripts
   ```

2. **Run the Streamlit app:**
   ```bash
   streamlit run app_sqlite.py
   ```

3. **Open your browser** and go to `http://localhost:8501`

## Usage

1. **Upload Data**: 
   - Go to the "Data" tab
   - Upload a CSV file with the following columns: `Type`, `Date`, `Name`, `Amount`, `Currency`, `Category`, `Account`, `Status`
   - Click "Generate Dashboard"

2. **Sample Data**: 
   - A sample CSV file `sample_transactions.csv` is provided for testing

3. **Explore Dashboard**:
   - Use the "Dashboard" tab to view charts and analytics
   - Apply filters using the sidebar

## CSV Format

Your CSV file should have these exact columns:
- `Type`: "Income" or "Expense"
- `Date`: Date in YYYY-MM-DD format
- `Name`: Description of the transaction
- `Amount`: Numeric amount
- `Currency`: Currency code (e.g., PHP, USD)
- `Category`: Transaction category
- `Account`: Account name
- `Status`: Transaction status (should be "Reconciled" for processing)

## Database

The application uses SQLite and creates a local database file `personal_finance_dashboard.db` in the scripts directory. No database setup is required.

## Troubleshooting

1. **Python not found**: Make sure Python is installed and added to your PATH
2. **Module not found**: Install dependencies using the pip command above
3. **Port already in use**: Streamlit will automatically use a different port if 8501 is busy

## Features

- **Account Balance Tracking**: View net worth and individual account balances over time
- **Expense Analysis**: Categorize and visualize spending patterns
- **Income Tracking**: Monitor income sources and trends
- **Payment Methods**: Analyze preferred payment and receiving methods
- **Time-based Views**: Switch between daily, weekly, and monthly views
- **Interactive Charts**: All charts are interactive and filterable

## File Structure

```
personal-finance-dashboard/
├── scripts/
│   ├── app_sqlite.py          # Main Streamlit application (SQLite version)
│   ├── database_sqlite.py     # Database functions for SQLite
│   ├── read_queries_sqlite.py # Query functions for SQLite
│   ├── queries_sqlite.sql      # SQLite-compatible SQL queries
│   └── sample_transactions.csv # Sample data for testing
├── images/                    # Application images
└── README_SQLITE.md          # This file
```
