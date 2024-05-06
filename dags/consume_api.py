from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import requests
import csv


def fetch_data():
    api_url = "http://10.43.101.149/data?group_number=5"
    csv_file = "data/covertype.csv"

    response = requests.get(api_url)
    data = response.json()["data"]

    with open(csv_file, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for row in data:
            writer.writerow(row)


with DAG(
    "api_to_csv",
    description="Fetch data from the covertype API and save in file",
    start_date=datetime(2024, 4, 7),
    end_date=datetime(2024, 4, 7, 1),
    schedule_interval=timedelta(minutes=1),
):
    get_data_task = PythonOperator(task_id="fetch_data", python_callable=fetch_data)

    get_data_task
