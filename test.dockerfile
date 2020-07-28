FROM debian:buster

COPY backend /srv/app

RUN apt-get update && apt-get install -y python3 python3-pip python3-venv

RUN rm -rf /var/lib/apt/lists/*

RUN rm -rf /srv/app/venv

RUN cd /srv/app \
&& python3 -m venv venv \
&& . venv/bin/activate \
&& pip3 install wheel \
&& pip3 install -r requirements.txt \
&& python3 db.py

RUN mkdir /srv/library

EXPOSE 80

WORKDIR /srv/app

CMD [ "bash", "/srv/app/start.sh" ]

