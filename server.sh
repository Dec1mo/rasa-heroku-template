#!/bin/sh

if [ -z "$PORT"]
then
  PORT=5005
fi

# rasa run --enable-api --port $PORT
rasa run --endpoints ./app/endpoints.yml --credentials ./app/credentials.yml --enable-api --port $PORT
