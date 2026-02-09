-- Personal Finance Dashboard - MySQL Database Initialization
-- This script creates the complete database schema and inserts sample data

-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS personal_finance_dashboard 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE personal_finance_dashboard;

-- Drop tables if they exist (for clean re-initialization)
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS raw_transactions;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS accounts;

-- Create categories table
CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    type ENUM('Income', 'Expense', 'Both') DEFAULT 'Both',
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_name (name),
    INDEX idx_type (type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create accounts table
CREATE TABLE accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    type ENUM('Asset', 'Liability', 'Equity') DEFAULT 'Asset',
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_name (name),
    INDEX idx_type (type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create raw_transactions table (for CSV imports)
CREATE TABLE raw_transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Type VARCHAR(50),
    Date DATE,
    Name VARCHAR(255),
    Amount DECIMAL(15, 2),
    Currency VARCHAR(10),
    Category VARCHAR(100),
    Account VARCHAR(100),
    Status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_date (Date),
    INDEX idx_category (Category),
    INDEX idx_account (Account),
    INDEX idx_status (Status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create transactions table (processed data)
CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type ENUM('Income', 'Expense', 'Transfer') NOT NULL,
    date DATE NOT NULL,
    item VARCHAR(255) NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'PHP',
    category VARCHAR(100) NOT NULL,
    account VARCHAR(100) NOT NULL,
    status VARCHAR(50) DEFAULT 'Reconciled',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_date (date),
    INDEX idx_category (category),
    INDEX idx_account (account),
    INDEX idx_type (type),
    INDEX idx_status (status),
    FOREIGN KEY (category) REFERENCES categories(name) ON UPDATE CASCADE,
    FOREIGN KEY (account) REFERENCES accounts(name) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert default categories
INSERT INTO categories (name, type, description) VALUES
('Food & Dining', 'Expense', 'Restaurants, groceries, food delivery, coffee'),
('Transportation', 'Expense', 'Gas, public transport, ride-sharing, parking'),
('Shopping', 'Expense', 'Clothing, electronics, household items, personal care'),
('Entertainment', 'Expense', 'Movies, games, subscriptions, events'),
('Bills & Utilities', 'Expense', 'Electricity, water, internet, phone, rent'),
('Healthcare', 'Expense', 'Medicine, doctor visits, insurance, gym'),
('Education', 'Expense', 'Tuition, books, courses, supplies'),
('Personal', 'Expense', 'Haircut, gifts, donations, miscellaneous'),
('Travel', 'Expense', 'Flights, hotels, vacation expenses'),
('Salary', 'Income', 'Monthly salary and wages'),
('Freelance', 'Income', 'Freelance work and side gigs'),
('Business', 'Income', 'Business income and profits'),
('Investments', 'Income', 'Dividends, interest, capital gains'),
('Gifts', 'Income', 'Money received as gifts'),
('Refunds', 'Income', 'Refunds and rebates'),
('Transfer', 'Both', 'Money transfers between accounts'),
('Savings', 'Both', 'Money moved to savings accounts');

-- Insert default accounts
INSERT INTO accounts (name, type, description) VALUES
('Wallet', 'Asset', 'Physical cash and wallet'),
('Union Bank', 'Asset', 'Union Bank checking/savings account'),
('SeaBank', 'Asset', 'SeaBank digital account'),
('SeaBank Credit', 'Liability', 'SeaBank credit card'),
('GCash', 'Asset', 'GCash e-wallet and payments'),
('Maya', 'Asset', 'Maya e-wallet and digital banking'),
('Maya Easy Credit', 'Liability', 'Maya credit line and loans'),
('GrabPay', 'Asset', 'GrabPay e-wallet'),
('ShopeePay', 'Asset', 'ShopeePay e-wallet'),
('SPayLater', 'Liability', 'ShopeePay credit service'),
('SLoan', 'Liability', 'Shopee loan service'),
('Binance', 'Asset', 'Binance cryptocurrency account'),
('Ronin', 'Asset', 'Ronin wallet for gaming/crypto'),
('BDO', 'Asset', 'BDO bank account'),
('BPI', 'Asset', 'BPI bank account'),
('Borrowed Money', 'Liability', 'Money borrowed from others'),
('Loaned Money', 'Asset', 'Money loaned to others'),
('School Loans', 'Liability', 'Educational loans'),
('Emergency Fund', 'Asset', 'Emergency savings fund'),
('Investment Account', 'Asset', 'Stock and investment accounts');

-- Insert sample transactions for testing
INSERT INTO transactions (type, date, item, amount, currency, category, account, status) VALUES
-- Income examples
('Income', '2024-01-15', 'Monthly Salary', 50000.00, 'PHP', 'Salary', 'BDO', 'Reconciled'),
('Income', '2024-01-20', 'Freelance Project', 15000.00, 'PHP', 'Freelance', 'GCash', 'Reconciled'),
('Income', '2024-01-25', 'Investment Dividend', 2500.00, 'PHP', 'Investments', 'Binance', 'Reconciled'),

-- Expense examples
('Expense', '2024-01-16', 'Grocery Shopping', 3500.00, 'PHP', 'Food & Dining', 'Wallet', 'Reconciled'),
('Expense', '2024-01-17', 'Restaurant Dinner', 1200.00, 'PHP', 'Food & Dining', 'GCash', 'Reconciled'),
('Expense', '2024-01-18', 'Gas Station', 2000.00, 'PHP', 'Transportation', 'Union Bank', 'Reconciled'),
('Expense', '2024-01-19', 'Netflix Subscription', 369.00, 'PHP', 'Entertainment', 'Maya', 'Reconciled'),
('Expense', '2024-01-20', 'Electric Bill', 2500.00, 'PHP', 'Bills & Utilities', 'BPI', 'Reconciled'),
('Expense', '2024-01-21', 'Online Shopping', 2800.00, 'PHP', 'Shopping', 'ShopeePay', 'Reconciled'),
('Expense', '2024-01-22', 'Grab Ride', 350.00, 'PHP', 'Transportation', 'GrabPay', 'Reconciled'),
('Expense', '2024-01-23', 'Coffee', 180.00, 'PHP', 'Food & Dining', 'GCash', 'Reconciled'),
('Expense', '2024-01-24', 'Medicine', 850.00, 'PHP', 'Healthcare', 'Wallet', 'Reconciled'),
('Expense', '2024-01-25', 'Internet Bill', 1299.00, 'PHP', 'Bills & Utilities', 'Maya', 'Reconciled'),

-- Transfer examples
('Transfer', '2024-01-16', 'Transfer to Savings', 10000.00, 'PHP', 'Transfer', 'BDO', 'Reconciled'),
('Transfer', '2024-01-20', 'Load GCash', 5000.00, 'PHP', 'Transfer', 'Union Bank', 'Reconciled'),
('Transfer', '2024-01-25', 'Pay Credit Card', 8000.00, 'PHP', 'Transfer', 'BPI', 'Reconciled');

-- Create views for common queries
CREATE VIEW monthly_summary AS
SELECT 
    DATE_FORMAT(date, '%Y-%m') AS month,
    SUM(CASE WHEN type = 'Income' THEN amount ELSE 0 END) AS total_income,
    SUM(CASE WHEN type = 'Expense' THEN amount ELSE 0 END) AS total_expenses,
    SUM(CASE WHEN type = 'Income' THEN amount ELSE 0 END) - 
    SUM(CASE WHEN type = 'Expense' THEN amount ELSE 0 END) AS net_savings
FROM transactions
GROUP BY DATE_FORMAT(date, '%Y-%m')
ORDER BY month;

CREATE VIEW category_summary AS
SELECT 
    category,
    type,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_amount,
    AVG(amount) AS average_amount
FROM transactions
GROUP BY category, type
ORDER BY total_amount DESC;

CREATE VIEW account_summary AS
SELECT 
    account,
    COUNT(*) AS transaction_count,
    SUM(CASE WHEN type = 'Income' THEN amount ELSE 0 END) AS total_income,
    SUM(CASE WHEN type = 'Expense' THEN amount ELSE 0 END) AS total_expenses,
    SUM(CASE WHEN type = 'Income' THEN amount ELSE 0 END) - 
    SUM(CASE WHEN type = 'Expense' THEN amount ELSE 0 END) AS net_flow
FROM transactions
GROUP BY account
ORDER BY net_flow DESC;

-- Create stored procedures for common operations
DELIMITER //

CREATE PROCEDURE AddTransaction(
    IN p_type VARCHAR(10),
    IN p_date DATE,
    IN p_item VARCHAR(255),
    IN p_amount DECIMAL(15,2),
    IN p_currency VARCHAR(10),
    IN p_category VARCHAR(100),
    IN p_account VARCHAR(100),
    IN p_status VARCHAR(50)
)
BEGIN
    INSERT INTO transactions (type, date, item, amount, currency, category, account, status)
    VALUES (p_type, p_date, p_item, p_amount, p_currency, p_category, p_account, p_status);
    
    SELECT LAST_INSERT_ID() AS transaction_id;
END //

CREATE PROCEDURE GetTransactionsByDateRange(
    IN p_start_date DATE,
    IN p_end_date DATE
)
BEGIN
    SELECT * FROM transactions 
    WHERE date BETWEEN p_start_date AND p_end_date 
    ORDER BY date DESC;
END //

CREATE PROCEDURE GetCategoryExpenses(
    IN p_category VARCHAR(100),
    IN p_start_date DATE,
    IN p_end_date DATE
)
BEGIN
    SELECT 
        date,
        item,
        amount,
        account
    FROM transactions 
    WHERE category = p_category 
    AND type = 'Expense'
    AND date BETWEEN p_start_date AND p_end_date
    ORDER BY date DESC;
END //

DELIMITER ;

-- Show summary of created database
SELECT 'Database setup completed successfully!' AS message;
SELECT COUNT(*) AS categories_created FROM categories;
SELECT COUNT(*) AS accounts_created FROM accounts;
SELECT COUNT(*) AS sample_transactions FROM transactions;
