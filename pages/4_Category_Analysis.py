import streamlit as st
import pandas as pd
from utils.charts import create_pie_chart, create_bar_chart
from utils.data_loader import get_filtered_data



st.title("🏷️ Payment Category Analysis")
st.markdown("Breakdown of transactions by payment type.")

if 'df_transactions' not in st.session_state:
    st.warning("Please navigate from the main app page to ensure data is loaded.")
    st.stop()

filters = st.session_state.get('filters', {})
df_tx = get_filtered_data(st.session_state.df_transactions, **filters)

# Aggregated Category Data
cat_agg = df_tx.groupby('transaction_type').agg(
    total_count=('transaction_count', 'sum'),
    total_amount=('transaction_amount', 'sum')
).reset_index()

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Transaction Volume by Category")
    fig_pie_vol = create_pie_chart(cat_agg, 'transaction_type', 'total_count', None)
    st.plotly_chart(fig_pie_vol, use_container_width=True)

with col2:
    st.markdown("### Transaction Amount by Category")
    fig_pie_amt = create_pie_chart(cat_agg, 'transaction_type', 'total_amount', None)
    st.plotly_chart(fig_pie_amt, use_container_width=True)

st.markdown("---")
st.markdown("### 📊 Category Distribution over Time")

# Time series for categories
time_col = 'year'
if filters.get('year'):
    time_col = 'quarter'
    
trend_agg = df_tx.groupby([time_col, 'transaction_type'])['transaction_count'].sum().reset_index()

# Using a grouped bar chart
import plotly.express as px
from utils.charts import apply_fintech_theme

fig_trend = px.bar(trend_agg, x=time_col, y='transaction_count', color='transaction_type', 
                   barmode='group', title=f"Transaction Volume by {time_col.capitalize()}")
fig_trend = apply_fintech_theme(fig_trend)
st.plotly_chart(fig_trend, use_container_width=True)
