FROM python:3.6.2-stretch

WORKDIR /

ADD requirements.txt /
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -
RUN apt-get update
RUN apt-get install -y exiftool ffmpeg nodejs
RUN npm install -g bower gulp yuglify
RUN pip install -r /requirements.txt

#CMD ["honcho", "start"]