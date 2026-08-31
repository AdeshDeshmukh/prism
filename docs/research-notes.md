# PRISM — Research & Problem Validation Notes
**Track:** Astronomy + Tech | **Hackathon:** CSH Social Impact Ideathon 2026

---

## 1. Executive Summary & Core Value Proposition

Near the Earth's magnetic equator, post-sunset solar dynamics trigger massive plasma depletions in the ionosphere known as **equatorial plasma bubbles (EPBs)**. These turbulence zones cause **ionospheric scintillation**—rapid, intense fluctuations in the amplitude and phase of trans-ionospheric radio signals.

The impact is severe: Global Positioning System (GPS/GNSS) signals lose lock, signal-to-noise ratios ($C/N_0$) drop sharply, and positioning errors spike from centimeters to tens of meters or fail entirely.

While space agencies (NOAA, NASA, ESA) track planetary space weather, their public alerts focus on global geomagnetic storm indices ($K_p$, $D_{st}$). They fail to provide **localized, actionable, last-mile warnings** for equatorial regions in developing nations where precision GPS is critical for disaster response, maritime navigation, aviation, and agriculture.

**PRISM (Planetary Scintillation & Ionospheric Risk Indicator System)** bridges this gap by ingesting raw solar wind and ionospheric data, calculating localized $S_4$ scintillation risk scores, and delivering low-bandwidth alerts (SMS & REST APIs) directly to regional operators.

---

## 2. Scientific & Physical Foundations

### 2.1 The Equatorial Ionization Anomaly (EIA) & Rayleigh-Taylor Instability
* **Mechanics:** Near the magnetic equator, the solar EUV radiation creates high plasma density in the ionosphere's $F$-region (200–500 km altitude). During daytime, the vertical $E \times B$ drift lifts plasma upward, which then diffuses downward along geomagnetic field lines to $\pm 15^\circ$ magnetic latitude, forming the two crests of the Equatorial Ionization Anomaly (EIA).
* **Nighttime Instability:** After sunset, solar ionization stops and the bottomside $F$-region recombines quickly, creating a steep upward plasma density gradient. This inverted density configuration triggers the **Generalized Rayleigh-Taylor (GRT) Instability**.
* **Bubble Formation:** Low-density plasma from the bottomside surges upward through the dense $F$-region peak, creating non-linear plasma depletion tubes or "plasma bubbles" spanning thousands of kilometers along magnetic field lines.

```
       Sunlight / Solar Wind Impact
                 │
                 ▼
  [E x B Uplift at Magnetic Equator]
                 │
                 ▼ (Post-Sunset Inversion)
  [Rayleigh-Taylor Instability]
                 │
                 ▼
  [Equatorial Plasma Bubbles (EPBs)] ──> Causes diffraction of GPS L1/L2 signals
                                     ──> High S4 Index (Scintillation)
```

### 2.2 Ionospheric Scintillation Parameters
1. **Amplitude Scintillation Index ($S_4$):**
   The primary metric for measuring intensity fluctuations in radio signals.
   $$S_4 = \sqrt{\frac{\langle I^2 \rangle - \langle I \rangle^2}{\langle I \rangle^2}}$$
   *where $I$ is the received signal intensity.*
   * **$S_4 < 0.2$:** Negligible / Quiet ionosphere.
   * **$0.2 \le S_4 < 0.5$:** Moderate scintillation (minor GPS cycle slips, reduced accuracy).
   * **$S_4 \ge 0.5$:** Severe scintillation (total loss of GPS carrier lock, multi-meter positioning errors).

2. **Phase Scintillation Index ($\sigma_\phi$):**
   Measures phase variance over interval $\Delta t$ (typically 1 minute):
   $$\sigma_\phi = \sqrt{\langle \phi^2 \rangle - \langle \phi \rangle^2}$$
   *Crucial for RTK (Real-Time Kinematic) precision applications.*

3. **Geomagnetic Disturbance Markers:**
   * **$K_p$ Index:** 3-hour quasi-logarithmic scale (0–9) measuring global geomagnetic activity.
   * **$D_{st}$ Index:** Disturbance Storm Time index measuring ring current intensity (nT). Severe storms ($D_{st} < -100\text{ nT}$) dramatically expand EPB occurrence.

---

## 3. Public Data Sources & Integration Strategy

PRISM synthesizes multi-source space weather telemetry into unified regional risk tiers:

