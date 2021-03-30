FROM rasa/rasa:latest
USER root

COPY app /app
COPY server.sh /app/server.sh

USER root
RUN chmod -R 777 /app
# USER 1001

RUN pip install --upgrade pip
RUN pip install underthesea

RUN rasa train nlu

ENTRYPOINT ["/app/server.sh"]
