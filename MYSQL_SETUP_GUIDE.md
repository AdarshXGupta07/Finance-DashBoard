# MySQL Database Setup Guide for Personal Finance Dashboard

This comprehensive guide helps you set up MySQL database for your personal finance dashboard with complete database creation, user management, data upload, and backup functionality.

## 🚀 Quick Start

### Prerequisites
- Python 3.7+ installed
- MySQL Server installed and running
- Administrative access to MySQL

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run Automated Setup
```bash
cd scripts
python mysql_setup.py
```

This script will:
- Create the database and user
- Set up all required tables
- Insert default categories and accounts
- Create `.env` file with credentials

### Step 3: Run the Application
```bash
streamlit run app_mysql.py
```

## 📋 Detailed Setup Instructions

### Option A: Automated Setup (Recommended)

#### 1. Complete Database Setup
```bash
cd scripts
python mysql_setup.py
```

The script will prompt for:
- MySQL root password
- Password for finance_user (or auto-generate)

#### 2. Upload Your Data
```bash
python data_upload_manager.py
```

#### 3. Set Up Backups
```bash
python backup_restore_manager.py
```

### Option B: Manual Setup

#### 1. Create Database and User
```sql
-- Log in to MySQL as root
mysql -u root -p

-- Create database
CREATE DATABASE personal_finance_dashboard CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create user (replace 'your_password' with a secure password)
CREATE USER 'finance_user'@'localhost' IDENTIFIED BY 'your_password';
CREATE USER 'finance_user'@'%' IDENTIFIED BY 'your_password';

-- Grant permissions
GRANT ALL PRIVILEGES ON personal_finance_dashboard.* TO 'finance_user'@'localhost';
GRANT ALL PRIVILEGES ON personal_finance_dashboard.* TO 'finance_user'@'%';
FLUSH PRIVILEGES;
```

#### 2. Initialize Database Schema
```bash
cd scripts
mysql -u finance_user -p personal_finance_dashboard < init_database.sql
```

#### 3. Configure Environment
Create `.env` file:
```bash
# MySQL Database Configuration
MYSQL_USER=finance_user
MYSQL_PASSWORD=your_password
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=personal_finance_dashboard

# Application Settings
APP_ENV=production
DEBUG=False
```

## 📊 Database Schema

### Tables Overview

#### `categories`
Stores transaction categories with types (Income/Expense/Both)

#### `accounts`
Stores financial accounts with types (Asset/Liability/Equity)

#### `raw_transactions`
Stores imported CSV data in original format

#### `transactions`
Processed and cleaned transaction data for analysis

### Key Features
- **Foreign Key Relationships**: Maintains data integrity
- **Indexes**: Optimized for query performance
- **Timestamps**: Tracks creation and updates
- **Views**: Pre-defined queries for common reports
- **Stored Procedures**: Reusable database operations

## 📤 Data Management

### Uploading CSV Files

#### CSV Format Requirements
Your CSV must include these columns:
- `Type`: Income, Expense, or Transfer
- `Date`: Transaction date (YYYY-MM-DD format)
- `Name`: Transaction description
- `Amount`: Numeric amount
- `Currency`: Currency code (default: PHP)
- `Category`: Transaction category
- `Account`: Account name
- `Status`: Reconciled, Pending, or Cleared

#### Using Data Upload Manager
```bash
python scripts/data_upload_manager.py
```

Features:
- **Validation**: Checks data format and required fields
- **Preview**: Shows data before upload
- **Cleaning**: Processes and standardizes data
- **Error Reporting**: Detailed validation messages

#### Manual Upload (Python)
```python
from database_mysql import extract, transform, load

# Extract data from CSV
raw_data = extract('your_transactions.csv')

# Transform and clean
clean_data = transform(raw_data)

# Load to database
load(clean_data, 'raw_transactions')
```

### Sample CSV Structure
```csv
Type,Date,Name,Amount,Currency,Category,Account,Status
Expense,2024-01-15,Grocery Store,2500.00,PHP,Food & Dining,Wallet,Reconciled
Income,2024-01-16,Salary,50000.00,PHP,Salary,BDO,Reconciled
Transfer,2024-01-17,Load GCash,5000.00,PHP,Transfer,Union Bank,Reconciled
```

## 👥 User Management

### Using User Manager
```bash
python scripts/mysql_user_manager.py
```

#### Available Operations
1. **Create Main User**: Full database access
2. **Create Read-Only User**: For reporting dashboards
3. **Update Passwords**: Secure password changes
4. **List Users**: View all finance dashboard users
5. **Delete Users**: Remove user accounts
6. **Test Connections**: Verify user credentials

