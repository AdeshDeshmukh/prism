# PRISM — Pitch Deck Structure & Slide Blueprint
**Track:** Astronomy + Tech | **Hackathon:** CSH Social Impact Ideathon 2026

---

## Slide 1: Title & Tagline
* **Title:** PRISM (Planetary Scintillation & Ionospheric Risk Indicator System)
* **Tagline:** *"Refracting space-weather complexity into equatorial clarity."*
* **Track:** Astronomy + Tech
* **Team:** CyberSyntax Hub Social Impact Team
* **Visual:** Minimalist glassmorphic prism refracting a raw solar wind beam into green/yellow/red risk alerts over an equatorial Earth globe.

---

## Slide 2: The Hook & Real-World Problem
* **Headline:** *"When Space Weather Strikes the Equator, GPS Fails Without Warning."*
* **The Scenario:** Following an earthquake in an equatorial coastal zone, search-and-rescue (SAR) teams deploy autonomous drones and maritime boats. Post-sunset, GPS accuracy drops from 1 meter to >30 meters or loses carrier lock completely.
* **The Physics:** Solar flares trigger **Equatorial Plasma Bubbles (EPBs)** via Rayleigh-Taylor instability in the ionospheric $F$-region (200–500 km altitude), causing severe **ionospheric scintillation**.
* **Visual:** Split screen showing nominal GPS vs. degraded satellite signal trajectories passing through turbulent plasma bubbles.

---

## Slide 3: The Gap — Why Current Solutions Fail
* **The Macro Problem:** Space agencies (NOAA, NASA, ESA) broadcast global geomagnetic storm alerts ($K_p \ge 7$), but do not provide hyper-localized warnings where plasma bubbles form ($\pm 20^\circ$ latitude).
* **The Last-Mile Gap:** Existing tools export complex NetCDF4 ionograms for astrophysicists, missing last-mile workers (disaster coordinators, farmers, regional pilots) who need low-bandwidth alerts (SMS / REST APIs).
* **Visual:** Diagram showing raw complex data trapped at top levels vs. PRISM bridging the last-mile gap to ground operators.

---

## Slide 4: The Solution — PRISM
* **Core Concept:** Just as a glass prism refracts white light into distinct bands, PRISM ingests raw solar wind & ionospheric telemetry and refracts it into 3 clear, actionable risk tiers: **LOW**, **MODERATE**, **SEVERE**.
* **Key Innovation:**
  * Automated data ingestion (NOAA SWPC, NASA ICON, SCINDA receivers).
  * Real-time $S_4$ amplitude scintillation index calculation.
  * Low-latency alert dispatch (SMS via Africa's Talking / Twilio + REST APIs).
* **Visual:** High-level PRISM pipeline illustration.

---

## Slide 5: Scientific Foundation & Scintillation Modeling
* **The Science Metric:** Amplitude Scintillation Index ($S_4$):
  $$S_4 = \sqrt{\frac{\langle I^2 \rangle - \langle I \rangle^2}{\langle I \rangle^2}}$$
* **Operational Tiers:**
  * **$S_4 < 0.2$ (LOW):** Quiet ionosphere; nominal GPS precision.
  * **$0.2 \le S_4 < 0.5$ (MODERATE):** Mild signal degradation; minor cycle slips.
  * **$S_4 \ge 0.5$ (SEVERE):** Severe carrier lock loss; RTK tractor steering & drone SAR failure risk.
* **Visual:** $S_4$ waveform graph showing signal amplitude diffraction spikes.

---

## Slide 6: System Architecture & Tech Stack
* **Microservices Breakdown:**
  * **Python Science Engine (FastAPI & SunPy):** Ingests NOAA/SCINDA telemetry and computes $S_4$ risk scores.
  * **Go Alert Service:** High-throughput polling worker and SMS dispatch engine.
  * **TimescaleDB:** Time-series hypertable storing spatial readings and alert audit logs.
  * **Grafana Dashboard:** Live regional risk map and historical trend monitoring.
* **Visual:** Clean system architecture flowchart matching `docs/architecture.md`.

---

## Slide 7: Real-World Social Impact & Beneficiaries
1. **Disaster Response & SAR:** 1–2 hour advance warnings allow rescue teams to activate inertial navigation backups.
2. **Precision Agriculture:** Prevents RTK tractor steering failures in equatorial farming belts (East Africa, Latin America).
3. **Regional Aviation & Telecom:** Monitored flight corridors and port vessel navigation safety.
* **Visual:** 3 icon columns highlighting Disaster Response, Agriculture, and Maritime Aviation.

---

## Slide 8: Feasibility, Phased Rollout & Challenges
* **Phase 1 (Current):** Nowcasting engine using public NOAA SWPC & synthetic SCINDA feeds.
* **Phase 2 (Future):** Regional partnerships with equatorial university GNSS receivers for ground telemetry validation.
* **Honest Boundaries:** Acknowledging 1–3 hour forecast limits due to non-linear plasma turbulence.
* **Visual:** Phased roadmap timeline graphic.

---

## Slide 9: Conclusion & Devpost Link
* **Summary:** PRISM makes space-weather complexity understandable and actionable for the communities that need it most.
* **Open Source Repo:** `github.com/AdeshDeshmukh/prism`
* **Track:** Astronomy + Tech
