"""
SCINDA Ground Receiver Network Telemetry Client Module.
Simulates and fetches S4 amplitude scintillation index and phase scintillation (sigma_phi)
for equatorial and low-latitude receiver stations.
"""

from datetime import datetime, timezone
from typing import Dict, Any
import numpy as np


class SCINDAClient:
    """Client for retrieving regional S4 scintillation telemetry from ground stations."""

    def __init__(self, api_url: str = "https://api.scinda-network.org/v1"):
        self.api_url = api_url

    def fetch_s4_reading(
        self,
        latitude: float,
        longitude: float,
        current_kp: float = 2.5,
        target_time: datetime = None
    ) -> Dict[str, Any]:
        """
        Calculates or retrieves S4 scintillation index for given coordinates.
        Incorporates diurnal variation (post-sunset peak ~19:00-02:00 Local Solar Time)
        and magnetic latitude dependence.
        """
        if target_time is None:
            target_time = datetime.now(timezone.utc)

        # Local Solar Time (LST) calculation
        utc_hours = target_time.hour + (target_time.minute / 60.0)
        lst = (utc_hours + (longitude / 15.0)) % 24.0

        # Magnetic Equator proximity factor (Peak at +/-10-15 degrees EIA crests)
        is_equatorial = abs(latitude) <= 25.0
        eia_crest_factor = np.exp(-0.5 * ((abs(latitude) - 12.0) / 7.0) ** 2) if is_equatorial else 0.05

        # Post-sunset Rayleigh-Taylor diurnal factor (peaks at ~21:00 LST)
        hour_diff = min(abs(lst - 21.0), 24.0 - abs(lst - 21.0))
        diurnal_weight = np.exp(-0.5 * (hour_diff / 3.0) ** 2)

        # Base noise + storm enhancement
        geomagnetic_scaling = max(1.0, (current_kp / 3.0) ** 1.5)
        base_s4 = 0.06 + (0.55 * eia_crest_factor * diurnal_weight * geomagnetic_scaling)

        # Add minor realistic variance
        noise = float(np.random.normal(0, 0.015))
        final_s4 = float(np.clip(base_s4 + noise, 0.03, 1.15))

        # Phase scintillation index sigma_phi (radians) closely correlates with S4
        sigma_phi = float(np.clip(final_s4 * 0.45 + np.random.normal(0, 0.01), 0.02, 0.90))

        # Station identifier assignment
        station_name = f"SCINDA_{'EQ' if is_equatorial else 'MID'}_{abs(int(latitude)):02d}{'N' if latitude >= 0 else 'S'}_{abs(int(longitude)):03d}{'E' if longitude >= 0 else 'W'}"

        return {
            "latitude": latitude,
            "longitude": longitude,
            "local_solar_time_hours": round(lst, 2),
            "s4_index": round(final_s4, 3),
            "sigma_phi_rad": round(sigma_phi, 3),
            "station": station_name,
            "timestamp": target_time.isoformat()
        }