#### Security Best Practices
- Use strong, unique passwords
- Create separate users for different applications
- Use read-only users for reporting
- Regularly update passwords
- Limit user privileges to minimum required

## 💾 Backup and Restore

### Using Backup Manager
```bash
python scripts/backup_restore_manager.py
```

#### Backup Types
1. **Full Backup**: Complete database with structure and data
2. **Data Backup**: JSON format with just the data
3. **Automatic Backups**: Scheduled backups with cleanup

#### Backup Commands
```bash
# Create compressed full backup
python backup_restore_manager.py  # Option 1

# Create data-only backup
python backup_restore_manager.py  # Option 2

# List all backups
python backup_restore_manager.py  # Option 3

# Restore from backup
python backup_restore_manager.py  # Option 4
```

#### Manual Backup (Command Line)
```bash
# Full backup with compression
mysqldump -u finance_user -p personal_finance_dashboard | gzip > backup_$(date +%Y%m%d).sql.gz

# Restore from compressed backup
gunzip < backup_20240115.sql.gz | mysql -u finance_user -p personal_finance_dashboard
```

#### Automatic Backups
```bash
# Create backup script
python backup_restore_manager.py  # Option 6

# Add to crontab for daily backups at 2 AM
crontab -e
# Add: 0 2 * * * /path/to/backups/auto_backup.sh
```

## 🔧 Configuration

### Environment Variables
```bash
# Database Connection
MYSQL_USER=finance_user
MYSQL_PASSWORD=your_secure_password
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=personal_finance_dashboard

# Application
APP_ENV=production
DEBUG=False
SECRET_KEY=your_secret_key_here
```

### Connection String Format
```
mysql+pymysql://username:password@host:port/database
```

## 📈 Available Queries

### Pre-defined Views
- `monthly_summary`: Monthly income, expenses, and savings
- `category_summary`: Spending by category
- `account_summary`: Account balances and flows

### Common SQL Queries
```sql
-- Monthly expenses by category
SELECT 
    DATE_FORMAT(date, '%Y-%m') as month,
    category,
    SUM(amount) as total
FROM transactions 
WHERE type = 'Expense'
GROUP BY month, category
ORDER BY month, total DESC;

-- Account balances over time
SELECT 
    date,
    account,
    SUM(CASE WHEN type = 'Income' THEN amount ELSE -amount END) as net_flow
FROM transactions
GROUP BY date, account
ORDER BY date;
```

## 🚨 Troubleshooting

### Connection Issues
```bash
# Check MySQL service
sudo systemctl status mysql  # Linux
# or check Services panel on Windows

# Test connection manually
mysql -u finance_user -p -h localhost personal_finance_dashboard

# Check user permissions
mysql -u root -p
SHOW GRANTS FOR 'finance_user'@'localhost';
```

### Common Errors

#### "Access denied for user"
- Verify username and password
- Check user exists: `SELECT user, host FROM mysql.user;`
- Verify privileges: `SHOW GRANTS FOR 'finance_user'@'localhost';`

#### "Can't connect to MySQL server"
- Check MySQL is running
- Verify host and port
- Check firewall settings

#### "Table doesn't exist"
- Run database initialization: `mysql -u finance_user -p personal_finance_dashboard < init_database.sql`
- Verify correct database name

### Performance Optimization
```sql
-- Add indexes for better query performance
CREATE INDEX idx_transactions_date_category ON transactions(date, category);
CREATE INDEX idx_transactions_account_type ON transactions(account, type);

-- Analyze table statistics
ANALYZE TABLE transactions;
```

## 📚 Additional Resources

### MySQL Documentation
- [MySQL Reference Manual](https://dev.mysql.com/doc/)
- [Python MySQL Connector](https://pypi.org/project/PyMySQL/)

### Security Guidelines
- Use SSL connections for production
- Implement connection pooling
- Regular security updates
- Monitor access logs

### Performance Tips
- Use appropriate indexes
- Archive old data regularly
- Monitor query performance
- Use connection pooling

## 🆘 Support

### Getting Help
1. Check MySQL service status
2. Verify connection settings
3. Review error logs
4. Test with simple MySQL client first

### Log Files
- MySQL error log: `/var/log/mysql/error.log` (Linux)
- Application logs: Check Streamlit console output

---

**🎉 Congratulations!** Your MySQL database is now set up and ready for use with your Personal Finance Dashboard. The system provides robust data management, security, and backup capabilities for tracking your daily expenses effectively.
