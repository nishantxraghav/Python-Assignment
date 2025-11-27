import pandas as pd
import numpy as np
import os

def create_dummy_data():
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)

    # Generate 365 days of data
    dates = pd.date_range(start='2024-01-01', periods=365, freq='D')
    
    # Generate synthetic weather data
    np.random.seed(42)
    temperature = np.random.normal(loc=25, scale=10, size=365)  # Mean 25C
    rainfall = np.random.gamma(shape=1, scale=5, size=365)      # Skewed rainfall
    rainfall[rainfall < 2] = 0                                  # Many dry days
    humidity = np.random.uniform(low=30, high=90, size=365)     # 30-90% humidity

    # Create DataFrame
    df = pd.DataFrame({
        'Date': dates,
        'Temperature_C': temperature.round(1),
        'Rainfall_mm': rainfall.round(1),
        'Humidity_Pct': humidity.round(1)
    })

    # Introduce some missing values (NaN) to satisfy "Cleaning" requirement
    df.loc[10:15, 'Temperature_C'] = np.nan
    df.loc[50:55, 'Humidity_Pct'] = np.nan

    # Save to CSV
    df.to_csv('data/weather_data.csv', index=False)
    print("✅ 'data/weather_data.csv' created successfully.")

if __name__ == "__main__":
    create_dummy_data()
