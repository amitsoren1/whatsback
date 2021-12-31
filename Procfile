release: python manage.py makemigrations chats users
release: python manage.py migrate
release: python manage.py collectstatic --no-input

web: gunicorn -b 0.0.0.0:$PORT -k eventlet -w 1 chatback.wsgi:application
