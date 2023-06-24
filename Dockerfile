FROM python:3-slim as build
RUN pip install virtualenv
RUN virtualenv /venv -p python3
ADD ./src/requirements.txt /
RUN /venv/bin/pip install -r /requirements.txt

FROM python:3-slim
RUN apt-get update;apt-get install -y exiftool ffmpeg && rm -rf /var/lib/apt/lists/*
EXPOSE 8000
WORKDIR /src
COPY --from=build /venv /venv
COPY ./src /src
RUN adduser --system --no-create-home django
USER django
ENTRYPOINT ["/venv/bin/uvicorn"]
CMD ["vidtrest.asgi:application", "--host", "0.0.0.0", "--reload"]