@echo off
echo ===========================================
echo Starting AI Billing Intelligence System...
echo ===========================================

echo Installing dependencies...
pip install -r requirements.txt

echo Starting FastAPI Backend...
start cmd /k "uvicorn api:app --reload"

echo Starting Streamlit Frontend...
start cmd /k "streamlit run app.py"

echo ===========================================
echo System is running!
echo Backend:  http://127.0.0.1:8000
echo Frontend: http://localhost:8501
echo ===========================================
pause
