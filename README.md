# Fulfill — Order Fulfillment Control Center

This project turns the multithreaded priority scheduler into a small full-stack order fulfillment operations dashboard. It models the background work behind an online store: payment verification, inventory reservation, pick & pack, fraud review, shipping labels, and carrier booking.

The Python backend exposes a REST API and runs real worker threads. The React dashboard polls live queue, worker, resource, and activity data; operators can create work items and inspect task priority and status.

> This is a local development/demo application. Tasks and metrics are held in memory and reset when the API process restarts. A production deployment should add durable storage, authentication, observability, and a persistent message broker.

## Stack

- **Backend:** Python 3.10+, FastAPI, Uvicorn, threaded in-memory priority scheduler.
- **Frontend:** React, Vite, Lucide icons.
- **Scenario:** online store order fulfillment with priority- and resource-aware task dispatch.

## Start the application

Open two terminals from the project root.

### 1. Start the API

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000
```

The API documentation is available at `http://localhost:8000/docs`.

### 2. Start the React dashboard

```powershell
cd frontend
npm install
npm run dev
```

Open the Vite URL shown in the terminal (normally `http://localhost:5173`). The dashboard refreshes automatically every 2.5 seconds. The backend starts with sample fulfillment tasks; use **Create task** to add more or **Load demo orders** to add another sample batch.

## API endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/api/health` | API health check |
| `GET` | `/api/dashboard` | Live metrics, priority totals, and recent activity |
| `GET` | `/api/tasks` | List tasks; optionally filter with `?status=QUEUED`, `RUNNING`, or `COMPLETED` |
| `POST` | `/api/tasks` | Validate and queue a fulfillment task |
| `POST` | `/api/demo/seed` | Add a sample batch of fulfillment tasks |

Task input validates order ID, task type, priority, weight, required resource units, and estimated execution duration. The queue accepts up to 100 waiting tasks and returns HTTP 429 when full.

## Scheduling behavior

- Three worker threads execute jobs concurrently.
- `HIGH` priority is dispatched before `MEDIUM`, then `LOW`; weight breaks ties within a priority.
- Tasks waiting for 15 seconds are promoted to the next priority level to reduce starvation.
- Workers select a task that fits currently available resource units, avoiding resource-related head-of-line blocking.
- The API reports current resource utilization, average wait and execution times, and a recent activity feed.

## Legacy terminal simulation

The original standalone producer/consumer demo is still available from the project root:

```powershell
python main.py
```

It uses settings in `configuration.py` and prints a final run summary.

## Project layout

- `backend/main.py` — FastAPI app, request validation, and API routes.
- `backend/scheduler_service.py` — thread-safe in-memory task store, priority aging, resources, workers, and metrics.
- `frontend/src/App.jsx` — React dashboard and task creation flow.
- `frontend/src/styles.css` — responsive dashboard styling.
- `frontend/src/main.jsx` — React entry point.
- `configuration.py`, `producer.py`, `scheduler.py`, `worker.py`, and related root modules — original standalone simulation.
