from read_queries_sqlite import query

print('=== Checking Database Status ===')
transactions = query('transactions')
print(f'Transactions in database: {len(transactions)}')

if len(transactions) == 0:
    print('❌ No data found! You need to:')
    print('1. Go to Data tab')
    print('2. Upload sample_transactions.csv')
    print('3. Click Generate Dashboard')
else:
    print('✅ Data is available')
    print(f'Date range: {transactions["date"].min()} to {transactions["date"].max()}')
    print(f'Accounts: {transactions["Account"].unique()}')
