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
docker-compose run web bash /config/startup.sh
docker-compose up
```

## Install media server

* requires docker

```
docker-compose up
docker-compose run web sh /config/startup.sh
```

### Resetting

```
docker-compose stop
docker-compose rm
make db.clear
make reset
```

### Crons

```
5 8 * * Sun /usr/local/bin/docker-compose run worker python manage.py dumpdata > /var/services/homes/rosscdh/backup-data/vidtrest.json > /dev/null 2>&1
```

### Cloud backup

```
/var/services/homes/rosscdh/backup-data/vidtrest.json
/var/services/homes/rosscdh/vidtrest/media
```


### Tasks

```
# reprocess a video by its id
python /var/services/homes/rosscdh/vidtrest/manage.py process_video :video_id
```