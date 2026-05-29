# FabPulse — The Pulse of Precision Manufacturing

---

## Inspiration

This didn't start as a startup idea. It started as a frustration.

I'm an electronics engineer, specialized in industrial control and instrumentation. Five years ago, I moved from Colombia to Canada and started working at a truss and wall panel manufacturing plant — not as an engineer, but as a production worker. I was on the floor every day, building the same structures I could have designed on paper.

And every day, I watched the same thing happen.

A person — sometimes two — would spend their entire shift transcribing information by hand. Production sheets to Excel. Cut times, assembly times, lumber quantities, metal plates used per job — all of it copied manually, row by row, into spreadsheets that were already wrong by the time they were finished. The data was late, it was inaccurate, and nobody trusted it enough to make real decisions from it.

I knew there had to be a better way. And I had a computer at my station.

So I built one.

With what I had available — a plant computer and the Visual Basic editor inside Microsoft Excel — I built the first version of what would eventually become FabPulse. It wasn't elegant. But it worked. Each workstation had its own interface. The files talked to each other. Data flowed from the stations to a central plant file automatically. No more manual transcription. No more end-of-day data entry marathons.

Then I built the manager file — a separate interface where the supervisor could dispatch jobs to stations, review production data, add employees, correct operator errors, and track lumber and plate quantities by project. It pulled everything together: cut times, assembly times, material consumption — aggregated instantly, in real time, from a simple Excel dashboard.

My coworkers started using it. The transcription person got reassigned to more valuable work. The data got cleaner. The manager started trusting the numbers.

That's when I realized: *this isn't a spreadsheet. This is a product.*

The problem I had solved wasn't unique to my plant. Every truss plant, every wall panel manufacturer, every modular builder in North America was running the same manual process — because nobody had built them a real alternative. The software industry had never looked closely enough at the production floor to understand what was actually happening there.

I had. Because I was there.

From that Excel VBA system, I moved to Python for the analytics layer — cleaner data made more sophisticated reporting possible. Then came the dashboard. Then the KPI engine. Then the realization that to serve any plant — not just mine — the system needed to be configurable, cloud-native, and independent of Excel entirely.

That evolution became FabPulse: a platform that any fabrication plant can configure to its own stations, workflows, and processes — and that uses AI to turn production data into decisions, not just reports.

The hackathon didn't create this idea. The plant floor did.

---

## What It Does

FabPulse is a cloud-native SaaS platform that transforms analog fabrication plants into data-driven operations. It has three layers that work together:

**Kiosk PWA — the plant floor interface.** Each workstation (saws, assembly tables, finishing stations) runs a Progressive Web App locked in fullscreen kiosk mode. Workers check in with a PIN and log task start/stop events with a single tap. The kiosk works fully offline — if the factory Wi-Fi drops, workers continue without interruption. Data queues locally and syncs automatically the moment connectivity returns. No data loss. No manual intervention.

**Manager Dashboard — real-time operations visibility.** Plant managers see a live job board: every active job, which station it's at, which worker is on it, and how long it's been running. The Labor Efficiency Index (LEI) compares engineering-estimated hours against actual floor time per job, per station, and per worker — updated continuously. Bottlenecks surface visually before they become crises.

**SEC Simulator — predictive scheduling powered by Vertex AI.** The Scheduled End of Construction Simulator answers the question every plant manager dreads: *"When will this job actually be done?"*

Using Monte Carlo simulation running on Gemini, the model samples daily production velocity and runs $N = 1{,}000$ iterations per job:

$$v_i \sim \mathcal{N}(\bar{v} \cdot a,\ \sigma_v^2)$$

Where $\bar{v}$ is historical daily output, $a$ is current attendance rate, and $\sigma_v^2$ is observed output variance. The result is three statistically grounded delivery dates:

| Confidence | Use Case |
|---|---|
| $P_{50}$ | Most likely completion under current conditions |
| $P_{70}$ | Confident estimate for client commitments |
| $P_{95}$ | Conservative date for high-stakes contracts |

Managers adjust variables interactively — add a shift, simulate losing workers, reprioritize a batch — and predictions update instantly.

