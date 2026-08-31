"""
Multi-factor Risk Scoring Aggregator.
Combines geomagnetic Kp index, solar wind speed, and local S4 reading into a unified risk tier.
"""
from typing import Dict, Any

def evaluate_regional_risk(s4_index: float, kp_index: float, latitude: float) -> Dict[str, Any]:
    """Combines S4 index, Kp index, and geomagnetic latitude into an actionable risk assessment."""
    is_equatorial = abs(latitude) <= 20.0

    # Risk tier determination
    if s4_index >= 0.5 or (kp_index >= 6.0 and is_equatorial):
        tier = "SEVERE"
        action = "DO NOT USE UNASSISTED GPS FOR RTK/DRONES; SWITCH TO INERTIAL BACKUP"
    elif s4_index >= 0.2 or kp_index >= 4.0:
        tier = "MODERATE"
        action = "EXPECT MINOR GPS DRIFT; MONITOR POSITIONING ACCURACY"
    else:
        tier = "LOW"
        action = "GPS IONOSPHERIC CONDITIONS NOMINAL"

    return {
        "risk_tier": tier,
        "s4_index": s4_index,
        "kp_index": kp_index,
        "recommended_action": action
    }
