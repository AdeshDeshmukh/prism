import sys
from pathlib import Path
from typing import Dict

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
except ImportError:
    from ingest.noaa_client import NOAAClient
    from ingest.scinda_client import SCINDAClient
    from analysis.risk_scoring import evaluate_regional_risk

# --- Pydantic Response Schemas ---
class HealthResponse(BaseModel):
    status: str = Field(default="healthy")
    service: str = Field(default="science-engine")

class TelemetryData(BaseModel):
    kp_index: float = Field(..., description="Geomagnetic Kp index (0 to 9)")
    s4_index: float = Field(..., description="Amplitude Scintillation S4 index (0 to 1.0+)")

class RiskAssessmentDetail(BaseModel):
    risk_tier: str = Field(..., description="LOW, MODERATE, or SEVERE")
    s4_index: float
    kp_index: float
    recommended_action: str

class RiskAssessmentResponse(BaseModel):
    location: Dict[str, float]
    telemetry: TelemetryData
    assessment: RiskAssessmentDetail

# --- App Initialization ---
app = FastAPI(
    title="PRISM Science Engine API",
    description="Space-Weather Analysis & Equatorial Ionospheric Scintillation Risk Scoring",
    version="1.0.0"
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

@app.get("/health", response_model=HealthResponse, tags=["Health"])
def health_check():
    """Service liveness & health check endpoint."""
    return HealthResponse(status="healthy", service="science-engine")

@app.get("/risk", response_model=RiskAssessmentResponse, tags=["Scintillation Risk"])
def get_risk_assessment(
    latitude: float = Query(..., ge=-90.0, le=90.0, description="Target Latitude (-90 to 90)"),
    longitude: float = Query(..., ge=-180.0, le=180.0, description="Target Longitude (-180 to 180)")
):
    """
    Computes real-time ionospheric scintillation risk assessment for target geographical coordinates.
    Integrates NOAA SWPC solar wind/Kp telemetry with SCINDA equatorial receiver data.
    """
    kp_data = noaa.fetch_kp_index()
    scinda_data = scinda.fetch_s4_reading(latitude, longitude)
    
    assessment = evaluate_regional_risk(
        s4_index=scinda_data["s4_index"],
        kp_index=kp_data["kp_index"],
        latitude=latitude
    )
    
    return RiskAssessmentResponse(
        location={"latitude": latitude, "longitude": longitude},
        telemetry=TelemetryData(
            kp_index=kp_data["kp_index"],
            s4_index=scinda_data["s4_index"]
        ),
        assessment=RiskAssessmentDetail(
            risk_tier=assessment["risk_tier"],
            s4_index=assessment["s4_index"],
            kp_index=assessment["kp_index"],
            recommended_action=assessment["recommended_action"]
        )
    )
