# CLAUDE.md — FabPulse Master Context
# Load this file at the start of every Claude Code session.

---

## What is FabPulse?

FabPulse is a cloud-native, multi-tenant SaaS platform that provides real-time operational intelligence for off-site construction fabrication plants (truss, wall panel, floor systems).

**One-liner:** FabPulse gives fabrication plants real-time visibility into their production — so they can cut waste, fix bottlenecks, and protect their margins.

**Tagline:** The Pulse of Precision Manufacturing.

---

## Hackathon Context

- **Competition:** XPRIZE x Google — Build with Gemini
- **Deadline:** August 17, 2026 @ 1:00pm PDT
- **Prize pool:** $2,000,000
- **Category:** Small Business Services
- **Key requirement:** Real revenue + real customers + AI running in production + Google Cloud

**Current phase:** See `SCHEDULE.md` for the active week and tasks.

---

## Tech Stack (Do Not Deviate)

### Backend
- **Language:** Python 3.12
- **Framework:** FastAPI (async)
- **Database:** PostgreSQL via Supabase
- **Auth:** Supabase Auth (JWT + RLS)
- **ORM:** SQLAlchemy + Alembic
- **Hosting:** Google Cloud Run
- **AI:** Vertex AI — Gemini 1.5 Pro

### Frontend (both apps)
- **Framework:** React 18 + Vite + TypeScript
- **Styling:** Tailwind CSS
- **State:** Zustand
- **Data fetching:** TanStack Query
- **Charts:** Recharts

### Kiosk PWA specific
- **Offline storage:** IndexedDB via `idb` library
- **Service worker:** Workbox via Vite PWA plugin
- **Sync:** Background Sync API

### Google Cloud Services
- Cloud Run — backend hosting
- Vertex AI (Gemini) — SEC Simulator + generative reports
- Firebase — offline sync bridge
- BigQuery — analytics warehouse
- Cloud Logging — AI execution logs (hackathon evidence)

### Payments
- Stripe (subscriptions: Starter $299/mo, Growth $599/mo, Pro $1,499/mo)

---

## Brand System

- **Primary color:** #1D9E75 (teal)
- **Light teal:** #5DCAA5
- **Dark teal:** #0F6E56
- **Ink (dark bg):** #0D1117
- **Off-white:** #F0F6FF
- **Alert red:** #E24B4A
- **Font:** Inter (Google Fonts)
- **Logo:** "Fab" in off-white/dark + "Pulse" in teal, always together with pulse icon

See `BRAND.md` for full brand guide reference.

---

## Core Data Models

```
Plant → Division → Station (kiosk lives here)
Plant → Worker
Plant → Job → TaskLog (worker + station + time)
Job → SimulationRun (Vertex AI SEC output)
Plant → Subscription (Stripe)
```

Full schema in `ARCHITECTURE.md`.

---

## Key Business Rules

1. **Multi-tenant isolation:** Every DB query MUST be scoped by `plant_id`. RLS enforced at Supabase level.
2. **Offline first:** Kiosk must work with zero network. Tasks queue in IndexedDB, sync via Background Sync.
3. **Optimistic UI:** Kiosk UI updates immediately on user action — never wait for server confirmation.
4. **AI logging:** Every Vertex AI call MUST log the request ID to `simulation_runs` table. This is hackathon submission evidence.
5. **Stripe webhooks:** Never provision/deprovision features without webhook confirmation — never trust client-side payment status.
6. **Kiosk auth:** Kiosks authenticate with a `kiosk_token` (station-scoped), NOT with a user JWT.

---

## API Conventions

- Base URL: `https://api.fabpulse.io`
- Auth header: `Authorization: Bearer <jwt>`
- Kiosk auth header: `X-Kiosk-Token: <kiosk_token>`
- All timestamps: ISO 8601 UTC
- All IDs: UUID v4
- Error format:
```json
{
  "error": "string",
  "detail": "string",
  "code": "SNAKE_CASE_ERROR_CODE"
}
```

---

## Folder Structure

```
fabpulse/
├── apps/
│   ├── api/          # FastAPI backend
│   ├── dashboard/    # Manager React app
│   └── kiosk/        # PWA React app
├── packages/
│   ├── shared-types/ # TypeScript interfaces
│   └── ui/           # Shared components
├── infrastructure/   # GCP configs
├── docs/             # All context files (this folder)
└── CLAUDE.md         # This file
```

