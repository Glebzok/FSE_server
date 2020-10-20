FROM ubuntu:20.04

RUN apt update
RUN apt install -y git python3 python3-pip

RUN git clone --single-branch --branch master https://github.com/Glebzok/FSE_server.git

WORKDIR /FSE_server

RUN pip3 install -r Requirements

ARG CACHE_DATE=2016-01-01

RUN rm -rf *
RUN rm -rf .git

RUN git clone --single-branch --branch master https://github.com/Glebzok/FSE_server.git .

EXPOSE 5000

RUN python3 ./download_nltk_data.py
#RUN python3 ./add_articles.py -r -y 2 -a 2
#RUN gunicorn --bind 0.0.0.0:5000 wsgi:app