| Data Source | Provider | Parameters Extracted | Ingestion Mechanism | Update Frequency |
| :--- | :--- | :--- | :--- | :--- |
| **DSCOVR / ACE** | NOAA SWPC | Solar wind speed ($v_{sw}$), Density ($N_p$), IMF $B_z$ vector | REST JSON API | Real-time (1-min) |
| **Geomagnetic Indices** | NOAA SWPC | $K_p$ index, $A_p$ index, 3-Day Geomagnetic Forecast | REST JSON API | 1-hour / 3-hour |
| **ICON / GOLD Missions** | NASA Space Physics Data Facility (SPDF) | Equatorial plasma depletion images, Far-UV emissions | NetCDF4 via HTTP / FTP | Orbital pass (~90 min) |
| **SCINDA / Low-Latitude Receivers** | NOAA / IGS / Academic Networks | Ground receiver $S_4$ readings, Total Electron Content (TEC) | RINEX / ASCII streams / Synthetic Fallback | 1-min to 15-min |

---

## 4. Beneficiary Scenarios & Real-World Impact

### Scenario A: Disaster Response & Emergency Search-and-Rescue (SAR)
* **Location:** Equatorial archipelagos (e.g., Indonesia, Philippines) or coastal South America (e.g., Ecuador).
* **The Problem:** Following earthquakes or floods, rescue teams deploy autonomous drones and maritime rescue boats relying on GPS/GNSS position tracking. Post-sunset ionospheric scintillation drops GPS accuracy from 1 meter to >30 meters or causes complete signal dropouts, stalling life-saving operations.
* **PRISM Impact:** PRISM dispatches automated SMS alerts to local SAR command centers 1–2 hours prior to predicted scintillation windows, allowing operators to switch to inertial navigation backups or reschedule autonomous drone flights.

### Scenario B: Precision Agriculture
* **Location:** Equatorial farming corridors (e.g., East Africa, Northern Brazil).
* **The Problem:** Automated tractors and aerial spraying drones use Real-Time Kinematic (RTK) GPS for centimeter-level crop management. Unannounced phase scintillation ($\sigma_\phi$) breaks RTK carrier phase lock, causing tractors to deviate from rows and destroy crops.
* **PRISM Impact:** Sends SMS risk warnings ("*HIGH SCINTILLATION RISK: 19:00 - 22:00 LOCAL TIME*") directly to farm managers, preventing costly equipment damage and crop losses.

### Scenario C: Regional Aviation & Maritime Telecommunications
* **Location:** Busy equatorial flight paths and maritime straits (e.g., Strait of Malacca).
* **The Problem:** ADS-B (Automatic Dependent Surveillance-Broadcast) aircraft tracking and port tugboat positioning degrade during geomagnetic storms.
* **PRISM Impact:** Exposes a high-availability REST API (`GET /v1/risk?lat=...&lon=...`) consumed by regional port authorities and local flight dispatchers to monitor ionospheric health.

---

## 5. Why Existing Solutions Fail (The Last-Mile Gap)

1. **Macro-Scale Focus:** NOAA SWPC and ESA space weather alerts provide global planetary conditions ($K_p \ge 7$). They do not map *where* specific plasma bubbles will form at local equatorial coordinates ($ \pm 20^\circ$ latitude).
2. **High Technical Barrier:** Existing tools export raw NetCDF4 files or complex ionograms meant for space physicists, not emergency coordinators or tractor drivers.
3. **Lack of Low-Bandwidth Delivery:** High-end dashboards require stable broadband, which is often down in rural equatorial regions or during post-disaster scenarios. PRISM prioritizes lightweight SMS and minimal JSON payloads.

---

## 6. Scope, System Boundaries & Scientific Limitations

To maintain credibility for judging, PRISM explicitly outlines its operational boundaries:

* **Forecast Horizon:** Ionospheric plasma bubble turbulence is inherently non-linear and turbulent. PRISM provides **nowcasting and short-term probabilistic forecasting (1–3 hours)** based on pre-reversal enhancement (PRE) solar wind triggers, rather than multi-day deterministic forecasts.
* **Data Dependency:** When real-time ground-based $S_4$ station data is sparse in remote regions, PRISM utilizes empirical scintillation proxy models derived from $K_p$, solar flux ($F10.7$), local solar time (LST), and historical SCINDA climatology.
* **Complementary Role:** PRISM does not replace primary satellite navigation systems; it serves as an early-warning risk mitigation overlay.

---

## 7. Next Phase Readiness
With Phase 1 complete, the problem statement, scientific equations ($S_4$), public data schemas, and beneficiary use cases are fully established. Proceed to **Phase 2 (Repo Setup)** and **Phase 3 (Monorepo Directory Structure)**.
