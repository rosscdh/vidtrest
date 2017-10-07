FROM python:3.6.2-stretch

WORKDIR /

RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -
RUN npm -g install bower gulp
RUN apt-get update
RUN apt-get install -y exiftool ffmpeg
RUN pip install -r /requirements.txt

#CMD ["honcho", "start"]