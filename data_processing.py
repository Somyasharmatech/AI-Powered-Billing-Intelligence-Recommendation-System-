import pandas as pd
import os

DATA_FILE = "billing_data.csv"

def load_billing_data():
    if not os.path.exists(DATA_FILE):
        return pd.DataFrame()
    return pd.read_csv(DATA_FILE)

def get_user_data(user_id: int):
    df = load_billing_data()
    if df.empty: return None
    user_data = df[df["user_id"] == user_id]
    if user_data.empty: return None
    return user_data.to_dict(orient="records")[0]

def get_all_data():
    df = load_billing_data()
    return df.to_dict(orient="records")

def get_analytics():
    df = load_billing_data()
    if df.empty:
        return {"total_users": 0, "total_revenue": 0, "most_used_plan": "N/A", "revenue_by_plan": {}, "usage_counts": {}}
    
    total_users = len(df)
    total_revenue = int(df["bill_amount"].sum())
    most_used_plan = df["plan"].mode()[0] if not df.empty else "N/A"
    
    revenue_by_plan = df.groupby("plan")["bill_amount"].sum().to_dict()
    usage_counts = df["usage"].value_counts().to_dict()
    
    return {
        "total_users": total_users,
        "total_revenue": total_revenue,
        "most_used_plan": most_used_plan,
        "revenue_by_plan": revenue_by_plan,
        "usage_counts": usage_counts
    }
