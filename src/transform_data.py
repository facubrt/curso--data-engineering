import pandas as pd
import numpy as np
from datetime import datetime

# E(T)L
def transform_data(raw_data):
  # CONSTRUCCIÓN DE DATAFRAME
  data = []
  for day in raw_data:
    df = pd.DataFrame(raw_data[day])
    data.append(
      {
        "timestamp": datetime.now(),
        "date": day, 
        "near_earth_objects": len(df), 
        "absolute_magnitude_min": df["absolute_magnitude_h"].min(), 
        "absolute_magnitude_max": df["absolute_magnitude_h"].max(), 
        "potentially_hazardous": np.sum(df['is_potentially_hazardous_asteroid'] == True), 
        "sentry_objects": np.sum(df['is_sentry_object'] == True) 
      }
    )
  day_df = pd.DataFrame(data)
  # ORDENAR LOS DATOS OBTENIDOS POR FECHA
  day_df.sort_values(by='date', inplace = True)
  return day_df
