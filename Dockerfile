FROM python:3.6.2-stretch

WORKDIR /

ADD ./vidtrest /vidtrest
ADD ./config /config
ADD ./manage.py /manage.py
ADD ./requirements.txt /
ADD ./Procfile /

RUN apt-get update
RUN apt-get install -y exiftool ffmpeg
RUN pip install -r /requirements.txt

#CMD ["honcho", "start"]