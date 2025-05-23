FROM bitnami/spark:3.5.5

USER root
RUN install_packages python3 python3-pip
COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY main.py /opt/bitnami/spark/main.py
WORKDIR /opt/bitnami/spark


