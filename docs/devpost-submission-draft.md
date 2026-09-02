# Devpost Submission Form Copy — PRISM
**Hackathon:** CSH Social Impact Ideathon 2026 | **Track:** Astronomy + Tech

---

## Submission Form Fields (Copy & Paste directly into Devpost)

### Project / Idea Name
`PRISM — Refracting Space-Weather Complexity into Equatorial Clarity`

### Tagline
`Refracting space-weather complexity into equatorial clarity.`

### Track
`Astronomy + Tech`

### GitHub Code Repository
`https://github.com/AdeshDeshmukh/prism`

---

### Problem Statement: What real-world problem are you addressing?
**Scale of the problem:** Over **4.5 billion GPS-enabled devices** operate globally, with more than **500 million users** in precision-GPS-dependent sectors—disaster response, precision agriculture, and regional aviation—concentrated in the equatorial belt across Sub-Saharan Africa, Southeast Asia, and Latin America.

Following major solar flares and Coronal Mass Ejections (CMEs), Earth's upper atmosphere experiences severe electromagnetic turbulence. Near the magnetic equator ($\pm 15^\circ$ latitude), post-sunset solar dynamics create massive ionospheric plasma depletions known as **Equatorial Plasma Bubbles (EPBs)**. These bubbles diffract satellite signals passing through the ionosphere—a phenomenon known as **ionospheric scintillation**.

When ionospheric scintillation strikes, Global Positioning System (GPS/GNSS) signals lose carrier phase lock, signal-to-noise ratios ($C/N_0$) plummet, and positioning accuracy degrades from 1 meter to over 30 meters or drops completely.

While space-faring nations monitor space weather to protect orbital satellites, developing equatorial regions receive **no localized, actionable last-mile warnings**. In these regions, precision GPS is critical for disaster search-and-rescue (SAR) drones, automated precision agriculture, regional flight navigation, and coastal maritime safety.

---

### Proposed Solution: What is your idea and how would it work?
**Plain-English Summary:**  
*PRISM is a real-time early-warning system that sends automated SMS text alerts to farmers, disaster rescue teams, and pilots in equatorial Africa and Latin America — warning them when GPS satellites are about to fail due to solar storms.*

Just as an optical glass prism takes a single beam of complex white light and refracts it into readable spectral bands, **PRISM (Planetary Scintillation & Ionospheric Risk Indicator System)** takes raw, complex planetary space-weather telemetry (solar wind speed, IMF $B_z$, $K_p$ geomagnetic index, and $S_4$ ground receiver data) and refracts it into 3 clear, actionable risk tiers:

* **LOW ($S_4 < 0.2$):** Quiet ionosphere; nominal GPS precision.
* **MODERATE ($0.2 \le S_4 < 0.5$):** Mild signal degradation; minor GNSS cycle slips expected. Recommend dual-frequency fallback.
* **SEVERE ($S_4 \ge 0.5$):** Heavy ionospheric scintillation; total carrier lock loss risk. **Field operators are advised to switch autonomous drones and RTK tractors to Inertial Navigation System (INS) backup.**

