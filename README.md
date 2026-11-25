# Learnova — AI-Powered Gamified Learning Platform

> **Learn AI by Building AI.** Master Python, Machine Learning, Data Science, Deep Learning, and Generative AI through interactive lessons, real-world projects, AI-powered mentorship, and game-based learning.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Node.js 22+
- Docker (optional, for sandbox mode and full compose setup)

### 1. Backend Setup

```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS/Linux  
source .venv/bin/activate

pip install -r requirements.txt
```

**Configure environment:**
```bash
# Copy and edit environment file
cp ../.env.example ../.env
# Edit .env — set DATABASE_URL, AI_API_KEY (optional), etc.
```

**Run the backend (SQLite for quick dev — no Postgres needed):**
```bash
uvicorn app.main:app --reload
# API docs at http://localhost:8000/api/docs
```

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
# App at http://localhost:5173
```

### 3. Full Stack with Docker Compose

```bash
# From project root
docker compose up --build
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
```

---

## 🏗️ Architecture

```
LearNova/
├── backend/                 # Python 3.12 + FastAPI
│   ├── app/
│   │   ├── main.py         # FastAPI app + lifespan
│   │   ├── api/v1/         # All REST endpoints
│   │   ├── core/           # Config, security, logging
│   │   ├── db/             # Session, seed data
│   │   ├── models/         # SQLAlchemy 2.0 models
│   │   ├── services/       # Gamification, sandbox, mentor, rate limiting
│   │   └── workers/        # Celery tasks
│   ├── alembic/            # Database migrations
│   ├── tests/              # pytest test suite
│   └── requirements.txt
├── frontend/               # React 18 + TypeScript + Vite
│   ├── src/
│   │   ├── pages/          # All app pages
│   │   ├── components/     # Reusable UI components
│   │   ├── store/          # Zustand state (auth, ui)
│   │   ├── lib/            # API client, utilities
│   │   └── router.tsx      # React Router config
│   └── package.json
├── sandbox/
│   ├── Dockerfile.sandbox  # Hardened Python execution environment
│   └── runner.py           # Security-validated code runner
├── docker-compose.yml
└── .env.example
```

---

## 🎮 Features

### Learning Engine
- **6 Learning Paths**: Python Foundations → Data Science → Machine Learning → Deep Learning → Generative AI → AI Engineering
- **Interactive Lessons** with text, code blocks, callouts, and embedded quizzes
- **8 Quiz Types**: Multiple choice, true/false, predict output, fill-in-blank, debug, code completion
- **Progress Tracking** with backend-verified lesson completion

### Gamification (fully server-backed)
- **XP Ledger** — idempotency-keyed transactions prevent duplicate awards
- **10-Level System** — AI Explorer → AI Mastermind with level-up animations
- **Timezone-Aware Streaks** — streak freezes, 6 milestone bonuses (3/7/14/30/60/100 days)
- **12 Achievements** — criteria-based, automatically evaluated after each activity
- **Daily & Weekly Quests** — auto-generated, progress-tracked, claimable rewards
- **3 Leaderboards** — Global, Weekly, Monthly with privacy controls

### Python Playground
- Monaco Editor with Python syntax highlighting
- 5 learning modes: Write & Run, Complete Code, Debug, Predict Output, Challenge
- **Isolated sandbox execution** — Docker container or hardened subprocess, never `eval()` in FastAPI
- Security: blocked modules (os, subprocess, socket, etc.), stripped env, 5s timeout

### Socratic AI Mentor
- Configurable OpenAI-compatible provider (GPT-4o, Claude, etc.)
- 7 teaching modes: Hint, Beginner, Deep Technical, Debug, Test Me, Interview, Example
- **Transparent local fallback** when no API key — clearly labeled, still educational
- Persistent conversation history, rate limiting

### Real-World Projects
- Customer Churn Prediction (Pandas + XGBoost)
- Enterprise RAG Assistant (LangChain + ChromaDB)
- Backend-verified evaluation with keyword/criteria checks

---

## Phase Completion Snapshot

The project has working foundations and backend coverage, but the original nine phases are **not all complete**. Current known gaps:

| Phase | Status | Remaining work |
|---|---|---|
| 1. Project Foundation | Core scaffold and production Alembic startup present | Verify the full Docker Compose stack in a Docker-enabled environment. |
| 2. Auth, Onboarding & Dashboard | Registration, login, reset, onboarding, dashboard, and profile screens present | Add end-to-end coverage and refine validation/error states across auth and settings. |
| 3. Learning Engine | Backend paths, lessons, quizzes, and learner screens present | Complete support for all eight quiz question types and validate the depth/coverage of content across all six paths. |
| 4. Gamification | Backend XP, streaks, quests, achievements, and leaderboards present | Finish learner-facing notification/reward UX and test privacy controls and claim flows end to end. |
| 5. AI Mentor | Provider fallback, persistent messages, and conversation UI present | Streaming responses and complete provider-failure/usage observability are not implemented. |
| 6. Playground & Visualization Lab | Monaco editor and sandbox execution present | The five guided modes and eight Math/ML visualizations are not implemented in the UI. |
| 7. Real-World Project Lab | Project catalog, detail view, and backend evaluation present | Complete the four specialized project experiences, datasets, milestones, and retrieval pipeline. |
| 8. Admin & Analytics | Basic admin metrics/users APIs and learner stats present | Content CRUD, AI usage/submission management, richer analytics charts, and full admin screens remain. |
| 9. Hardening, Testing & Docs | README, environment template, pytest, and Vitest present | Add Playwright E2E coverage and deployment/CI validation; review production security and operational settings before release. |

This snapshot is a scope checklist, not a production-readiness guarantee.

---

## 🔧 Configuration

| Variable | Description | Default |
|---|---|---|
| `DATABASE_URL` | PostgreSQL or SQLite | SQLite (dev) |
| `AI_API_KEY` | OpenAI-compatible key | Empty (uses local fallback) |
| `AI_BASE_URL` | API base URL | OpenAI |
| `AI_MODEL` | Model name | gpt-4o-mini |
| `SANDBOX_MODE` | `docker` or `subprocess` | subprocess |
| `SECRET_KEY` | JWT signing secret | Dev default |

---

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest tests/ -v

# Frontend type check + tests
cd frontend
npm run build
```

---

## 🔐 Security

- **Argon2** password hashing
- **HTTP-only cookie** JWTs with CSRF protection
- **Role-based access control** enforced server-side
- **Sandboxed code execution** — never runs user code in main process
- **Input validation** via Pydantic + SQLAlchemy parameterized queries
- **Rate limiting** with Redis-backed sliding window

---

## 📄 License

MIT — Build something amazing!
