FROM python:3

ENV PYTHONUNBUFFERED 1
ENV POSTGRES_PASSWORD=password

RUN mkdir /vidtrest
WORKDIR /vidtrest

RUN pip install -r /vidtrest/requirements.txt
CMD gunicorn -b :8000 --workers=3 vidtrest.wsgi:application --reload