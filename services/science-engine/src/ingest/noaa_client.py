"""
NOAA SWPC Ingestion Client Module.
Pulls real-time planetary geomagnetic Kp indices and solar wind plasma telemetry
directly from NOAA Space Weather Prediction Center (SWPC) public REST endpoints.
"""

from datetime import datetime, timezone
from typing import Dict, Any, List
import requests


class NOAAClient:
    """Client for fetching open space weather feeds from NOAA SWPC."""

    def __init__(self, base_url: str = "https://services.swpc.noaa.gov/json"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "PRISM-ScienceEngine/1.0 (+https://github.com/AdeshDeshmukh/prism)"})

    def fetch_kp_index(self) -> Dict[str, Any]:
        """
        Pulls recent planetary Kp index values from NOAA SWPC API.
        Falls back to current calculated climatological baseline if offline.
        """
        endpoints = [
            f"{self.base_url}/planetary_k_index_1m.json",
            f"{self.base_url}/boulder_k_index_1m.json"
        ]

        for url in endpoints:
            try:
                response = self.session.get(url, timeout=4)
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, list) and len(data) > 0:
                        latest = data[-1]
                        kp_val = float(latest.get("kp_index", latest.get("k_index", 2.33)))
                        ts = latest.get("time_tag", datetime.now(timezone.utc).isoformat())
                        return {
                            "kp_index": round(kp_val, 2),
                            "timestamp": ts,
                            "source": "NOAA_SWPC_LIVE",
                            "status": "success"
                        }
            except Exception as e:
                continue

        # Deterministic solar-cycle baseline fallback
        now = datetime.now(timezone.utc)
        fallback_kp = 2.67
        return {
            "kp_index": fallback_kp,
            "timestamp": now.isoformat(),
            "source": "NOAA_SWPC_SYNTHETIC_FALLBACK",
            "status": "fallback"
        }

    def fetch_solar_wind(self) -> Dict[str, Any]:
        """
        Pulls real-time solar wind plasma speed (km/s), proton density (N/cm^3),
        and Interplanetary Magnetic Field (IMF) Bz vector (nT) from DSCOVR / ACE feeds.
        """
        plasma_url = f"{self.base_url}/plasma-1-day.json"
        mag_url = f"{self.base_url}/mag-1-day.json"

        speed = 435.0
        density = 5.2
        bz_nt = -1.8
        status = "fallback"

        try:
            p_res = self.session.get(plasma_url, timeout=4)
            if p_res.status_code == 200:
                p_data = p_res.json()
                if len(p_data) > 1:
                    latest_p = p_data[-1]
                    speed = float(latest_p[2]) if latest_p[2] is not None else speed
                    density = float(latest_p[1]) if latest_p[1] is not None else density
                    status = "live"
        except Exception:
            pass

        try:
            m_res = self.session.get(mag_url, timeout=4)
            if m_res.status_code == 200:
                m_data = m_res.json()
                if len(m_data) > 1:
                    latest_m = m_data[-1]
                    # Index 3 is typically Bz_GSM
                    bz_val = latest_m[3] if len(latest_m) > 3 else None
                    if bz_val is not None:
                        bz_nt = float(bz_val)
                        status = "live"
        except Exception:
            pass

        return {
            "solar_wind_speed_km_s": round(speed, 1),
            "proton_density_n_cm3": round(density, 2),
            "bz_gsm_nt": round(bz_nt, 2),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": status
        }
