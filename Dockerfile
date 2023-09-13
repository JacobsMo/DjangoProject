FROM python:3.9

RUN mkdir /sources/
COPY . /sources/
WORKDIR /sources/
RUN cd /sources/

RUN pip3 install -r requirements.txt
