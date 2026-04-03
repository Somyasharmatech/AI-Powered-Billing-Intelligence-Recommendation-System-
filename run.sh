#!/bin/bash
echo "==========================================="
echo "Starting AI Billing Intelligence System..."
echo "==========================================="

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Starting FastAPI Backend..."
uvicorn api:app --reload &
BACKEND_PID=$!

echo "Starting Streamlit Frontend..."
streamlit run app.py &
FRONTEND_PID=$!

echo "==========================================="
echo "System is running!"
echo "Backend:  http://127.0.0.1:8000"
echo "Frontend: http://localhost:8501"
echo "==========================================="

# Wait for both processes
wait $BACKEND_PID
wait $FRONTEND_PID
