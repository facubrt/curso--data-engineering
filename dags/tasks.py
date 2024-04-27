import pandas as pd
from dotenv import load_dotenv
from src.config import get_api_url, connect_to_redshift
from src.extract_data import extract_data
from src.transform_data import transform_data
from src.load_data import load_data
from src.send_mail import send_mail
from src.constants import NAME_TABLE

def extract_neodata():
  load_dotenv()
  api_url = get_api_url()

  raw_data = extract_data(api_url)
  return raw_data

def transform_neodata(ti): 
  data = ti.xcom_pull(task_ids=["extract_neodata"], key="return_value")[0]
  df = transform_data(data)

  return df.to_json()

def load_neodata(ti):
  connection = connect_to_redshift()
  data = ti.xcom_pull(task_ids=["transform_neodata"], key="return_value")[0]
  neo_data = pd.read_json(data)
  load_data(connection=connection, name_table=NAME_TABLE, data=neo_data)

def ph_alert(ti):
  data = ti.xcom_pull(task_ids=["transform_neodata"], key="return_value")[0]
  neo_data = pd.read_json(data)
  ph_count = neo_data['potentially_hazardous'].values
  if int(ph_count) > 0:
    content = ""
    subject = "[Alerta AIRFLOW] Objetos peligrosos detectados NEO_API"
    if int(ph_count) == 1:
      content = f"--- Este es un correo generado automáticamente ---\n\nSe ha detectado {int(ph_count)} objeto peligroso a través de NEO_API."
    else:
      content = content = f"--- Este es un correo generado automáticamente ---\n\nSe han detectado {int(ph_count)} objetos peligrosos a través de NEO_API."
    print(subject)
    print(content)
    send_mail(subject, content)

                      

