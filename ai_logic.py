import os
import pandas as pd
from dotenv import load_dotenv
from typing import Dict, Any, List

# Setup for LLM with LangChain
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.chains import RetrievalQA

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
USE_MOCK = len(OPENAI_API_KEY) == 0

llm = None
vector_store = None
qa_chain = None

def init_rag_system(csv_path: str = "billing_data.csv"):
    global llm, vector_store, qa_chain
    if USE_MOCK:
        print("Running in MOCK mode (no OPENAI_API_KEY found).")
        return
    
    try:
        df = pd.read_csv(csv_path)
        documents = []
        for index, row in df.iterrows():
            content = f"User ID: {row['user_id']}, Plan: {row['plan']}, Usage: {row['usage']}, Data Used: {row['data_used']}, Bill Amount: {row['bill_amount']}"
            documents.append(Document(page_content=content, metadata={"user_id": row["user_id"], "plan": row["plan"]}))
        
        embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
        vector_store = FAISS.from_documents(documents, embeddings)
        
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=OPENAI_API_KEY)
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vector_store.as_retriever()
        )
        print("RAG System Initialized with OpenAI.")
    except Exception as e:
        print(f"Failed to initialize RAG system: {str(e)}")

def reindex_data():
    print("Reindexing data...")
    init_rag_system()

init_rag_system()

def explain_bill(user_data: Dict[str, Any]) -> str:
    if USE_MOCK:
        extra_charge = "which resulted in additional charges being applied." if user_data["usage"] == "high" else "which aligns with the normal limits."
        return (f"The user is currently subscribed to the **{user_data['plan']} plan**.\n"
                f"Based on historical data, usage sits at **{user_data['data_used']}** ({user_data['usage']}), "
                f"{extra_charge} \n"
                f"**Total Outstanding Balance:** ${user_data['bill_amount']}")
    
    prompt = (f"Act as a professional financial billing analyst. Explain the bill for User ID {user_data['user_id']}. "
              f"They are subscribed to the {user_data['plan']} plan, have {user_data['usage']} data consumption tracking at {user_data['data_used']}, "
              f"and their current generated bill is {user_data['bill_amount']}. "
              "Provide a natural, structured paragraph explanation detailing why the bill is this amount based on these parameters.")
    return qa_chain.run(prompt)

def recommend_plan(user_data: Dict[str, Any]) -> str:
    if USE_MOCK:
        if user_data["usage"] == "high":
            return (f"**Recommendation Evaluation:**\n"
                    f"Our analytics indicate sustained high usage ({user_data['data_used']}) on the {user_data['plan']} tier. "
                    f"To prevent ongoing overage charges and optimize financial efficiency, we strongly suggest migrating this account to the **Premium Plan**.")
        elif user_data["usage"] == "low":
            return (f"**Recommendation Evaluation:**\n"
                    f"Customer utilization is currently low ({user_data['data_used']}). Continuing on the {user_data['plan']} tier is not cost effective. "
                    f"Downgrading to the **Basic Plan** is recommended to maximize value.")
        else:
            return (f"**Recommendation Evaluation:**\n"
                    f"The current **{user_data['plan']} Plan** effectively supports this user's consumption parameters without incurring unnecessary overflow charges.")
    
    prompt = (f"Act as a professional enterprise consultant. Based on the following customer profile: (Plan Subscribed: {user_data['plan']}, "
              f"Data Usage Metrics: {user_data['usage']}, Exact Volume: {user_data['data_used']}). "
              "Please evaluate their profile and output a structured, professional business recommendation on the optimal subscription plan for them going forward. Explain the financial reasoning.")
    return qa_chain.run(prompt)

def detect_anomaly(all_data: List[Dict[str, Any]]) -> dict:
    df = pd.DataFrame(all_data)
    anomalies = []
    
    dup_count = df.duplicated(subset=['user_id']).sum()
    if dup_count > 0:
        anomalies.append(f"- User records duplicated. Total duplicates: **{dup_count} entries**.")
        
    high_bills = df[df['bill_amount'] > 1000]
    for uid in high_bills['user_id']:
        anomalies.append(f"- User {uid} generated an unusually high bill exceeding safe thresholds.")
        
    mismatches = df[(df['plan'] == 'Basic') & (df['bill_amount'] > 500)]
    for uid in mismatches['user_id']:
        anomalies.append(f"- User {uid} (Basic Plan) billed exceptionally high, indicating severe undetected overages.")
         
    if not anomalies:
         return {"count": 0, "report": "✔ System check passed. No anomalies detected in current billing cycles."}
         
    report = f"⚠ {len(anomalies)} anomalies detected:\n" + "\n".join(anomalies)
    
    return {"count": len(anomalies), "report": report}

def query_data(query: str, all_data: List[Dict[str, Any]]) -> str:
    if USE_MOCK:
        df = pd.DataFrame(all_data)
        if "highest revenue" in query.lower():
            revenue_by_plan = df.groupby("plan")["bill_amount"].sum()
            best_plan = revenue_by_plan.idxmax()
            return f"**Analysis Result:** Based on financial aggregation, the plan driving the highest systemic revenue is the **{best_plan} plan**."
        return "I am operating in local mock mode. Please query simple constraints like 'Which plan generates highest revenue?' to test UI integrations seamlessly!"
        
    return qa_chain.run(query)
