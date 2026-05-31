# FabPulse — 90-Day Hackathon Schedule
# XPRIZE x Google: Build with Gemini
# Deadline: August 17, 2026 @ 1:00pm PDT

---

## Overview

| Phase | Days | Focus | Exit Criteria |
|---|---|---|---|
| Phase 1 — Build | Days 1–30 | MVP in production at test plant | Working app, real data, AI live |
| Phase 2 — Ship | Days 31–60 | First paying customers | 3–5 plants, Stripe revenue |
| Phase 3 — Grow | Days 61–90 | Scale + document + submit | Full submission package ready |

---

## PHASE 1 — BUILD (Days 1–30)
> Goal: Functional MVP deployed in production at your test plant. AI making real decisions. Google Cloud integrated.

### Week 1 (Days 1–7) — Foundation
- [x] Set up monorepo structure (see `ARCHITECTURE.md`)
- [x] Initialize Supabase project (PostgreSQL + Auth + Realtime)
- [ ] Initialize Firebase project (Firestore for offline sync queue)
- [ ] Deploy FastAPI backend skeleton to Cloud Run ← **next session**
- [x] Set up CI/CD pipeline (GitHub Actions → Cloud Run) — workflow created, pendiente primer deploy
- [x] Define core data models: Plant, Division, Station, Job, Worker, TaskLog, SimulationRun, Subscription
- [x] Configure multi-tenant schema (plant_id scoping on all tables)
- [ ] Register domain: fabpulse.io
- [ ] Set up Google Analytics + basic logging from day 1

**Exit criteria:** Backend running on Cloud Run. Database schema migrated. Auth working.

---

### Week 2 (Days 8–14) — Kiosk PWA
- [ ] Build PWA kiosk shell (React + Vite + PWA manifest)
- [ ] Implement IndexedDB queue for offline task logging
- [ ] Build worker check-in / check-out UI
- [ ] Build task start / task complete flow
- [ ] Implement Background Sync (Service Worker)
- [ ] Test offline → online sync loop end-to-end
- [ ] Lock kiosk mode (disable browser nav, fullscreen API)
- [ ] Deploy to Vercel / Firebase Hosting

**Exit criteria:** Kiosk works fully offline. Syncs automatically when network returns. No data loss on reconnect.

---

### Week 3 (Days 15–21) — Manager Dashboard
- [ ] Build web dashboard shell (React + Tailwind, brand colors from `BRAND.md`)
- [ ] Live job board: active jobs per station, status, assigned workers
- [ ] Labor Efficiency Index (LEI): engineering time vs actual time, per job
- [ ] Station Yield view: batches completed per station this week/month
- [ ] Attendance board: who is clocked in right now
- [ ] Job dispatch: assign jobs, set priority, add notes from dashboard → kiosk
- [ ] Real-time updates via Supabase Realtime (WebSocket)

**Exit criteria:** Manager can see live plant activity. Dashboard updates without page refresh.

---

### Week 4 (Days 22–30) — AI Integration + Beta Launch
- [ ] Integrate Vertex AI (Gemini API) for SEC Simulator
- [ ] Build Monte Carlo engine: 1,000+ simulations per job
- [ ] Output P50 / P70 / P95 completion date predictions
- [ ] Build interactive simulator UI (adjust attendance, shifts → see updated predictions)
- [ ] Set up Vertex AI logging (agent execution logs for hackathon submission)
- [ ] Generate first AI report (PDF via Puppeteer or WeasyPrint)
- [ ] Deploy kiosk on test plant floor (your plant)
- [ ] Collect first real production data
- [ ] Screenshot everything — this is your product evidence

**Exit criteria:** AI running in production. Real data flowing. Vertex AI logs captured. First PDF report generated.

---

## PHASE 2 — SHIP (Days 31–60)
> Goal: 3–5 paying plants on Stripe. Real revenue. Real customer contacts for submission.

### Week 5 (Days 31–37) — Monetization Setup
- [ ] Set up Stripe: 3 products (Starter $299, Growth $599, Pro $1,499/mo)
- [ ] Build subscription flow: signup → Stripe Checkout → plant provisioned automatically
- [ ] Add Stripe webhook: handle payment success, cancellation, failed payment
- [ ] Build onboarding wizard: plant setup in under 10 minutes
- [ ] Create quick-start video (Loom): "From signup to live kiosk in 30 minutes"
- [ ] Set up customer support channel (email or Slack)
- [ ] Finalize pricing page on fabpulse.io

**Exit criteria:** A plant manager can sign up, pay, and deploy without your help.

---

### Week 6 (Days 38–44) — First Sales Push
- [ ] Personal outreach to plant contacts (warm leads first)
- [ ] Offer 30-day free trial → convert to paid at day 31
- [ ] Target: 2 plants live on trial, 1 plant paying
- [ ] Document every customer: name, email, phone, plant name, location
- [ ] Collect written or video testimonials from beta users
- [ ] Run first full AI report for a paying customer
- [ ] Fix critical bugs discovered in real production use

