import streamlit as st
import pandas as pd
from utils.charts import create_bar_chart
from utils.data_loader import get_filtered_data



st.title("📍 District Analysis")
st.markdown("Deep dive into district-level performance metrics.")

if 'df_transactions' not in st.session_state:
    st.warning("Please navigate from the main app page to ensure data is loaded.")
    st.stop()

filters = st.session_state.get('filters', {})
df_tx = get_filtered_data(st.session_state.df_transactions, **filters)

# State selector specific to this page if global filter isn't set
selected_state = filters.get('state')
if not selected_state:
    states = sorted(df_tx['state'].unique().tolist())
    selected_state = st.selectbox("Select a State to View Districts", states)
    # filter data for this state
    df_tx = df_tx[df_tx['state'] == selected_state]
else:
    st.info(f"Viewing districts for globally selected state: **{selected_state}**")

st.markdown("---")

dist_agg = df_tx.groupby('district').agg(
    total_count=('transaction_count', 'sum'),
    total_amount=('transaction_amount', 'sum')
).reset_index()

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"#### Top Districts by Volume in {selected_state}")
    top_districts_vol = dist_agg.sort_values(by='total_count', ascending=True).tail(10)
    fig_vol = create_bar_chart(top_districts_vol, 'total_count', 'district', None, orientation='h', color_col='total_count')
    st.plotly_chart(fig_vol, use_container_width=True)

with col2:
    st.markdown(f"#### Top Districts by Amount in {selected_state}")
    top_districts_amt = dist_agg.sort_values(by='total_amount', ascending=True).tail(10)
    fig_amt = create_bar_chart(top_districts_amt, 'total_amount', 'district', None, orientation='h', color_col='total_amount')
    st.plotly_chart(fig_amt, use_container_width=True)
