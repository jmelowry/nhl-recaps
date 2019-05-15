FROM python:3.7-alpine3.8

#update apk repo
RUN echo "http://dl-4.alpinelinux.org/alpine/v3.8/main" >> /etc/apk/repositories && \
    echo "http://dl-4.alpinelinux.org/alpine/v3.8/community" >> /etc/apk/repositories

# install chromedriver
RUN apk update
RUN apk add --update chromium chromium-chromedriver python-dev py-pip build-base

# install selenium
RUN pip install selenium

RUN mkdir -p /nhl_recaps
ADD . /nhl_recaps
WORKDIR /nhl_recaps
RUN python setup.py install
