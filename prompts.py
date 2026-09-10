# prompts.py
CLIMATE_INTERPRETATION_SYSTEM_PROMPT = """
You are an expert climatologist specializing in the South Asian Monsoon system and Indus Basin agriculture. 
Analyze the calculated climate metrics (GDD, SPI, PET, Huglin Index) for the specified Pakistan coordinates. 
Provide a professional, localized assessment focusing on crop viability, irrigation stress, and risk patterns.
"""

REPORT_TEMPLATE = """
### 📊 Automated Agro-Climate Assessment Report
**Geographic Domain:** Latitude {lat}°N, Longitude {lon}°E  
**Elevation:** {elevation}m ASL  

#### 1. Thermal Profiles & Growing Degree Days (GDD)
* Accumulation Trend: {gdd_summary}
* Huglin Heliothermal Index Value: {huglin_val:.2f}

#### 2. Hydrological Matrix & Evapotranspiration
* Reference Crop Evapotranspiration (PET Total): {pet_total:.2f} mm
* Standardized Precipitation Index Baseline (SPI-30 Mean): {spi_mean:.2f}

#### 3. Strategic Field Recommendations
{recommendations}
"""
