# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster

ARG GARMINEMAIL
ARG GARMINPASSWORD

ENV GARMINEMAIL=$GARMINEMAIL
ENV GARMINPASSWORD=$GARMINPASSWORD

# RUN echo "Value is ${GARMINEMAIL}"

RUN mkdir app && chown -R 33:33 /app 

WORKDIR /app 

RUN mkdir logs && chown -R 33:33 logs

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .
CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0", "--debug"]