FROM debian:buster

COPY backend /srv/app

RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-pip python3-venv

RUN apt-get install -y nginx

RUN rm -rf /var/lib/apt/lists/*

COPY nginx/ /etc/nginx/sites-available/

RUN rm /etc/nginx/sites-enabled/default

RUN ln -s /etc/nginx/sites-available/fari /etc/nginx/sites-enabled

RUN nginx -t

RUN rm -rf /srv/app/venv

RUN rm /srv/app/app/db.sqlite

RUN cd /srv/app \
&& python3 -m venv venv \
&& . venv/bin/activate \
&& pip3 install wheel \
&& pip3 install -r requirements.txt \
&& python3 db.py

RUN mkdir /srv/library

EXPOSE 80

WORKDIR /srv/app

CMD [ "bash", "-c", "service nginx start && . venv/bin/activate && ./venv/bin/gunicorn --workers 4 --timeout 600 --access-logfile access.log --error-logfile error.log --bind unix:/srv/fari.sock wsgi:app" ]

