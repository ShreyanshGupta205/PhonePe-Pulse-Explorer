import streamlit as st
import pandas as pd
from utils.charts import create_line_chart, create_bar_chart
from utils.data_loader import get_filtered_data



st.title("📊 High-Level Overview")
st.markdown("Key metrics and national trends across PhonePe.")

# Ensure session state is initialized
if 'df_transactions' not in st.session_state or 'df_users' not in st.session_state:
    st.warning("Please navigate from the main app page to ensure data is loaded.")
    st.stop()

# Get filters
filters = st.session_state.get('filters', {})
df_tx = get_filtered_data(st.session_state.df_transactions, **filters)
df_usr = get_filtered_data(st.session_state.df_users, **filters)

# Key Metrics
st.markdown("### 🏆 Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)

total_tx = df_tx['transaction_count'].sum()
total_amt = df_tx['transaction_amount'].sum()
total_users = df_usr.groupby(['state', 'district'])['registered_users'].max().sum() # approx max users
total_opens = df_usr['app_opens'].sum()

with col1:
    st.metric(label="Total Transactions", value=f"{total_tx:,.0f}", help="Total number of transactions across all selected filters.")
with col2:
    st.metric(label="Total Value (₹)", value=f"₹{total_amt:,.0f}", help="Cumulative monetary value of transactions.")
with col3:
    st.metric(label="Registered Users", value=f"{total_users:,.0f}", help="Approximate number of registered users in selected regions.")
with col4:
    st.metric(label="App Opens", value=f"{total_opens:,.0f}", help="Total number of times the app was opened.")

st.markdown("---")

# Charts row 1
col1, col2 = st.columns(2)

with col1:
    # Monthly (or Quarterly) trend
    trend_df = df_tx.groupby(['year', 'quarter'])['transaction_count'].sum().reset_index()
    trend_df['Period'] = trend_df['year'].astype(str) + " Q" + trend_df['quarter'].astype(str)
    fig_trend = create_line_chart(trend_df, 'Period', 'transaction_count', "Transaction Volume Trend")
    st.plotly_chart(fig_trend, use_container_width=True)
    
with col2:
    # Value growth
    val_df = df_tx.groupby(['year', 'quarter'])['transaction_amount'].sum().reset_index()
    val_df['Period'] = val_df['year'].astype(str) + " Q" + val_df['quarter'].astype(str)
    fig_val = create_line_chart(val_df, 'Period', 'transaction_amount', "Payment Value Growth (₹)")
    st.plotly_chart(fig_val, use_container_width=True)

st.markdown("---")

# Catgeory Breakdown and Top States
col3, col4 = st.columns([1, 1])

with col3:
    st.markdown("### 🏷️ Category Breakdown")
    cat_df = df_tx.groupby('transaction_type')['transaction_amount'].sum().reset_index()
    cat_df = cat_df.sort_values(by='transaction_amount', ascending=False)
    st.dataframe(cat_df, hide_index=True, use_container_width=True)

with col4:
    st.markdown("### 🔝 Top States")
    top_states = df_tx.groupby('state')['transaction_count'].sum().reset_index()
    top_states = top_states.sort_values(by='transaction_count', ascending=False).head(10)
    fig_states = create_bar_chart(top_states, 'state', 'transaction_count', None)
    st.plotly_chart(fig_states, use_container_width=True)
