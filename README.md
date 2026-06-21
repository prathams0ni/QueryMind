<div align="center">

<img src="https://img.shields.io/badge/QueryMind-AI%20SQL%20Engine-3b82f6?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PGNpcmNsZSBjeD0iMTIiIGN5PSI1IiByPSIyIiBmaWxsPSJ3aGl0ZSIvPjxjaXJjbGUgY3g9IjUiIGN5PSIxNyIgcj0iMiIgZmlsbD0id2hpdGUiLz48Y2lyY2xlIGN4PSIxOSIgY3k9IjE3IiByPSIyIiBmaWxsPSJ3aGl0ZSIvPjxjaXJjbGUgY3g9IjEyIiBjeT0iMTIiIHI9IjIuNSIgZmlsbD0id2hpdGUiLz48L3N2Zz4=" />

# QueryMind

### AI-Powered Natural Language → SQL Engine

**Upload your data. Ask anything. Get answers instantly.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Groq](https://img.shields.io/badge/Groq-LLaMA%203.3%2070B-F55036?style=flat-square)](https://groq.com)
[![SQLite](https://img.shields.io/badge/SQLite-In--Memory-003B57?style=flat-square&logo=sqlite&logoColor=white)](https://sqlite.org)
[![Render](https://img.shields.io/badge/Deploy-Render-46E3B7?style=flat-square&logo=render&logoColor=white)](https://render.com)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)](LICENSE)

[Live Demo](#) · [Report Bug](https://github.com/pratham-soni/QueryMind/issues) · [Request Feature](https://github.com/pratham-soni/QueryMind/issues)

</div>

---

## What is QueryMind?

QueryMind lets anyone — regardless of SQL knowledge — query their own data using plain English. Upload a CSV or Excel file, type a question like *"Show top 10 customers by revenue"*, and QueryMind generates and executes the SQL query, returning results with auto-visualizations.

No database setup. No SQL knowledge needed. No data leaves your session.

---

## Features

- **Natural Language → SQL** — Powered by LLaMA 3.3 70B via Groq API
- **Upload CSV / Excel** — Multiple tables per session, auto schema detection
- **Auto-retry on error** — Up to 4 self-correction attempts if SQL fails
- **Edit before running** — Tweak the generated SQL inline before executing
- **Smart visualizations** — Bar, Line, and Pie charts auto-generated from results
- **Export results** — Download query results as CSV instantly
- **3 free queries** — Default quota with upgrade path to unlimited via own API key
- **Futuristic dark UI** — Built with vanilla HTML/CSS/JS, no framework overhead
- **Admin dashboard** — Track usage, sessions, and query logs in real time
- **Render-ready** — One-click deploy with `render.yaml` included

---

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                        QueryMind Flow                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  User uploads CSV/Excel                                         │
│         │                                                       │
│         ▼                                                       │
│  pandas reads file → SQLite table (in session temp dir)        │
│         │                                                       │
│         ▼                                                       │
│  Schema extracted (table names, column types, sample rows)     │
│         │                                                       │
│         ▼                                                       │
│  User asks question in natural language                        │
│         │                                                       │
│         ▼                                                       │
│  Prompt built (schema + question) → Groq API (LLaMA 3.3 70B)  │
│         │                                                       │
│         ▼                                                       │
│  SQL generated → validated → executed on SQLite                │
│         │                                                       │
│         ├── Error? → Auto-correct prompt → retry (max 4x)      │
│         │                                                       │
│         ▼                                                       │
│  Results returned → Table + Chart + Export                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

> **Privacy:** Only schema structure and 3 sample rows are sent to Groq for SQL generation. Your actual data stays entirely on the server — never uploaded to any external service.

---

## Tech Stack

| Layer       | Technology                          |
|-------------|-------------------------------------|
| Backend     | Python · Flask 3.0                  |
| LLM         | Groq API · LLaMA 3.3 70B Versatile  |
| Database    | SQLite (per-session, in temp dir)   |
| Data        | pandas · openpyxl                   |
| Frontend    | Vanilla HTML · CSS · JavaScript     |
| Charts      | Chart.js 4.4                        |
| Fonts       | Inter · JetBrains Mono              |
| Deployment  | Render.com · Gunicorn               |

---

## Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/pratham-soni/QueryMind.git
cd QueryMind
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

```bash
cp .env.example .env
```

Edit `.env`:

```env
GROQ_API_KEY=gsk_your_key_here        # Get free at console.groq.com
SECRET_KEY=your_random_secret_here
ADMIN_PASSWORD=your_admin_password    # For /admin dashboard
```

### 4. Run

```bash
python app.py
```

Open `http://localhost:5000` in your browser.

---

## Getting a Free Groq API Key

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up — no credit card required
3. Click **API Keys** → **Create new key**
4. Copy the key and add it to `.env` or paste it in the app sidebar

**Free tier limits** (per API key):
| Limit | Value |
|-------|-------|
| Requests / minute | 30 |
| Tokens / minute | 12,000 |
| Requests / day | 1,000 |
| Tokens / day | 100,000 |

---

## Deploy to Render

### One-click deploy

1. Fork this repo to your GitHub
2. Go to [render.com](https://render.com) → **New Web Service**
3. Connect your GitHub repo — Render auto-detects `render.yaml`
4. Add environment variables in the Render dashboard:
   - `GROQ_API_KEY` — your Groq key
   - `ADMIN_PASSWORD` — choose a password for `/admin`
5. Click **Deploy** — live in ~2 minutes

### Manual deploy config

```yaml
# render.yaml (already included)
services:
  - type: web
    name: querymind
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
```

---

## Admin Dashboard

Access the admin panel at `/admin?key=YOUR_ADMIN_PASSWORD`

**What you can see:**
- Total sessions and new sessions today
- Total queries and queries today
- How many users brought their own API key
- Per-session breakdown: IP, query count, tables uploaded, last active
- Full query log: question, generated SQL, success/fail, key type

---

## Project Structure

```
QueryMind/
├── app.py              # Flask app — all API routes
├── db.py               # SQLite session management
├── llm.py              # Groq API client
├── prompt_builder.py   # SQL prompt templates + schema truncation
├── executor.py         # Retry loop + SQL cleaning
├── analytics.py        # Session & query tracking
├── requirements.txt    # Python dependencies
├── render.yaml         # Render deployment config
├── .env.example        # Environment variable template
├── .gitignore
└── templates/
    ├── index.html      # Full SPA frontend
    └── admin.html      # Admin dashboard
```

---

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/` | Serve the main app |
| `GET`  | `/api/config` | Backend key status + free limit |
| `POST` | `/api/upload` | Upload CSV/Excel file |
| `GET`  | `/api/tables` | List tables + schema |
| `POST` | `/api/query` | Generate + execute SQL |
| `POST` | `/api/export` | Download results as CSV |
| `POST` | `/api/delete_table` | Remove a table |
| `POST` | `/api/clear` | Clear session data |
| `GET`  | `/admin?key=` | Admin dashboard |

---

## Contributing

Pull requests are welcome. For major changes, please open an issue first.

1. Fork the repo
2. Create a branch: `git checkout -b feature/your-feature`
3. Commit: `git commit -m "Add your feature"`
4. Push: `git push origin feature/your-feature`
5. Open a pull request

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

<div align="center">

Built with ⚡ by **[Pratham Soni](https://github.com/pratham-soni)**

*QueryMind — Open Source · 2025*

</div>
