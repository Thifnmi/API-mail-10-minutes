FROM python:3.8

EXPOSE 80

RUN mkdir -p /src
WORKDIR /src

RUN apt-get update

COPY requirements.txt /src

RUN pip install -r requirements.txt


COPY . /src


CMD flask run -h 0.0.0.0 -p 80
#&& python worker.py --mode=kafka