---

## Current Priorities (update weekly)

> **Week 1 focus — Foundation (Days 1–7)**
> - [x] Monorepo structure set up
> - [x] Supabase project initialized (schema + RLS applied)
> - [x] Core data models defined (Plant, Division, Station, Worker, Job, TaskLog, SimulationRun, Subscription)
> - [x] Multi-tenant schema configured (plant_id scoping + RLS on all tables)
> - [x] FastAPI backend skeleton running locally — /health ✅ /health/db ✅
> - [x] CI/CD pipeline created (GitHub Actions → Cloud Run)
> - [ ] Deploy FastAPI to Cloud Run — **NEXT: complete GCP setup**
> - [ ] Initialize Firebase project
> - [ ] Register domain fabpulse.io

> **Stack note:** Python 3.14 (not 3.12). `google-cloud-aiplatform` commented out until Week 4 (pyiceberg/MSVC issue on Windows). Supabase connection uses pooler port 6543 + ssl=require.

---

## Patterns to Always Follow

### FastAPI route pattern
```python
@router.post("/jobs/{job_id}/tasks", response_model=TaskResponse)
async def create_task(
    job_id: UUID,
    payload: TaskCreate,
    current_plant: Plant = Depends(get_current_plant),
    db: AsyncSession = Depends(get_db)
):
    # Always verify job belongs to current plant
    job = await get_job_or_404(db, job_id, plant_id=current_plant.id)
    task = await task_service.create(db, job, payload)
    return task
```

### Offline queue pattern (kiosk)
```typescript
// Always try network first, fall back to queue
async function logTask(payload: TaskPayload) {
  try {
    await api.post('/tasks', payload);
  } catch (error) {
    if (!navigator.onLine) {
      await offlineQueue.add({ endpoint: '/tasks', payload });
      // UI shows optimistic update regardless
    } else {
      throw error; // Real error, not offline
    }
  }
}
```

### Vertex AI call pattern
```python
async def call_gemini(prompt: str, job_id: str) -> GeminiResponse:
    response = await gemini_client.generate_content(prompt)
    # ALWAYS log for hackathon evidence
    await log_ai_call(
        job_id=job_id,
        request_id=response.request_id,
        model=GEMINI_MODEL,
        tokens_used=response.usage_metadata.total_token_count
    )
    return response
```

---

## Hackathon Submission Requirements

Track progress against these — every item must be ready by Aug 17, 2026:

- [ ] GitHub repo (shared with testing@devpost.com and judging@hacker.fund)
- [ ] 3-minute video showing AI in production + revenue
- [ ] Written narrative 500–1000 words (template in `NARRATIVE-TEMPLATE.md`)
- [ ] Stripe dashboard export (revenue evidence)
- [ ] Corporate ID (if registered)
- [ ] Marketing spend disclosure (even if $0)
- [ ] Vertex AI agent execution logs
- [ ] Google Cloud API usage records
- [ ] Customer contact list (name, email, phone)
- [ ] Customer testimonials

---

## Do Not

- Do not use `any` in TypeScript — always type properly
- Do not store secrets in code — use environment variables only
- Do not skip `plant_id` scoping on any DB query
- Do not call Vertex AI without logging the request ID
- Do not implement features outside the current week's scope
- Do not use inline styles — use Tailwind classes
- Do not use `console.log` in production — use structured logging

---

## Useful Commands

```bash
# Backend
cd apps/api
uvicorn main:app --reload

# Dashboard
cd apps/dashboard
npm run dev

# Kiosk
cd apps/kiosk
npm run dev

# Database migrations
cd apps/api
alembic upgrade head

# Deploy to Cloud Run
gcloud run deploy fabpulse-api \
  --source apps/api \
  --region us-central1 \
  --allow-unauthenticated
```

---

## Contact / Accounts

- **Devpost project:** [URL]
- **GitHub repo:** [URL]
- **Supabase project:** [URL]
- **Google Cloud project:** fabpulse-prod
- **Stripe dashboard:** [URL]
- **Domain:** fabpulse.io
