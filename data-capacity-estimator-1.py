import streamlit as st

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
        "Current Daily Data (GB)": kb_to_gb(current_daily_data_kb),
        "Current Monthly Data (GB)": kb_to_gb(current_monthly_data_kb),
        "Current Yearly Data (GB)": kb_to_gb(current_yearly_data_kb),
        "Projected Daily Data After Retention Period (GB)": kb_to_gb(projected_daily_data_kb),
        "Projected Monthly Data After Retention Period (GB)": kb_to_gb(projected_monthly_data_kb),
        "Projected Yearly Data After Retention Period (GB)": kb_to_gb(projected_yearly_data_kb)
    }

# Streamlit UI
st.title("Data Capacity Estimator for Payment Service")

# Input fields
current_users = st.number_input("Current Number of Users", value=100000)
daily_transactions_per_user = st.number_input("Daily Transactions per User", value=5)
average_transaction_size_kb = st.number_input("Average Transaction Size (KB)", value=0.5)
users_growth_rate = st.number_input("User Growth Rate (monthly, %)", value=5.0)
transactions_growth_rate = st.number_input("Transaction Growth Rate (monthly, %)", value=3.0)
retention_period_months = st.number_input("Retention Period (months)", value=12)

# Button to calculate
if st.button("Calculate Capacity"):
    results = calculate_data_capacity(current_users, daily_transactions_per_user, average_transaction_size_kb, 
                                      users_growth_rate, transactions_growth_rate, retention_period_months)

    # Display results
    st.subheader("Data Capacity Requirements")
    for metric, value in results.items():
        st.write(f"{metric}: {value:.2f} GB")
