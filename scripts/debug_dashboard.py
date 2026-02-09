from read_queries_sqlite import query
import streamlit as st
import plotly.express as px

st.title('Dashboard Debug - Testing All Charts')

# Test all charts individually
st.header('1. Account Balance Over Time')
try:
    monthly_amount_over_time = query("monthly_amount_over_time")
    if not monthly_amount_over_time.empty:
        st.write(f"Data shape: {monthly_amount_over_time.shape}")
        st.write("Columns:", list(monthly_amount_over_time.columns))
        fig_accounts_over_time = px.line(monthly_amount_over_time, x='month', y=['net_worth'], title='Account Balance Over Time')
        st.plotly_chart(fig_accounts_over_time, use_container_width=True)
    else:
        st.error("No monthly data available.")
except Exception as e:
    st.error(f"Error in Account Balance: {e}")

st.markdown("---")

st.header('2. Payment Methods')
try:
    payment_methods = query("payment_methods")
    if not payment_methods.empty:
        st.write(f"Data shape: {payment_methods.shape}")
        st.dataframe(payment_methods)
        fig_payment_methods = px.bar(payment_methods, x='account', y='amount', title='Payment Methods')
        st.plotly_chart(fig_payment_methods, use_container_width=True)
    else:
        st.error("No payment methods data available.")
except Exception as e:
    st.error(f"Error in Payment Methods: {e}")

st.markdown("---")

st.header('3. Receiving Methods')
try:
    receiving_methods = query("receiving_methods")
    if not receiving_methods.empty:
        st.write(f"Data shape: {receiving_methods.shape}")
        st.dataframe(receiving_methods)
        fig_receiving_methods = px.bar(receiving_methods, x='account', y='amount', title='Receiving Methods')
        st.plotly_chart(fig_receiving_methods, use_container_width=True)
    else:
        st.error("No receiving methods data available.")
except Exception as e:
    st.error(f"Error in Receiving Methods: {e}")

st.markdown("---")

st.header('4. Expenses Per Category')
try:
    expenses_per_category = query("expenses_per_category")
    if not expenses_per_category.empty:
        st.write(f"Data shape: {expenses_per_category.shape}")
        st.dataframe(expenses_per_category)
        fig_expenses_by_category = px.pie(expenses_per_category, values='expenses', title='Expenses Per Category', names='category', hole=0.4)
        fig_expenses_by_category.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_expenses_by_category, use_container_width=True)
    else:
        st.error("No expenses data available.")
except Exception as e:
    st.error(f"Error in Expenses Category: {e}")

st.markdown("---")

st.header('5. Income Per Category')
try:
    income_per_category = query("income_per_category")
    if not income_per_category.empty:
        st.write(f"Data shape: {income_per_category.shape}")
        st.dataframe(income_per_category)
        fig_income = px.pie(income_per_category, values='income', names='category', title='Income Per Category', hole=0.4)
        fig_income.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_income, use_container_width=True)
    else:
        st.error("No income data available.")
except Exception as e:
    st.error(f"Error in Income Category: {e}")

st.markdown("---")

st.header('6. Monthly Expenses')
try:
    monthly_expenses = query("monthly_expenses")
    if not monthly_expenses.empty:
        st.write(f"Data shape: {monthly_expenses.shape}")
        st.dataframe(monthly_expenses)
        fig_monthly_expenses = px.line(monthly_expenses, x='month', y='expenses', title='Monthly Expenses')
        st.plotly_chart(fig_monthly_expenses, use_container_width=True)
    else:
        st.error("No monthly expenses data available.")
except Exception as e:
    st.error(f"Error in Monthly Expenses: {e}")
