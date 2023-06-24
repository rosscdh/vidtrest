#!/bin/bash

python manage.py bower_install --allow-root
python manage.py migrate
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'password123')"
python manage.py collectstatic --no-input
#python manage.py loaddata
