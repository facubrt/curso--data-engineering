import pandas as pd
import numpy as np
import requests
import config
from psycopg2.extras import execute_values
from dotenv import load_dotenv
from datetime import datetime


# (E)TL
def extract_data(url):
  try:
    response = requests.get(url).json()
    neo = response['near_earth_objects']
    return neo
  except Exception as e:
    print(e)

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

# ET(L)
def load_data(connection, name_table, data):
    dtypes= data.dtypes
    cols= list(dtypes.index )
    tipos= list(dtypes.values)
    type_map = {'datetime64[ns]': 'TIMESTAMP', 'int64': 'INT','float64': 'FLOAT','object': 'VARCHAR(50)'}
    sql_dtypes = [type_map[str(dtype)] for dtype in tipos]
    column_defs = [f"{name} {data_type}" for name, data_type in zip(cols, sql_dtypes)]
    # ESQUEMA DE LA TABLA EN REDSHIFT
    # CREA LA TABLA
    temp_table_schema = f"""
        CREATE TABLE IF NOT EXISTS temp_data (
          {', '.join(column_defs)}, primary key(date)
        );
        """
    table_schema = f"""
        CREATE TABLE IF NOT EXISTS {name_table} (
          {', '.join(column_defs)}, primary key(date)
        );
        """
    # CURSOR
    cursor = connection.cursor()
    cursor.execute(temp_table_schema)
    cursor.execute(table_schema)
    # VALORES A INSERTAR EN LA TABLA
    values = [tuple(x) for x in data.to_numpy()]
    # EJECUCIÓN PARA CARGAR EN REDSHIFT
    cursor.execute("BEGIN")
    ##
    execute_values(
        cursor,
        f'''
        INSERT INTO temp_data ({', '.join(cols)}) VALUES %s
        ''',
        values,
    )
    cursor.execute(f"""
      DELETE FROM {name_table}
      USING temp_data
      WHERE {name_table}.date = temp_data.date;
    """
    )
    cursor.execute(f"""
      INSERT INTO {name_table}
      SELECT * FROM temp_data;
    """
    )
    cursor.execute("DELETE FROM temp_data;")
    cursor.execute("COMMIT")
    print('Proceso terminado')
    connection.close()
  
# MAIN
if __name__ == '__main__':
  load_dotenv()
  api_url = config.get_api_url()
  # OBTENCIÓN DE DATOS DESDE API
  raw_data = extract_data(api_url)
  # TRANSFORMACIÓN DE DATOS Y CONSTRUCCIÓN DE DATAFRAME
  neo_data = transform_data(raw_data)
  #print(neo_data)
  # CARGA DE DATOS A REDSHIFT
  connection = config.connect_to_redshift()
  load_data(connection=connection, name_table="neo_data", data=neo_data)
