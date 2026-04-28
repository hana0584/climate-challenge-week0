
import streamlit as st
import pandas as pd
from utils import load_data, plot_temperature_trends  # Import our helper functions

st.set_page_config(page_title='African Climate Dashboard', layout='wide')


df = load_data()
if df.empty:
    st.stop() 

st.sidebar.header("🔍 Filter Data")


countries = df['Country'].unique()
selected_countries = st.sidebar.multiselect(
    "Select Countries", 
    options=countries, 
    default=countries.tolist()
)


min_year, max_year = int(df['Date'].dt.year.min()), int(df['Date'].dt.year.max())
year_range = st.sidebar.slider(
    "Select Year Range", 
    min_value=min_year, 
    max_value=max_year, 
    value=(min_year, max_year) 
)


climate_vars = {
    'T2M': '🌡️ Mean Temperature (°C)',
    'T2M_MAX': '🔥 Max Temperature (°C)',
    'PRECTOTCORR': '☔ Precipitation (mm/day)',
    'RH2M': '💧 Relative Humidity (%)',
    'WS2M': '💨 Wind Speed (m/s)'
}
selected_var_key = st.sidebar.selectbox(
    "Select Climate Variable", 
    options=list(climate_vars.keys()),
    format_func=lambda x: climate_vars[x] # Shows the friendly name in the dropdown
)


st.title("🌍 African Climate Trend Analysis Dashboard")
st.markdown("_Interactive visualizations for the COP32 position paper._")


st.subheader("📊 Key Climate Indicators")
# Use columns to display metrics side-by-side
col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_temp = df[(df['Country'].isin(selected_countries)) & (df['Date'].dt.year >= year_range[0]) & (df['Date'].dt.year <= year_range[1])]['T2M'].mean()
    st.metric("Average Temperature", f"{avg_temp:.1f} °C")


st.subheader("📈 Temperature Trends Over Time")
if selected_countries: # Only plot if at least one country is selected
    fig = plot_temperature_trends(df, selected_countries, year_range)
    st.pyplot(fig, use_container_width=True)
else:
    st.warning("Please select at least one country to display the temperature trend.")

st.subheader("🌧️ Precipitation Distribution by Country")
if selected_countries:
    filtered_box_data = df[(df['Country'].isin(selected_countries)) & (df['Date'].dt.year >= year_range[0]) & (df['Date'].dt.year <= year_range[1])]
    st.boxplot(data=filtered_box_data, x='Country', y='PRECTOTCORR')
else:
    st.warning("Please select at least one country to display the precipitation distribution.")