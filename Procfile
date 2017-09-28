web: gunicorn -b :8000 --workers=3 vidtrest.wsgi:application --reload
worker: python manage.py rqworker high default low
