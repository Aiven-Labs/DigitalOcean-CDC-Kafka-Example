import streamlit as st

# Streamlit app
def dashboard(dashboard_title: str, dashboard_header: str, dashboard_sidebar: str,):
    # Default settings
    st.set_page_config(
        page_title="Real-time Data",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Run the Streamlit app
    st.title(str.upper(dashboard_title))

    # Add Logo
    st.sidebar.image("images/logo.png", width=250)

    # Sidebar with user instructions
    st.sidebar.markdown(dashboard_sidebar)

    # Display weather data in the main section
    st.header(dashboard_header)
