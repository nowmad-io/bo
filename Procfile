release: python manage.py migrate --run-syncdb --noinput && python manage.py loaddata fixtures/categories.json
web: gunicorn nowmad.wsgi --log-file -
