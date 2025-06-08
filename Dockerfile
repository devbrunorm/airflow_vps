FROM apache/airflow:3.0.1

RUN pip install --no-cache-dir 'apache-airflow[amazon]'
RUN pip install apache-airflow-providers-amazon
RUN pip install apache-airflow-providers-common-messaging
RUN pip install aiobotocore