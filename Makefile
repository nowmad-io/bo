start_me_up:
	rm -vf db.sqlite3
	pip install -r requirements.txt -U
	python manage.py migrate --run-syncdb --noinput

	python manage.py loaddata fixtures/locations.json
	python manage.py loaddata fixtures/users.json
	python manage.py loaddata fixtures/reviews.json

start_server:
	python manage.py runserver
