FROM python:3.7.0-stretch

RUN apt-get update && \
    apt-get install -y apache2-utils && \
    rm -rf /var/lib/apt/lists/*

ADD requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt && rm /tmp/requirements.txt

WORKDIR "/usr/src/app"
COPY . .
RUN pip install -e ./
ENTRYPOINT ["entrypoint"]

MAINTAINER Colin Chartier <colin@kubenow.com>