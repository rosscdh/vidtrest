FROM python:3

WORKDIR /

ADD ./vidtrest /vidtrest
ADD ./config /config
ADD ./manage.py /manage.py
ADD ./requirements.txt /
ADD ./Procfile /

RUN apt-get update
RUN apt-get install -y nodejs npm
RUN npm i uglify -g
RUN pip install -r /requirements.txt


CMD ["honcho", "start"]