**Exit criteria:** At least 1 plant paying via Stripe. Customer contact info documented.

---

### Week 7 (Days 45–51) — Expand Customer Base
- [ ] Follow up with all warm contacts who haven't replied
- [ ] Ask beta customers for referrals (other plants they know)
- [ ] Target: 3 plants paying ($897/mo MRR minimum)
- [ ] Start tracking: MRR, churn risk, feature requests
- [ ] Improve onboarding based on beta feedback
- [ ] Add any missing features blocking adoption

**Exit criteria:** 3+ paying plants. Stripe dashboard showing recurring revenue.

---

### Week 8 (Days 52–60) — Revenue Evidence + Video
- [ ] Export Stripe dashboard (revenue evidence for submission)
- [ ] Record 3-minute demo video:
  - Show AI (Vertex AI / Gemini) making decisions in production
  - Show real plant data (anonymize if needed)
  - Show Stripe revenue
  - Show customer using the kiosk live
- [ ] Write draft of 500–1000 word narrative (see `NARRATIVE-TEMPLATE.md`)
- [ ] Compile agent execution logs from Vertex AI
- [ ] Document API usage records from Google Cloud Console

**Exit criteria:** Video recorded. Revenue exported. Narrative drafted. All evidence collected.

---

## PHASE 3 — GROW (Days 61–90)
> Goal: Scale revenue, polish submission, win.

### Week 9 (Days 61–67) — Scale Outreach
- [ ] Expand beyond warm contacts: LinkedIn outreach to plant managers
- [ ] Target: 5–8 paying plants ($1,500–$2,400/mo MRR)
- [ ] Set up basic marketing: SEO landing page, Google Ads (small budget)
- [ ] Document all marketing spend (required for submission)
- [ ] Add any high-impact features based on customer feedback

---

### Week 10 (Days 68–74) — Polish Product
- [ ] UI/UX pass on dashboard and kiosk
- [ ] Performance optimization (load times, sync speed)
- [ ] Security audit (auth, data isolation between tenants)
- [ ] Mobile responsiveness check on manager dashboard
- [ ] Test offline sync under different network conditions

---

### Week 11 (Days 75–81) — Submission Package
- [ ] Finalize written narrative (500–1000 words, see template)
- [ ] Compile all product evidence:
  - Vertex AI agent execution logs
  - Google Cloud API usage screenshots
  - Dashboard screenshots with real data
  - Kiosk in use on plant floor (photo/video)
- [ ] Compile customer evidence:
  - Full customer list (name, email, phone)
  - Testimonials (written or video)
- [ ] Export final Stripe P&L
- [ ] Document corporate ID (if registered)
- [ ] Document all hackathon-period expenses

---

### Week 12 (Days 82–90) — Final Review + Submit
- [ ] Final review of GitHub repo (clean, documented, shared with testing@devpost.com and judging@hacker.fund)
- [ ] Final review of 3-minute video (crisp, shows AI in production, shows revenue)
- [ ] Final review of written narrative
- [ ] Proofread all submission materials
- [ ] Submit before August 17, 2026 @ 1:00pm PDT ⚠️
- [ ] Post on LinkedIn / social media (visibility doesn't hurt)

---

## Key Metrics to Track Weekly

| Metric | Week 4 | Week 8 | Week 12 |
|---|---|---|---|
| Plants in production | 1 (test) | 3–5 | 5–8 |
| MRR | $0 | $897–$1,497 | $1,500–$2,400 |
| AI decisions logged | 100+ | 1,000+ | 5,000+ |
| Customer contacts | 1 | 3–5 | 5–8 |
| Vertex AI API calls | Live | Growing | Documented |

---

## Submission Checklist (Final)

- [ ] GitHub repo (public or shared with judging emails)
- [ ] 3-minute video (AI in production + revenue proof)
- [ ] Written narrative (500–1000 words)
- [ ] Revenue evidence (Stripe export or bank statement)
- [ ] Corporate ID (if available)
- [ ] Marketing/acquisition spend disclosure
- [ ] Agent execution logs
- [ ] API usage records
- [ ] Customer contact list
- [ ] Customer testimonials

---

## Risk Register

| Risk | Likelihood | Mitigation |
|---|---|---|
| Plant Wi-Fi issues delay testing | High | Offline mode is core feature — this validates the product |
| Sales cycle too long for 90 days | Medium | Offer free trial weeks 5–6, convert in week 7 |
| Google Cloud integration blocked | Low | Firebase (simpler) as fallback before Vertex AI |
| Competitor spotted during hackathon | Low | Domain expertise is moat — no one knows this floor like you |
| No revenue by day 60 | Low | 1 paying plant at $299 is enough — focus on warm contacts first |
