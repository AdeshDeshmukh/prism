# PRISM Data Sources Specification

This document details the public space-weather telemetry endpoints consumed by PRISM.

## 1. NOAA Space Weather Prediction Center (SWPC)
* **Real-time Solar Wind (DSCOVR/ACE):** `https://services.swpc.noaa.gov/json/plasma-1-day.json`
* **Planetary Kp Index:** `https://services.swpc.noaa.gov/json/planetary_k_index_1m.json`
* **3-Day Geomagnetic Forecast:** `https://services.swpc.noaa.gov/text/3-day-forecast.txt`

## 2. NASA Space Physics Data Facility (SPDF)
* **NASA ICON Satellite Data:** Ionospheric Density & Temperature Profiles via CDAWeb.
* **NASA GOLD Mission:** Far-Ultraviolet Imaging of Equatorial Plasma Depletion Bubbles.

## 3. SCINDA / Ground GNSS Telemetry
* **Receiver Network:** Low-latitude scintillation monitor network measuring Amplitude Scintillation Index ($S_4$) and Total Electron Content (TEC).
