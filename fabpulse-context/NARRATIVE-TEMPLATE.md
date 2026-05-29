# FabPulse — Hackathon Narrative Template
# XPRIZE x Google: Build with Gemini
# Required: 500–1,000 words

---

> **Instructions:** This is a template. Replace all [BRACKETED] sections with your real data before submitting.
> Target length: 600–800 words. Be specific. Judges read hundreds of these — data beats claims.

---

## How FabPulse Operates with AI — and Why It Had to Be Built This Way

I work on the floor of a fabrication plant. Every day, I watched plant managers make critical decisions — job scheduling, staffing, delivery commitments — based on gut feeling, whiteboards, and spreadsheets that were outdated the moment they were printed.

The off-site construction industry — truss plants, wall panel manufacturers, modular builders — designs with precision engineering software. But it manages its production floor with tools from 1995. The result is a persistent operational blind spot: managers don't know their real cost of production, station progress is invisible until work physically moves, and any network disruption stops data collection entirely.

FabPulse was built to close that blind spot — with AI at its operational core.

---

### What AI Does vs. What Humans Do

**AI executes:**

- **Predictive scheduling (SEC Simulator):** Every job in FabPulse is continuously analyzed by a Monte Carlo simulation engine running on Vertex AI (Gemini). The model ingests current production velocity, team attendance, station throughput history, and remaining engineering hours — then runs [1,000+] simulation iterations to output P50, P70, and P95 completion dates. Plant managers receive a statistically grounded delivery date, not a guess. This runs automatically every time production data is updated — no human triggers it.

- **Generative monthly reports:** At period close, Gemini analyzes the plant's full dataset — efficiency trends, station yield, labor performance — and writes a narrative operations report: what worked, what didn't, and three concrete recommendations for the next period. A task that previously took managers 4–8 hours of manual spreadsheet work now happens in under 60 seconds, automatically.

- **Anomaly flagging:** When a station's lead time exceeds its historical average by more than [X%], the system flags it automatically and surfaces it on the manager dashboard. No rule needed to be configured — the AI benchmarks each station against its own baseline.

**Humans do:**

- Log task start and stop events at kiosk stations (this is the raw data input)
- Review AI-generated predictions and reports and decide whether to act on them
- Configure plant structure, job routes, and shift schedules in the admin panel
- Sell to new customers, provide support, and build product features

The ratio of AI-to-human decisions in production: for every manager decision, the platform has already executed [X] AI-driven analyses, simulations, and automated outputs.

---

### Building the Business

FabPulse launched its first production deployment on [DATE] at [YOUR PLANT NAME] — a [truss/wall panel/floor system] manufacturer in [CITY]. Real workers. Real jobs. Real production data.

Within [X] days, the system had logged [X] task events, run [X] SEC simulations via Vertex AI, and generated [X] automated reports. The offline sync architecture — a core design decision — proved its value on day [X] when the plant's Wi-Fi went down for [X] hours. Zero data was lost. Workers continued logging without interruption. The system synced silently when connectivity returned.

By [DATE], FabPulse had [X] paying plants generating $[MRR]/month in recurring revenue. Each plant signed up through a self-serve Stripe checkout — no sales call required. Onboarding from signup to live kiosk takes under 30 minutes.

The jobs and economic opportunities FabPulse creates:

- **Plant managers** gain 4–8 hours per month previously spent on manual reporting
- **Production supervisors** make staffing decisions with data instead of instinct — reducing overtime costs
- **Workers** get fair, data-backed visibility into their own efficiency scores
- **Potential:** As FabPulse scales, each plant deployment creates demand for a part-time FabPulse administrator role — someone who manages the platform, trains new workers, and interprets reports. This is a new job category the platform enables at scale.

---

### Why This Category (Small Business Services)

The [~4,200] truss and panel plants in North America are almost all small and mid-size businesses — family-owned operations with 15–80 workers, no dedicated IT department, and no budget for enterprise ERP. They are systematically underserved by software. FabPulse is priced and designed for them specifically: self-serve, no implementation consultant, operational within hours.

---

### The Stack That Makes It Real

FabPulse runs on Google Cloud Run (FastAPI backend), Supabase (PostgreSQL + Realtime), Vertex AI (Gemini for simulation and reports), and Firebase (offline sync bridge for kiosk nodes). Every AI call is logged in Google Cloud Logging — the execution trail is real, continuous, and auditable.

This is not a demo. It is a business, running in production, making money, with AI at its core.

---

*Revenue evidence, customer contacts, agent execution logs, and API usage records attached separately.*
