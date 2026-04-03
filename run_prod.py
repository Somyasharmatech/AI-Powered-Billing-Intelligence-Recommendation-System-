import subprocess
import time
import os
import sys

if __name__ == "__main__":
    print("Starting production server...")
    
    # Start FastAPI backend on internal port 8000
    backend = subprocess.Popen([sys.executable, "-m", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"])
    
    # Wait a few seconds for the backend to initialize
    time.sleep(3)
    
    # Set default API_URL so the frontend connects locally, regardless of Where it runs!
    os.environ["API_URL"] = "http://127.0.0.1:8000"
    
    # Start Streamlit frontend on the Port provided by the Cloud Provider (or 8501 locally)
    port = os.environ.get("PORT", "8501")
    frontend = subprocess.Popen([sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", port, "--server.address", "0.0.0.0"])
    
    try:
        backend.wait()
        frontend.wait()
    except KeyboardInterrupt:
        backend.terminate()
        frontend.terminate()
        sys.exit(0)
