from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import Optional
import shutil
import data_processing
import ai_logic

app = FastAPI(title="AI Billing Intelligence API")

class UserRequest(BaseModel):
    user_id: int
    
class QueryRequest(BaseModel):
    query: str

@app.post("/explain_bill")
def explain_bill(req: UserRequest):
    user_data = data_processing.get_user_data(req.user_id)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    explanation = ai_logic.explain_bill(user_data)
    return {"explanation": explanation}

@app.post("/recommend_plan")
def recommend_plan(req: UserRequest):
    user_data = data_processing.get_user_data(req.user_id)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    recommendation = ai_logic.recommend_plan(user_data)
    return {"recommendation": recommendation}

@app.get("/detect_anomaly")
def detect_anomaly():
    all_data = data_processing.get_all_data()
    report = ai_logic.detect_anomaly(all_data)
    return report

@app.post("/query_data")
def query_data(req: QueryRequest):
    all_data = data_processing.get_all_data()
    answer = ai_logic.query_data(req.query, all_data)
    return {"answer": answer}

@app.post("/upload_data")
async def upload_data(file: UploadFile = File(...)):
    with open("billing_data.csv", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # Reinitialize the RAG system to use the new data
    ai_logic.reindex_data()
    return {"message": "File uploaded and indexed successfully"}

@app.get("/analytics")
def get_analytics():
    return data_processing.get_analytics()
