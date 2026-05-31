# FabPulse — Dev Log

---

## Session 01 — May 28, 2026

**Focus:** Brand identity, project documentation, hackathon strategy, GitHub setup

---

### What Was Done

**1. Named the product**
Evaluated 15+ name options including JobLogger, BuildPulse, PlantPulse, ShopPulse, FloorPulse, FabPulse. Final decision: **FabPulse** — short, industry-specific, memorable, and pitch-ready.
- Tagline: *"The Pulse of Precision Manufacturing"*
- Elevator pitch: *"FabPulse gives fabrication plants real-time visibility into their production — so they can cut waste, fix bottlenecks, and protect their margins."*

**2. Built the complete brand system**
- Primary color: `#1D9E75` (teal)
- Typography: Inter 700 / 600 / 400
- Logo: pulse waveform icon + "Fab" dark / "Pulse" teal
- Border radius scale, spacing scale, UI components, badges, metric cards
- Brand voice: clear, direct, empathic, professional
- Do's and Don'ts defined
- CSS variables ready to paste into any project

**3. Designed the thumbnail (3:2 SVG)**
- Version 1: standard pulse waveform
- Version 2 (final): house-shaped pulse — waveform rises as left wall, peaks as roof, drops as right wall, returns to baseline
- Represents off-site construction visually — the pulse IS the house

**4. Exported brand assets**
- `fabpulse-brand-guide.html` — complete self-contained brand guide
- `fabpulse-thumbnail-house.svg` — final thumbnail at 1200×800px

**5. Rewrote the project description**
Original document had "AI-powered" in title, no market numbers, no competitive landscape, mixed Spanish/English, and no pricing. Rewrote entirely:
- Replaced "AI-powered" → "Operational Intelligence"
- Added market size: $130B industry, $1.8B TAM
- Added competitive table: FabPulse vs. Procore, Fishbowl, Custom ERP
- Added pricing tiers: Starter $299/mo, Growth $599/mo, Pro $1,499/mo
- Added ROI argument: payback under 90 days
- Exported as `fabpulse-project-description.md`

**6. Analyzed the hackathon and defined strategy**
- Competition: XPRIZE x Google — Build with Gemini
- Prize pool: $2,000,000 — 1st place $500,000
- Deadline: August 17, 2026
- Requirements: real revenue + real customers + AI in production + Google Cloud
- Category: Small Business Services
- Key decision: FabPulse competes independently — NOT under MyBuildingTools umbrella
- Key advantages identified:
  - Direct access to a real plant for beta testing from day 1
  - Warm contacts at multiple plants for first sales
  - Domain expertise from 5 years working on the floor

**7. Built the 90-day execution plan**
- Month 1 (Days 1–30): Build MVP, deploy at test plant, AI live in production
- Month 2 (Days 31–60): First paying customers, target 3–5 plants ($897–$1,497/mo MRR)
- Month 3 (Days 61–90): Scale, document evidence, prepare submission
- Exported as `SCHEDULE.md`

**8. Defined full technical architecture**
- Backend: FastAPI + PostgreSQL/Supabase + Google Cloud Run
- Frontend: React 18 + TypeScript + Vite + Tailwind CSS
- Kiosk PWA: offline-first with IndexedDB queue + Background Sync
- AI: Vertex AI — Gemini 1.5 Pro (SEC Simulator + generative reports)
- Multi-tenant isolation via Row Level Security
- Full SQL schema defined (plants, divisions, stations, workers, jobs, task_logs, simulation_runs, subscriptions)
- Monte Carlo simulation with Bayesian cold-start prior for new plants
- Exported as `ARCHITECTURE.md`

**9. Defined MVP scope**
- Phase 1 (30 days): auth, kiosk PWA, manager dashboard, SEC Simulator, Stripe billing
- Phase 2 (60 days): analytics charts, generative reports, Pro tier
- Phase 3 (90 days): polish, mobile, integrations
- Explicitly out of scope: native mobile app, inventory tracking, payroll, on-premise
- Exported as `MVP-SCOPE.md`

**10. Wrote all Devpost submission documents**
- `DEVPOST-STORY.md`: 7 required sections with real origin story
  - Inspiration: Colombia → Canada → truss plant worker → Excel VBA → Python → FabPulse
  - What it does: kiosk PWA, manager dashboard, SEC Simulator, generative reports
  - How I built it: architecture, offline sync code, Monte Carlo math with LaTeX
  - Challenges: offline sync on Android, factory floor UX, compressing sales cycle
  - Accomplishments: tested on real plant, Excel VBA to Vertex AI arc, self-serve onboarding
  - What I learned: offline-first, trust in 45 seconds, prediction beats reporting
  - What's next: MiTek integration, QR scanning, anomaly detection *(in dev)*, multi-plant *(in dev)*
- `DEVPOST-BUILT-WITH.md`: full tech stack ready to paste into Devpost
- `NARRATIVE-TEMPLATE.md`: 500–1000 word narrative with real data placeholders

