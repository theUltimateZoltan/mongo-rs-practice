FROM python:latest

WORKDIR /home/app/

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src .

ENTRYPOINT /bin/bash
