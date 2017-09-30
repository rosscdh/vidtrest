Vidtrest
--------

Videos by keyword

* save videos
* retrieve metadata
* searchable by tags
* template tags provided
* upload to s3 and parse metadata async


## Server required installs

* __exiftool__ : sudo apt-get install exiftool / brew install exiftool
* __ffmpeg__ : sudo apt-get install ffmpeg / brew install ffmpeg


## Installation

```
docker-compose up db  # create db stuff
docker-compose run vidtrest sh /config/startup.sh
docker-compose up
```

## Install media server

* requires docker

```
docker-compose up
docker-compose run vidtrest sh /config/startup.sh
```

### Resetting

```
docker-compose stop
docker-compose rm
make db.clear
make reset
```