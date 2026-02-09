-- Personal Finance Dashboard - Comprehensive Database Schema
-- 7 Entity Design with Normalized Structure

-- Entity 1: Users
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    INDEX idx_username (username),
    INDEX idx_email (email)
);

-- Entity 2: Categories
CREATE TABLE categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL,
    category_type ENUM('income', 'expense') NOT NULL,
    description TEXT,
    icon VARCHAR(50),
    color VARCHAR(7),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_category_name (category_name),
    INDEX idx_category_type (category_type)
);

-- Entity 3: Accounts
CREATE TABLE accounts (
    account_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    account_name VARCHAR(100) NOT NULL,
    account_type ENUM('bank', 'wallet', 'credit_card', 'digital_wallet', 'investment', 'loan', 'other') NOT NULL,
    balance DECIMAL(15,2) DEFAULT 0.00,
    currency VARCHAR(3) DEFAULT 'PHP',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_user_accounts (user_id),
    INDEX idx_account_type (account_type)
);

-- Entity 4: Tags
CREATE TABLE tags (
    tag_id INT AUTO_INCREMENT PRIMARY KEY,
    tag_name VARCHAR(50) UNIQUE NOT NULL,
    color VARCHAR(7) DEFAULT '#007bff',
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_tag_name (tag_name)
);

-- Entity 5: Transactions
CREATE TABLE transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT NOT NULL,
    category_id INT NOT NULL,
    amount DECIMAL(15,2) NOT NULL,
    transaction_type ENUM('income', 'expense', 'transfer') NOT NULL,
    date DATE NOT NULL,
    description TEXT,
    status ENUM('pending', 'reconciled', 'cancelled') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE RESTRICT,
    FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE RESTRICT,
    INDEX idx_account_transactions (account_id),
    INDEX idx_category_transactions (category_id),
    INDEX idx_transaction_date (date),
    INDEX idx_transaction_type (transaction_type),
    INDEX idx_transaction_status (status)
);

-- Entity 6: Budgets
CREATE TABLE budgets (
    budget_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    category_id INT NOT NULL,
    amount_limit DECIMAL(15,2) NOT NULL,
    period_type ENUM('weekly', 'monthly', 'quarterly', 'yearly') NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE CASCADE,
    INDEX idx_user_budgets (user_id),
    INDEX idx_category_budgets (category_id),
    INDEX idx_budget_period (period_type),
    INDEX idx_budget_dates (start_date, end_date)
);

-- Entity 7: Transaction_Tags (Junction Table for Many-to-Many)
CREATE TABLE transaction_tags (
    transaction_id INT NOT NULL,
    tag_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (transaction_id, tag_id),
    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(tag_id) ON DELETE CASCADE
);

-- Insert sample data for testing
INSERT INTO users (username, email, password_hash) VALUES 
('demo_user', 'demo@example.com', 'hashed_password_here');

INSERT INTO categories (category_name, category_type, description, icon) VALUES 
('Salary', 'income', 'Monthly salary and wages', '💰'),
('Freelance', 'income', 'Freelance work income', '💻'),
('Food', 'expense', 'Food and dining expenses', '🍔'),
('Transportation', 'expense', 'Transport and travel costs', '🚗'),
('Utilities', 'expense', 'Monthly utility bills', '💡'),
('Entertainment', 'expense', 'Entertainment and leisure', '🎬'),
('Shopping', 'expense', 'Shopping and retail purchases', '🛍️'),
('Healthcare', 'expense', 'Medical and health expenses', '🏥');

INSERT INTO accounts (user_id, account_name, account_type, balance, currency) VALUES 
(1, 'BDO Savings', 'bank', 10000.00, 'PHP'),
(1, 'BPI Checking', 'bank', 5000.00, 'PHP'),
(1, 'GCash Wallet', 'digital_wallet', 1500.00, 'PHP'),
(1, 'Maya Wallet', 'digital_wallet', 800.00, 'PHP'),
(1, 'Cash Wallet', 'wallet', 330.00, 'PHP'),
(1, 'SeaBank', 'digital_wallet', 120.00, 'PHP'),
(1, 'GrabPay', 'digital_wallet', 100.00, 'PHP'),
(1, 'ShopeePay', 'digital_wallet', 300.00, 'PHP');

