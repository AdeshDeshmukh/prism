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
PRISM (Planetary Scintillation & Ionospheric Risk Indicator System) is an open-source, end-to-end space-weather nowcasting and alerting system. 

It continuously ingests open space-weather telemetry (solar wind speed, IMF $B_z$, $K_p$ geomagnetic index, and $S_4$ ground receiver data), calculates localized amplitude scintillation indices, and categorizes regional ionospheric risk into 3 actionable tiers:
* **LOW ($S_4 < 0.2$):** Nominal ionospheric conditions; GPS positioning is fully accurate.
* **MODERATE ($0.2 \le S_4 < 0.5$):** Moderate signal degradation; minor GNSS cycle slips expected.
* **SEVERE ($S_4 \ge 0.5$):** Heavy ionospheric scintillation; risk of total carrier phase lock loss. Operators are advised to switch autonomous drones and RTK machinery to inertial navigation backup.

PRISM dispatches these alerts via low-bandwidth SMS messages (using Africa's Talking / Twilio) and high-availability REST APIs (`GET /risk?latitude=...&longitude=...`).

---

### 3. How We Built It
PRISM is engineered as a modular microservices architecture:
* **Python Science Engine (`services/science-engine`):** Built with FastAPI, `SunPy`, and `SpacePy`. Ingests real-time solar wind data from NOAA SWPC and computes the Amplitude Scintillation Index ($S_4$):
  $$S_4 = \sqrt{\frac{\langle I^2 \rangle - \langle I \rangle^2}{\langle I \rangle^2}}$$
* **Go Alert Service (`services/alert-service`):** A high-throughput background polling engine that checks risk scores per region, dispatches SMS notifications to field subscribers, and logs metrics.
* **TimescaleDB (`db/migrations`):** A time-series database optimized for storing geospatial scintillation telemetry and alert audit logs using hypertables.
* **Grafana Dashboard (`services/dashboard`):** Provisioned monitoring dashboards displaying live equatorial risk maps and historical $S_4$ index trends.
* **Docker Compose (`infra/docker-compose.yml`):** Complete one-command containerization for local execution and deployment.

---

### 4. Use of Astronomy & Space Physics
PRISM is deeply rooted in space physics:
* **Equatorial Ionization Anomaly (EIA):** Incorporates the daytime $E \times B$ upward plasma drift and post-sunset recombination dynamics.
* **Rayleigh-Taylor Instability:** Models how steep upward density gradients trigger non-linear plasma depletion tubes.
* **Scintillation Metrics:** Evaluates both Amplitude Scintillation ($S_4$) and Phase Scintillation ($\sigma_\phi$) to protect carrier-phase lock in GNSS receivers.

---

### 5. Social Impact & Beneficiaries
1. **Disaster Search & Rescue (SAR):** Prevents autonomous rescue drones and maritime search vessels from suffering navigation failures during nocturnal search missions in equatorial coastal areas.
2. **Precision Agriculture:** Warns farmers in East Africa and South America before phase scintillation breaks Real-Time Kinematic (RTK) tractor guidance, preventing crop damage.
3. **Regional Aviation & Telecom:** Provides flight dispatchers and port authorities with a real-time ionospheric health dashboard.

---

### 6. Challenges We Ran Into
* **Turbulent Non-Linearity:** Ionospheric plasma bubble formation involves chaotic Rayleigh-Taylor fluid dynamics, making long-term deterministic forecasting difficult. We limited our operational model to 1–3 hour nowcasting and short-term probabilistic forecasting.
* **Ground Receiver Sparsity:** Real-time $S_4$ ground monitoring stations are sparse in rural equatorial regions. We developed empirical fallback models relying on $K_p$ indices, local solar time, and historical climatology.

---

### 7. Accomplishments That We're Proud Of
* Designed and built a complete monorepo microservices architecture connecting Python, Go, TimescaleDB, and Grafana.
* Maintained a strict, clean Git workflow on GitHub ([AdeshDeshmukh/prism](https://github.com/AdeshDeshmukh/prism)) using feature branches and Pull Requests.
* Translated complex space physics equations into simple, human-readable SMS alerts for non-technical ground workers.

---

### 8. What We Learned
* How solar wind parameters (DSCOVR/ACE $v_{sw}$ and IMF $B_z$) directly influence equatorial ionospheric electric fields.
* Best practices for timeseries data modeling using TimescaleDB hypertables.
* Designing resilient last-mile notification systems for low-bandwidth environments.

---

### 9. What's Next for PRISM
* **Ground Receiver Partnerships:** Collaborating with equatorial universities to ingest real-time GNSS receiver telemetry.
* **Machine Learning Trajectory Prediction:** Integrating LSTM networks to forecast plasma bubble drift paths across equatorial longitudinal sectors.

---

## Required Disclosures & Attributions

### AI Tool Usage Disclosure
*In accordance with CSH Social Impact Ideathon rules:*
AI tools were used as a supporting resource to assist with software architecture design, SQL schema generation, and documentation formatting. All core problem identification, space physics reasoning, mathematical modeling, and final submission narrative were authored and validated by the student team.

### Data & External Resource Credits
* **NOAA Space Weather Prediction Center (SWPC):** Solar wind telemetry (DSCOVR/ACE) and $K_p$ geomagnetic index APIs.
* **NASA Space Physics Data Facility (SPDF):** NASA ICON & GOLD mission ionospheric observations.
* **SCINDA / IGS Network:** Equatorial ground receiver scintillation metrics and data specifications.
