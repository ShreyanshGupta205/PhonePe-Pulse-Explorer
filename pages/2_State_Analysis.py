import streamlit as st
import pandas as pd
from utils.charts import create_bar_chart, create_india_choropleth
from utils.data_loader import get_filtered_data



st.title("🗺️ State-wise Analysis")
st.markdown("Geographic distribution of transactions across India.")

if 'df_transactions' not in st.session_state:
    st.warning("Please navigate from the main app page to ensure data is loaded.")
    st.stop()

filters = st.session_state.get('filters', {})
df_tx = get_filtered_data(st.session_state.df_transactions, **filters)

# Aggregated State Data
state_agg = df_tx.groupby('state').agg(
    total_count=('transaction_count', 'sum'),
    total_amount=('transaction_amount', 'sum')
).reset_index()

st.markdown("### 🇮🇳 Transaction Activity Map")
map_metric = st.selectbox("Select Metric for Map", ["Transaction Count", "Transaction Amount"])
val_col = 'total_count' if map_metric == "Transaction Count" else 'total_amount'

fig_map = create_india_choropleth(state_agg, 'state', val_col, f"India - {map_metric}")
st.plotly_chart(fig_map, use_container_width=True)

st.markdown("---")
st.markdown("### 📊 State Comparison")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Top States by Transaction Count")
    top_count = state_agg.sort_values(by='total_count', ascending=True).tail(10)
    fig_count = create_bar_chart(top_count, 'total_count', 'state', None, orientation='h', color_col='total_count')
    st.plotly_chart(fig_count, use_container_width=True)

with col2:
    st.markdown("#### Top States by Transaction Amount (₹)")
    top_amt = state_agg.sort_values(by='total_amount', ascending=True).tail(10)
    fig_amt = create_bar_chart(top_amt, 'total_amount', 'state', None, orientation='h', color_col='total_amount')
    st.plotly_chart(fig_amt, use_container_width=True)
