# FabPulse: Operational Intelligence for Off-Site Construction

**One-liner:** FabPulse transforms analog fabrication plants into data-driven operations — delivering real-time production visibility, predictive scheduling, and AI-generated reporting through a cloud-native platform built for the realities of the factory floor.

---

## 1. The Problem

The off-site construction industry — truss plants, wall panel manufacturers, modular builders — designs with precision engineering software but manages production with spreadsheets, whiteboards, and institutional memory.

This creates a critical operational blind spot:

- **Plant managers don't know their real cost of production** until a job is done — sometimes weeks later
- **Station progress is invisible** until work physically moves to the next stage
- **Any network disruption halts data collection**, creating gaps that corrupt reporting
- **Completion dates are guesses**, not predictions — leading to missed deadlines and broken client trust

This isn't a niche problem. The off-site construction market is valued at over **$130B globally** and growing at 6.5% CAGR, yet operational software penetration remains below 15%. Most plants are running a 21st-century product with 20th-century operations management.

---

## 2. The Solution

FabPulse is a **cloud-native SaaS platform** with offline-resilient edge nodes, purpose-built for fabrication plants. It closes the operational blind spot by making every station, every batch, and every labor hour visible — in real time.

### Architecture: Cloud-First, Offline-Tolerant

Most industrial software fails in one of two ways: it requires constant connectivity, or it stores data locally and never integrates. FabPulse solves both.

**Cloud Core (FastAPI + PostgreSQL/Supabase):** The system of record lives in the cloud. Managers access a live operations dashboard from any device — monitoring active jobs, attendance, shift efficiency, and station throughput in real time.

**PWA Kiosk Nodes (Edge Resilience):** Each workstation — saws, assembly tables, finishing stations — runs a Progressive Web App in kiosk mode. These nodes operate in two modes seamlessly:

- **Online:** Every task start/stop syncs instantly to the cloud, updating all dashboards in real time
- **Offline:** If the factory network goes down, workers continue logging without interruption. All data is queued in IndexedDB locally
- **Background Sync:** The moment connectivity returns, the queue flushes silently and chronologically — no data loss, no manual intervention

This architecture is not a workaround. It's a deliberate design decision that makes FabPulse deployable in environments where competitors simply don't work.

---

## 3. Core Features

### A. Dynamic Production Management

- **Job Lifecycle Control:** Full tracking from intake to delivery through configurable production routes (e.g., Cut → Frame → QC → Shipped)
- **Live Dispatch:** Managers push job assignments, priority changes, and critical notes directly to station screens from the cloud dashboard
- **Multi-Tenant Configuration:** Every plant defines its own divisions, stations, and workflows — no rigid templates, no expensive customization projects

### B. Real-Time Operations Analytics

- **Labor Efficiency Index:** Compares engineering-estimated time against actual floor time per job, per station, and per worker — updated continuously
- **Station Yield & Lead Time:** Identifies which stations complete the most batches and which create the longest delays — pinpointing bottlenecks visually before they become crises
- **Shift Dashboard:** Live attendance, active job count, and efficiency score for every shift — giving supervisors a single screen to manage the floor

### C. Predictive Scheduling — SEC Simulator

The SEC (Scheduled End of Construction) Simulator is FabPulse's core differentiator.

Rather than reporting what already happened, SEC predicts what will happen — with statistical confidence.

Using **Monte Carlo simulation**, the engine runs thousands of scenarios based on current production velocity, team attendance, station capacity, and historical variance. It outputs:

- **50th percentile:** Most likely completion date under normal conditions
- **70th percentile:** Confident delivery estimate for client commitments
- **95th percentile:** Conservative date for high-stakes contracts

Plant managers can adjust variables interactively — simulate the impact of adding a shift, losing two workers, or reprioritizing a batch — and see updated predictions instantly. No other tool in this space does this.

### D. Generative Reporting

FabPulse auto-generates monthly and annual performance reports in PDF — without any manual input. Each report includes:

- Efficiency trends by station, shift, and job type
- Top performers highlighted by labor efficiency score
- **AI-written narrative analysis:** What worked well, areas of concern, recommended actions for next period

Reports are ready the morning after period close — a task that currently takes plant managers 4–8 hours of manual spreadsheet work.

---

## 4. Market & Business Model

**Target Market:**
- Primary: Truss, wall panel, and floor system manufacturers in North America (~4,200 plants)
- Secondary: Modular home builders, steel framing manufacturers, and prefab MEP shops
- Total addressable market: $1.8B in operational software spend for off-site construction (US + Canada)

**Pricing (SaaS Subscription):**

| Tier | Target | Price |
|---|---|---|
| Starter | 1 plant, up to 5 stations | $299/month |
| Growth | 1 plant, unlimited stations | $599/month |
| Pro | Multi-plant, API access, custom reports | $1,499/month |

**Unit Economics:** Target payback period under 90 days for a mid-size plant — based on documented efficiency gains of 12–18% in comparable manufacturing digitization deployments.

---

## 5. Competitive Landscape

| | FabPulse | Procore | Fishbowl | Custom ERP |
|---|---|---|---|---|
| Off-site construction focus | ✅ | ❌ | ❌ | Partial |
| Real-time station tracking | ✅ | ❌ | ❌ | Rare |
| Offline resilience | ✅ | ❌ | ❌ | ❌ |
| Predictive scheduling | ✅ | ❌ | ❌ | ❌ |
| Generative reports | ✅ | ❌ | ❌ | ❌ |
| Setup time | Days | Months | Weeks | 6–18 months |
| Price | $299–1,499/mo | $10K+/yr | $4K+/yr | $50K–500K |

No existing tool combines real-time floor tracking, offline resilience, and predictive scheduling for this specific industry. FabPulse is not competing against enterprise ERP — it's filling a gap those systems explicitly ignore.

---

## 6. Why FabPulse Wins

FabPulse is not a hackathon idea built around a technology. It's a technology built around a documented, expensive, and largely unsolved industry problem.

Three things make it defensible:

**Domain depth.** The system models the actual workflows of truss and panel manufacturing — job routes, station types, batch logic, labor efficiency calculations — not generic "manufacturing." This specificity is a moat.

**Architecture that works in the real world.** Offline resilience isn't a feature — it's the reason plants with unreliable Wi-Fi can actually adopt the platform. Competitors skip this. We built it in from day one.

**Prediction, not just reporting.** Every competitor in this space shows you what happened. FabPulse shows you what's going to happen — and lets you change it. The SEC Simulator turns a dashboard into a decision-making tool.

---

> *FabPulse gives fabrication plants real-time visibility into their production — so they can cut waste, fix bottlenecks, and protect their margins.*

---

*FabPulse Brand Guide v1.0 · The Pulse of Precision Manufacturing · Confidential*
