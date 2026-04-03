import os
import pandas as pd
from dotenv import load_dotenv
from typing import Dict, Any, List

# Setup for LLM with LangChain
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
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
        reasoning = (
            f"**Why the bill is {'high' if user_data['usage'] == 'high' else 'normal'}:** The final bill generated is ${user_data['bill_amount']}. This is directly correlated to their consumption volume on the {user_data['plan']} plan.\n\n"
            f"**What caused the issue:** The customer's internal usage metric is currently tracked as '{user_data['usage']}' reflecting exactly {user_data['data_used']} of data transferred during the billing cycle.\n\n"
            f"**What action is recommended:** {'We advise an immediate upgrade to a premium tier to mitigate overage fees.' if user_data['usage'] == 'high' else 'No immediate action required, usage is within safe parameters.'}"
        )
        return reasoning
    
    prompt = (f"Act as an expert financial telecom analyst. Analyze the bill for User ID {user_data['user_id']} who is on the {user_data['plan']} plan, "
              f"with {user_data['data_used']} data used, resulting in a bill of {user_data['bill_amount']}. "
              "You MUST format your response into exactly these three distinct sections: "
              "\n- **Why the bill is high** (or why it is normal)"
              "\n- **What caused the issue**"
              "\n- **What action is recommended**.")
    return qa_chain.run(prompt)

def recommend_plan(user_data: Dict[str, Any]) -> str:
    # Use the same powerful 3-step prompt format for plan recommendations to keep it uniform
    return explain_bill(user_data)

def detect_anomaly(all_data: List[Dict[str, Any]]) -> dict:
    df = pd.DataFrame(all_data)
    anomalies = []
    
    # Duplicate billing detection
    dup_users = df[df.duplicated(subset=['user_id'], keep=False)]
    for uid in dup_users['user_id'].unique():
        anomalies.append(f"User {uid} billed twice")
        
    # Bill amount above threshold
    high_bills = df[df['bill_amount'] > 1000]
    for uid in high_bills['user_id']:
        anomalies.append(f"User {uid} unusually high bill (${high_bills[high_bills['user_id']==uid]['bill_amount'].values[0]})")
        
    # Unusual usage pattern
    mismatches = df[(df['plan'] == 'Basic') & ((df['bill_amount'] > 500) | (df['usage'] == 'high'))]
    for uid in mismatches['user_id']:
        if uid not in high_bills['user_id'].values:
            anomalies.append(f"User {uid} exhibits unusual usage pattern for Basic tier.")
         
    if len(anomalies) == 0:
         return {"count": 0, "report": "✔ No unusual anomalies detected."}
         
    report = f"⚠ {len(anomalies)} anomalies detected:\n"
    for anomaly in anomalies:
        report += f"- {anomaly}\n"
    
    return {"count": len(anomalies), "report": report}

def query_data(query: str, all_data: List[Dict[str, Any]]) -> str:
    if USE_MOCK:
        df = pd.DataFrame(all_data)
        if "highest revenue" in query.lower():
            best_plan = df.groupby("plan")["bill_amount"].sum().idxmax()
            return f"**Result:** The highest revenue generation stems from the **{best_plan} plan**."
        return "Local mock mode limits query generation. Connect your OpenAI API key for full natural language interaction."
        
    return qa_chain.run(query)
