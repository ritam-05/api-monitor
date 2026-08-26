# API Monitor 🚀

A production-ready, full-stack API monitoring dashboard for registering API endpoints and tracking their **health, uptime, response times, and status codes** over time.

---

## 🌟 Features

* **Dashboard**

  * Overview of active endpoints
  * Total uptime
  * Healthy vs. unhealthy APIs

* **Endpoint Management**

  * Create monitored endpoints
  * Edit endpoint configurations
  * Delete endpoints

* **Monitoring Engine**

  * Asynchronous HTTP health checks
  * Response-time measurement
  * HTTP status-code tracking
  * Concurrent monitoring using `asyncio` and `httpx`

* **Analytics**

  * Uptime calculation
  * Response-time analytics
  * Historical monitoring data

* **Serverless Ready**

  * Designed for Vercel's serverless architecture
  * Automated monitoring through Vercel Cron

---

## 🛠️ Tech Stack

| Layer       | Technology                               |
| ----------- | ---------------------------------------- |
| Frontend    | Next.js, React, TypeScript               |
| Styling     | Tailwind CSS                             |
| Charts      | Recharts                                 |
| Backend     | Python, FastAPI                          |
| Validation  | Pydantic                                 |
| HTTP Client | HTTPX                                    |
| ORM         | SQLAlchemy                               |
| Database    | SQLite (Local) → PostgreSQL (Production) |
| Deployment  | Vercel                                   |
| Scheduling  | Vercel Cron                              |

---

## 📐 Architecture & Serverless Strategy

Traditional monitoring applications often use a continuously running background process:

```python
while True:
    check_endpoints()
    sleep(60)
```

This approach is not suitable for serverless platforms such as Vercel because serverless functions can **spin down when idle**.

### Serverless Solution

API Monitor uses a scheduled, event-driven architecture:

```text
┌─────────────────┐
│   Vercel Cron   │
│   Every 5 min   │
└────────┬────────┘
         │
         ▼
┌──────────────────────────┐
│ GET /api/engine/run-checks│
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│     FastAPI Backend      │
│                          │
│  asyncio + httpx         │
│  Concurrent API Checks   │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│        Database          │
│                          │
│ Status • Response Time   │
│ Uptime • Timestamps      │
└──────────────────────────┘
```

Every **5 minutes**, Vercel Cron triggers:

```text
GET /api/engine/run-checks
```

The FastAPI backend then:

1. Fetches all active endpoints.
2. Sends concurrent HTTP requests using `asyncio` and `httpx`.
3. Measures response times.
4. Records HTTP status codes and health status.
5. Saves monitoring results to the database.
6. Terminates after completing the checks.

This provides periodic monitoring without requiring a permanently running server.

---

# 💻 Local Setup

## 1. Clone the Repository

```bash
git clone https://github.com/your-username/api-monitor.git
cd api-monitor
```

---

## 2. Frontend Setup

Install the frontend dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Frontend:

```text
http://localhost:3000
```

---

## 3. Backend Setup

Create a Python virtual environment:

```bash
python -m venv .venv
```

### Windows — PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

### macOS / Linux

```bash
source .venv/bin/activate
```

Install backend dependencies:

```bash
pip install -r api/requirements.txt
```

Start the FastAPI development server:

```bash
uvicorn api.main:app --reload --port 8000
```

Backend:

```text
http://localhost:8000
```

Interactive API documentation:

```text
http://localhost:8000/api/docs
```

---

# 🔐 Environment Variables

Create a `.env.local` file in the root directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

---

# 📊 Monitoring Flow

The monitoring process follows this flow:

```text
Active API Endpoints
        │
        ▼
Vercel Cron Trigger
        │
        ▼
FastAPI Monitoring Endpoint
        │
        ▼
Concurrent HTTP Requests
        │
        ├── Response Status
        ├── Response Time
        └── Health Status
        │
        ▼
Database
        │
        ▼
Dashboard & Analytics
```

---

# 🚀 Future Improvements

* [ ] Add email alerting when an endpoint goes down
* [ ] Add Slack alerting
* [ ] Support custom HTTP headers for authenticated endpoints
* [ ] Add user authentication with NextAuth or Auth0
* [ ] Add configurable monitoring intervals
* [ ] Add incident history
* [ ] Add endpoint response-body validation
* [ ] Add detailed uptime reports

---

# 📦 GitHub Setup

## Step 1 — Create a GitHub Repository

1. Go to [GitHub](https://github.com/) and log in.
2. Click the **+** icon in the top-right corner.
3. Select **New repository**.
4. Name the repository:

```text
api-monitor
```

5. Set the repository visibility to **Public**.
6. Leave the following options unchecked:

   * Add a README file
   * Add `.gitignore`
   * Add a license
7. Click **Create repository**.

The repository should be completely empty because the project already exists locally.

---

# 🔗 Step 2 — Connect the Local Repository

Open PowerShell at the root of the project.

Add the GitHub remote:

```powershell
git remote add origin https://github.com/YourUsername/api-monitor.git
```

Replace `YourUsername` with your actual GitHub username.

---

# 🌿 Step 3 — Set the Main Branch

```powershell
git branch -M main
```

---

# 💾 Step 4 — Commit the README

```powershell
git add README.md
git commit -m "docs: add professional README for portfolio"
```

---

# 🚀 Step 5 — Push to GitHub

```powershell
git push -u origin main
```

Your project should now be available on GitHub.

---

## 📁 Project Structure

A typical project structure looks like:

```text
api-monitor/
│
├── api/
│   ├── main.py
│   ├── requirements.txt
│   └── ...
│
├── app/
│   └── ...
│
├── public/
│   └── ...
│
├── .env.local
├── package.json
├── README.md
└── ...
```

---

## 🎯 Project Goal

API Monitor demonstrates how to build a **production-oriented monitoring system** using a modern full-stack architecture while handling the constraints of **serverless infrastructure, asynchronous networking, database persistence, and scheduled background jobs**.
