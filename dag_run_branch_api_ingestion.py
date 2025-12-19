from airflow import DAG
from airflow.providers.amazon.aws.operators.glue import AwsGlueJobOperator
from datetime import datetime

with DAG(
    dag_id="branch_api_to_s3_raw",
    start_date=datetime(2025, 1, 1),
    schedule_interval="0 9 * * *",
    catchup=False,
    tags=["api", "glue", "raw"]
) as dag:

    trigger_glue = AwsGlueJobOperator(
        task_id="run_branch_api_ingestion",
        job_name="branch_api_raw_ingestion",
        region_name="ap-south-1",
        aws_conn_id="aws_default",
        retries=2
    )

    trigger_glue
