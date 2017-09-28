FROM python:3

WORKDIR /

ADD ./vidtrest /vidtrest
ADD ./config /config
ADD ./manage.py /manage.py
ADD ./requirements.txt /
ADD ./Procfile /

RUN pip install -r /requirements.txt

#RUN python manage.py migrate
#RUN python manage.py create_superuser
#RUN python manage.py collectstatic --no-input
#RUN python manage.py loaddata

CMD ["honcho", "start"]