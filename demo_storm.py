#!/usr/bin/env python3
"""
PRISM — Interactive Space-Weather Storm Simulator & Live Demonstration CLI.
Simulates a Coronal Mass Ejection (CME) impacting Earth's equatorial ionosphere,
triggering Rayleigh-Taylor instability and severe GPS scintillation warnings.

Usage:
    python demo_storm.py
"""

import sys
import time
from pathlib import Path
from datetime import datetime, timezone

# Add service paths
ROOT_DIR = Path(__file__).resolve().parent
ENGINE_DIR = ROOT_DIR / "services" / "science-engine"
sys.path.insert(0, str(ENGINE_DIR))
sys.path.insert(0, str(ENGINE_DIR / "src"))

try:
    from src.ai.forecaster import IonosphericForecaster
    from src.analysis.risk_scoring import evaluate_regional_risk
    from src.ingest.noaa_client import NOAAClient
    from src.ingest.scinda_client import SCINDAClient
except ImportError:
    from ai.forecaster import IonosphericForecaster
    from analysis.risk_scoring import evaluate_regional_risk
    from ingest.noaa_client import NOAAClient
    from ingest.scinda_client import SCINDAClient


# ANSI Color Codes
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"


def print_banner():
    banner = f"""
{CYAN}{BOLD}╔══════════════════════════════════════════════════════════════════════════╗
║   PRISM — Planetary Scintillation & Ionospheric Risk Indicator System    ║
║   Track: Astronomy + Tech | CSH Social Impact Ideathon 2026              ║
╚══════════════════════════════════════════════════════════════════════════╝{RESET}
"""
    print(banner)


def render_gauge(value: float, max_val: float = 1.0, width: int = 24) -> str:
    filled = int((min(value, max_val) / max_val) * width)
    empty = width - filled
    
    if value < 0.2:
        color = GREEN
    elif value < 0.5:
        color = YELLOW
    else:
        color = RED

    bar = f"{color}{'█' * filled}{DIM}{'░' * empty}{RESET}"
    return f"[{bar}] {color}{value:0.2f}{RESET}"