**Generative Reports.** At period close, Gemini analyzes the full dataset and writes a narrative monthly operations report: efficiency trends, top performers, bottleneck identification, and three concrete recommendations. A task that previously took 4–8 hours of manual spreadsheet work now takes under 60 seconds, triggered automatically.

---

## How I Built It

### From Excel VBA to Cloud-Native SaaS — My Journey

The first version was built entirely inside Microsoft Excel's Visual Basic editor — individual station files that communicated with a central plant file, feeding a manager dashboard that tracked jobs, materials, and labor in real time. It was the right tool for the environment: no installation, no IT department, no budget required.

When the data layer matured and the limitations of Excel became the bottleneck, the analytics layer moved to Python. Cleaner data enabled more sophisticated reporting. That Python layer became the foundation for the current FastAPI backend.

FabPulse today is the full evolution of that original system — rebuilt from scratch on modern infrastructure, configurable for any plant, and independent of Excel entirely.

### Current Architecture

```
Manager Dashboard (React + Vite + TypeScript)
        │
        ▼
   FastAPI Backend ──── Google Cloud Run
        │
        ├── Supabase (PostgreSQL + Realtime + Auth + RLS)
        ├── Vertex AI — Gemini 1.5 Pro (SEC Simulator + Reports)
        ├── Firebase (Offline sync bridge)
        └── BigQuery (Analytics warehouse + AI execution logs)

Kiosk PWA (React + Workbox Service Worker)
        │
        ├── Online  → POST tasks directly to API (< 500ms)
        └── Offline → Queue in IndexedDB → Background Sync on reconnect
```

### Offline Sync

The kiosk intercepts failed network requests and queues them in IndexedDB. When connectivity returns, Background Sync replays the queue chronologically:

```typescript
async function logTask(payload: TaskPayload) {
  try {
    await api.post('/tasks', payload);
  } catch {
    if (!navigator.onLine) {
      await offlineQueue.add({
        endpoint: '/tasks',
        payload,
        queued_at: new Date().toISOString()
      });
    }
  }
}
```

### SEC Simulator — Bayesian Cold Start

New plants have limited historical data, making variance estimation unreliable early on. I implemented a Bayesian prior seeded from industry benchmarks for the first 30 days, gradually replaced by the plant's own observed variance as data accumulated:

$$\sigma_v^2 \leftarrow \frac{n \cdot \hat{\sigma}^2 + n_0 \cdot \sigma_0^2}{n + n_0}$$

Where $n_0$ is the prior sample weight and $\sigma_0^2$ is the industry baseline variance. This gives new plants meaningful predictions from day one instead of wildly uncertain intervals.

---

## Challenges I Ran Into

**Reliable offline sync on Android tablets.** Background Sync API has inconsistent support across Android versions — the most common kiosk device in plant environments. I went through three implementations before landing on a Workbox-based approach stable across all devices tested on a real production floor.

**UX for workers who don't think in "sessions."** Early prototypes had confirmation dialogs, success notifications, and loading spinners. Workers on the floor didn't want any of it. Every piece of UI I removed made the product faster and better received. The final kiosk has exactly three screens: check in, active job, task complete. Anything beyond that was noise.

**Compressing a 6-month sales cycle into weeks.** Manufacturing software typically takes 6–18 months to sell. I made FabPulse fully self-serve — a plant manager can sign up, configure their plant, and deploy a live kiosk in under 30 minutes with no sales call required. That was an engineering and UX challenge as much as a business one.

**Monte Carlo accuracy with small datasets.** Early in a plant's lifecycle, limited historical data means high uncertainty in $\sigma_v^2$. Without the Bayesian prior, the spread between $P_{50}$ and $P_{95}$ was so wide it was useless. Getting cold-start behavior right took multiple iterations of the model.

---

## Accomplishments I'm Proud Of

**It was tested on a real plant floor — from day one.** Not a sandbox. Not a mock environment. Real workers, real jobs, real production data. The offline sync survived an actual network outage with zero data loss.

**The journey from Excel VBA to Vertex AI.** The same problem that was first solved with a macro inside a spreadsheet is now solved with Monte Carlo simulation running on Google's most capable AI model. That's the full arc — and it's real.

