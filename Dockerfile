FROM rasa/rasa:latest

COPY app /app
COPY server.sh /app/server.sh

USER root
RUN chmod -R 777 /app
USER 1001

chmod -R 777 /opt/venv/lib/python3.8/site-packages
RUN pip3 install underthesea
RUN rasa train nlu

ENTRYPOINT ["/app/server.sh"]
