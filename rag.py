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
        extra_charge = "Extra charge applied" if user_data["usage"] == "high" else "No extra charges"
        return f"User is on {user_data['plan']} plan.\nUsed {user_data['data_used']} data.\n{extra_charge}.\nTotal bill: {user_data['bill_amount']}"
    
    prompt = f"Explain the bill for User ID {user_data['user_id']}. They are on the {user_data['plan']} plan, have {user_data['usage']} usage with {user_data['data_used']} data, and their bill is {user_data['bill_amount']}."
    return qa_chain.run(prompt)

def recommend_plan(user_data: Dict[str, Any]) -> str:
    if USE_MOCK:
        if user_data["usage"] == "high":
            return f"Given the high usage of {user_data['data_used']}, we suggest upgrading to the Premium Plan."
        elif user_data["usage"] == "low":
            return f"Given the low usage of {user_data['data_used']}, the Basic Plan is perfect."
        else:
            return f"The current {user_data['plan']} Plan seems to fit the required usage well."
    
    prompt = f"Based on this user's data (Plan: {user_data['plan']}, Usage: {user_data['usage']}, Data: {user_data['data_used']}), what is the best plan for them going forward and why?"
    return qa_chain.run(prompt)

def detect_anomaly(all_data: List[Dict[str, Any]]) -> str:
    df = pd.DataFrame(all_data)
    anomalies = []
    
    dup_count = df.duplicated(subset=['user_id']).sum()
    if dup_count > 0:
        anomalies.append(f"Found {dup_count} duplicate user entries.")
        
    high_bills = df[df['bill_amount'] > 1000]
    if not high_bills.empty:
        anomalies.append(f"Found suspiciously high bills for user IDs: {', '.join(high_bills['user_id'].astype(str).tolist())}.")
        
    mismatches = df[(df['plan'] == 'Basic') & (df['bill_amount'] > 500)]
    if not mismatches.empty:
         anomalies.append(f"Found Basic plan users with unusually high bills indicating excess usage: Users {', '.join(mismatches['user_id'].astype(str).tolist())}.")
         
    if not anomalies:
         return "No obvious anomalies detected in the current billing data."
         
    if USE_MOCK:
         return "\n".join(anomalies)
         
    prompt = f"Analyze the following anomalies detected in the billing data and provide a concise professional report:\n{chr(10).join(anomalies)}"
    return qa_chain.run(prompt) if hasattr(qa_chain, 'run') else llm.invoke(prompt).content

def query_data(query: str, all_data: List[Dict[str, Any]]) -> str:
    if USE_MOCK:
        df = pd.DataFrame(all_data)
        if "highest revenue" in query.lower():
            revenue_by_plan = df.groupby("plan")["bill_amount"].sum()
            best_plan = revenue_by_plan.idxmax()
            return f"The plan that generates the highest revenue is the {best_plan} plan."
        return "I am a mock bot. I can only answer simple queries like 'Which plan generates highest revenue?' right now."
        
    return qa_chain.run(query)
