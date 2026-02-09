# Personal Finance Dashboard - MySQL Version

This version uses MySQL database for enhanced performance and scalability.

## Prerequisites

1. **Python 3.7+** with pip
2. **MySQL Server** installed and running
3. **Python MySQL connector**

## MySQL Setup

### 1. Install MySQL Server

**Windows:**
- Download from: https://dev.mysql.com/downloads/mysql/
- Run installer and note your root password
- Start MySQL service

**macOS:**
```bash
brew install mysql
brew services start mysql
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql
sudo systemctl enable mysql
```

### 2. Create Database and User

```sql
-- Log in to MySQL
mysql -u root -p

-- Create database
CREATE DATABASE personal_finance_dashboard;

-- Create user (replace 'your_password' with your password)
CREATE USER 'finance_user'@'localhost' IDENTIFIED BY 'your_password';

-- Grant permissions
GRANT ALL PRIVILEGES ON personal_finance_dashboard.* TO 'finance_user'@'localhost';
FLUSH PRIVILEGES;

EXIT;
```

### 3. Install Python Dependencies

```bash
pip install pandas sqlalchemy streamlit plotly pillow pymysql
```

### 4. Configure Connection

**Option 1: Environment Variables (Recommended)**
```bash
# Windows (Command Prompt)
set MYSQL_USER=finance_user
set MYSQL_PASSWORD=your_password
set MYSQL_HOST=localhost
set MYSQL_PORT=3306
set MYSQL_DATABASE=personal_finance_dashboard

# Linux/macOS
export MYSQL_USER=finance_user
export MYSQL_PASSWORD=your_password
export MYSQL_HOST=localhost
export MYSQL_PORT=3306
export MYSQL_DATABASE=personal_finance_dashboard
```

**Option 2: Modify database_mysql.py**
Edit the connection settings directly in the file.

## Running the Application

1. **Navigate to scripts directory:**
   ```bash
   cd scripts
   ```

2. **Run the MySQL version:**
   ```bash
   streamlit run app_mysql.py
   ```

3. **Open browser** and go to `http://localhost:8501`

## Features

- ✅ **MySQL Database**: Scalable and performant
- ✅ **Multi-user Support**: Handle concurrent access
- ✅ **Enhanced Security**: User authentication
- ✅ **ACID Compliance**: Reliable transactions
- ✅ **All Original Features**: Charts, analytics, data management

## Testing the Connection

1. Open the application
2. Check the sidebar for "MySQL Connection" section
3. Click "Test MySQL Connection" button
4. Should show "✅ MySQL connection successful!"

## Troubleshooting

### Connection Errors
- **Check MySQL service**: `sudo systemctl status mysql` (Linux) or Services panel (Windows)
- **Verify credentials**: Ensure username/password are correct
- **Check firewall**: MySQL port (3306) should be open

### Module Not Found
```bash
pip install pymysql
```

### Database Creation Issues
- Use the "Setup Database" button in the Data tab
- Or run SQL commands manually in MySQL client

## Migration from SQLite

If you have data in SQLite and want to migrate to MySQL:

1. Export your data from SQLite version
2. Set up MySQL as described above
3. Import data using the MySQL version
4. All your charts and analytics will work the same

## Performance Benefits

| Feature | SQLite | MySQL |
|---------|--------|-------|
| Concurrent Users | 1-2 | 100+ |
| Dataset Size | <1GB | TB+ |
| Query Performance | Good | Excellent |
| Backup/Restore | File copy | Advanced tools |
| Security | File-level | User-level |

## Support

For issues:
1. Check MySQL service status
2. Verify connection settings
3. Test with simple MySQL client first
4. Check application logs for detailed errors
