from datetime import datetime
from airflow.models import DAG
from airflow.models.variable import Variable
from airflow.providers.amazon.aws.sensors.sqs import SqsSensor
from airflow.operators.python import PythonVirtualenvOperator
from airflow.operators.empty import EmptyOperator

DEFAULT_ARGS = {
   'start_date': datetime(2022, 9, 20),
   'schedule_interval': None,
   'catchup': False,
}

def get_queue_content(xcom_result):
    import pandas as pd
    from datetime import datetime
    print("Mensagens recebidas:")
    print(xcom_result)
    df = pd.DataFrame(eval(xcom_result))
    df['created_at'] = datetime.now()
    df['timezone'] = 'UTC'
    print(df)
    print("Total de mensagens:", len(df))

with DAG(
    dag_id='localstack_concept_example',
    schedule="0 * * * *",
    max_active_runs=1,
    default_args=DEFAULT_ARGS
) as dag:

    read_from_queue = SqsSensor(
        task_id="read_from_queue",
        sqs_queue="http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/localstack-queue",
        aws_conn_id="localstack",
        poke_interval=60,
        timeout=360,
        mode='reschedule',
    )

    get_queue_content = PythonVirtualenvOperator(
        task_id="get_queue_content",
        python_callable=get_queue_content,
        requirements=[
            "pandas==2.2.3"
        ],
        system_site_packages=False,
        op_kwargs={
            "xcom_result": "{{ ti.xcom_pull(task_ids='read_from_queue', key='messages') }}"
        },
        trigger_rule='all_success',
    )

    no_messages = EmptyOperator(
        task_id="no_messages",
        trigger_rule='one_failed',
    )

    read_from_queue >> [no_messages, get_queue_content]