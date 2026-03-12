import streamlit as st

def apply_custom_styles():
    """
    Applies custom CSS for the PaisaPulse dashboard.
    """
    st.markdown("""
    <style>
        :root {
            --primary-color: #5f259f;
            --secondary-color: #00d09c;
            --background-color: #f8f9fa;
        }
        
        .main {
            background-color: var(--background-color);
        }
        
        h1, h2, h3 {
            color: var(--primary-color) !important;
            font-weight: 700 !important;
        }
        
        .stMetric {
            background-color: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            border-top: 4px solid var(--primary-color);
        }
        
        [data-testid="stSidebar"] {
            border-right: 1px solid #f0f0f0;
        }
    </style>
    """, unsafe_allow_html=True)
