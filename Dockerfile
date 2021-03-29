FROM rasa/rasa:latest

COPY app /app
COPY server.sh /app/server.sh

USER root
RUN chmod -R 777 /app
USER 1001

RUN pip install --upgrade pip
RUN useradd -m docker && echo "docker:docker" | chpasswd && adduser docker sudo
USER docker

RUN pip install underthesea --user
RUN rasa train nlu

ENTRYPOINT ["/app/server.sh"]
