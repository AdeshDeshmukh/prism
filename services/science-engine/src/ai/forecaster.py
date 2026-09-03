"""
PRISM AI Forecaster — Physics-Informed Ionospheric Scintillation Predictive Engine.
Implements multi-step time-series forecasting for S4 amplitude scintillation index
using solar wind telemetry (v_sw, Bz), geomagnetic Kp index, local solar time (LST),
and Rayleigh-Taylor growth rate proxies.
"""

from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any
import numpy as np


@dataclass
class ForecastHorizon:
    lead_time_hours: int
    target_timestamp: str
    predicted_s4: float
    confidence_lower_95: float
    confidence_upper_95: float
    predicted_risk_tier: str
    warning_flag: bool


@dataclass
class ForecastResult:
    latitude: float
    longitude: float
    current_s4: float
    current_kp: float
    forecast_horizons: List[ForecastHorizon]
    epb_formation_probability: float
    primary_instability_driver: str
    actionable_guidance: str


class IonosphericForecaster:
    """
    Predictive engine modeling Equatorial Plasma Bubble (EPB) evolution
    and trans-ionospheric scintillation over 1 to 3 hour lead times.
    """

    def __init__(self):
        # Empirical weights derived from SCINDA / IGS climatology & PRE drift dynamics
        self.kp_weight = 0.045
        self.bz_south_weight = 0.035
        self.vsw_scaling = 0.0006
        self.pre_sunset_peak_hour = 20.0  # 20:00 Local Solar Time peak

    def _calculate_local_solar_time(self, utc_time: datetime, longitude: float) -> float:
        """Calculates Local Solar Time (LST in decimal hours 0-24) from longitude."""
        utc_hours = utc_time.hour + (utc_time.minute / 60.0) + (utc_time.second / 3600.0)
        lst = (utc_hours + (longitude / 15.0)) % 24.0
        return lst

    def _rayleigh_taylor_growth_factor(self, lst: float, latitude: float) -> float:
        """
        Estimates Generalized Rayleigh-Taylor (GRT) growth factor gamma_RT.
        Peak instability occurs near the magnetic equator post-sunset (19:00 - 23:00 LST).
        """
        # Dip latitude penalty outside the +/-15-20 deg equatorial belt
        lat_factor = np.exp(-0.5 * (abs(latitude) / 12.0) ** 2)

        # Diurnal bell-curve around post-sunset Pre-Reversal Enhancement (PRE)
        hour_diff = min(abs(lst - self.pre_sunset_peak_hour), 24.0 - abs(lst - self.pre_sunset_peak_hour))
        diurnal_factor = np.exp(-0.5 * (hour_diff / 2.5) ** 2)

        return float(lat_factor * diurnal_factor)

    def forecast_trajectory(
        self,
        latitude: float,
        longitude: float,
        current_s4: float,
        current_kp: float,
        solar_wind_speed: float = 450.0,
        bz_nt: float = -2.0,
        history_s4: List[float] = None,
        base_time: datetime = None
    ) -> ForecastResult:
        """
        Generates +1h, +2h, and +3h lead-time forecasts for ionospheric scintillation.
        """
        if base_time is None:
            base_time = datetime.now(timezone.utc)

        if history_s4 is None or len(history_s4) < 3:
            # Seed synthetic short-term trend
            history_s4 = [max(0.02, current_s4 * 0.85), max(0.03, current_s4 * 0.92), current_s4]

        # Calculate short-term rate of change dS4/dt
        ds4_dt = float(np.polyfit(np.arange(len(history_s4)), history_s4, deg=1)[0])

        # Drivers
        southward_bz_impact = max(0.0, -bz_nt) * self.bz_south_weight
        solar_wind_impact = max(0.0, solar_wind_speed - 400.0) * self.vsw_scaling
        geomagnetic_impact = current_kp * self.kp_weight

        horizons: List[ForecastHorizon] = []
        max_s4_predicted = current_s4

        for step in [1, 2, 3]:
            lead_hours = step
            target_dt = base_time + timedelta(hours=lead_hours)
            target_lst = self._calculate_local_solar_time(target_dt, longitude)
            grt_factor = self._rayleigh_taylor_growth_factor(target_lst, latitude)

            # Combined predictive equation
            growth_term = grt_factor * (southward_bz_impact + solar_wind_impact + geomagnetic_impact + 0.15)
            trend_term = ds4_dt * (1.2 ** step)
            
            # Non-linear damping / saturation of S4 at ~1.2 (strong scattering regime)
            projected = current_s4 + (growth_term * step * 0.4) + trend_term
            projected_s4 = float(np.clip(projected, 0.02, 1.25))

            # Uncertainty expands with lead time
            error_margin = 0.05 * np.sqrt(step) + (0.10 * grt_factor)
            lower_bound = float(max(0.01, projected_s4 - error_margin))
            upper_bound = float(min(1.40, projected_s4 + error_margin))

            # Risk tier
            if projected_s4 >= 0.5:
                tier = "SEVERE"
                warn = True
            elif projected_s4 >= 0.2:
                tier = "MODERATE"
                warn = False
            else:
                tier = "LOW"
                warn = False

            if projected_s4 > max_s4_predicted:
                max_s4_predicted = projected_s4

            horizons.append(ForecastHorizon(
                lead_time_hours=lead_hours,
                target_timestamp=target_dt.isoformat(),
                predicted_s4=round(projected_s4, 3),
                confidence_lower_95=round(lower_bound, 3),
                confidence_upper_95=round(upper_bound, 3),
                predicted_risk_tier=tier,
                warning_flag=warn
            ))

        # EPB Probability
        current_lst = self._calculate_local_solar_time(base_time, longitude)
        current_grt = self._rayleigh_taylor_growth_factor(current_lst, latitude)
        prob_epb = float(np.clip(
            (current_grt * 0.5) + (current_kp / 9.0 * 0.3) + (max(0.0, -bz_nt) / 20.0 * 0.2),
            0.05, 0.98
        ))

        # Primary instability driver identification
        if bz_nt < -5.0 and current_kp >= 5.0:
            driver = "Geomagnetic Storm Triggered (Southward IMF Bz Coupling)"
        elif current_grt > 0.6:
            driver = "Post-Sunset Pre-Reversal Enhancement (Rayleigh-Taylor Instability)"
        elif solar_wind_speed > 600.0:
            driver = "High-Speed Solar Wind Stream (HSSWS) Compression"
        else:
            driver = "Quiet Background Climatological Variance"

        # Actionable guidance
        if max_s4_predicted >= 0.5:
            guidance = (
                f"⚠️ HIGH RISK ALERT: S4 predicted to exceed 0.50 within 1–3 hours. "
                f"Prepare to switch autonomous drones and RTK tractor systems to Inertial Navigation (INS) backup."
            )
        elif max_s4_predicted >= 0.2:
            guidance = (
                f"ℹ️ ADVISORY: Moderate scintillation expected. Expect minor GNSS cycle slips; "
                f"enable dual-frequency multi-constellation receivers."
            )
        else:
            guidance = "✅ NOMINAL: Ionospheric conditions expected to remain stable across all lead times."

        return ForecastResult(
            latitude=latitude,
            longitude=longitude,
            current_s4=round(current_s4, 3),
            current_kp=round(current_kp, 2),
            forecast_horizons=horizons,
            epb_formation_probability=round(prob_epb * 100.0, 1),
            primary_instability_driver=driver,
            actionable_guidance=guidance
        )
