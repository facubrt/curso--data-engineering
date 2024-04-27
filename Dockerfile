FROM apache/airflow:2.8.4

COPY requirements.txt .

RUN pip install -r requirements.txt

ENV PATH="/opt/airflow/src:/opt/airflow/dags:${PATH}"
ENV PYTHONPATH="/opt/airflow/src:/opt/airflow/dags:${PYTHONPATH}"

ENTRYPOINT ["/usr/bin/dumb-init", "--", "/entrypoint"]

CMD []