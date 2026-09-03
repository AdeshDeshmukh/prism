import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

# Ensure services/science-engine and its virtualenv site-packages are on sys.path
SERVICE_ROOT = Path(__file__).resolve().parent.parent.parent
SITE_PACKAGES = SERVICE_ROOT / ".venv" / "lib" / "python3.14" / "site-packages"

if str(SERVICE_ROOT) not in sys.path:
    sys.path.insert(0, str(SERVICE_ROOT))
if str(SERVICE_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(SERVICE_ROOT / "src"))
if SITE_PACKAGES.exists() and str(SITE_PACKAGES) not in sys.path:
    sys.path.insert(0, str(SITE_PACKAGES))

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

try:
    from src.ingest.noaa_client import NOAAClient
    from src.ingest.scinda_client import SCINDAClient
    from src.analysis.risk_scoring import evaluate_regional_risk
    from src.ai.forecaster import IonosphericForecaster
except ImportError:
    from ingest.noaa_client import NOAAClient
    from ingest.scinda_client import SCINDAClient
    from analysis.risk_scoring import evaluate_regional_risk
    from ai.forecaster import IonosphericForecaster

# --- Pydantic Response Schemas ---
class HealthResponse(BaseModel):
    status: str = Field(default="healthy")
    service: str = Field(default="science-engine")
    version: str = Field(default="2.0.0")
    timestamp: str

class TelemetryData(BaseModel):
    kp_index: float = Field(..., description="Geomagnetic Kp index (0 to 9)")
    s4_index: float = Field(..., description="Amplitude Scintillation S4 index (0 to 1.0+)")
    sigma_phi_rad: Optional[float] = Field(default=None, description="Phase scintillation in radians")
    solar_wind_speed_km_s: Optional[float] = Field(default=None)
    bz_gsm_nt: Optional[float] = Field(default=None)

class RiskAssessmentDetail(BaseModel):
    risk_tier: str = Field(..., description="LOW, MODERATE, or SEVERE")
    s4_index: float
    kp_index: float
    recommended_action: str

class RiskAssessmentResponse(BaseModel):
    location: Dict[str, float]
    telemetry: TelemetryData
    assessment: RiskAssessmentDetail
    timestamp: str

class ForecastHorizonModel(BaseModel):
    lead_time_hours: int
    target_timestamp: str
    predicted_s4: float
    confidence_lower_95: float
    confidence_upper_95: float
    predicted_risk_tier: str
    warning_flag: bool

class ForecastResponse(BaseModel):
    location: Dict[str, float]
    current_s4: float
    current_kp: float
    forecast_horizons: List[ForecastHorizonModel]
    epb_formation_probability_percent: float
    primary_instability_driver: str
    actionable_guidance: str
    model: str = "PRISM Physics-Informed ML Forecaster v2.0"

class StormSimulationStep(BaseModel):
    timeline_hour: float
    description: str
    solar_wind_speed_km_s: float
    bz_nt: float
    kp_index: float
    s4_index: float
    risk_tier: str
    alert_triggered: bool

class StormSimulationResponse(BaseModel):
    simulation_scenario: str
    target_location: Dict[str, float]
    steps: List[StormSimulationStep]
    summary: str


# --- App Initialization ---
app = FastAPI(
    title="PRISM Science Engine API",
    description="Planetary Scintillation & Ionospheric Risk Indicator System — Space-Weather Nowcasting & AI Predictive Forecasting",
    version="2.0.0"
)

# Enable CORS for frontend/dashboard access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

noaa = NOAAClient()
scinda = SCINDAClient()
forecaster = IonosphericForecaster()


@app.get("/health", response_model=HealthResponse, tags=["Health"])
def health_check():
    """Service liveness & health check endpoint."""
    return HealthResponse(
        status="healthy",
        service="science-engine",
        version="2.0.0",
        timestamp=datetime.now(timezone.utc).isoformat()
    )


@app.get("/risk", response_model=RiskAssessmentResponse, tags=["Scintillation Risk"])
def get_risk_assessment(
    latitude: float = Query(..., ge=-90.0, le=90.0, description="Target Latitude (-90 to 90)"),
    longitude: float = Query(..., ge=-180.0, le=180.0, description="Target Longitude (-180 to 180)")
):
    """
    Computes real-time ionospheric scintillation risk assessment for target geographical coordinates.
    Integrates live NOAA SWPC solar wind/Kp telemetry with localized SCINDA scintillation models.
    """
    kp_data = noaa.fetch_kp_index()
    sw_data = noaa.fetch_solar_wind()
    scinda_data = scinda.fetch_s4_reading(latitude, longitude, current_kp=kp_data["kp_index"])

    assessment = evaluate_regional_risk(
        s4_index=scinda_data["s4_index"],
        kp_index=kp_data["kp_index"],
        latitude=latitude
    )

    return RiskAssessmentResponse(
        location={"latitude": latitude, "longitude": longitude},
        telemetry=TelemetryData(
            kp_index=kp_data["kp_index"],
            s4_index=scinda_data["s4_index"],
            sigma_phi_rad=scinda_data.get("sigma_phi_rad"),
            solar_wind_speed_km_s=sw_data.get("solar_wind_speed_km_s"),
            bz_gsm_nt=sw_data.get("bz_gsm_nt")
        ),
        assessment=RiskAssessmentDetail(
            risk_tier=assessment["risk_tier"],
            s4_index=assessment["s4_index"],
            kp_index=assessment["kp_index"],
            recommended_action=assessment["recommended_action"]
        ),
        timestamp=datetime.now(timezone.utc).isoformat()
    )


