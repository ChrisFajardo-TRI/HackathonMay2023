FROM python:3.10-slim-buster

RUN apt update
RUN apt install make
RUN python3 -m pip install -U pip

WORKDIR /workspace
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt
