from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.amazon.aws.operators.glue import AwsGlueJobOperator
from airflow.operators.email_operator import EmailOperator
from airflow.utils.trigger_rule import TriggerRule

default_args = {
    'owner': 'BrayanVilla',
    'depends_on_past': False,
    'email': ['villabryan12@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='transactions_etl',
    default_args=default_args,
    description='ETL DAG para procesar transacciones desde S3 hacia Snowflake usando Glue y Hudi',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:

    # Tarea: Ejecutar el job de Glue
    run_glue_job = AwsGlueJobOperator(
        task_id='run_glue_job',
        job_name='transactions_glue_job',  # Nombre del job en AWS Glue
        script_location='s3://ld-poc-nequi/glue/scripts/script_pyspark.py',  # Ajustar al path real
        iam_role_name='GlueServiceRole',   # Rol de Glue
        region_name='us-east-1'
    )

    # Tarea: Notificar por email si hay falla
    notify_failure = EmailOperator(
        task_id='notify_failure',
        to='villabryan12@gmail.com',
        subject='ETL DAG Failed',
        html_content='El DAG transactions_etl ha fallado. Revisar logs para más detalles.',
        trigger_rule=TriggerRule.ONE_FAILED
    )

    run_glue_job >> notify_failure
