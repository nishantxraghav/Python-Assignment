import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

os.makedirs('output', exist_ok=True)

def load_and_clean_data(filepath):
    """Task 1 & 2: Load data, handle NaNs, and convert dates."""
    print("--- Loading and Cleaning Data ---")
    df = pd.read_csv(filepath)
    
    df['Date'] = pd.to_datetime(df['Date'])
    
    df.ffill(inplace=True)
    

    df = df[['Date', 'Temperature_C', 'Rainfall_mm', 'Humidity_Pct']]
    
    print("Data Info after cleaning:")
    print(df.info())
    return df

def compute_statistics(df):
    """Task 3: Calculate statistics using NumPy."""
    print("\n--- Statistical Analysis ---")
    
    temps = df['Temperature_C'].to_numpy()
    
    stats = {
        "Mean Temp": np.mean(temps),
        "Max Temp": np.max(temps),
        "Min Temp": np.min(temps),
        "Std Dev Temp": np.std(temps)
    }
    
    for k, v in stats.items():
        print(f"{k}: {v:.2f}")
    
    return stats

def perform_grouping(df):
    """Task 5: Group by Month."""
    print("\n--- Grouping Data ---")
    df_indexed = df.set_index('Date')
 
    monthly_stats = df_indexed.resample('ME').agg({
        'Temperature_C': 'mean',
        'Rainfall_mm': 'sum',
        'Humidity_Pct': 'mean'
    })
    
    return monthly_stats

def create_visualizations(df, monthly_data):
    """Task 4: Create required plots."""
    print("\n--- Generating Plots ---")
    
    plt.figure(figsize=(10, 6))
    plt.plot(df['Date'], df['Temperature_C'], color='orange', linewidth=1)
    plt.title('Daily Temperature Trend (2024)')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.grid(True, alpha=0.3)
    plt.savefig('output/1_daily_temperature.png')
    plt.close()

    plt.figure(figsize=(10, 6))
    months = monthly_data.index.strftime('%b')
    plt.bar(months, monthly_data['Rainfall_mm'], color='skyblue')
    plt.title('Total Monthly Rainfall')
    plt.xlabel('Month')
    plt.ylabel('Rainfall (mm)')
    plt.savefig('output/2_monthly_rainfall.png')
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.scatter(df['Humidity_Pct'], df['Temperature_C'], alpha=0.5, c='purple')
    plt.title('Correlation: Humidity vs Temperature')
    plt.xlabel('Humidity (%)')
    plt.ylabel('Temperature (°C)')
    plt.savefig('output/3_scatter_humidity_temp.png')
    plt.close()

    fig, ax = plt.subplots(2, 1, figsize=(10, 10))
    
    ax[0].plot(df['Date'], df['Temperature_C'], 'r-')
    ax[0].set_title('Temperature Overview')
    ax[0].set_ylabel('Temp (°C)')
    
    ax[1].plot(df['Date'], df['Humidity_Pct'], 'b-')
    ax[1].set_title('Humidity Overview')
    ax[1].set_ylabel('Humidity (%)')
    
    plt.tight_layout()
    plt.savefig('output/4_dashboard_bonus.png')
    plt.close()
    print("✅ All plots saved to 'output/' folder.")

def export_results(df):
    """Task 6: Export cleaned data."""
    df.to_csv('data/cleaned_weather_data.csv', index=False)
    print("✅ Cleaned data exported to 'data/cleaned_weather_data.csv'.")

if __name__ == "__main__":
    file_path = 'data/weather_data.csv'
    
    weather_df = load_and_clean_data(file_path)
    
    stats = compute_statistics(weather_df)
    monthly_df = perform_grouping(weather_df)
    
    create_visualizations(weather_df, monthly_df)
    
    export_results(weather_df)
