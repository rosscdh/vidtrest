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
pip install -r requirements.txt
./manage.py migrate
./manage.py createsuperuser
```