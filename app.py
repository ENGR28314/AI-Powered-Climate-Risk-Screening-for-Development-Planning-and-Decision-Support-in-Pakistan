# app.py
import streamlit as st
import pandas as pd
import os
import workflow
import environmental_rules as rules
import prompts

st.set_page_config(page_title="Pakistan Climate Core Engine", layout="wide", page_icon="🇵🇰")

st.title("🇵🇰 Pakistan Climate Analytics & Agro-Eco Engine")
st.caption("Modular architecture separating calculation schemas, regulatory thresholds, and visualization interfaces.")

# Check for database/sample configuration mapping file loading
if os.path.exists("sample_projects.csv"):
    projects_df = pd.read_csv("sample_projects.csv")
else:
    projects_df = pd.DataFrame()

# Data Repository Registration Engine Mapping
DATA_REGISTRY = {
    "PMD Station Records (Emulator Layer)": workflow.PmdEmulatorSource()
}

with st.sidebar:
    st.header("🏢 Domain Selection Matrix")
    
    if not projects_df.empty:
        project_options = ["Manual Coordinates Configuration..."] + projects_df['project_name'].tolist()
        selected_project = st.selectbox("Load Standard Benchmark Project Pipeline", project_options)
        
        if selected_project != "Manual Coordinates Configuration...":
            p_data = projects_df[projects_df['project_name'] == selected_project].iloc[0]
            lat_init, lon_init, elev_init = float(p_data['latitude']), float(p_data['longitude']), float(p_data['elevation_m'])
            start_yr_init, end_yr_init = int(p_data['start_year']), int(p_data['end_year'])
        else:
            lat_init, lon_init, elev_init, start_yr_init, end_yr_init = 31.5204, 74.3587, 210, 2020, 2025
    else:
        lat_init, lon_init, elev_init, start_yr_init, end_yr_init = 31.5204, 74.3587, 210, 2020, 2025

    selected_source_name = st.selectbox("Select Climate Data Engine Feed", list(DATA_REGISTRY.keys()))
    lat = st.number_input("Latitude (N Grid Coordinate Zone)", min_value=23.0, max_value=37.0, value=lat_init, step=0.01)
    lon = st.number_input("Longitude (E Grid Coordinate Zone)", min_value=60.0, max_value=80.0, value=lon_init, step=0.01)
    elevation = st.number_input("Elevation (Meters Above Sea Level)", min_value=0, max_value=8000, value=int(elev_init))
    
    start_yr = st.slider("Target Analysis Lower Bound Year", 2010, 2026, start_yr_init)
    end_yr = st.slider("Target Analysis Upper Bound Year", 2010, 2026, end_yr_init)
    
    execute_pipeline = st.button("Execute Pipeline Metrics Array", type="primary", use_container_width=True)

if execute_pipeline:
    with st.spinner("Executing architecture workflow abstraction layer..."):
        try:
            source = DATA_REGISTRY[selected_source_name]
            raw_df = source.fetch_data(latitude=lat, longitude=lon, start_year=start_yr, end_year=end_yr)
            
            # Map structural mutations out of direct UI scope
            raw_df['GDD'] = workflow.calculate_gdd(raw_df)
            raw_df['SPI_30'] = workflow.calculate_spi(raw_df)
            raw_df['PET'] = workflow.calculate_penman_monteith_pet(raw_df, elevation=elevation)
            
            # Formulate aggregate indexes via computational engine contracts
            huglin_val = workflow.calculate_huglin_index(raw_df, latitude=lat)
            drought_verdict = rules.trigger_drought_alerts(raw_df['SPI_30'])
            thermal_verdict = rules.evaluate_crop_thermal_suitability(huglin_val)
            
            # Structure Dashboard Layout Grid Columns
            m1, m2, m3 = st.columns(3)
            m1.metric("Calculated Cumulative Huglin Index", f"{huglin_val:.1f}")
            m2.metric("Total Evapotranspiration Loss (PET)", f"{raw_df['PET'].sum():.1f} mm")
            m3.metric("Latest Moisture Matrix Score (SPI-30)", f"{raw_df['SPI_30'].iloc[-1]:.2f}")
            
            st.subheader("⚠️ Eco-Zoning Threshold & Risk Mitigation Evaluations")
            st.info(f"**Thermal Zoning Assessment:** {thermal_verdict}")
            st.warning(f"**Hydrological Drought Matrix Standing:** {drought_verdict}")
            
            c1, c2 = st.columns(2)
            with c1:
                st.subheader("Reference Crop Evapotranspiration Dynamics (PET)")
                st.line_chart(raw_df, x='date', y='PET', color="#FF8F00")
            with c2:
                st.subheader("Standardized Precipitation Index Volatility Curve (SPI-30)")
                st.line_chart(raw_df, x='date', y='SPI_30', color="#2E7D32")
                
            st.subheader("📋 Structuring Automated Narrative Report Array Metadata")
            report_text = prompts.REPORT_TEMPLATE.format(
                lat=lat, lon=lon, elevation=elevation,
                gdd_summary=f"Total GDD Units compiled over range: {raw_df['GDD'].sum():.1f} C-Days",
                huglin_val=huglin_val, pet_total=raw_df['PET'].sum(), spi_mean=raw_df['SPI_30'].mean(),
                recommendations=f"- Focus matching parameters into local regimes.\\n- {thermal_verdict}\\n- {drought_verdict}"
            )
            st.markdown(report_text)
            
            st.subheader("📁 Processed Primary Data Array Layer Output Matrix")
            st.dataframe(raw_df, use_container_width=True)
            
        except Exception as err:
            st.error(f"Critical execution error mapped inside abstract array workflow: {str(err)}")
else:
    st.info("Select parameters or pick a benchmark benchmark pipeline mapping configurations profile from the sidebar layout context matrix to begin processing.")
