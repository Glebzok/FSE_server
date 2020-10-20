FROM ubuntu:20.04

RUN apt update
RUN apt install -y git python3 python3-pip

RUN git clone --single-branch --branch master https://github.com/Glebzok/FSE_server.git

WORKDIR /FSE_server

RUN pip3 install -r Requirements