PRISM dispatches these alerts via low-bandwidth SMS messages (using Africa's Talking / Twilio APIs) directly to basic mobile phones without cellular internet, as well as via high-availability REST APIs (`GET /risk?latitude=...&longitude=...`).

---

### Technology Component: How does technology, science, or engineering contribute to the solution?
PRISM is deeply grounded in space physics and modern software engineering:

1. **Space Physics & Scintillation Mathematics:** Incorporates the Equatorial Ionization Anomaly (EIA) $E \times B$ plasma drift mechanics and Generalized Rayleigh-Taylor (GRT) Instability. Computes the **Amplitude Scintillation Index ($S_4$)**:
   $$S_4 = \sqrt{\frac{\langle I^2 \rangle - \langle I \rangle^2}{\langle I \rangle^2}}$$
   where $I$ is received GNSS signal intensity over 60-second intervals.
2. **Python Science Engine (`services/science-engine`):** Microservice built with FastAPI, `SunPy`, and `SpacePy` that continuously ingests open space-weather telemetry from NOAA SWPC and NASA SPDF.
3. **Go High-Throughput Alert Engine (`services/alert-service`):** Concurrent background worker routine built in Go that polls regional risk levels every 60 seconds and dispatches SMS alerts.
4. **TimescaleDB Time-Series Persistence (`db/migrations`):** PostgreSQL database optimized with hypertables for fast spatial and temporal indexing of scintillation telemetry.
5. **Grafana Real-Time Dashboard (`services/dashboard`):** Automated containerized dashboard displaying live equatorial risk heatmaps.
6. **Docker Compose Stack (`infra/docker-compose.yml`):** Single-command multi-container orchestration environment.

---

### Target Users or Beneficiaries: Who would benefit?
PRISM protects over **500 million people** living in the equatorial belt whose safety and economic stability depend on satellite positioning:

1. **Disaster Search & Rescue (SAR) Teams (Primary Persona: Commander Maya, Coastal Emergency Response):** Autonomous rescue drones and emergency boats operating in flood-prone equatorial zones rely on GNSS. PRISM prevents drone crashes by triggering early fallback to Inertial Navigation Systems (INS).
2. **Smallholder & Commercial Farmers (Primary Persona: Samuel, East African Co-op Leader):** Precision agriculture tractors use Real-Time Kinematic (RTK) GPS for automated seed planting. Signal loss causes meter-level tractor drift, ruining crops. PRISM alerts farmers before daily operations start.
3. **Regional Aviation & Maritime Authorities (Primary Persona: Captain Santos, Regional Airway Dispatch):** Supplies air traffic controllers and port authorities with a real-time ionospheric health REST API to prevent signal loss during landing approaches.

---

### Potential Impact: What could improve if the idea were implemented?
* **Economic Protection:** GPS-dependent precision agriculture and maritime logistics generate over **$300 Billion annually** across Sub-Saharan Africa and Latin America (World Bank Open Data, 2023). Early-warning systems analogous to PRISM — such as flood early-warning systems studied by the UNDRR — have demonstrated significant reductions in unplanned operational downtime for GPS-dependent equipment.
* **Life Safety in Disasters:** In emergency flood recovery, a single drone navigation failure during a nocturnal search mission can delay emergency supply delivery by critical hours. PRISM early warnings ensure drone operators switch to INS backup prior to launch, keeping life-saving operations on schedule.
* **Democratization of Space Science:** Makes complex space-weather intelligence accessible to developing nations without requiring multi-billion-dollar satellite infrastructure.
* **UN SDG Alignment:** PRISM directly contributes to **SDG 13 (Climate Action)** — by building resilience to space-weather-triggered infrastructure disruptions — and **SDG 9 (Industry, Innovation and Infrastructure)** — by providing open-source, low-cost scientific infrastructure for equatorial communities.

---

### Feasibility / Implementation Plan: How could this idea realistically be developed?
PRISM is structured in a practical, 3-phase implementation roadmap:

* **Phase 1: Science Engine & Microservices Architecture (Completed):** Engineered full monorepo codebase containing Python FastAPI engine, Go polling engine, TimescaleDB hypertables, Docker Compose stack, and Grafana dashboard. Validated $S_4$ equations using open NOAA SWPC telemetry.
* **Phase 2: Regional Ground Receiver Pilot (Q4 2026):** Partner with university research labs in Nairobi (Kenya) and Natal (Brazil) to connect 10 low-cost dual-frequency GNSS ground receivers to PRISM's ingest API. (Estimated pilot budget: $15,000 — eligible for the ITU Digital Innovation Fund or Google.org Impact Challenge.)
* **Phase 3: AI Predictive Forecasting (Q1 2027):** Train Long Short-Term Memory (LSTM) neural networks to predict EPB drift velocity and direction 1–3 hours before occurrence.

---

### Challenges or Limitations: What obstacles would need to be addressed?
* **Turbulent Non-Linearity:** Ionospheric plasma bubble formation involves chaotic fluid dynamics, making long-term deterministic forecasting beyond 3 hours difficult. PRISM focuses on real-time nowcasting and short-term probabilistic alerts (1–3 hours).
* **Ground Station Sparsity:** Ground monitoring stations in rural Africa are sparse. We implemented empirical fallback models relying on $K_p$ indices, local solar time (LST), and historical SCINDA climatology when direct receiver data is unavailable.
* **Field Worker Adoption:** Ground operators in remote equatorial regions may have limited digital literacy or no smartphone access. PRISM directly addresses this by deliberately designing for basic SMS delivery — no smartphone, no app, and no data connection required. Alerts are plain-text messages in simple, actionable language delivered to any feature phone.

---

### Pitch Materials: Presentation, Pitch Deck, Visual, or Supporting Material
* **🎨 Visual Pitch Deck — 9 Illustrated Slides (Primary Pitch Material):** [`https://github.com/AdeshDeshmukh/prism/blob/main/pitch/PITCH_DECK.md`](https://github.com/AdeshDeshmukh/prism/blob/main/pitch/PITCH_DECK.md)
* **💻 GitHub Repository & Full Open-Source Codebase:** [`https://github.com/AdeshDeshmukh/prism`](https://github.com/AdeshDeshmukh/prism)
* **📐 Visual Architecture, ER Diagrams & Data Flow Sequence:** High-resolution Mermaid diagrams embedded in [`README.md`](https://github.com/AdeshDeshmukh/prism#readme).

---

## Required Disclosures & Attributions

### AI Tool Usage Disclosure
*In accordance with CSH Social Impact Ideathon rules:*
AI tools were used as a supporting resource to assist with software architecture design, SQL schema generation, and documentation formatting. All core problem identification, space physics reasoning, mathematical modeling, and final submission narrative were authored and validated by the student team.

### Data & External Resource Credits
* **NOAA Space Weather Prediction Center (SWPC):** Real-time solar wind telemetry (DSCOVR/ACE) and $K_p$ geomagnetic index APIs.
* **NASA Space Physics Data Facility (SPDF):** NASA ICON & GOLD mission ionospheric observations.
* **SCINDA / IGS Network:** Equatorial ground receiver scintillation metrics and data specifications.
