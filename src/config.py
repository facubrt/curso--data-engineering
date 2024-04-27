import os
import psycopg2
from constants import TODAY

def get_api_url():
  # API https://api.nasa.gov/ - Near Earth Object Web Service
  API_KEY = os.getenv('API_KEY')
  api_url = 'https://api.nasa.gov/neo/rest/v1/feed?start_date=' + TODAY + '&end_date=' + TODAY + '&api_key=' + API_KEY
  return api_url

def connect_to_redshift():
  # DB REDSHIFT
  URL_DB = os.getenv("URL_DB")
  NAME_DB = os.getenv("NAME_DB")
  USER_DB =  os.getenv("USER_DB")
  PASSWORD_DB = os.getenv("PASSWORD_DB")
  PORT_DB = os.getenv("PORT_DB")

  try:
    # CONECTAR A LA BASE DE DATOS DE REDSHIFT
    connection = psycopg2.connect(
        host=URL_DB,
        dbname=NAME_DB,
        user=USER_DB,
        password=PASSWORD_DB,
        port=PORT_DB
    )
    print("Conexión con Redshift exitosa")
    return connection
  
  except Exception as e:
    print(e)