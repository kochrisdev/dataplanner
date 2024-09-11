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
st.title("📊 Fun Data Capacity Estimator 123 💡")

st.markdown("""
Welcome to the **Data Capacity Estimator**! Input your service's details below and see how much data you need today and in the future!
""")

# Input fields with default values
if 'current_users' not in st.session_state:
    st.session_state['current_users'] = 100000
if 'daily_transactions_per_user' not in st.session_state:
    st.session_state['daily_transactions_per_user'] = 5
if 'average_transaction_size_kb' not in st.session_state:
    st.session_state['average_transaction_size_kb'] = 0.5
if 'users_growth_rate' not in st.session_state:
    st.session_state['users_growth_rate'] = 5.0
if 'transactions_growth_rate' not in st.session_state:
    st.session_state['transactions_growth_rate'] = 3.0
if 'retention_period_months' not in st.session_state:
    st.session_state['retention_period_months'] = 12

# Input widgets
current_users = st.number_input("👥 Current Number of Users", value=st.session_state['current_users'])
daily_transactions_per_user = st.number_input("🔄 Daily Transactions per User", value=st.session_state['daily_transactions_per_user'])
average_transaction_size_kb = st.number_input("💾 Average Transaction Size (KB)", value=st.session_state['average_transaction_size_kb'])
users_growth_rate = st.number_input("📈 User Growth Rate (monthly, %)", value=st.session_state['users_growth_rate'])
transactions_growth_rate = st.number_input("📊 Transaction Growth Rate (monthly, %)", value=st.session_state['transactions_growth_rate'])
retention_period_months = st.number_input("🗓️ Retention Period (months)", value=st.session_state['retention_period_months'])

# Buttons
calculate_button = st.button("🚀 Calculate Capacity")
reset_button = st.button("🔄 Reset to Defaults")

# Reset button action
if reset_button:
    st.session_state['current_users'] = 100000
    st.session_state['daily_transactions_per_user'] = 5
    st.session_state['average_transaction_size_kb'] = 0.5
    st.session_state['users_growth_rate'] = 5.0
    st.session_state['transactions_growth_rate'] = 3.0
    st.session_state['retention_period_months'] = 12
    # Rerun is not needed, inputs will automatically update

# Calculate and display results
if calculate_button:
    results = calculate_data_capacity(current_users, daily_transactions_per_user, average_transaction_size_kb, 
                                      users_growth_rate, transactions_growth_rate, retention_period_months)
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
