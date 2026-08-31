# PRISM — Refracting Space-Weather Complexity into Equatorial Clarity

> **Planetary Scintillation & Ionospheric Risk Indicator System**
> *Track:* Astronomy + Tech | *Event:* CSH Social Impact Ideathon 2026

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Track](https://img.shields.io/badge/Track-Astronomy%20%2B%20Tech-blue.svg)](#)

---

## 🌟 Concept Summary

Solar flares and coronal mass ejections disturb Earth's upper atmosphere. Near the geomagnetic equator, post-sunset Rayleigh-Taylor instabilities form **equatorial plasma bubbles (EPBs)**. These turbulence zones cause severe **ionospheric scintillation**—rapid fluctuations in GPS satellite signal phase and amplitude that degrade positioning accuracy from 1 meter to over 30 meters or cause complete loss of carrier lock.

While rich nations and space agencies (NOAA, NASA) track macro-scale space weather, equatorial developing regions—where precision GPS is vital for disaster response, maritime navigation, aviation, and agriculture—receive no localized, actionable warnings.

**PRISM** takes raw, complex public space-weather data (NOAA SWPC, NASA ICON, SCINDA) and **refracts it into hyper-localized, actionable risk signals** (Low, Moderate, Severe) delivered via lightweight SMS alerts and REST APIs to last-mile operators.

---

## 🏗️ System Architecture Overview

```
 [NOAA SWPC APIs] ──┐
 [NASA ICON Data]  ──┼──> [Python Science Engine] ──> Localized S4 Risk Score
 [SCINDA Network] ──┘         (FastAPI / SunPy)
                                      │
                                      ▼
                           [Go Alert Service] ───> [SMS Gateway: Africa's Talking / Twilio]
                                      │            (Disaster Coordinators, Farmers)
                                      ▼
                              [TimescaleDB]
                                      │
                                      ▼
                             [Grafana Dashboard]
```

---

## 🔬 Key Scientific Metrics

PRISM evaluates ionospheric health using the **Amplitude Scintillation Index ($S_4$)**:

$$S_4 = \sqrt{\frac{\langle I^2 \rangle - \langle I \rangle^2}{\langle I \rangle^2}}$$

* **$S_4 < 0.2$ (LOW):** Quiet ionosphere; nominal GPS accuracy.
* **$0.2 \le S_4 < 0.5$ (MODERATE):** Mild signal degradation; minor cycle slips.
* **$S_4 \ge 0.5$ (SEVERE):** Severe carrier lock loss; RTK GPS failure risk.

---

## 📂 Repository Structure

```
prism/
├── README.md                           # Project Overview & Setup
├── LICENSE                             # MIT License
├── .gitignore                          # Global Ignore Rules
├── docs/                               # Architecture, Research & Deck Outlines
│   └── research-notes.md               # Phase 1 Scientific Validation Brief
├── services/                           # Microservices
│   ├── science-engine/                 # Python Space-Weather Analytics (FastAPI)
│   ├── alert-service/                  # Go Polling & SMS Dispatch Engine
│   └── dashboard/                      # Grafana Dashboard Provisioning
├── db/                                 # TimescaleDB Migration Schemas
└── infra/                              # Docker Compose Deployment Specs
```

---

## 🚀 Quick Start (Local Development)

```bash
# Clone the repository (Local workspace)
cd prism

# Spin up full stack locally via Docker Compose (TimescaleDB, Science Engine, Alert Service, Grafana)
docker-compose -f infra/docker-compose.yml up --build
```

---

## 📜 Data Attributions & Acknowledgments

PRISM acknowledges open data provided by:
* **NOAA Space Weather Prediction Center (SWPC)** — Real-time solar wind & geomagnetic indices ($K_p$).
* **NASA Space Physics Data Facility (SPDF)** — NASA ICON & GOLD satellite ionospheric depletion data.
* **SCINDA / IGS Network** — Equatorial ground receiver scintillation metrics.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