@app.get("/forecast", response_model=ForecastResponse, tags=["AI Forecasting"])
def get_predictive_forecast(
    latitude: float = Query(..., ge=-90.0, le=90.0, description="Target Latitude (-90 to 90)"),
    longitude: float = Query(..., ge=-180.0, le=180.0, description="Target Longitude (-180 to 180)")
):
    """
    Runs the Physics-Informed ML Predictive Forecaster to project S4 scintillation risk
    for +1h, +2h, and +3h lead times with 95% confidence intervals.
    """
    kp_data = noaa.fetch_kp_index()
    sw_data = noaa.fetch_solar_wind()
    scinda_data = scinda.fetch_s4_reading(latitude, longitude, current_kp=kp_data["kp_index"])

    result = forecaster.forecast_trajectory(
        latitude=latitude,
        longitude=longitude,
        current_s4=scinda_data["s4_index"],
        current_kp=kp_data["kp_index"],
        solar_wind_speed=sw_data.get("solar_wind_speed_km_s", 450.0),
        bz_nt=sw_data.get("bz_gsm_nt", -1.5)
    )

    horizons = [
        ForecastHorizonModel(
            lead_time_hours=h.lead_time_hours,
            target_timestamp=h.target_timestamp,
            predicted_s4=h.predicted_s4,
            confidence_lower_95=h.confidence_lower_95,
            confidence_upper_95=h.confidence_upper_95,
            predicted_risk_tier=h.predicted_risk_tier,
            warning_flag=h.warning_flag
        )
        for h in result.forecast_horizons
    ]

    return ForecastResponse(
        location={"latitude": latitude, "longitude": longitude},
        current_s4=result.current_s4,
        current_kp=result.current_kp,
        forecast_horizons=horizons,
        epb_formation_probability_percent=result.epb_formation_probability,
        primary_instability_driver=result.primary_instability_driver,
        actionable_guidance=result.actionable_guidance
    )


@app.get("/telemetry/live", tags=["Space Weather Telemetry"])
def get_live_telemetry():
    """Returns the live space-weather telemetry stream ingested from NOAA SWPC."""
    kp_data = noaa.fetch_kp_index()
    sw_data = noaa.fetch_solar_wind()
    return {
        "geomagnetic": kp_data,
        "solar_wind": sw_data,
        "system_status": "ONLINE",
        "ingested_at": datetime.now(timezone.utc).isoformat()
    }


@app.get("/simulate/storm", response_model=StormSimulationResponse, tags=["Simulation"])
def simulate_coronal_mass_ejection(
    latitude: float = Query(default=-1.2921, description="Simulation Latitude (default: Nairobi, Kenya)"),
    longitude: float = Query(default=36.8219, description="Simulation Longitude")
):
    """
    Simulates a major Coronal Mass Ejection (CME) shockwave hitting Earth's magnetosphere,
    triggering post-sunset Rayleigh-Taylor instability and severe ionospheric scintillation.
    """
    scenario_steps = [
        (0.0, "Quiet Pre-Event Solar Wind Conditions", 380.0, 1.2, 1.67, 0.08, "LOW", False),
        (1.0, "CME Shockwave Front Impact — IMF Bz turns Southward", 620.0, -8.5, 4.33, 0.18, "LOW", False),
        (2.0, "Geomagnetic Ring Current Intensification & Sunset PRE", 750.0, -14.2, 6.00, 0.36, "MODERATE", True),
        (3.0, "Rayleigh-Taylor Instability Peak — Equatorial Plasma Bubble Eruption", 810.0, -18.7, 7.33, 0.74, "SEVERE", True),
        (4.0, "Severe Scintillation Regime — GPS Carrier Phase Lock Loss", 780.0, -15.1, 7.00, 0.82, "SEVERE", True),
        (5.0, "Plasma Bubble Diffusion & Magnetic Storm Recovery Phase", 540.0, -4.2, 4.67, 0.29, "MODERATE", False),
        (6.0, "Nominal Conditions Restored", 420.0, 0.8, 2.33, 0.11, "LOW", False),
    ]

    steps: List[StormSimulationStep] = []
    for (t, desc, vsw, bz, kp, s4, tier, alert) in scenario_steps:
        steps.append(StormSimulationStep(
            timeline_hour=t,
            description=desc,
            solar_wind_speed_km_s=vsw,
            bz_nt=bz,
            kp_index=kp,
            s4_index=s4,
            risk_tier=tier,
            alert_triggered=alert
        ))

    return StormSimulationResponse(
        simulation_scenario="CME-Induced Equatorial Ionospheric Storm & EPB Lifecycle",
        target_location={"latitude": latitude, "longitude": longitude},
        steps=steps,
        summary="Simulates full 6-hour space weather disturbance demonstrating PRISM's automated transition from LOW -> MODERATE -> SEVERE alerts."
    )
