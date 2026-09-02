# PRISM — Official Pitch Deck Presentation
**Track:** Astronomy + Tech | **Hackathon:** CSH Social Impact Ideathon 2026

---

## 📸 Presentation Visual Slides

![Slide 1: Title Slide](slides/slide-01-title.jpg)

---

### Slide 1: Title & Vision
* **Title:** PRISM — Refracting Space-Weather Complexity into Equatorial Clarity
* **Subtitle:** Planetary Scintillation & Ionospheric Risk Indicator System
* **Track:** Astronomy + Tech
* **Vision:** Democratizing real-time space-weather early warnings for developing nations in equatorial belts.

---

### Slide 2: The Hook & Real-World Problem
* **Headline:** *"When Space Weather Strikes the Equator, GPS Fails Without Warning."*
* **The Problem:** Following solar flares, post-sunset **Equatorial Plasma Bubbles (EPBs)** form via Rayleigh-Taylor instabilities in the ionosphere (200–500 km altitude).
* **The Impact:** Signals diffract, causing **ionospheric scintillation**. GPS positioning accuracy drops from 1 meter to over 30 meters or suffers total loss of carrier lock.
* **Who Suffers:** Disaster rescue drones, precision agriculture tractors, and regional coastal vessels.

---

### Slide 3: The Gap — Why Existing Solutions Fail
* **Planetary Focus vs. Regional Reality:** NOAA SWPC and ESA monitor global planetary storms ($K_p \ge 7$), but ignore hyper-localized equatorial plasma bubble dynamics.
* **Academic Complexity:** Tools like International Reference Ionosphere (IRI) output complex NetCDF4 files meant for astrophysicists — impossible for field workers to use.
* **Connectivity Blindspot:** Existing dashboards require high-speed broadband. Rural equatorial zones need low-bandwidth SMS alerts.

---

![Slide 4: System Architecture & Data Flow](slides/slide-04-solution.jpg)

---

### Slide 4: The Solution — PRISM Architecture
* **Ingestion:** Open space-weather APIs (NOAA SWPC solar wind, NASA ICON/GOLD, SCINDA ground stations).
* **Science Engine:** Python FastAPI engine calculating real-time Amplitude Scintillation ($S_4$) index.
* **Storage:** TimescaleDB time-series hypertables logging geospatial readings.
* **Alert Poller:** High-throughput Go service dispatching automated SMS warnings via Africa's Talking / Twilio.
* **Dashboard:** Provisioned Grafana risk heatmap.

---

### Slide 5: Scientific Foundation & $S_4$ Scintillation Modeling
* **Mathematical Model:**
  $$S_4 = \sqrt{\frac{\langle I^2 \rangle - \langle I \rangle^2}{\langle I \rangle^2}}$$
* **Operational Risk Tiers:**
  * 🟢 **LOW ($S_4 < 0.2$):** Nominal conditions; full GNSS precision.
  * 🟡 **MODERATE ($0.2 \le S_4 < 0.5$):** Mild signal degradation; minor cycle slips.
  * 🔴 **SEVERE ($S_4 \ge 0.5$):** Heavy scintillation; high carrier lock loss risk. **Switch to Inertial Navigation (INS)**.

---

### Slide 6: System Microservices Breakdown
* **Python Science Engine (`services/science-engine`):** Solar wind data parser, $S_4$ index math, REST API endpoints.
* **Go Alert Engine (`services/alert-service`):** Concurrent background worker routine querying database every 60s.
* **TimescaleDB (`db/migrations`):** Hypertable data partition strategy for fast geospatial time-series indexing.
* **Docker Compose (`infra/docker-compose.yml`):** Single-command multi-container deployment.

---

![Slide 7: Real-World Social Impact & Beneficiaries](slides/slide-07-impact.jpg)

---

### Slide 7: Real-World Social Impact & Beneficiaries
1. **Disaster Search & Rescue (SAR) Drones:** Prevents drone crashes during flood/earthquake night searches by alerting operators to activate INS backup.
2. **Precision Agriculture:** Protects RTK tractor guidance systems from losing carrier phase lock, preventing crop damage across East Africa and South America.
3. **Regional Aviation & Maritime:** Supplies port authorities and airfield dispatchers with a real-time ionospheric health REST API.

---

### Slide 8: Feasibility & 3-Phase Implementation Roadmap
* **Phase 1: Science Engine & Microservices (Completed):** Open-source codebase, Docker Compose stack, database migrations, and REST API.
* **Phase 2: Regional Receiver Pilot (Q4 2026):** Partnering with university research labs in Nairobi (Kenya) and Natal (Brazil) for 10 dual-frequency ground receiver nodes.
* **Phase 3: AI Predictive Forecasting (Q1 2027):** Integrating LSTM neural networks to forecast plasma bubble drift trajectories 1–3 hours ahead.

---

### Slide 9: Conclusion & Call to Action
* **Open Source Repository:** [https://github.com/AdeshDeshmukh/prism](https://github.com/AdeshDeshmukh/prism)
* **Track:** Astronomy + Tech | **CSH Social Impact Ideathon 2026**
* **Tagline:** *"Refracting space-weather complexity into equatorial clarity."*
