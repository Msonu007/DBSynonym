FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y redis-server && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt streamlit


COPY . .

EXPOSE 8000 8501 6379


CMD bash -c "redis-server --daemonize yes && uvicorn main:app --host 0.0.0.0 --port 8000 & streamlit run frontend.py --server.port 8501"
