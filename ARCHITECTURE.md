# FabPulse — Technical Architecture
# Version 1.0

---

## System Overview

FabPulse is a cloud-native, multi-tenant SaaS platform with offline-resilient edge nodes. It consists of three main layers:

1. **Cloud Core** — FastAPI backend + PostgreSQL (Supabase) + Google Cloud services
2. **Manager Dashboard** — React web app for supervisors and plant managers
3. **Kiosk PWA** — React Progressive Web App running on workstation tablets

```
┌─────────────────────────────────────────────────────────────┐
│                        INTERNET                             │
└──────────┬──────────────────────────┬───────────────────────┘
           │                          │
┌──────────▼──────────┐   ┌───────────▼──────────────────────┐
│   Manager Dashboard │   │         Kiosk PWA                │
│   (React + Vite)    │   │   (React + Vite + PWA)           │
│   fabpulse.io/app   │   │   fabpulse.io/kiosk              │
│                     │   │                                  │
│ - Live job board    │   │  Online Mode:                    │
│ - LEI analytics     │   │    → POST tasks directly to API  │
│ - SEC Simulator     │   │                                  │
│ - Reports           │   │  Offline Mode:                   │
│ - Admin panel       │   │    → Queue tasks in IndexedDB    │
└──────────┬──────────┘   │    → Background Sync on reconnect│
           │              └───────────┬──────────────────────┘
           │ HTTPS / WS               │ HTTPS
┌──────────▼──────────────────────────▼──────────────────────┐
│                    CLOUD CORE                               │
│                                                             │
│  FastAPI (Python)          deployed on Google Cloud Run     │
│  ├── /auth        → Supabase Auth (JWT)                     │
│  ├── /plants      → Multi-tenant plant management           │
│  ├── /jobs        → Job lifecycle CRUD                      │
│  ├── /tasks       → Task logging (start/stop)               │
│  ├── /workers     → Worker management + attendance          │
│  ├── /analytics   → LEI, yield, lead time calculations      │
│  ├── /simulator   → SEC Monte Carlo (calls Vertex AI)       │
│  └── /reports     → PDF generation                          │
│                                                             │
│  Supabase                                                   │
│  ├── PostgreSQL   → Primary database (multi-tenant)         │
│  ├── Realtime     → WebSocket subscriptions for dashboard   │
│  └── Auth         → JWT + Row Level Security                │
│                                                             │
│  Google Cloud                                               │
│  ├── Cloud Run    → FastAPI backend container               │
│  ├── Vertex AI    → Gemini API (SEC Simulator + Reports)    │
│  ├── Firebase     → Offline sync queue (IndexedDB bridge)   │
│  └── BigQuery     → Long-term analytics warehouse           │
└─────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

### Backend
| Layer | Technology | Reason |
|---|---|---|
| Runtime | Python 3.12 | Fast iteration, great AI library support |
| Framework | FastAPI | Async, auto-docs, production-grade |
| Database | PostgreSQL via Supabase | Multi-tenant, Row Level Security, Realtime built-in |
| Auth | Supabase Auth | JWT, social login, RLS integration |
| Container | Docker | Consistent deploys |
| Hosting | Google Cloud Run | Serverless, scales to zero, GCP requirement |
| ORM | SQLAlchemy + Alembic | Migrations, type safety |
| Task Queue | Cloud Tasks (GCP) | Async report generation |

### Frontend — Manager Dashboard
| Layer | Technology | Reason |
|---|---|---|
| Framework | React 18 + Vite | Fast builds, great DX |
| Language | TypeScript | Type safety across components |
| Styling | Tailwind CSS | Utility-first, matches brand system |
| State | Zustand | Lightweight global state |
| Data fetching | TanStack Query | Caching, realtime sync |
| Charts | Recharts | Lightweight, customizable |
| Realtime | Supabase Realtime | WebSocket subscriptions |
| PDF | React-PDF / Puppeteer | Report generation |

### Frontend — Kiosk PWA
| Layer | Technology | Reason |
|---|---|---|
| Framework | React 18 + Vite | Shared codebase with dashboard |
| PWA | Vite PWA Plugin + Workbox | Service worker, offline caching |
| Offline storage | IndexedDB (idb library) | Task queue when network is down |
| Sync | Background Sync API | Auto-flush queue on reconnect |
| Kiosk lock | Fullscreen API + custom CSS | Prevent accidental navigation |

### Google Cloud Services (Required)
| Service | Usage | Hackathon Role |
|---|---|---|
| Cloud Run | FastAPI backend hosting | Primary compute |
| Vertex AI (Gemini) | SEC Simulator + AI reports | AI-native operations evidence |
| Firebase Firestore | Offline sync bridge | Edge resilience |
| BigQuery | Analytics warehouse | Production data logs |
| Cloud Tasks | Async PDF generation | Background job processing |
| Cloud Logging | Agent execution logs | Hackathon submission evidence |

---

## Database Schema

### Core Tables

```sql
-- Tenants (one per company)
CREATE TABLE plants (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  company_name TEXT NOT NULL,
  timezone TEXT NOT NULL DEFAULT 'America/Toronto',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Divisions within a plant (e.g., Truss, Wall Panel, Floor)
CREATE TABLE divisions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  plant_id UUID REFERENCES plants(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Workstations (e.g., Saw Station, Assembly Table 1)
CREATE TABLE stations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  division_id UUID REFERENCES divisions(id) ON DELETE CASCADE,
  plant_id UUID REFERENCES plants(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  kiosk_token TEXT UNIQUE, -- used to authenticate the kiosk device
  is_active BOOLEAN DEFAULT TRUE
);

-- Workers
CREATE TABLE workers (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  plant_id UUID REFERENCES plants(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  employee_id TEXT,
  pin TEXT, -- 4-digit kiosk PIN
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Jobs (a production order)
CREATE TABLE jobs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  plant_id UUID REFERENCES plants(id) ON DELETE CASCADE,
  division_id UUID REFERENCES divisions(id),
  job_number TEXT NOT NULL,
  customer_name TEXT,
  description TEXT,
  engineering_hours NUMERIC, -- estimated hours from engineering
  status TEXT DEFAULT 'pending', -- pending, in_progress, completed, on_hold
  priority INTEGER DEFAULT 0,
  due_date DATE,
  started_at TIMESTAMPTZ,
  completed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Task logs (the core data unit — every start/stop event)
CREATE TABLE task_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  plant_id UUID REFERENCES plants(id) ON DELETE CASCADE,
  job_id UUID REFERENCES jobs(id) ON DELETE CASCADE,
  station_id UUID REFERENCES stations(id),
  worker_id UUID REFERENCES workers(id),
  started_at TIMESTAMPTZ NOT NULL,
  completed_at TIMESTAMPTZ,
  duration_minutes NUMERIC GENERATED ALWAYS AS (
    EXTRACT(EPOCH FROM (completed_at - started_at)) / 60
  ) STORED,
  synced_at TIMESTAMPTZ DEFAULT NOW(), -- when it arrived from offline queue
  offline_created BOOLEAN DEFAULT FALSE, -- flagged if created offline
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- AI Simulation runs (logged for hackathon evidence)
CREATE TABLE simulation_runs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  plant_id UUID REFERENCES plants(id),
  job_id UUID REFERENCES jobs(id),
  input_params JSONB, -- attendance %, shift hours, etc.
  output_p50 DATE,
  output_p70 DATE,
  output_p95 DATE,
  iterations INTEGER DEFAULT 1000,
  vertex_ai_request_id TEXT, -- Google Cloud trace ID
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Subscriptions
CREATE TABLE subscriptions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  plant_id UUID REFERENCES plants(id),
  stripe_customer_id TEXT,
  stripe_subscription_id TEXT,
  tier TEXT, -- starter, growth, pro
  status TEXT, -- active, cancelled, past_due
  current_period_end TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Row Level Security (Multi-Tenant Isolation)
```sql
-- Workers can only see their own plant data
ALTER TABLE jobs ENABLE ROW LEVEL SECURITY;
CREATE POLICY "plant_isolation" ON jobs
  USING (plant_id = auth.jwt() ->> 'plant_id');

-- Same pattern applied to all tables
```

---

## Offline Sync Architecture

The kiosk offline flow is the most critical technical piece — and the most impressive for judges.

```
ONLINE MODE
─────────────────────────────────────────────
Worker taps "Start Task"
  → React state update (optimistic UI)
  → POST /api/tasks { job_id, worker_id, started_at }
  → 200 OK
  → Supabase Realtime broadcasts to dashboard
  → Dashboard updates in < 1 second

OFFLINE MODE (network drops)
─────────────────────────────────────────────
Worker taps "Start Task"
  → React state update (optimistic UI — no visual difference)
  → fetch() fails (network error caught)
  → Task written to IndexedDB queue:
    {
      id: uuid(),
      endpoint: '/api/tasks',
      payload: { job_id, worker_id, started_at },
      queued_at: ISO timestamp,
      synced: false
    }
  → UI shows "Offline — data saved locally" indicator

RECONNECTION
─────────────────────────────────────────────
Network returns
  → Service Worker fires 'sync' event
  → Background Sync reads all { synced: false } from IndexedDB
  → Replays each request to API in chronological order
  → API accepts with offline_created: true flag
  → Each record marked { synced: true } in IndexedDB
  → Dashboard catches up via Supabase Realtime
  → Zero data loss, zero manual intervention
```

---

## AI Integration — Vertex AI (Gemini)

### SEC Simulator (Scheduled End of Construction)

```python
# /api/simulator/sec
async def run_sec_simulation(job_id: str, params: SimParams):
    # 1. Pull historical velocity for this job/division
    velocity_data = await get_production_velocity(job_id)

    # 2. Build Monte Carlo prompt for Vertex AI
    prompt = f"""
    You are a construction scheduling AI.
    
    Job: {job.job_number} — {job.description}
    Remaining engineering hours: {remaining_hours}
    Historical daily output: {velocity_data}
    Current team attendance: {params.attendance_pct}%
    Shift hours per day: {params.shift_hours}
    
    Run a Monte Carlo simulation with 1000 iterations.
    Account for variance in daily output, attendance fluctuation,
    and station bottlenecks.
    
    Return JSON with:
    - p50_date: most likely completion date
    - p70_date: confident delivery date  
    - p95_date: conservative date
    - confidence_factors: key risks affecting the range
    """

    # 3. Call Vertex AI — this call is logged automatically in Cloud Logging
    response = await vertex_ai_client.generate_content(prompt)
    
    # 4. Parse and store result (stores vertex_ai_request_id for submission)
    result = parse_simulation_response(response)
    await store_simulation_run(job_id, params, result, response.request_id)
    
    return result
```

### Generative Reports

```python
# /api/reports/monthly
async def generate_monthly_report(plant_id: str, month: str):
    # 1. Aggregate real data
    metrics = await get_monthly_metrics(plant_id, month)
    
    # 2. Send to Gemini for narrative analysis
    prompt = f"""
    You are an operations analyst for a fabrication plant.
    
    Monthly data for {metrics.plant_name} — {month}:
    - Overall efficiency: {metrics.lei_avg}%
    - Jobs completed: {metrics.jobs_completed}
    - Top station: {metrics.top_station} ({metrics.top_station_yield} batches)
    - Bottleneck station: {metrics.bottleneck} (avg {metrics.bottleneck_delay}h delay)
    - Top performer: {metrics.top_worker} ({metrics.top_worker_lei}% efficiency)
    
    Write a professional monthly operations report with three sections:
    1. What worked well (2-3 specific observations)
    2. Areas of concern (2-3 specific issues with data)
    3. Recommended actions for next month (3 concrete steps)
    
    Tone: clear, direct, actionable. No generic filler.
    """
    
    narrative = await vertex_ai_client.generate_content(prompt)
    
    # 3. Combine with charts → PDF
    pdf = await generate_pdf_report(metrics, narrative.text)
    return pdf
```

---

## Monorepo Structure

```
fabpulse/
├── apps/
│   ├── api/                    # FastAPI backend
│   │   ├── main.py
│   │   ├── routers/
│   │   │   ├── auth.py
│   │   │   ├── jobs.py
│   │   │   ├── tasks.py
│   │   │   ├── workers.py
│   │   │   ├── analytics.py
│   │   │   ├── simulator.py
│   │   │   └── reports.py
│   │   ├── models/
│   │   ├── services/
│   │   │   ├── vertex_ai.py    # Gemini integration
│   │   │   ├── monte_carlo.py  # SEC Simulator logic
│   │   │   └── pdf_gen.py      # Report generation
│   │   ├── db/
│   │   │   ├── schema.sql
│   │   │   └── migrations/
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   ├── dashboard/              # Manager web app
│   │   ├── src/
│   │   │   ├── pages/
│   │   │   │   ├── JobBoard.tsx
│   │   │   │   ├── Analytics.tsx
│   │   │   │   ├── Simulator.tsx
│   │   │   │   ├── Reports.tsx
│   │   │   │   └── Admin.tsx
│   │   │   ├── components/
│   │   │   ├── hooks/
│   │   │   └── store/
│   │   ├── package.json
│   │   └── vite.config.ts
│   │
│   └── kiosk/                  # PWA for workstations
│       ├── src/
│       │   ├── pages/
│       │   │   ├── CheckIn.tsx
│       │   │   ├── ActiveJob.tsx
│       │   │   └── TaskComplete.tsx
│       │   ├── offline/
│       │   │   ├── queue.ts    # IndexedDB queue manager
│       │   │   └── sync.ts     # Background sync handler
│       │   └── sw.ts           # Service worker
│       ├── package.json
│       └── vite.config.ts
│
├── packages/
│   ├── shared-types/           # TypeScript interfaces shared across apps
│   └── ui/                     # Shared React components (brand system)
│
├── infrastructure/
│   ├── cloudbuild.yaml         # Google Cloud Build config
│   ├── cloudrun.yaml           # Cloud Run service config
│   └── terraform/              # Optional: IaC for GCP resources
│
├── docs/
│   ├── ARCHITECTURE.md         # This file
│   ├── SCHEDULE.md
│   ├── BRAND.md
│   ├── PROJECT.md
│   └── NARRATIVE-TEMPLATE.md
│
├── .github/
│   └── workflows/
│       └── deploy.yml          # CI/CD: push to main → deploy to Cloud Run
│
├── CLAUDE.md                   # Context for Claude Code sessions
└── README.md
```

---

## Deployment Pipeline

```
Developer pushes to main
  → GitHub Actions triggers
  → Run tests
  → Build Docker image
  → Push to Google Artifact Registry
  → Deploy to Cloud Run (zero downtime)
  → Run DB migrations (Alembic)
  → Notify via Slack/email

Kiosk PWA + Dashboard:
  → Vite build
  → Deploy to Firebase Hosting
  → Service Worker updated automatically
  → Existing kiosks receive update silently
```

---

## Environment Variables

```env
# Supabase
SUPABASE_URL=
SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=

# Google Cloud
GOOGLE_CLOUD_PROJECT=fabpulse-prod
VERTEX_AI_LOCATION=us-central1
GEMINI_MODEL=gemini-1.5-pro

# Stripe
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
STRIPE_STARTER_PRICE_ID=
STRIPE_GROWTH_PRICE_ID=
STRIPE_PRO_PRICE_ID=

# App
APP_URL=https://fabpulse.io
API_URL=https://api.fabpulse.io
JWT_SECRET=
```

---

## Security Considerations

- **Multi-tenant isolation:** All queries scoped by plant_id. RLS enforced at DB level
- **Kiosk auth:** Devices authenticate with a plant-scoped kiosk token (not user JWT)
- **Worker PINs:** 4-digit PINs hashed with bcrypt, never stored in plain text
- **API rate limiting:** Cloud Run + FastAPI middleware (slowapi)
- **HTTPS everywhere:** Cloud Run enforces TLS. Firebase Hosting enforces TLS
- **Offline data:** IndexedDB data is device-local, cleared after successful sync

---

## Performance Targets

| Metric | Target |
|---|---|
| Dashboard load time | < 2 seconds |
| Kiosk task log (online) | < 500ms round trip |
| Realtime dashboard update | < 1 second after task logged |
| Offline sync flush | < 5 seconds after reconnect |
| SEC Simulator response | < 10 seconds (Vertex AI call) |
| PDF report generation | < 30 seconds |
| API uptime | 99.9% (Cloud Run SLA) |
