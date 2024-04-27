from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from src.send_mail import send_mail
from tasks import extract_neodata, transform_neodata, load_neodata, ph_alert


default_args={
    'owner': 'facubrt',
    'retries':1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    default_args=default_args,
    dag_id='neo_dag',
    description= 'NEO DAG',
    schedule="0 20 * * *",
    start_date=datetime(2024, 4, 1),
    #schedule_interval='@daily'
    catchup=False,
    tags=["neo_dag"]
    ) as dag:

    pre_workflow = EmptyOperator(task_id='pre_workflow')

    get_neodata = PythonOperator(task_id='extract_neodata', python_callable=extract_neodata)

    clean_neodata = PythonOperator(task_id='transform_neodata', python_callable=transform_neodata)

    insert_neodata = PythonOperator(task_id='load_neodata', python_callable=load_neodata)

    send_alert = PythonOperator(task_id='send_alert', python_callable=ph_alert)

    post_workflow = EmptyOperator(task_id='post_workflow')

    # etl = PythonOperator(task_id="main_etl", python_callable=main_etl)

    # enviar_resultado = PythonOperator(task_id="send_mail", python_callable=send_mail)

    pre_workflow >> get_neodata >> clean_neodata >> insert_neodata >> send_alert >> post_workflow