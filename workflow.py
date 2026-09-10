# workflow.py
from abc import ABC, abstractmethod
import pandas as pd
import numpy as np

class BaseClimateSource(ABC):
    @abstractmethod
    def fetch_data(self, latitude: float, longitude: float, start_year: int, end_year: int) -> pd.DataFrame:
        pass

class PmdEmulatorSource(BaseClimateSource):
    def fetch_data(self, latitude: float, longitude: float, start_year: int, end_year: int) -> pd.DataFrame:
        date_range = pd.date_range(start=f"{start_year}-01-01", end=f"{end_year}-12-31", freq='D')
        np.random.seed(int(latitude + longitude))
        
        df = pd.DataFrame({
            'date': date_range,
            'temp_max': np.random.uniform(18.0, 48.0, size=len(date_range)),
            'temp_min': np.random.uniform(4.0, 29.0, size=len(date_range)),
            'precipitation': np.random.exponential(scale=1.5, size=len(date_range))
        })
        # Simulate Monsoon season trends (July-August)
        df.loc[df['date'].dt.month.isin([7, 8]), 'precipitation'] *= 5.0
        return df

def calculate_gdd(df: pd.DataFrame, base_temp: float = 10.0) -> pd.DataFrame:
    t_mean = (df['temp_max'] + df['temp_min']) / 2
    return np.maximum(t_mean - base_temp, 0)

def calculate_spi(df: pd.DataFrame, window: int = 30) -> pd.Series:
    rolling_precip = df['precipitation'].rolling(window=window, min_periods=1).sum()
    mean, std = rolling_precip.mean(), rolling_precip.std()
    return pd.Series(0, index=df.index) if std == 0 or np.isnan(std) else (rolling_precip - mean) / std

def calculate_huglin_index(df: pd.DataFrame, latitude: float) -> float:
    df_active = df[(df['date'].dt.month >= 4) & (df['date'].dt.month <= 9)].copy()
    if df_active.empty: return 0.0
    t_mean = (df_active['temp_max'] + df_active['temp_min']) / 2
    d = 1.00 if latitude <= 30 else (1.02 if latitude <= 34 else 1.03)
    return float((((np.maximum(t_mean - 10, 0) + np.maximum(df_active['temp_max'] - 10, 0)) / 2) * d).sum())

def calculate_penman_monteith_pet(df: pd.DataFrame, elevation: float = 500.0) -> pd.Series:
    t_max, t_min = df['temp_max'], df['temp_min']
    t_mean = (t_max + t_min) / 2
    p = 101.3 * (((293 - 0.0065 * elevation) / 293) ** 5.26)
    gamma = 0.000665 * p
    delta = (4098 * (0.6108 * np.exp((17.27 * t_mean) / (t_mean + 237.3)))) / ((t_mean + 237.3) ** 2)
    es = ((0.6108 * np.exp((17.27 * t_max) / (t_max + 237.3))) + (0.6108 * np.exp((17.27 * t_min) / (t_min + 237.3)))) / 2
    vpd = es * 0.35  
    doy = df['date'].dt.dayofyear
    rns = 0.77 * (0.75 * (24.0 + 12.0 * np.sin((2 * np.pi * doy / 365) - 1.39)))
    return np.maximum(((0.408 * delta * rns) + (gamma * (900 / (t_mean + 273)) * 2.0 * vpd)) / (delta + (gamma * (1 + 0.34 * 2.0))), 0.0)