**AI that makes a decision, not just a chart.** The SEC Simulator doesn't show a graph of past performance — it tells you, with statistical confidence, when your job will be done. That's a fundamentally different kind of software, and plant managers responded to it immediately.

**Self-serve onboarding in under 30 minutes.** From Stripe checkout to live kiosk on the floor — no implementation consultant, no IT department, no configuration calls. That's a first for this industry.

**Domain expertise that can't be faked.** Understanding the difference between how a truss plant routes jobs versus a wall panel division — and building software that reflects that operational reality — comes from having worked that floor. It's a moat no generalist team can replicate quickly.

---

## What I Learned

**Start with what you have.** The first version of FabPulse ran inside Excel. It wasn't scalable, it wasn't elegant, and it was exactly right for where the product needed to start. The constraint forced clarity about what actually mattered: clean data, real time, zero manual transcription.

**Offline-first is not a feature — it's a constraint.** If you don't design for offline from day one in an industrial environment, you will rebuild your entire data layer mid-project. I learned this early enough to fix it. Most industrial software doesn't learn it until a client complains.

**Trust is earned in 45 seconds.** My first beta user spent less than a minute with the kiosk and said: *"This is basically what we already do, but the computer remembers it."* That reaction — zero learning curve, immediate recognition — means the product is working correctly.

**Prediction beats reporting every time.** Every plant manager I spoke to said the same thing: they don't need more reports about what already happened — they need to know what's going to happen in time to do something about it. That single insight shaped every AI decision I made.

**AI is most powerful when it's invisible.** The best reaction I got wasn't "wow, this has AI." It was "this just tells me what I need to know." When AI is doing its job right, nobody comments on the technology. They comment on the outcome.

---

## What's Next for FabPulse

FabPulse is a business, not a hackathon project. The competition was the forcing function — the goal is to become the operational standard for the off-site construction industry.

### Currently In Development

**Anomaly detection — from reactive to proactive** *(in development)*
When a station's lead time exceeds its historical baseline by a meaningful margin, FabPulse flags it automatically — before it cascades into a missed delivery date. Currently managers discover bottlenecks when it's already too late. This feature makes the system a proactive advisor, not just a recorder. The detection engine is built on top of the same production data already flowing through the platform — no new data collection required.

**Multi-plant dashboard** *(in development)*
For companies operating more than one facility, a unified view across all plants — efficiency, throughput, active jobs, and bottlenecks — from a single screen. Companies with two or three plants currently have no way to compare performance across facilities or identify which plant is underperforming. This closes that gap.

### Near-Term Roadmap

**MiTek / Alpine bidirectional integration — closing the full loop.**
Today, engineers design jobs in MiTek or Alpine and export estimated hours — which someone then types manually into FabPulse. The next step is a direct API integration in both directions:

- *Inbound:* FabPulse pulls job specs and engineering hours automatically from MiTek the moment a design is approved. Zero manual entry.
- *Outbound:* FabPulse sends real production data back to MiTek — actual times vs. estimated, material consumption, station performance. Engineers see how their designs perform on the real floor and can refine future estimates based on ground truth.

This closes the loop between design and production that has never been closed before in this industry.

**Mobile batch tracking with QR / barcode scanning.**
Today, workers identify jobs on the kiosk by searching or typing a job number — which introduces errors and slows down the logging process. The next version introduces a mobile scanning layer:

- Workers or supervisors scan a QR code or barcode on the physical batch with a phone camera
- The job loads instantly — no search, no typing, no errors
- The scan is also a location event: FabPulse knows which station the batch is at, when it arrived, and how long it stays there

This turns physical batch movement into real-time location data — giving managers a live map of where every job is on the plant floor at any moment. Something that today is completely invisible.

### The Bigger Picture

The off-site construction market is valued at over $130B globally and growing at 6.5% CAGR. Software penetration in plant operations remains below 15%. Every plant still running on spreadsheets and whiteboards is a potential FabPulse customer.

The MiTek integration alone opens a partnership channel with the dominant design software in the industry — a distribution lever that no competitor currently has.

The plant floor has always had a pulse. I built the monitor.
