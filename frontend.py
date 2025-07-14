import streamlit as st
import requests
import time

API_URL = st.sidebar.text_input("API URL", "http://localhost:8000/api/synonyms")
cache_backend = st.sidebar.selectbox("Cache Backend", ["inmemory", "redis"])
ttl = st.sidebar.number_input("Cache TTL (seconds)", min_value=1, value=600)

st.title("Synonym Table Viewer")

if st.sidebar.button("Update Config"):
    resp = requests.post(
        API_URL.replace("/synonyms", "/update"),
        json={"cache_backend": cache_backend, "ttl": ttl}
    )
    status_ = st.sidebar.success(resp.json().get("status"))
    info_box = st.sidebar.info("Server restarting... Please wait 10 seconds.")
    time.sleep(10)
    status_.empty()
    info_box.empty()
    try:
        resp = requests.get(API_URL, params={"ttl": ttl, "cache_backend": cache_backend})
        data = resp.json()
        st.write(f"Cache Hit: {data.get('from_cache')}")
        st.table(data.get("items"))
    except Exception as e:
        st.error(f"Error fetching data: {e}")
if st.sidebar.button("getData"):
    params = {"ttl": ttl, "cache_backend": cache_backend}
    try:
        resp = requests.get(API_URL, params=params)
        data = resp.json()
        st.write(f"Cache Hit: {data.get('from_cache')}")
        st.table(data.get("items"))
    except Exception as e:
        st.error(f"Error fetching data: {e}")