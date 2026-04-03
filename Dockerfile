FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose ports (FastAPI and Streamlit)
EXPOSE 8000 8501

CMD ["python", "run_prod.py"]
