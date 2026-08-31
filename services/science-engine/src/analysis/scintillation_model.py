"""
Ionospheric Scintillation Modeling Engine.
Evaluates S4 metrics and plasma bubble conditions.
"""

def calculate_s4_index(intensity_variance: float, mean_intensity: float) -> float:
    """Calculates S4 index = sqrt(var(I) / mean(I)^2)."""
    if mean_intensity <= 0:
        return 0.0
    return (intensity_variance ** 0.5) / mean_intensity

def determine_scintillation_severity(s4_index: float) -> str:
    """Categorizes S4 index into operational risk categories."""
    if s4_index < 0.2:
        return "LOW"
    elif s4_index < 0.5:
        return "MODERATE"
    else:
        return "SEVERE"
