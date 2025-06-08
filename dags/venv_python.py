"""
### Venv Documentation
"""

from __future__ import annotations

import textwrap
from datetime import datetime, timedelta

from airflow.providers.standard.operators.python import PythonVirtualenvOperator, PythonOperator

from airflow.sdk import DAG

def callable_virtualenv():
    """
    Example function that will be performed in a virtual environment.

    Importing at the function level ensures that it will not attempt to import the
    library before it is installed.
    """
    from time import sleep
    import colorama
    from colorama import Back, Fore, Style
    import pandas as pd

    print(Fore.RED + "some red text")
    print(Back.GREEN + "and with a green background")
    print(Style.DIM + "and in dim text")
    print(Style.RESET_ALL)
    for _ in range(4):
        print(Style.DIM + "Please wait...", flush=True)
        sleep(1)
    print(colorama.__version__)
    print(pd.__version__)
    print("Finished")

with DAG(
    "venv_python",
    default_args={
        "depends_on_past": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
    description="A simple tutorial DAG",
    schedule=None,
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["example"],
) as dag:

    virtualenv_task = PythonVirtualenvOperator(
        task_id="virtualenv_python",
        python_callable=callable_virtualenv,
        requirements=[
            "colorama==0.4.0",
            "pandas==2.2.3"
        ],
        system_site_packages=False,
    )

    python_task = PythonOperator(
        task_id="python",
        python_callable=callable_virtualenv
    )