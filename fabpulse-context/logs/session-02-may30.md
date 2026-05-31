# FabPulse — Dev Log

---

## Session 02 — May 31, 2026

**Focus:** FastAPI backend skeleton, Supabase schema + RLS, local environment running, CI/CD pipeline

---

### What Was Done

**1. Construí el backend completo de FastAPI**

Partiendo de un monorepo vacío (solo `.gitkeep` files), construí el backend completo desde cero:

- **`main.py`** — FastAPI app con CORS configurado para `fabpulse.io` y localhost, error handlers con el formato JSON estándar `{error, detail, code}`
- **`config.py`** — `pydantic-settings` leyendo variables desde `.env`, todas las claves necesarias para Supabase, GCP, Stripe
- **`database.py`** — SQLAlchemy 2.0 async engine con `asyncpg`, pool de conexiones configurado, `ssl=require` para Supabase
- **`dependencies.py`** — `get_current_plant` valida el JWT de Supabase y extrae `app_metadata.plant_id`; `get_kiosk_station` valida el header `X-Kiosk-Token` para autenticación de kioscos

**2. Definí los 8 modelos SQLAlchemy 2.0**

Usando la sintaxis `Mapped[]` de SQLAlchemy 2.0 (no el estilo legado):

- `Plant` — raíz del tenant, contiene divisiones, estaciones, trabajadores, jobs
- `Division` — Truss, Wall Panel, Floor Systems
- `Station` — estación de trabajo, tiene `kiosk_token` único para autenticación de dispositivo
- `Worker` — con `pin_hash` (bcrypt) — **no** `pin TEXT` como estaba en ARCHITECTURE.md, la regla de seguridad manda hash
- `Job` — orden de producción, ciclo de vida completo (pending → in_progress → completed)
- `TaskLog` — unidad de dato central; tiene `duration_minutes` como columna `GENERATED ALWAYS AS STORED` en PostgreSQL
- `SimulationRun` — output del SEC Simulator, almacena `vertex_ai_request_id` para evidencia del hackathon
- `Subscription` — Stripe integration, tiers: starter/growth/pro

**3. Schemas Pydantic v2 y 11 routers**

Schemas con `ConfigDict(from_attributes=True)` (no el `orm_mode` de v1). Routers implementados:

- `/health` y `/health/db` — status checks
- `/auth` — estado de autenticación, plant info
- `/plants` — `POST /` crea plant + setea `plant_id` en Supabase `app_metadata` via Admin API; `GET /me` retorna plant del usuario
- `/divisions`, `/stations`, `/workers`, `/jobs` — CRUD completo con multi-tenant scoping
- `/tasks` — `POST /` para kiosco (auth por token); `POST /manual` para manager (auth por JWT)
- `/analytics`, `/simulator`, `/reports` — stubs que retornan `501 Not Implemented` con nota de scope (Week 3–4)

**4. Schema de base de datos con RLS inline**

Aprendizaje clave: Supabase muestra un warning si creás tablas sin activar RLS inmediatamente. En lugar de dos archivos separados (`schema.sql` + `rls_policies.sql`), el schema final es **un solo archivo** donde cada tabla es seguida inmediatamente por:

```sql
ALTER TABLE jobs ENABLE ROW LEVEL SECURITY;
CREATE POLICY "plant_isolation" ON jobs
  USING (plant_id::TEXT = auth.jwt() -> 'app_metadata' ->> 'plant_id');
```

Esto garantiza que nunca existe una ventana donde una tabla esté desprotegida.

**5. Alembic async configurado**

- `alembic.ini` apuntando a `alembic/` directory
- `alembic/env.py` con patrón async correcto (`asyncio.run(run_migrations_online())`)
- Migración `001_initial_schema.py` — usa `op.execute()` raw SQL para `task_logs` porque la columna computed `GENERATED ALWAYS AS STORED` no puede ser autogenerada por Alembic

**6. Supabase project inicializado**

- Proyecto creado en supabase.com
- `schema.sql` aplicado en el SQL Editor — tablas + RLS activo en una sola ejecución
- Connection string configurada: **pooler en puerto 6543** (no el puerto 5432 directo)
- Confirmado: `/health/db` retorna `{"status":"ok","database":"connected"}`

**7. Dockerfile y CI/CD**

- `Dockerfile` — `python:3.14-slim`, corre en puerto 8080, 2 workers uvicorn
- `.github/workflows/deploy.yml` — trigger en `apps/api/**`, OIDC auth a GCP, build → Artifact Registry → deploy Cloud Run
- `infrastructure/cloudrun.yaml` — Cloud Run service config con Secret Manager integration para todas las claves sensibles

---

### Problemas encontrados y soluciones

**Python 3.14 + dependencias pinneadas**

Las versiones exactas (`pydantic-core==2.9.2`, `asyncpg==0.29.0`) no tenían wheels pre-compilados para Python 3.14 en Windows — intentaban compilar desde Rust/C y fallaban por falta de MSVC.

*Solución:* Cambiar todas las dependencias de `==` a `>=`. pip resuelve la versión más reciente compatible con Python 3.14.

**`pyiceberg` sin compilador C**

`google-cloud-aiplatform` (y al parecer `supabase` SDK en versiones nuevas) arrastra `pyiceberg` como dependencia transitiva — una librería de Apache Iceberg con una extensión C que necesita Visual Studio Build Tools.

*Solución:* `google-cloud-aiplatform` comentado hasta Week 4. `supabase` SDK removido (no se importa en ningún lado — usamos `httpx` directo para el Admin API y `asyncpg` para la DB).

**Puerto 5432 con timeout**

