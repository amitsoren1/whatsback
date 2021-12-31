release: python manage.py collectstatic --no-input

web: gunicorn -b 0.0.0.0:$PORT -k eventlet -w 1 chatback.wsgi:application
