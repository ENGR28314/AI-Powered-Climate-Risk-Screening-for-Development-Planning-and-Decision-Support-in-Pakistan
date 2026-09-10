# environmental_rules.py
import pandas as pd
import numpy as np

def evaluate_crop_thermal_suitability(huglin_index: float) -> str:
    if huglin_index < 1500:
        return "Cool Zone: Suitable for early-maturing varieties and northern fodder crops."
    elif 1500 <= huglin_index < 2100:
        return "Temperate/Moderate Zone: High suitability for standard cash crops and stone fruits."
    elif 2100 <= huglin_index < 3000:
        return "Warm/Sub-tropical Zone: Highly favorable for Punjab cotton belt and Basmati rice."
    else:
        return "Extreme Arid Hot Zone: High heat stress. Requires specific heat-tolerant varieties and drip irrigation."

def trigger_drought_alerts(spi_series: pd.Series) -> str:
    if spi_series.empty:
        return "Insufficient baseline data."
    latest_spi = spi_series.iloc[-1]
    if latest_spi <= -2.0:
        return "🚨 CRITICAL: Extreme Drought Alert. Immediate water table preservation required."
    elif -2.0 < latest_spi <= -1.5:
        return "⚠️ SEVERE: Severe Meteorological Drought. Initiate deficit irrigation protocols."
    elif -1.5 < latest_spi <= -1.0:
        return "📉 MODERATE: Moderate Drought Alert. Soil moisture degradation monitored."
    else:
        return "✅ NORMAL: Normal to wet moisture balancing conditions across the target grid."
