release: python manage.py migrate --run-syncdb --noinput
web: gunicorn nowmad.wsgi --log-file -