def run_storm_simulation():
    print_banner()
    print(f"{BOLD}🎯 Target Location:{RESET} Nairobi, Kenya (Lat: -1.2921°, Lon: 36.8219° — Magnetic Equator Belt)")
    print(f"{BOLD}📡 Beneficiary Nodes:{RESET} Disaster SAR Drones, RTK Precision Agriculture Tractors\n")
    print(f"{CYAN}--- INITIATING 6-HOUR CME SOLAR STORM SIMULATION TIMELINE ---{RESET}\n")

    forecaster = IonosphericForecaster()

    # Timeline of the CME Storm Scenario
    timeline = [
        {
            "hour": "T+00:00",
            "desc": "Quiet Background Solar Wind (Pre-Event Baseline)",
            "vsw": 385.0,
            "bz": 1.5,
            "kp": 1.67,
            "s4": 0.08,
            "sms_recipient": None
        },
        {
            "hour": "T+01:00",
            "desc": "CME Shock Arrival — Solar Wind Compression & Magnetic Reconnection",
            "vsw": 630.0,
            "bz": -7.8,
            "kp": 4.33,
            "s4": 0.17,
            "sms_recipient": None
        },
        {
            "hour": "T+02:00",
            "desc": "Post-Sunset Inversion: Pre-Reversal Enhancement (PRE) Peak",
            "vsw": 740.0,
            "bz": -13.5,
            "kp": 5.67,
            "s4": 0.38,
            "sms_recipient": "Samuel (East Africa Agriculture Co-op)"
        },
        {
            "hour": "T+03:00",
            "desc": "Rayleigh-Taylor Growth: Equatorial Plasma Bubbles (EPBs) Erupting",
            "vsw": 820.0,
            "bz": -18.2,
            "kp": 7.33,
            "s4": 0.78,
            "sms_recipient": "Commander Maya (Coastal SAR Drone Command)"
        },
        {
            "hour": "T+04:00",
            "desc": "Deep Scintillation Regime — Severe GPS Carrier Lock Loss",
            "vsw": 790.0,
            "bz": -15.0,
            "kp": 7.00,
            "s4": 0.84,
            "sms_recipient": "Captain Santos (Regional Airway Dispatch)"
        },
        {
            "hour": "T+05:00",
            "desc": "Plasma Bubble Drift & Recombination (Recovery Phase)",
            "vsw": 560.0,
            "bz": -3.5,
            "kp": 4.00,
            "s4": 0.28,
            "sms_recipient": None
        },
        {
            "hour": "T+06:00",
            "desc": "Ionosphere Stabilized — Nominal GNSS Accuracy Restored",
            "vsw": 410.0,
            "bz": 0.5,
            "kp": 2.00,
            "s4": 0.09,
            "sms_recipient": None
        }
    ]

    for step in timeline:
        assessment = evaluate_regional_risk(
            s4_index=step["s4"],
            kp_index=step["kp"],
            latitude=-1.2921
        )
        tier = assessment["risk_tier"]
        
        if tier == "LOW":
            tier_badge = f"{GREEN}[🟢 LOW RISK]{RESET}"
        elif tier == "MODERATE":
            tier_badge = f"{YELLOW}[🟡 MODERATE RISK]{RESET}"
        else:
            tier_badge = f"{RED}{BOLD}[🔴 SEVERE SCINTILLATION RISK]{RESET}"

        print(f"{BOLD}{step['hour']}{RESET} — {step['desc']}")
        print(f"  ├─ Solar Wind: {step['vsw']:0.0f} km/s | IMF Bz: {step['bz']:+0.1f} nT | Geomagnetic Kp: {step['kp']:0.2f}")
        print(f"  ├─ S4 Amplitude Scintillation Index: {render_gauge(step['s4'])}")
        print(f"  ├─ Risk Assessment: {tier_badge}")
        print(f"  └─ Guidance: {DIM}{assessment['recommended_action']}{RESET}")

        # SMS Dispatch Event
        if step["sms_recipient"]:
            print(f"     {CYAN}⚡ [SMS DISPATCH GATEWAY]{RESET} Delivered priority alert to: {BOLD}{step['sms_recipient']}{RESET}")
            if tier == "SEVERE":
                print(f"     {RED}📩 Payload: 'PRISM SEVERE ALERT: S4={step['s4']:.2f}. GNSS carrier loss imminent. SWITCH DRONES/TRACTORS TO INS BACKUP.'{RESET}")
            else:
                print(f"     {YELLOW}📩 Payload: 'PRISM ADVISORY: S4={step['s4']:.2f}. Minor GPS drift expected in target sector.'{RESET}")

        print("")
        time.sleep(0.4)

    # Demonstrate the AI Predictive 3-Hour Forecast
    print(f"\n{CYAN}{BOLD}--- AI PREDICTIVE FORECAST DEMONSTRATION (Phase 3 Engine) ---{RESET}")
    forecast = forecaster.forecast_trajectory(
        latitude=-1.2921,
        longitude=36.8219,
        current_s4=0.78,
        current_kp=7.33,
        solar_wind_speed=820.0,
        bz_nt=-18.2
    )

    print(f"🧠 {BOLD}Primary Instability Driver:{RESET} {forecast.primary_instability_driver}")
    print(f"📊 {BOLD}Equatorial Plasma Bubble (EPB) Probability:{RESET} {RED}{forecast.epb_formation_probability}%{RESET}")
    print(f"\n{BOLD}3-Hour Predictive Scintillation Trajectory:{RESET}")
    for h in forecast.forecast_horizons:
        badge = f"{RED}🔴 SEVERE{RESET}" if h.predicted_risk_tier == "SEVERE" else (f"{YELLOW}🟡 MODERATE{RESET}" if h.predicted_risk_tier == "MODERATE" else f"{GREEN}🟢 LOW{RESET}")
        print(f"  • +{h.lead_time_hours}h Lead Time: Predicted S4 = {h.predicted_s4:0.2f} (95% CI: [{h.confidence_lower_95:0.2f} - {h.confidence_upper_95:0.2f}]) -> {badge}")

    print(f"\n{BOLD}🤖 Actionable Machine Guidance:{RESET} {forecast.actionable_guidance}")
    print(f"\n{GREEN}{BOLD}✅ PRISM End-to-End Simulation & ML Validation Completed Successfully!{RESET}\n")


if __name__ == "__main__":
    run_storm_simulation()
