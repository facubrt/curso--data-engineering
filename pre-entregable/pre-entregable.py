import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta

# CONSTRUCCIÓN DE URL Y CONSULTA DE API
# API https://api.nasa.gov/
# Near Earth Object Web Service
API_KEY = 'WnvDv550SuYfAfP9V9eqiWGpn4obrthY21pxgmES'
DAYS_TO_SUBTRACT = 7
TODAY = datetime.now().strftime('%Y-%m-%d')
START_DATE = (datetime.now() - timedelta(days=DAYS_TO_SUBTRACT)).strftime('%Y-%m-%d')
END_DATE = datetime.now().strftime('%Y-%m-%d')
URL = 'https://api.nasa.gov/neo/rest/v1/feed?start_date=' + START_DATE + '&end_date=' + END_DATE + '&api_key=' + API_KEY
#
response = requests.get(URL).json()

# CONSTRUCCIÓN DE DATAFRAME
data = []
for day in response['near_earth_objects']:
  df = pd.DataFrame(response['near_earth_objects'][day])
  data.append({"date": day, "near_earth_objects": len(df), "absolute_magnitude_min": df["absolute_magnitude_h"].min(), "absolute_magnitude_max": df["absolute_magnitude_h"].max(), "potentially_hazardous": np.sum(df['is_potentially_hazardous_asteroid'] == True), "sentry_objecs": np.sum(df['is_sentry_object'] == True) })
day_df = pd.DataFrame(data)

# ORDENAR LOS DATOS OBTENIDOS POR FECHA
day_df.sort_values(by='date', inplace = True)
print(day_df)