La `DATABASE_URL` con el host directo de Supabase (`db.[ref].supabase.co:5432`) daba `TimeoutError [Errno 10060]` — el puerto estaba siendo bloqueado.

*Solución:* Usar el **Connection Pooler** (Transaction mode, puerto 6543) + `connect_args={"ssl": "require"}` en el engine de SQLAlchemy.

---

### Files Created

| File | Location | Purpose |
|---|---|---|
| `main.py` | `apps/api/` | FastAPI app entry point |
| `config.py` | `apps/api/` | pydantic-settings, env vars |
| `database.py` | `apps/api/` | SQLAlchemy async engine |
| `dependencies.py` | `apps/api/` | Auth dependencies (JWT + kiosk token) |
| `requirements.txt` | `apps/api/` | Python deps con `>=` para Python 3.14 |
| `Dockerfile` | `apps/api/` | python:3.14-slim, port 8080 |
| `models/` (8 archivos) | `apps/api/models/` | SQLAlchemy 2.0 modelos |
| `schemas/` (5 archivos) | `apps/api/schemas/` | Pydantic v2 schemas |
| `routers/` (11 archivos) | `apps/api/routers/` | FastAPI routers |
| `services/` (3 stubs) | `apps/api/services/` | vertex_ai, monte_carlo, pdf_gen |
| `schema.sql` | `apps/api/db/` | Schema + RLS policies (archivo único) |
| `alembic.ini` | `apps/api/` | Alembic config |
| `env.py` + `001_initial_schema.py` | `apps/api/alembic/` | Alembic async setup + migración inicial |
| `cloudrun.yaml` | `infrastructure/` | Cloud Run service definition |
| `deploy.yml` | `.github/workflows/` | GitHub Actions CI/CD |

---

### Decisions Made

| Decision | Rationale |
|---|---|
| Python 3.14 (no downgrade a 3.12) | El usuario ya tiene 3.14 instalado; las dependencias se pueden adaptar |
| `>=` en lugar de `==` en requirements | Wheels pre-compilados para 3.14 solo están en versiones nuevas |
| Remover `supabase` SDK | No se usa — la conexión directa via asyncpg es más eficiente |
| Schema + RLS en un solo archivo | Elimina ventana de exposición, Supabase no lanza warning |
| `workers.pin` → `pin_hash` | Seguridad no-negociable: PINs nunca en texto plano |
| Connection pooler (puerto 6543) + ssl=require | Puerto 5432 bloqueado; pooler es más robusto para conexiones no-persistentes |
| JSON key para GitHub Actions | Más simple que Workload Identity para hackathon — se puede migrar después |
| `task_logs.duration_minutes` como computed column | Cálculo en DB garantiza consistencia aunque los datos vengan offline |

---

### Next Session — Google Cloud + First Deploy

**Goal:** GCP configurado, primer deploy a Cloud Run, URL pública funcionando.

**Checklist antes de empezar:**
- [ ] `gcloud` CLI instalado y autenticado
- [ ] Billing habilitado en GCP
- [ ] JSON key de service account listo para subir a GitHub Secrets

**Starting prompt:**
```
Lee CLAUDE.md — vamos a completar el setup de Google Cloud y hacer 
el primer deploy a Cloud Run.

Necesito:
1. Crear el proyecto fabpulse-prod, habilitar APIs
2. Crear Artifact Registry repo
3. Configurar secrets en Secret Manager
4. Crear service account + bajar JSON key
5. Agregar GCP_CREDENTIALS a GitHub Secrets
6. git push y verificar que el workflow deploye correctamente
```

**Files to have open:** `CLAUDE.md`, `.github/workflows/deploy.yml`, `infrastructure/cloudrun.yaml`

---

*Session duration: ~4 hours*
*"Local is alive. Production is next."*

---

## 📱 Social Media — Session 02

### LinkedIn
> 🏗️ Day 3 of building FabPulse — the backend is alive.
>
> Today I built the entire FastAPI skeleton for FabPulse from scratch:
> - 8 database models (Plant, Division, Station, Worker, Job, TaskLog, SimulationRun, Subscription)
> - 11 API routers with full multi-tenant isolation
> - Supabase PostgreSQL with Row Level Security on every table
> - Kiosk authentication via device token (not user JWT)
> - PIN verification with bcrypt hashing
>
> The moment that mattered most today wasn't the code. It was this response:
>
> `{"status": "ok", "database": "connected"}`
>
> That's my FastAPI backend talking to my Supabase database. Multi-tenant isolation active. Auth layer working.
>
> For a fabrication plant to trust their production data to a SaaS platform, every layer has to be correct from day 1. No shortcuts on security.
>
> Next: Google Cloud Run. The first public URL.
>
> #FabPulse #BuildWithGemini #XPRIZE #FastAPI #Supabase #Day3 #BackendDev

---

### X / Twitter
> Day 3 ✅
>
> FastAPI backend running locally.
> Supabase connected.
> Multi-tenant isolation: active.
> `/health/db`: {"status": "ok"} ✅
>
> 8 models. 11 routers. RLS on every table.
>
> Next stop: Cloud Run 🚀
>
> #FabPulse #BuildWithGemini #Day3

---

### Instagram / Reels caption
> Day 3 — the backend is alive 🚀
>
> Built the entire FastAPI skeleton today: database models, API routes, multi-tenant security, kiosk authentication.
>
> The best moment: seeing `{"status":"ok","database":"connected"}` in the browser.
>
> It means the API is talking to the database. Security layers are working. The foundation is solid.
>
> Next: deploying to Google Cloud Run so there's a real public URL.
>
> 87 days left. 🏗️⚡
>
> #FabPulse #BuildWithGemini #Hackathon #Day3 #FastAPI #BackendDev #SaaS #IndieHacker
