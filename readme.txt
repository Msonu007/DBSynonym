 Here is an updated `README.md` reflecting your current design, API endpoints, and deployment details.

---

# DataEngineSynonymSystem

A FastAPI backend and Streamlit frontend for managing and viewing synonym tables, with flexible caching (in-memory or Redis) and Dockerized deployment.

## Features

- **FastAPI** backend serving synonym data from a SQL database.
- **Streamlit** frontend for interactive config and data viewing.
- **Configurable cache**: switch between in-memory and Redis for performance.
- **Dockerized**: runs Redis, FastAPI, and Streamlit in one container.
- **Async**: uses async SQLAlchemy and cache for scalability.

## Design Decisions

- **Cache Abstraction**: The cache layer uses an abstract base class, allowing easy switching between in-memory and Redis backends.
- **Config Reload**: Changing cache settings via the frontend updates `.env` and triggers a server restart for immediate effect.
- **Async Database Access**: SQLModel and SQLAlchemy async engine ensure non-blocking DB operations.
- **Frontend/Backend Separation**: Streamlit interacts with FastAPI via HTTP, keeping UI and API loosely coupled.
- **Docker Integration**: All services (Redis, API, frontend) run together for simple deployment and local development.

## API Endpoints

All endpoints are prefixed with `/api`.

### `GET /api/synonyms`

Returns the full synonym table.

**Response:**
```json
{
  "from_cache": true,
  "items": [
    {
      "word_id": 1,
      "word": "happy",
      "synonyms_json": "[\"joyful\", \"cheerful\"]"
    }
  ]
}
```

### `POST /api/update`

Updates cache configuration and restarts the server.

**Request JSON:**
```json
{
  "cache_backend": "redis",
  "ttl": 600,
  "redis_url": "redis://localhost:6379/0"
}
```

**Response:**
```json
{
  "status": "updated, restarting..."
}
```

## Usage

1. **Build and run with Docker:**
   ```sh
   docker build -t synonym-system .
   docker run -p 8000:8000 -p 8501:8501 -p 6379:6379 synonym-system
   ```

2. **Access the frontend:**
   Open [http://localhost:8501](http://localhost:8501) in your browser.

3. **API direct access:**
   Use [http://localhost:8000/docs](http://localhost:8000/docs) for interactive API docs.

## Configuration

- `.env` file controls cache backend, TTL, and Redis URL.
- Update config via the Streamlit sidebar; server restarts automatically.

## Requirements

- Python 3.11+
- Docker (for containerized setup)

## License

MIT

---