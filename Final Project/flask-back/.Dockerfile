FROM python:3.7.2

WORKDIR /opt/app

RUN apt-get update -y
RUN apt-get -y install build-essential cmake

COPY requirements.txt .
RUN pip install git+https://www.github.com/keras-team/keras-contrib.git
RUN pip install -r requirements.txt

COPY ./ .
CMD python3 flask_app.py