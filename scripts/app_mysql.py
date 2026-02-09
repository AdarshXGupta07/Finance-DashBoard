from database_mysql import extract, transform, load, drop, create_database
from read_queries_mysql import query
import streamlit as st
import plotly.express as px
from PIL import Image

def main():
    # ----- PAGE SETUP -----
    st.set_page_config(page_title='Personal Finance Dashboard - MySQL Version',
                    page_icon=':money_with_wings:',
                    layout='wide')

    # ----- TITLE & TABS -----
    st.title('Personal Finance Dashboard - MySQL Version')
    tab1, tab2, tab3, tab4 = st.tabs(['Home', 'Data', 'Dashboard', 'Documentation'])

    # ----- SIDE BAR ----- 
    with st.sidebar:
        st.header('Filters')
        # Accounts filter
        column_options = [
            'net_worth', 'wallet', 'unionbank', 'seabank', 'seabank_credit', 'gcash',
            'maya', 'maya_easy_credit', 'grabpay', 'shopeepay', 'spaylater', 'sloan',
            'binance', 'ronin', 'bdo', 'bpi', 'borrowed_money', 'loaned_money', 'school_loans'
        ]
        selected_columns = st.multiselect('Select accounts to display:', column_options, default=['net_worth'])
        # Views filter
        view = st.radio("Select view:", ["monthly", "weekly", "daily"], index=1, horizontal = True, key = "sidebar")
        
        st.markdown("---")
        st.subheader("MySQL Connection")
        if st.button("Test MySQL Connection"):
            try:
                from database_mysql import get_mysql_connection
                from sqlalchemy import create_engine, text
                conn_uri = get_mysql_connection()
                engine = create_engine(conn_uri)
                with engine.connect() as connection:
                    result = connection.execute(text("SELECT 1"))
                st.success("✅ MySQL connection successful!")
            except Exception as e:
                st.error(f"❌ MySQL connection failed: {str(e)}")

    # ----- HOME TAB -----
    with tab1:
        with st.container():
            st.subheader('Project Overview - MySQL Version')
            st.markdown("""
                        The Personal Finance Dashboard extracts expenditure data from Bluecoins and creates a dashboard to aid in budgeting and financial management. 
                        This version uses MySQL database for enhanced performance and scalability.
                        """ )
            try:
                personal_finance = Image.open('../images/finance.jpg')
                st.image(personal_finance, caption='Source: LittlePigPower/Shutterstock.com', use_container_width=True)
            except FileNotFoundError:
                st.warning(f"Image not found")

        with st.container():
            st.subheader('MySQL Advantages')
            st.markdown("""
                        **Why MySQL over SQLite?**
                        
                        - 🚀 **Better Performance**: Optimized for larger datasets
                        - 👥 **Multi-user Support**: Handle concurrent users
                        - 📈 **Scalability**: Grows with your data needs
                        - 🔒 **Advanced Security**: User permissions and access control
                        - 🔄 **ACID Compliance**: Reliable transactions
                        """ )

        with st.container():
            st.subheader('Get Started')
            st.markdown("""
                        **Setup Requirements:**
                        
                        1. Install MySQL Server
                        2. Create database and user
                        3. Set environment variables or update connection settings
                        4. Install Python MySQL connector: `pip install pymysql`
                        5. Upload your CSV data in the Data tab
                        """ )
    try:
        # ----- DATA TAB -----
        with tab2:
            # File input
            file = st.file_uploader("Upload file here")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Generate Dashboard"):
                    if file is not None:
                        try:
                            raw_transactions = extract(file)
                            load(raw_transactions, "raw_transactions")
                            cleaned_transactions = transform(raw_transactions)
                            load(cleaned_transactions, "transactions")
                            st.success("Dashboard generated successfully!")
                        except Exception as e:
                            st.error(f"Error processing file: {str(e)}")
                    else:
                        st.error("Please upload a file before generating the dashboard.")
            
            with col2:
                if st.button("Setup Database"):
                    try:
                        create_database()
                        st.success("Database setup completed!")
                    except Exception as e:
                        st.error(f"Database setup error: {str(e)}")
            
            if st.button("Clear Data"):
                try:
                    drop("raw_transactions")
                    drop("transactions")
                    st.success("Data cleared successfully!")
                except Exception as e:
                    st.error(f"Error clearing data: {str(e)}")
            
            # DataFrames
            with st.expander('Raw Transactions Data'):
                raw_transactions = query("raw_transactions")
                if not raw_transactions.empty:
                    st.dataframe(raw_transactions, height=400, use_container_width= True)
                else:
                    st.info("No raw transactions data available. Please upload a CSV file first.")
            
            with st.expander('Cleaned Transactions Data'):
                cleaned_transactions = query("transactions")
                if not cleaned_transactions.empty:
                    st.dataframe(cleaned_transactions, height=400, use_container_width= True)
                else:
                    st.info("No cleaned transactions data available. Please upload a CSV file first.")
            
            with st.expander('Accounts Data'):
                accounts = query("daily_amount_over_time")
                if not accounts.empty:
                    st.dataframe(accounts, height=400, use_container_width= True)
                else:
                    st.info("No accounts data available. Please upload a CSV file first.")

        # ----- DASHBOARD TAB -----
        with tab3:
            # Check if data exists
            test_data = query("transactions")
            if test_data.empty:
                st.warning("No data available. Please upload a CSV file in the Data tab first.")
                return

            # Account Balance Over Time
            with st.container():
                if view == 'monthly':   
                    monthly_amount_over_time = query("monthly_amount_over_time")
                    if not monthly_amount_over_time.empty:
                        fig_accounts_over_time = px.line(monthly_amount_over_time , x='month', y=selected_columns, title='Account Balance Over Time')
                        st.plotly_chart(fig_accounts_over_time, use_container_width= True)
                    else:
                        st.info("No monthly data available.")

                elif view == 'weekly':   
                    weekly_amount_over_time = query("weekly_amount_over_time")
                    if not weekly_amount_over_time.empty:
                        fig_accounts_over_time = px.line(weekly_amount_over_time , x='week', y=selected_columns, title='Account Balance Over Time')
                        st.plotly_chart(fig_accounts_over_time, use_container_width= True)
                    else:
                        st.info("No weekly data available.")

                elif view == 'daily':   
                    daily_amount_over_time = query("daily_amount_over_time")
                    if not daily_amount_over_time.empty:
                        fig_accounts_over_time = px.line(daily_amount_over_time , x='day', y=selected_columns, title='Account Balance Over Time')
                        st.plotly_chart(fig_accounts_over_time, use_container_width= True)
                    else:
                        st.info("No daily data available.")

            st.markdown("""---""")
            
            b1, b2 = st.columns(2)
            # Payment Methods
            with b1:
                payment_methods = query("payment_methods")
                if not payment_methods.empty:
                    fig_payment_methods = px.bar(payment_methods, x='account', y='amount', title='Payment Methods')
                    st.plotly_chart(fig_payment_methods, use_container_width= True)
                else:
                    st.info("No payment methods data available.")
            
            # Receiving Methods
            with b2:
                receiving_methods = query("receiving_methods")
                if not receiving_methods.empty:
                    fig_receiving_methods = px.bar(receiving_methods, x='account', y='amount', title='Receiving Methods')
                    st.plotly_chart(fig_receiving_methods, use_container_width= True)
                else:
                    st.info("No receiving methods data available.")

            st.markdown("""---""")

            c1, c2 = st.columns(2)
            # Expenses Per Category
            with c1:
                expenses_per_category = query("expenses_per_category")
                if not expenses_per_category.empty:
                    fig_expenses_by_category = px.pie(expenses_per_category, values='expenses', title='Expenses Per Category', names='category', hole=0.4)
                    fig_expenses_by_category.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig_expenses_by_category, use_container_width= True)
                else:
                    st.info("No expenses data available.")
            
            # Income Per Category
            with c2:
                income_per_category = query("income_per_category")
                if not income_per_category.empty:
                    fig_income = px.pie(income_per_category, values='income', names='category', title='Income Per Category', hole=0.4)
                    fig_income.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig_income, use_container_width= True)
                else:
                    st.info("No income data available.")

            st.markdown("""---""")

            d1, d2 = st.columns(2)
            # Top Expenses
            with d1:
                st.markdown("###### Top Expenses")
                if not expenses_per_category.empty:
                    st.dataframe(expenses_per_category, height=400, use_container_width= True)
                else:
                    st.info("No expenses data available.")
            
            # Top Income Sources
            with d2:
                st.markdown("###### Top Income Sources")
                if not income_per_category.empty:
                    st.dataframe(income_per_category, height=400, use_container_width= True)
                else:
                    st.info("No income data available.")

            st.markdown("""---""")

            # Expenses Over Time
            with st.container():
                if view == 'monthly':
                    monthly_expenses = query("monthly_expenses")
                    if not monthly_expenses.empty:
                        fig_monthly_expenses = px.line(monthly_expenses, x='month', y='expenses', title='Monthly Expenses')
                        st.plotly_chart(fig_monthly_expenses, use_container_width= True)
                    else:
                        st.info("No monthly expenses data available.")
                
                elif view == "weekly":
                    weekly_expenses = query("weekly_expenses")
                    if not weekly_expenses.empty:
                        fig_weekly_expenses = px.line(weekly_expenses, x='week', y='expenses', title='Weekly Expenses')
                        st.plotly_chart(fig_weekly_expenses, use_container_width= True)
                    else:
                        st.info("No weekly expenses data available.")
                
                elif view == "daily":
                    daily_expenses = query("daily_expenses")
                    if not daily_expenses.empty:
                        fig_daily_expenses = px.line(daily_expenses, x='day', y='expenses', title='Daily Expenses')
                        st.plotly_chart(fig_daily_expenses, use_container_width= True)
                    else:
                        st.info("No daily expenses data available.")
    except Exception as e:
            st.error(f"An error occurred: {str(e)}")

    # ----- DOCUMENTATIONS TAB -----
    with tab4:
        st.subheader('Entity Relationship Diagram')
        try:
            er_diagram = Image.open('../images/er_diagram.png')
            st.image(er_diagram, caption='Database Schema - Entity Relationship Diagram', use_container_width=True)
        except FileNotFoundError:
                st.warning(f"ER Diagram not found")

        st.subheader('Data Flow Architecture')
        try:
            data_flow = Image.open('../images/data_flow_diagram.png')
            st.image(data_flow, caption='Data Processing Pipeline', use_container_width=True)
        except FileNotFoundError:
                st.warning(f"Data Flow Diagram not found")

        st.subheader('MySQL Database Schema')
        st.markdown("""
        ### Enhanced MySQL Architecture:
        
        **📋 Tables Structure:**
        - `raw_transactions`: Original CSV data as uploaded
        - `transactions`: Cleaned and processed data
        
        **🔧 MySQL Advantages:**
        - **Performance**: Optimized for large datasets
        - **Concurrency**: Handle multiple users
        - **Security**: User-level permissions
        - **Scalability**: Grows with your needs
        - **ACID Compliance**: Reliable transactions
        
        **📊 Data Types:**
        - `type`: VARCHAR(20) - Income/Expense
        - `date`: DATETIME - Transaction timestamp
        - `amount`: DECIMAL(15,2) - Monetary value
        - `category`: VARCHAR(50) - Category name
        - `account`: VARCHAR(50) - Account name
        - `status`: VARCHAR(20) - Processing status
        
        **🚀 Performance Features:**
        - Indexing on date and account fields
        - Optimized queries for analytics
        - Connection pooling for efficiency
        - Query caching for faster dashboard
        """)


if __name__ == '__main__':
    main()
