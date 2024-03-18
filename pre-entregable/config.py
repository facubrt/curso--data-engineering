import os
from constants import START_DATE, END_DATE
from dotenv import load_dotenv

# CONSTRUCCIÓN DE URL Y CONSULTA DE API
# API https://api.nasa.gov/
# Near Earth Object Web Service
load_dotenv()
API_KEY = os.getenv('API_KEY')
URL = 'https://api.nasa.gov/neo/rest/v1/feed?start_date=' + START_DATE + '&end_date=' + END_DATE + '&api_key=' + API_KEY