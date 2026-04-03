# 🧾 AI-Powered Billing Intelligence & Recommendation System

An intelligent full-stack application designed to automate bill explanations, detect billing anomalies, and recommend customized plans using a powerful combination of Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG).

![Project Theme: Black & Red](https://img.shields.io/badge/Theme-Black%20%26%20Red-red) ![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688) ![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B) ![LangChain](https://img.shields.io/badge/AI-LangChain-blue)

---

## 🔥 Key Features
* **Strict Analytical AI Framework:** Every query rigorously outputs a 4-step logic framework (1. Explanation, 2. Reason, 3. Recommendation, 4. Business Insight) assessing precisely why bills are charged and establishing immediate actionable business impact.
* **Top Insights Dashboard:** Upload customized `.csv` databases dynamically and instantly view absolute total aggregations, anomaly hit-rates, and interactive Plotly-powered charts detailing Revenue and Usage distribution.
* **Smart Anomaly Detection:** Scans your entire database intelligently for identically duplicated bill paths, excessively high bills transcending thresholds, or raw usage mismatches resulting from hidden system errors, alerting administrators directly via dashboard diagnostic warning banners.
* **Session Memory Logs:** Deep integration with `st.session_state` logs exactly every action undertaken globally (Data queries, Database changes, Plan optimizations) into the navigation sidebar actively for administrators.
* **Natural Language Data Querying:** Ask your database human queries like *"Which plan generates the highest revenue?"* and get immediate computational answers.

---

## 🏗 System Architecture
* **Frontend:** Streamlit (*Premium Black & Red Dynamic UI*)
* **Backend:** FastAPI (*Interactive automatic endpoint documentation*)
* **AI reasoning layer:** OpenAI `gpt-3.5-turbo` & LangChain
* **Vector Store / Embeddings:** FAISS local chunking + OpenAI Embeddings
* **Packaging:** Pre-configured Docker & Docker Compose setup

---

## 🚀 How to Run Locally

### Prerequisites
1. Python 3.11+
2. An OpenAI API Key (Obtain from [platform.openai.com](https://platform.openai.com/api-keys)).

### Option 1: 1-Click Launch (Windows/Mac)
1. Clone this repository to your local machine.
2. Create a `.env` file in the root directory and add your key:
   ```env
   OPENAI_API_KEY=sk-your-openai-api-key
   ```
3. Run the automated script! 
   * **Windows:** Simply double-click `run.bat`
   * **Linux/Mac:** Run `bash run.sh`
   
*Note: This command automatically installs dependencies, boots the FastAPI server on port `8000`, and opens the Streamlit frontend UI on port `8501` automatically.*

### Option 2: Docker Compose
If you have Docker installed, you can spin up the entire isolated ecosystem with one command:
```bash
docker-compose up -d
```

---

## ☁️ How to Deploy to the Cloud (Render.com)

The project is fully ready for a 1-click cloud deployment.

1. Fork or push this repository to your own GitHub account.
2. Sign up on [Render.com](https://render.com) and create a **New Web Service**.
3. Connect your GitHub repository.
4. **Configuration Details:**
   * **Build Command:** `pip install -r requirements.txt`
   * **Start Command:** `python run_prod.py`
5. **Environment Variables:** Add the single requirement:
   * Key: `OPENAI_API_KEY`
   * Value: `sk-your-openai-key-here`
   *(Note: The internal `API_URL` routing is handled 100% automatically by the `run_prod.py` script!)*
6. Click **Deploy**. Render will automatically detect the Dockerfile, execute the production script, and give you a live HTTPS public Web Address!

---

## 📖 User Guide: How to Use the Application

Once you have the application open in your browser, here is how to navigate and utilize the features:

### 1. Uploading Custom Data
By default, the app uses dummy billing data. To use your own real data:
* Look at the left sidebar under **📁 Data Management**.
* Click **"Upload billing_data.csv"** and select a `.csv` file from your computer. (Ensure it has columns like `user_id, plan, usage, data_used, bill_amount`).
* Click **"Process & Re-index"**. The system will upload your file, securely save it, and automatically retrain the AI's logic on your brand new dataset!

### 2. Billing Explanation Tab
* Enter a `User ID` matching a row in your CSV database.
* Click **"Explain Bill"**.
* **Output:** A natural language summary written by the AI explaining what plan the user is on, how much data they used, if extra charges were applied, and why the final bill is the amount it is.

### 3. Plan Recommendation Tab
* Enter a `User ID`.
* Click **"Get Recommendation"**.
* **Output:** The AI analyzes the user's data consumption habits and makes an active business recommendation (e.g., suggesting a downgrade to standard if usage is extremely low, or an upgrade to premium to prevent overage charges).

### 4. Anomaly Detection Tab (Raw Logs)
* Click **"Run Diagnostics"**.
* **Output:** The AI scans the *entire* dataset simultaneously. It flags duplicate items, mismatched plans, and suspicious financial anomalies. Below its explanation, the raw flagged Pandas DataFrame is presented cleanly so administrators can view the exact problematic rows.

### 5. Data Query Tab
* Type a natural language question (e.g., *"Which plan generates the highest revenue?"*).
* Click **"Search"**.
* **Output:** A concise, chat-style correct response calculated directly from your billing data logic utilizing Python data analysis algorithms underneath.

### 6. Analytics Dashboard Tab
* No inputs required!
* **Output:** Visual, interactive charts built with `plotly`. Hover over the slices on the **Revenue** pie chart to see precise percentages, or review the **Usage Trends** bar chart to see how data consumption falls within your customer base.

---

## 📚 API Documentation 
When your backend server is running (locally or in the cloud), FastAPI automatically generates an interactive swagger interface so you can test endpoints programmatically.  

Simply navigate to: `http://localhost:8000/docs` (or your live cloud URL + `/docs`) to interact with:
* `POST /explain_bill`
* `POST /recommend_plan`
* `GET  /detect_anomaly`
* `POST /query_data`
* `POST /upload_data`
* `GET  /analytics`
