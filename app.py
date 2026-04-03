import streamlit as st
import requests
import os
import pandas as pd
import plotly.express as px

# API Base URL
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="AI Billing Intelligence", page_icon="🧾", layout="wide")

st.markdown("""
<style>
body, .stApp {
    background-color: #0d0d0d;
    color: white;
}
.stButton>button {
    background-color: red !important;
    color: white !important;
    border: none;
    border-radius: 5px;
    font-weight: bold;
    padding: 10px 24px;
    transition: 0.3s;
}
.stButton>button:hover {
    background-color: #ff3333 !important;
    border-color: #ff3333 !important;
}
h1, h2, h3 {
    color: #ff4d4d !important;
}
.css-1d391kg, .stSidebar {
    background-color: #1a1a1a !important;
}
</style>
""", unsafe_allow_html=True)

st.title("AI Billing Intelligence System ⚡")
st.markdown("Automate bill explanation, detect anomalies, and recommend plans using AI.")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a Feature", [
    "Billing Explanation", 
    "Plan Recommendation", 
    "Anomaly Detection", 
    "Data Query",
    "📊 Analytics Dashboard"
])

st.sidebar.header("📁 Data Management")
uploaded_file = st.sidebar.file_uploader("Upload billing_data.csv", type=["csv"])
if uploaded_file is not None:
    if st.sidebar.button("Process & Re-index", key="upload_btn"):
        with st.spinner("Uploading and updating AI index..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
                res = requests.post(f"{API_URL}/upload_data", files=files)
                if res.status_code == 200:
                    st.sidebar.success("Database uploaded & system re-indexed!")
                else:
                    st.sidebar.error("Upload failed.")
            except requests.exceptions.ConnectionError:
                st.sidebar.error("API Server is not running.")

def display_response(text):
    st.info(text)

if page == "Billing Explanation":
    st.header("🧾 Billing Explanation")
    user_id = st.text_input("Enter User ID", "101")
    if st.button("Explain Bill"):
        with st.spinner("Analyzing..."):
            try:
                res = requests.post(f"{API_URL}/explain_bill", json={"user_id": int(user_id)})
                if res.status_code == 200:
                    display_response(res.json().get("explanation", ""))
                else:
                    st.error(f"Error: {res.json().get('detail', 'Unknown error')}")
            except requests.exceptions.ConnectionError:
                st.error("API Server is not running.")

elif page == "Plan Recommendation":
    st.header("🎯 Plan Recommendation")
    user_id = st.text_input("Enter User ID", "102")
    if st.button("Get Recommendation"):
        with st.spinner("Analyzing Usage..."):
            try:
                res = requests.post(f"{API_URL}/recommend_plan", json={"user_id": int(user_id)})
                if res.status_code == 200:
                    display_response(res.json().get("recommendation", ""))
                else:
                    st.error(f"Error: {res.json().get('detail', 'Unknown error')}")
            except requests.exceptions.ConnectionError:
                st.error("API Server is not running.")

elif page == "Anomaly Detection":
    st.header("🚨 Anomaly Detection (Logs)")
    st.write("Scan the entire billing database for irregularities, duplicates, or abnormal charges.")
    if st.button("Run Diagnostics"):
        with st.spinner("Scanning for anomalies..."):
            try:
                res = requests.get(f"{API_URL}/detect_anomaly")
                if res.status_code == 200:
                    display_response(res.json().get("anomalies", ""))
                    st.write("### Raw Flagged Data view")
                    df = pd.read_csv("billing_data.csv")
                    # Display a raw view as requested for full log access
                    st.dataframe(df, use_container_width=True)
                else:
                    st.error("Failed to fetch anomalies.")
            except requests.exceptions.ConnectionError:
                st.error("API Server is not running.")

elif page == "Data Query":
    st.header("🔍 Data Query")
    query = st.text_input("Enter your query:", "Which plan generates highest revenue?")
    if st.button("Search"):
        with st.spinner("Querying data..."):
            try:
                res = requests.post(f"{API_URL}/query_data", json={"query": query})
                if res.status_code == 200:
                    display_response(res.json().get("answer", ""))
                else:
                    st.error("Failed to fetch data.")
            except requests.exceptions.ConnectionError:
                st.error("API Server is not running. Please start FastAPI on port 8000.")

elif page == "📊 Analytics Dashboard":
    st.header("📊 Interactive Analytics")
    try:
        res = requests.get(f"{API_URL}/analytics")
        if res.status_code == 200:
            data = res.json()
            rev_data = data.get("revenue_by_plan", {})
            use_data = data.get("usage_counts", {})
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Revenue per Plan")
                if rev_data:
                    df_rev = pd.DataFrame(list(rev_data.items()), columns=['Plan', 'Revenue'])
                    fig_rev = px.pie(df_rev, names='Plan', values='Revenue', 
                                     color_discrete_sequence=['#ff4d4d', '#ff1a1a', '#800000', '#cc0000'])
                    fig_rev.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
                    st.plotly_chart(fig_rev, use_container_width=True)
                else:
                    st.warning("No revenue data available.")
            
            with col2:
                st.subheader("Usage Trends")
                if use_data:
                    df_use = pd.DataFrame(list(use_data.items()), columns=['Usage Level', 'Count'])
                    fig_use = px.bar(df_use, x='Usage Level', y='Count', 
                                     color_discrete_sequence=['#ff3333'])
                    fig_use.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
                    st.plotly_chart(fig_use, use_container_width=True)
                else:
                    st.warning("No usage data available.")
        else:
            st.error("Failed to fetch analytics.")
    except requests.exceptions.ConnectionError:
        st.error("API Server is not running. Please start FastAPI on port 8000.")
