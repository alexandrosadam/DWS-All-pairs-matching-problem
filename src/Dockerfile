FROM bitnami/spark:3.5.5

USER root
RUN install_packages python3 python3-pip
COPY requirements.txt .
RUN pip3 install -r requirements.txt

WORKDIR /app
COPY . /app

CMD ["spark-submit", "--master", "spark://spark-master:7077", "main.py"]


