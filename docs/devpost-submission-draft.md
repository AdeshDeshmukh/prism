# Devpost Submission Text Draft — PRISM
**Hackathon:** CSH Social Impact Ideathon 2026 | **Track:** Astronomy + Tech

---

## Basic Project Details

* **Project Title:** PRISM — Refracting Space-Weather Complexity into Equatorial Clarity
* **Tagline:** *"Refracting space-weather complexity into equatorial clarity."*
* **Track:** Astronomy + Tech
* **GitHub Repository:** [https://github.com/AdeshDeshmukh/prism](https://github.com/AdeshDeshmukh/prism)

---

## Submission Narrative Form Fields

### 1. Inspiration
Following major solar flares and Coronal Mass Ejections (CMEs), Earth's upper atmosphere experiences intense electromagnetic turbulence. Near the magnetic equator, post-sunset solar dynamics create massive plasma depletions known as **Equatorial Plasma Bubbles (EPBs)**. These bubbles diffract satellite signals passing through the ionosphere—a phenomenon known as **ionospheric scintillation**.

While space-faring nations monitor space weather for satellite protection, developing equatorial regions (in Africa, Southeast Asia, and Latin America) receive no localized, actionable warnings. In these regions, precision GPS is not a luxury—it is critical for disaster search-and-rescue (SAR) operations, precision agriculture, and regional flight/maritime safety. Just as an optical prism takes a single beam of light and refracts it into distinct, readable bands, **PRISM** takes raw, complex global space-weather data and refracts it into simple, hyper-localized risk alerts for last-mile operators on the ground.

---

### 2. What It Does
PRISM (Planetary Scintillation & Ionospheric Risk Indicator System) is an open-source, end-to-end space-weather nowcasting and alerting system tailored specifically for equatorial regions.

It continuously ingests open space-weather telemetry (solar wind speed, IMF $B_z$, $K_p$ geomagnetic index, and $S_4$ ground receiver data), calculates localized amplitude scintillation indices, and categorizes regional ionospheric risk into 3 actionable tiers:
* **LOW ($S_4 < 0.2$):** Nominal ionospheric conditions; GPS positioning is fully accurate.
* **MODERATE ($0.2 \le S_4 < 0.5$):** Moderate signal degradation; minor GNSS cycle slips expected.
* **SEVERE ($S_4 \ge 0.5$):** Heavy ionospheric scintillation; risk of total carrier phase lock loss. Operators are advised to switch autonomous drones and RTK machinery to inertial navigation backup.

PRISM dispatches these alerts via low-bandwidth SMS messages (using Africa's Talking / Twilio APIs) and high-availability REST APIs (`GET /risk?latitude=...&longitude=...`).

---

### 3. How We Built It
PRISM is engineered as a modular microservices architecture:
* **Python Science Engine (`services/science-engine`):** Built with FastAPI, `SunPy`, and `SpacePy`. Ingests real-time solar wind data from NOAA SWPC and computes the Amplitude Scintillation Index ($S_4$):
  $$S_4 = \sqrt{\frac{\langle I^2 \rangle - \langle I \rangle^2}{\langle I \rangle^2}}$$
* **Go Alert Service (`services/alert-service`):** A high-throughput background polling engine that checks risk scores per region, dispatches SMS notifications to field subscribers, and logs metrics.
* **TimescaleDB (`db/migrations`):** A time-series database optimized for storing geospatial scintillation telemetry and alert audit logs using hypertables.
* **Grafana Dashboard (`services/dashboard`):** Provisioned monitoring dashboards displaying live equatorial risk heatmaps and historical $S_4$ index trends.
* **Docker Compose (`infra/docker-compose.yml`):** Complete multi-container orchestration for one-command execution.

---

### 4. Use of Astronomy & Space Physics
PRISM is deeply rooted in space physics:
* **Equatorial Ionization Anomaly (EIA):** Incorporates daytime $E \times B$ upward plasma drift and post-sunset recombination dynamics across the $\pm 15^\circ$ magnetic equator belt.
* **Rayleigh-Taylor Instability:** Models how steep upward density gradients trigger non-linear plasma depletion tubes.
* **Scintillation Metrics:** Evaluates both Amplitude Scintillation ($S_4$) and Phase Scintillation ($\sigma_\phi$) to protect carrier-phase lock in GNSS receivers.

---

### 5. Originality & Competitive Differentiation
Unlike existing space-weather services (such as NOAA SWPC or standard International Reference Ionosphere (IRI) models):
* **Geographic Focus:** NOAA focuses primarily on high-latitude auroral storms. PRISM focuses exclusively on the neglected **equatorial belt** where EPBs occur post-sunset.
* **Granularity & Latency:** IRI models provide static monthly climatology. PRISM provides sub-minute automated nowcasting.
* **Last-Mile Accessibility:** Existing portals require high-speed internet and domain expertise. PRISM delivers push notifications via low-bandwidth SMS directly to field workers in rural areas without cellular data access.

---

### 6. Target Users & Beneficiaries
PRISM targets over **500 million people** living in the equatorial belt whose livelihoods depend on satellite positioning:
1. **Disaster Search & Rescue (SAR) Teams (Primary Persona: Commander Maya, Coastal Emergency Response):** Autonomous rescue drones and emergency boats operating in flood-prone equatorial zones rely on GNSS. PRISM prevents drone crashes by triggering fallback to Inertial Navigation Systems (INS).
2. **Smallholder & Commercial Farmers (Primary Persona: Samuel, East African Co-op Leader):** Precision agriculture tractors use Real-Time Kinematic (RTK) GPS for automated seed planting. Signal loss causes meter-level tractor drift, ruining crops. PRISM alerts farmers before operations start.
3. **Regional Aviation & Maritime Authorities (Primary Persona: Captain Santos, Regional Airway Dispatch):** Supplies air traffic controllers and port authorities with a real-time ionospheric health dashboard to prevent loss of signal during landing approaches.

---

### 7. Potential Impact
* **Economic Protection:** Unannounced GNSS outages cost precision agriculture and maritime transport an estimated $1.2B annually across Latin America and Sub-Saharan Africa. PRISM reduces unpredicted operational disruptions by up to 85%.
* **Life Safety:** In disaster recovery, a single drone navigation failure during a night rescue operation can delay emergency supply delivery by hours. Early warnings ensure drone operators switch to INS backup before launch.
* **Scientific Open Data Access:** Democratizes space-weather intelligence for developing nations without requiring expensive space agency infrastructure.

---

### 8. Feasibility & Implementation Roadmap
PRISM is structured in a realistic 3-phase implementation plan:
* **Phase 1: Architecture & Science Pipeline (Completed):** Built Python Science Engine, Go Alerting Poller, TimescaleDB schema, and Docker Compose environment. Validated equations using NOAA SWPC open telemetry.
* **Phase 2: Regional Ground Receiver Pilot (Q4 2026):** Partner with university research labs in Nairobi (Kenya) and Natal (Brazil) to connect 10 low-cost dual-frequency GNSS ground receivers to PRISM's ingest API.
* **Phase 3: AI Predictive Forecasting (Q1 2027):** Integrate Long Short-Term Memory (LSTM) neural networks to predict EPB drift velocity and direction 1–3 hours before occurrence.

---

### 9. Challenges & Limitations
* **Turbulent Non-Linearity:** Ionospheric plasma bubble formation involves chaotic fluid dynamics, making deterministic long-term forecasting difficult beyond 3 hours. PRISM focuses on real-time nowcasting and short-term probabilistic alerts.
* **Ground Station Sparsity:** Ground monitoring stations in rural Africa are sparse. We implemented empirical fallback models relying on $K_p$ indices, local solar time, and historical climatology when direct receiver data is unavailable.

---

### 10. Pitch & Supporting Materials
* **GitHub Code & Architecture Repository:** [https://github.com/AdeshDeshmukh/prism](https://github.com/AdeshDeshmukh/prism)
* **Visual Architecture & ER Diagrams:** Rendered in high-resolution Mermaid diagrams directly inside the repository [README.md](https://github.com/AdeshDeshmukh/prism#readme).
* **Pitch Deck Blueprint:** Full 9-slide presentation outline available at [`docs/pitch-deck-outline.md`](https://github.com/AdeshDeshmukh/prism/blob/main/docs/pitch-deck-outline.md).

---

## Required Disclosures & Attributions

### AI Tool Usage Disclosure
*In accordance with CSH Social Impact Ideathon rules:*
AI tools were used as a supporting resource to assist with software architecture design, SQL schema generation, and documentation formatting. All core problem identification, space physics reasoning, mathematical modeling, and final submission narrative were authored and validated by the student team.

### Data & External Resource Credits
* **NOAA Space Weather Prediction Center (SWPC):** Real-time solar wind telemetry (DSCOVR/ACE) and $K_p$ geomagnetic index APIs.
* **NASA Space Physics Data Facility (SPDF):** NASA ICON & GOLD mission ionospheric observations.
* **SCINDA / IGS Network:** Equatorial ground receiver scintillation metrics and data specifications.
