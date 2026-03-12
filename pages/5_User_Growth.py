import streamlit as st
import pandas as pd
from utils.charts import create_line_chart, create_bar_chart
from utils.data_loader import get_filtered_data



st.title("👥 User Growth & Adoption")
st.markdown("Track registered users and app usage over time.")

if 'df_users' not in st.session_state:
    st.warning("Please navigate from the main app page to ensure data is loaded.")
    st.stop()

filters = st.session_state.get('filters', {})
df_usr = get_filtered_data(st.session_state.df_users, **filters)

# Global user metrics
col1, col2 = st.columns(2)

# Approximate max users to avoid summing same users over quarters incorrectly
# For total users at the latest quarter available
latest_year = df_usr['year'].max()
latest_quarter_df = df_usr[df_usr['year'] == latest_year]
latest_quarter = latest_quarter_df['quarter'].max()

current_users = df_usr[(df_usr['year'] == latest_year) & (df_usr['quarter'] == latest_quarter)]['registered_users'].sum()
total_opens = df_usr['app_opens'].sum()

with col1:
    st.metric(label="Total Registered Users (Latest)", value=f"{current_users:,.0f}")
with col2:
    st.metric(label="Total App Opens (Period)", value=f"{total_opens:,.0f}")

st.markdown("---")

# User Growth Trend
st.markdown("### 📈 Registered Users Over Time")
# Group by year and quarter
user_trend = df_usr.groupby(['year', 'quarter'])['registered_users'].sum().reset_index()
user_trend['Period'] = user_trend['year'].astype(str) + " Q" + user_trend['quarter'].astype(str)

fig_users = create_line_chart(user_trend, 'Period', 'registered_users', "Registered Users Growth")
st.plotly_chart(fig_users, use_container_width=True)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📱 App Opens Over Time")
    opens_trend = df_usr.groupby(['year', 'quarter'])['app_opens'].sum().reset_index()
    opens_trend['Period'] = opens_trend['year'].astype(str) + " Q" + opens_trend['quarter'].astype(str)
    
    fig_opens = create_line_chart(opens_trend, 'Period', 'app_opens', "App Opens Growth")
    st.plotly_chart(fig_opens, use_container_width=True)

with col2:
    st.markdown("### 🏆 Top States by Users")
    # Using the latest quarter data for state comparison
    state_users = current_users_df = df_usr[(df_usr['year'] == latest_year) & (df_usr['quarter'] == latest_quarter)]
    state_agg = state_users.groupby('state')['registered_users'].sum().reset_index().sort_values(by='registered_users', ascending=False).head(10)
    
    fig_state_usr = create_bar_chart(state_agg, 'state', 'registered_users', None)
    st.plotly_chart(fig_state_usr, use_container_width=True)
