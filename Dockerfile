FROM alpine

WORKDIR /usr/local/app

COPY dist/cajovyobchudek-*.tar.gz ./app.tar.gz
RUN tar -xf app.tar.gz --strip-components=1 -C .
RUN rm app.tar.gz

COPY requirements.txt requirements.txt
COPY gunicorn.py gunicorn.py

RUN \
  apk add --update py-pip jpeg-dev libwebp-dev zlib-dev libjpeg openrc busybox-initscripts && \
  apk add --no-cache postgresql-libs && \
  apk add --no-cache --virtual .build-deps g++ gcc python3-dev musl-dev postgresql-dev && \
  pip install -r requirements.txt --no-cache-dir && \
  apk --purge del .build-deps

EXPOSE 80

CMD gunicorn -c gunicorn.py cajovyobchudek.wsgi
