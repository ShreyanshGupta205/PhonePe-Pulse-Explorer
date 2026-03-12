import pandas as pd
import numpy as np
import streamlit as st

@st.cache_data
def load_data():
    """
    Generates mock PhonePe transaction and user data.
    Caches the generated data to prevent re-generation on each app interaction.
    """
    np.random.seed(42)  # For reproducible mock data
    
    states = [
        "Andaman & Nicobar Islands", "Andhra Pradesh", "Arunachal Pradesh",
        "Assam", "Bihar", "Chandigarh", "Chhattisgarh", "Dadra and Nagar Haveli and Daman and Diu",
        "Delhi", "Goa", "Gujarat", "Haryana", "Himachal Pradesh",
        "Jammu & Kashmir", "Jharkhand", "Karnataka", "Kerala", "Ladakh",
        "Lakshadweep", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya",
        "Mizoram", "Nagaland", "Odisha", "Puducherry", "Punjab",
        "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
        "Uttar Pradesh", "Uttarakhand", "West Bengal"
    ]
    
    # 5 dummy districts per state
    districts = {state: [f"District {i}" for i in range(1, 6)] for state in states}
    years = [2021, 2022, 2023, 2024]
    quarters = [1, 2, 3, 4]
    categories = ["Peer-to-Peer", "Merchant Payments", "Recharge & Bills", "Financial Services"]
    
    tx_records = []
    user_records = []
    
    for state in states:
        for dist in districts[state]:
            for year in years:
                for q in quarters:
                    # Users data logic (aggregate at state-district-year-quarter)
                    # Baseline users grows each year
                    trend_multiplier = (year - 2020) * 1.5 + (q * 0.2)
                    
                    # Ensure some random variance but overall growth
                    base_users = np.random.randint(10000, 100000)
                    registered_users = int(base_users * trend_multiplier)
                    app_opens = int(registered_users * np.random.uniform(3.0, 12.0))
                    
                    user_records.append({
                        "state": state,
                        "district": dist,
                        "year": year,
                        "quarter": q,
                        "registered_users": registered_users,
                        "app_opens": app_opens
                    })
                    
                    # Transactions data logic (spread across categories)
                    for cat in categories:
                        tx_count = int(app_opens * np.random.uniform(0.1, 0.8)) # transactions are a fraction of app opens
                        
                        # Amount varies by category
                        if cat == "Peer-to-Peer":
                            avg_amt = np.random.uniform(500, 3000)
                        elif cat == "Merchant Payments":
                            avg_amt = np.random.uniform(50, 800)
                        elif cat == "Recharge & Bills":
                            avg_amt = np.random.uniform(100, 1500)
                        else: # Financial Services
                            avg_amt = np.random.uniform(1000, 5000)
                            
                        tx_amount = tx_count * avg_amt
                        
                        tx_records.append({
                            "state": state,
                            "district": dist,
                            "year": year,
                            "quarter": q,
                            "transaction_type": cat,
                            "transaction_count": tx_count,
                            "transaction_amount": tx_amount
                        })
                        
    df_transactions = pd.DataFrame(tx_records)
    df_users = pd.DataFrame(user_records)
    
    return df_transactions, df_users

@st.cache_data
def get_state_summary(df):
    """
    Summarizes transaction data by state.
    """
    return df.groupby('state').agg({
        'transaction_count': 'sum',
        'transaction_amount': 'sum'
    }).reset_index()

def get_filtered_data(df, year=None, quarter=None, state=None, tx_type=None):
    """
    Utility function to filter data based on selected parameters.
    """
    filtered_df = df.copy()
    if year:
        filtered_df = filtered_df[filtered_df['year'] == year]
    if quarter:
        filtered_df = filtered_df[filtered_df['quarter'] == quarter]
    if state:
        filtered_df = filtered_df[filtered_df['state'] == state]
    if tx_type and 'transaction_type' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['transaction_type'] == tx_type]
        
    return filtered_df
