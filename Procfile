release: python manage.py migrate

web: gunicorn -b 0.0.0.0:$PORT -k eventlet -w 1 chatback.wsgi:application
