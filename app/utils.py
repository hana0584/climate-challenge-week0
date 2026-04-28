
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def load_data():
    """
    Loads all cleaned climate data and combines them.
    The @st.cache_data decorator ensures this function runs only once.
    """
    countries = ['ethiopia', 'kenya', 'sudan', 'tanzania', 'nigeria']
    all_data = []

    for country in countries:
        filepath = f'data/{country}_clean.csv'
        try:
            df = pd.read_csv(filepath, parse_dates=['Date'])
            df['Country'] = country.capitalize()
            all_data.append(df)
        except FileNotFoundError:
            st.error(f"Could not find data file for {country}. Make sure '{filepath}' exists.")
            return pd.DataFrame() # Return empty DataFrame if error

    if not all_data:
        return pd.DataFrame()
    combined = pd.concat(all_data, ignore_index=True)
    return combined

def plot_temperature_trends(data, countries, year_range):
    """
    Generates a matplotlib line chart for temperature trends.
    """
    filtered_data = data[(data['Country'].isin(countries)) & 
                         (data['Date'].dt.year >= year_range[0]) & 
                         (data['Date'].dt.year <= year_range[1])]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    # Group by month and country to calculate the average temperature
    monthly_temp = filtered_data.groupby([pd.Grouper(key='Date', freq='ME'), 'Country'])['T2M'].mean().reset_index()
    
    for country in countries:
        country_data = monthly_temp[monthly_temp['Country'] == country]
        if not country_data.empty:
            ax.plot(country_data['Date'], country_data['T2M'], label=country, linewidth=1.5)

    ax.set_title('Monthly Average Temperature Trends', fontsize=14)
    ax.set_xlabel('Date')
    ax.set_ylabel('Temperature (°C)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    return fig
