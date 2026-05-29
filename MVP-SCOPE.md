# FabPulse — MVP Scope
# What we build in 30 days. What we defer. What we skip entirely.

---

## The Rule

> Every feature decision must answer: "Does this help us get a paying customer in 60 days?"
> If no → defer. If yes → build it now.

---

## MVP — Must Have (Days 1–30)

These are the minimum features for a plant to go live and pay.

### Auth & Onboarding
- [x] Email + password signup (Supabase Auth)
- [x] Plant setup wizard: name, timezone, divisions, stations
- [x] Invite workers (generate PIN codes)
- [x] Kiosk device pairing (QR code or token entry)

### Kiosk PWA
- [x] Worker PIN login
- [x] View assigned jobs at this station
- [x] Start task → running timer
- [x] Complete task → log time
- [x] Offline mode: full functionality without network
- [x] Background sync on reconnect
- [x] Kiosk lock (fullscreen, no browser nav)

### Manager Dashboard
- [x] Live job board: all active jobs, status, station, worker
- [x] Create / edit / assign jobs
- [x] Set job priority and due date
- [x] Worker attendance: who is clocked in right now
- [x] Labor Efficiency Index (LEI) per job: engineering hours vs actual
- [x] Station view: jobs in progress per station

### AI — SEC Simulator (Vertex AI)
- [x] Monte Carlo simulation per job (1,000 iterations)
- [x] P50 / P70 / P95 completion date output
- [x] Basic UI: input attendance %, shift hours → see predictions
- [x] Log every Vertex AI request (Cloud Logging + DB)

### Payments
- [x] Stripe Checkout: Starter ($299/mo) and Growth ($599/mo) only
- [x] Webhook: provision plant on payment success
- [x] Basic subscription status in admin

### Infrastructure
- [x] Cloud Run deployment (FastAPI)
- [x] Firebase Hosting (dashboard + kiosk)
- [x] Supabase (DB + Auth + Realtime)
- [x] GitHub Actions CI/CD
- [x] fabpulse.io live with landing page

---

## Phase 2 — Ship (Days 31–60)

Build these once the first plant is live and we have feedback.

### Analytics
- [ ] Station Yield chart: batches per station per week
- [ ] Lead Time view: days from job creation to completion
- [ ] Worker performance leaderboard (opt-in, plant configurable)
- [ ] Historical efficiency trend (last 4 weeks)

### AI — Reports
- [ ] Monthly PDF report (Gemini narrative + charts)
- [ ] Auto-send report via email at month close
- [ ] Annual summary report

### Payments
- [ ] Pro tier ($1,499/mo): multi-plant, API access
- [ ] Customer portal (Stripe Billing Portal)
- [ ] Dunning management (failed payment emails)

### Onboarding
- [ ] Quick-start video (embedded in setup wizard)
- [ ] In-app tooltips and help text
- [ ] Email drip: day 1, day 7, day 14 after signup

---

## Phase 3 — Grow (Days 61–90)

Polish and scale — only if core product is stable.

### Product
- [ ] Mobile-responsive dashboard (for managers on phone)
- [ ] Push notifications (job overdue, bottleneck alert)
- [ ] Custom job route builder (drag and drop stages)
- [ ] Import jobs from CSV / Excel

### Integrations
- [ ] MiTek / Alpine integration (import engineering hours from truss software)
- [ ] QuickBooks export (labor costs per job)
- [ ] API for third-party integrations (Pro tier)

### Marketing
- [ ] SEO landing page (blog posts targeting "truss plant software")
- [ ] Case study: first plant customer story
- [ ] Referral program: $100 credit per referred plant

---

## Explicitly Out of Scope (Do Not Build)

These are good ideas for the future — but they are scope killers for this hackathon.

| Feature | Why deferred |
|---|---|
| Native mobile app (iOS/Android) | PWA covers the use case. App store takes weeks |
| Material / inventory tracking | Different data model, different buyer, different sale |
| Payroll integration | Compliance complexity, different sales cycle |
| Customer-facing portal | B2B first — plant manager is the buyer |
| AI chatbot / assistant | Nice to have, not core to the value prop |
| Custom branding per plant | Pro feature, not needed for MVP |
| Multi-language support | English-first for North American market |
| On-premise deployment | Cloud-native only — no exceptions |

---

## Definition of Done (for each feature)

A feature is done when:
1. It works in production (not just localhost)
2. It handles the offline case (for kiosk features)
3. It is scoped correctly by plant_id (no data leaks between tenants)
4. AI calls are logged with request IDs (for hackathon evidence)
5. It has been tested by a real user (you, on the plant floor)

---

## Technical Debt Allowed in MVP

- No unit tests required in Phase 1 (write them in Phase 3 if time allows)
- No full TypeScript strict mode in kiosk (use `// @ts-ignore` sparingly)
- Hard-coded Stripe price IDs are OK in Phase 1 (move to DB in Phase 2)
- Basic error handling is fine (generic 500 errors OK until Phase 2)
- No rate limiting until Phase 2

## Technical Debt NOT Allowed (Ever)

- Skipping plant_id scoping on any query
- Storing secrets in code
- Missing Vertex AI request ID logging
- Kiosk data loss on network drop