INSERT INTO tags (tag_name, color, description) VALUES 
('Business', '#ff6b6b', 'Business related transactions'),
('Personal', '#4ecdc4', 'Personal transactions'),
('Urgent', '#ff9f43', 'Urgent payments'),
('Recurring', '#48dbfb', 'Recurring transactions'),
('One-time', '#ff6348', 'One-time expenses');

-- Sample transactions
INSERT INTO transactions (account_id, category_id, amount, transaction_type, date, description, status) VALUES 
(1, 1, 10000.00, 'income', '2024-01-01', 'Monthly Salary', 'reconciled'),
(2, 2, 1000.00, 'income', '2024-01-15', 'Freelance Project', 'reconciled'),
(5, 3, 150.00, 'expense', '2024-01-02', 'Groceries', 'reconciled'),
(3, 4, 50.00, 'expense', '2024-01-03', 'Transportation', 'reconciled'),
(4, 5, 200.00, 'expense', '2024-01-20', 'Utilities Payment', 'reconciled'),
(6, 6, 100.00, 'expense', '2024-01-25', 'Entertainment', 'reconciled'),
(7, 7, 300.00, 'expense', '2024-02-10', 'Shopping', 'reconciled'),
(8, 3, 180.00, 'expense', '2024-02-05', 'Restaurant', 'reconciled');

-- Sample budgets
INSERT INTO budgets (user_id, category_id, amount_limit, period_type, start_date, end_date) VALUES 
(1, 3, 5000.00, 'monthly', '2024-01-01', '2024-01-31'),
(1, 4, 2000.00, 'monthly', '2024-01-01', '2024-01-31'),
(1, 5, 1500.00, 'monthly', '2024-01-01', '2024-01-31'),
(1, 6, 1000.00, 'monthly', '2024-01-01', '2024-01-31'),
(1, 7, 2000.00, 'monthly', '2024-01-01', '2024-01-31');

-- Sample transaction tags
INSERT INTO transaction_tags (transaction_id, tag_id) VALUES 
(1, 2), (2, 1), (3, 2), (4, 2), (5, 4), (6, 2), (7, 5), (8, 2);

-- Views for common queries
CREATE VIEW transaction_summary AS
SELECT 
    t.transaction_id,
    t.amount,
    t.transaction_type,
    t.date,
    t.description,
    a.account_name,
    c.category_name,
    u.username,
    GROUP_CONCAT(tag_name) AS tags
FROM transactions t
JOIN accounts a ON t.account_id = a.account_id
JOIN categories c ON t.category_id = c.category_id
JOIN users u ON a.user_id = u.user_id
LEFT JOIN transaction_tags tt ON t.transaction_id = tt.transaction_id
LEFT JOIN tags tg ON tt.tag_id = tg.tag_id
GROUP BY t.transaction_id;

CREATE VIEW budget_status AS
SELECT 
    b.budget_id,
    b.amount_limit,
    b.period_type,
    b.start_date,
    b.end_date,
    c.category_name,
    COALESCE(SUM(t.amount), 0) AS spent,
    b.amount_limit - COALESCE(SUM(t.amount), 0) AS remaining,
    ROUND((COALESCE(SUM(t.amount), 0) / b.amount_limit) * 100, 2) AS percentage_used
FROM budgets b
JOIN categories c ON b.category_id = c.category_id
LEFT JOIN transactions t ON t.category_id = b.category_id 
    AND t.date BETWEEN b.start_date AND b.end_date
    AND t.transaction_type = 'expense'
GROUP BY b.budget_id;
