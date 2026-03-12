import streamlit as st
from utils.data_loader import load_data, get_filtered_data

# Must be the first Streamlit command
st.set_page_config(
    page_title="PhonePe Pulse Dashboard",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    /* PhonePe brand colors */
    :root {
        --primary-color: #5f259f;
        --secondary-color: #00d09c;
        --background-color: #f8f9fa;
        --text-color: #333333;
    }
    
    .main {
        background-color: var(--background-color);
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3 {
        color: var(--primary-color) !important;
        font-weight: 700 !important;
    }
    
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-left: 5px solid var(--secondary-color);
    }
    
    [data-testid="stSidebar"] {
        background-color: white;
        border-right: 1px solid #e0e0e0;
    }
    
    /* Hide top header padding */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Load Data
df_transactions, df_users = load_data()

# Store in session state for pages to access easily
if 'df_transactions' not in st.session_state:
    st.session_state.df_transactions = df_transactions
if 'df_users' not in st.session_state:
    st.session_state.df_users = df_users

# Global Filters in Sidebar
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/7/71/PhonePe_Logo.svg", width=150)
st.sidebar.markdown("### 🔍 Global Filters")

# Year & Quarter filters
years = sorted(df_transactions['year'].unique().tolist())
quarters = sorted(df_transactions['quarter'].unique().tolist())

col1, col2 = st.sidebar.columns(2)
with col1:
    selected_year = st.selectbox("Year", ["All"] + years)
with col2:
    selected_quarter = st.selectbox("Quarter", ["All"] + quarters)

# Additional filters
states = sorted(df_transactions['state'].unique().tolist())
selected_state = st.sidebar.selectbox("State", ["All"] + states)

tx_types = sorted(df_transactions['transaction_type'].unique().tolist())
selected_tx_type = st.sidebar.selectbox("Transaction Type", ["All"] + tx_types)

# Update session state with selected filters
st.session_state.filters = {
    'year': selected_year if selected_year != "All" else None,
    'quarter': selected_quarter if selected_quarter != "All" else None,
    'state': selected_state if selected_state != "All" else None,
    'tx_type': selected_tx_type if selected_tx_type != "All" else None
}

st.sidebar.markdown("---")

# Define Navigation
overview = st.Page("pages/1_Overview.py", title="Overview", icon="📈", default=True)
state_analysis = st.Page("pages/2_State_Analysis.py", title="State Analysis", icon="🗺️")
district_analysis = st.Page("pages/3_District_Analysis.py", title="District Analysis", icon="📍")
category_analysis = st.Page("pages/4_Category_Analysis.py", title="Category Analysis", icon="🏷️")
user_growth = st.Page("pages/5_User_Growth.py", title="User Growth", icon="👥")

pg = st.navigation({
    "Analytics": [overview, state_analysis, district_analysis, category_analysis, user_growth]
})

pg.run()
