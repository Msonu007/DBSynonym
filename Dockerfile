FROM python:3.11-slim

WORKDIR /app

# Install system dependencies and Redis
RUN apt-get update && \
    apt-get install -y redis-server && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt streamlit

# Copy app code
COPY . .

EXPOSE 8000 8501 6379

# Start Redis, FastAPI, and Streamlit
CMD bash -c "redis-server --daemonize yes && uvicorn main:app --host 0.0.0.0 --port 8000 & streamlit run streamlit_app.py --server.port 8501"