**11. Set up GitHub repo**
- Created repo structure
- `README.md`: professional with badges, architecture diagram, getting started, pricing, roadmap with checkboxes, origin story
- `CLAUDE.md`: master context file for Claude Code sessions
- `docs/ARCHITECTURE.md`: full technical reference
- `docs/PROJECT.md`: complete project pitch
- `docs/assets/thumbnail.svg`: official thumbnail

---

### Files Created

| File | Location | Purpose |
|---|---|---|
| `fabpulse-brand-guide.html` | local | Complete brand guide |
| `fabpulse-thumbnail-house.svg` | `docs/assets/` | Official 3:2 thumbnail |
| `CLAUDE.md` | repo root | Claude Code master context |
| `SCHEDULE.md` | local | 90-day hackathon plan |
| `ARCHITECTURE.md` | `docs/` | Full technical architecture |
| `MVP-SCOPE.md` | local | Build scope and priorities |
| `NARRATIVE-TEMPLATE.md` | local | Hackathon narrative template |
| `DEVPOST-STORY.md` | local | Complete Devpost submission story |
| `DEVPOST-BUILT-WITH.md` | local | Tech stack for Devpost |
| `fabpulse-project-description.md` | `docs/PROJECT.md` | Full project pitch |
| `README.md` | repo root | GitHub repo README |

---

### Decisions Made

| Decision | Rationale |
|---|---|
| Name: FabPulse | Most memorable, industry-specific, pitch-ready |
| Color: teal `#1D9E75` | Green = efficiency/go in industrial context, not generic blue SaaS |
| House-shaped pulse | Waveform visually communicates off-site construction |
| Compete independently from MyBuildingTools | FabPulse story is stronger alone — win first, integrate later |
| Category: Small Business Services | ~4,200 plants in North America, all SMB, underserved |
| Google Cloud + Vertex AI | Required by hackathon + genuinely best fit for Monte Carlo AI |
| Self-serve onboarding | Must compress 6-month sales cycle to days for hackathon revenue |
| "I" not "We" in Devpost story | Solo founder, authentic story — "we" dilutes the personal origin |

---

### Next Session — Week 1 Build

**Goal:** Monorepo initialized, Supabase live, Cloud Run deployed, core schema migrated.

**Starting prompt:**
```
Read CLAUDE.md and ARCHITECTURE.md — then let's start Week 1.
Set up the monorepo structure, initialize Supabase, configure 
Google Cloud Run, and deploy the FastAPI backend skeleton 
with the core database schema.
```

**Files to attach:** `CLAUDE.md` + `ARCHITECTURE.md`

---

*Session duration: ~3 hours*
*"The plant floor has always had a pulse. I built the monitor."*

---

## 📱 Social Media — Session 01

### LinkedIn
> 🏗️ Day 1 of building FabPulse.
>
> I'm competing in the XPRIZE x Google hackathon — $2M in prizes, 90 days to build a real business with real revenue using the Gemini ecosystem.
>
> My project: **FabPulse** — real-time production intelligence for fabrication plants.
>
> The backstory: I'm an electronics engineer from Colombia. 5 years ago I moved to Canada and started working on the floor of a truss plant. I watched people spend entire shifts transcribing production data by hand — cut times, assembly times, lumber quantities — all copied manually into spreadsheets that were already wrong.
>
> So I built a solution with what I had: Excel VBA.
>
> It worked. Then I moved to Python. Then a full dashboard. Now — a cloud-native SaaS platform powered by Vertex AI and Google Cloud.
>
> Today I finished the brand, the architecture, the 90-day plan, and the GitHub repo.
>
> Tomorrow we start building.
>
> #FabPulse #Hackathon #XPRIZE #GoogleCloud #GeminiAI #BuildWithGemini #OffSiteConstruction #SaaS #IndieHacker #Day1

---

### X / Twitter
> Day 1 ✅ — Brand, architecture, 90-day plan, GitHub repo.
>
> Building @FabPulse for the @XPRIZE x @Google hackathon.
>
> Real-time production intelligence for fabrication plants — powered by Gemini + Cloud Run.
>
> From Excel VBA on a truss plant floor → cloud-native SaaS.
>
> 89 days left. Let's go. 🏗️⚡
>
> #BuildWithGemini #XPRIZE #Day1

---

### Instagram / Reels caption
> Started Day 1 of the XPRIZE x Google hackathon 🚀
>
> 90 days. Real product. Real revenue. Real customers.
>
> Building FabPulse — because I worked on a factory floor and watched people waste hours transcribing data by hand. There had to be a better way.
>
> Today: brand identity ✅ architecture ✅ 90-day plan ✅ GitHub repo ✅
>
> Next: writing real code.
>
> Follow the build 👇
> #FabPulse #BuildWithGemini #Hackathon #Day1 #IndieHacker #SaaS #GoogleCloud
