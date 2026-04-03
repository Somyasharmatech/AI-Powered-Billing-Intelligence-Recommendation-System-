import streamlit as st
import requests
import os
import pandas as pd
import plotly.express as px

# API Base URL
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="AI Billing Intelligence Dashboard", page_icon="🧾", layout="wide")

st.markdown("""
<style>
body, .stApp {
    background-color: #0d0d0d;
    color: white;
}
h1, h2, h3 {
    color: #ff1a1a;
}
.stButton>button {
    background-color: #ff1a1a;
    color: white;
    border-radius: 8px;
    border: none;
    padding: 10px 24px;
    font-weight: bold;
}
.css-1d391kg, .stSidebar {
    background-color: #1a1a1a !important;
}
div[data-testid="stMetricValue"] {
    color: #ff1a1a;
}
</style>
""", unsafe_allow_html=True)

st.title("AI Billing Intelligence Dashboard")
st.markdown("This system integrates with enterprise billing platforms to automate analysis, detect errors, and generate insights.")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Main Menu", [
    "1. Explain Bill", 
    "2. Recommend Plan", 
    "3. Detect Anomalies", 
    "4. Insights Dashboard"
])

st.sidebar.markdown("---")
st.sidebar.header("📁 Data Management")
uploaded_file = st.sidebar.file_uploader("Upload Billing Data", type=["csv"])
if uploaded_file is not None:
    if st.sidebar.button("Process & Re-index", key="upload_btn"):
        with st.spinner("Processing data & updating AI..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
                res = requests.post(f"{API_URL}/upload_data", files=files)
                if res.status_code == 200:
                    st.sidebar.success("Database uploaded & system re-indexed!")
                else:
                    st.sidebar.error("Upload failed.")
            except requests.exceptions.ConnectionError:
                st.sidebar.error("API Server is not running.")


if page == "1. Explain Bill":
    with st.container():
        st.header("🧾 Explain Bill")
        st.markdown("Provides structured, intelligent breakdown of customer usage profiles.")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            user_id = st.text_input("Enter target User ID:", "101")
            submit_btn = st.button("Generate Explanation")
            
        with col2:
            if submit_btn:
                with st.spinner("AI is analyzing profile..."):
                    try:
                        res = requests.post(f"{API_URL}/explain_bill", json={"user_id": int(user_id)})
                        if res.status_code == 200:
                            st.info(res.json().get("explanation", ""))
                        else:
                            st.error(f"Error: {res.json().get('detail', 'Unknown error')}")
                    except requests.exceptions.ConnectionError:
                        st.error("API Server is not responding.")

elif page == "2. Recommend Plan":
    with st.container():
        st.header("🎯 Recommend Plan")
        st.markdown("Automated strategic consultation on optimal plan tier modifications.")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            user_id = st.text_input("Enter target User ID:", "102")
            submit_btn = st.button("Generate Strategy")
            
        with col2:
            if submit_btn:
                with st.spinner("Calculating limits and usage distribution..."):
                    try:
                        res = requests.post(f"{API_URL}/recommend_plan", json={"user_id": int(user_id)})
                        if res.status_code == 200:
                            st.success(res.json().get("recommendation", ""))
                        else:
                            st.error(f"Error: {res.json().get('detail', 'Unknown error')}")
                    except requests.exceptions.ConnectionError:
                        st.error("API Server is not responding.")

elif page == "3. Detect Anomalies":
    with st.container():
        st.header("🚨 System Anomalies")
        st.markdown("Scan the entire billing database for irregularities, duplicates, or abnormal behaviors.")
        
        if st.button("Run Global Diagnostics"):
            with st.spinner("Scanning for anomalies..."):
                try:
                    res = requests.get(f"{API_URL}/detect_anomaly")
                    if res.status_code == 200:
                        data = res.json()
                        count = data.get("count", 0)
                        
                        if count > 0:
                            st.warning(f"⚠ High billing detected for {count} users or records.")
                            st.error(data.get("report", ""))
                        else:
                            st.success("✔ System Check Passed: No obvious anomalies detected.")
                            
                        st.markdown("### Raw Audit Logs")
                        df = pd.read_csv("billing_data.csv")
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.error("Failed to fetch anomalies.")
                except requests.exceptions.ConnectionError:
                    st.error("API Server is not responding.")

elif page == "4. Insights Dashboard":
    st.header("📊 Insights Dashboard")
    st.markdown("Active overview metrics integrated from enterprise billing platforms.")
    try:
        res = requests.get(f"{API_URL}/analytics")
        if res.status_code == 200:
            data = res.json()
            total_users = data.get("total_users", 0)
            most_used = data.get("most_used_plan", "N/A")
            rev_data = data.get("revenue_by_plan", {})
            use_data = data.get("usage_counts", {})
            
            high_usage_amount = use_data.get("high", 0)
            
            # --- METRICS CARDS ---
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Total Users", total_users)
            m2.metric("Most Used Plan", most_used)
            m3.metric("High Usage Users", high_usage_amount)
            m4.metric("Total Active Plans", len(rev_data))
            
            st.markdown("---")
            
            # --- CHARTS ---
            c1, c2 = st.columns(2)
            
            with c1:
                st.subheader("Revenue by Plan")
                if rev_data:
                    df_rev = pd.DataFrame(list(rev_data.items()), columns=['Plan', 'Revenue'])
                    fig_rev = px.bar(df_rev, x='Plan', y='Revenue', 
                                     color_discrete_sequence=['#ff1a1a'])
                    fig_rev.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
                    st.plotly_chart(fig_rev, use_container_width=True)
                else:
                    st.warning("No revenue data available.")
            
            with c2:
                st.subheader("Plan Distribution")
                if rev_data:
                    df_pie = pd.DataFrame(list(rev_data.items()), columns=['Plan', 'Revenue'])
                    fig_pie = px.pie(df_pie, names='Plan', values='Revenue', 
                                     color_discrete_sequence=['#ff1a1a', '#cc0000', '#800000', '#4d0000'])
                    fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
                    st.plotly_chart(fig_pie, use_container_width=True)
                else:
                    st.warning("No usage data available.")
        else:
            st.error("Failed to fetch analytics.")
    except requests.exceptions.ConnectionError:
        st.error("API Server is not responding.")

st.markdown("---")
st.markdown("##### 🔍 Global Realtime Query")
query = st.text_input("Ask a question about the billing data:", "Which plan generates highest revenue?")
if st.button("Search Database"):
    with st.spinner("AI querying..."):
        try:
            res = requests.post(f"{API_URL}/query_data", json={"query": query})
            if res.status_code == 200:
                st.info(res.json().get("answer", ""))
            else:
                st.error("Failed to fetch data.")
        except requests.exceptions.ConnectionError:
            st.error("API Server is not responding.")
