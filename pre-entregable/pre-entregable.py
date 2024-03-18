import pandas as pd
import numpy as np
import requests
from config import URL

response = requests.get(URL).json()
# CONSTRUCCIÓN DE DATAFRAME
data = []
for day in response['near_earth_objects']:
  df = pd.DataFrame(response['near_earth_objects'][day])
  data.append(
    {
      "date": day, 
      "near_earth_objects": len(df), 
      "absolute_magnitude_min": df["absolute_magnitude_h"].min(), 
      "absolute_magnitude_max": df["absolute_magnitude_h"].max(), 
      "potentially_hazardous": np.sum(df['is_potentially_hazardous_asteroid'] == True), 
      "sentry_objecs": np.sum(df['is_sentry_object'] == True) 
    }
  )
day_df = pd.DataFrame(data)

# ORDENAR LOS DATOS OBTENIDOS POR FECHA
day_df.sort_values(by='date', inplace = True)
print(day_df)

