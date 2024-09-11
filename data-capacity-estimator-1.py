import streamlit as st
import pandas as pd

# Function to calculate data capacity requirements
def calculate_data_capacity(current_users, daily_transactions_per_user, average_transaction_size_kb, 
                            users_growth_rate, transactions_growth_rate, retention_period_months):
    
    # Calculate current data generation
    current_daily_transactions = current_users * daily_transactions_per_user
    current_daily_data_kb = current_daily_transactions * average_transaction_size_kb
    current_monthly_data_kb = current_daily_data_kb * 30
    current_yearly_data_kb = current_daily_data_kb * 365

    # Project future growth (after retention period in months)
    projected_users = current_users * (1 + users_growth_rate / 100) ** retention_period_months
    projected_daily_transactions = daily_transactions_per_user * (1 + transactions_growth_rate / 100) ** retention_period_months
    projected_daily_data_kb = projected_users * projected_daily_transactions * average_transaction_size_kb
    projected_monthly_data_kb = projected_daily_data_kb * 30
    projected_yearly_data_kb = projected_daily_data_kb * 365

    # Convert KB to GB
    def kb_to_gb(kb):
        return kb / (1024**2)

    return {
        "Metric": ["Current Daily Data (GB)", "Current Monthly Data (GB)", "Current Yearly Data (GB)",
                   "Projected Daily Data After Retention Period (GB)", "Projected Monthly Data After Retention Period (GB)",
                   "Projected Yearly Data After Retention Period (GB)"],
        "Value (GB)": [kb_to_gb(current_daily_data_kb), kb_to_gb(current_monthly_data_kb), kb_to_gb(current_yearly_data_kb),
                       kb_to_gb(projected_daily_data_kb), kb_to_gb(projected_monthly_data_kb), kb_to_gb(projected_yearly_data_kb)]
    }

# Streamlit UI
st.title("📊 Data Capacity Estimator 123 💡")

st.markdown("""
Welcome to the **Data Capacity Estimator 123**! Input your data transaction details below and see how much data you need today and in the future!
""")

# Define default values
default_values = {
    'current_users': 100000,
    'daily_transactions_per_user': 5,
    'average_transaction_size_kb': 0.5,
    'users_growth_rate': 5.0,
    'transactions_growth_rate': 3.0,
    'retention_period_months': 12
}

# Initialize session state with default values if not already set
if 'current_users' not in st.session_state:
    st.session_state.update(default_values)

# Reset button action
if st.button("🔄 Reset to Defaults"):
    st.session_state.update(default_values)

# Input widgets bound to session state
current_users = st.number_input("👥 Current Number of Users", value=st.session_state['current_users'], key="current_users")
daily_transactions_per_user = st.number_input("🔄 Daily Transactions per User", value=st.session_state['daily_transactions_per_user'], key="daily_transactions_per_user")
average_transaction_size_kb = st.number_input("💾 Average Transaction Size (KB)", value=st.session_state['average_transaction_size_kb'], key="average_transaction_size_kb")
users_growth_rate = st.number_input("📈 User Growth Rate (monthly, %)", value=st.session_state['users_growth_rate'], key="users_growth_rate")
transactions_growth_rate = st.number_input("📊 Transaction Growth Rate (monthly, %)", value=st.session_state['transactions_growth_rate'], key="transactions_growth_rate")
retention_period_months = st.number_input("🗓️ Retention Period (months)", value=st.session_state['retention_period_months'], key="retention_period_months")

# Calculate and display results
if st.button("🚀 Calculate Capacity"):
    results = calculate_data_capacity(st.session_state['current_users'], st.session_state['daily_transactions_per_user'], 
                                      st.session_state['average_transaction_size_kb'], 
                                      st.session_state['users_growth_rate'], st.session_state['transactions_growth_rate'], 
                                      st.session_state['retention_period_months'])
    
    data_df = pd.DataFrame(results)

    st.subheader("✨ Data Capacity Requirements")
    st.dataframe(data_df)

    # CSV download option
    csv = data_df.to_csv(index=False).encode('utf-8')
    st.download_button("💾 Download as CSV", csv, "data_capacity_results.csv", "text/csv", key='download-csv')

st.markdown("""
---
😎 **Pro Tip**: Use the buttons to calculate or reset. Save your results to CSV for later reference!
""")
