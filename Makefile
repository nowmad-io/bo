PYTHON = ./venv/bin/python
PIP = ./venv/bin/pip

init:
	rm -rf venv
	find . -name '*.pyc' -delete
	@echo Creating venv with python `which python`
	virtualenv -p `which python` venv --verbose


export_fixtures:
	$(PYTHON) manage.py dumpdata --indent 2 authentication.travelUser > fixtures/users.json
	$(PYTHON) manage.py dumpdata --indent 2 friends.Friend > fixtures/friends.json
	$(PYTHON) manage.py dumpdata --indent 2 core.Location > fixtures/locations.json
	$(PYTHON) manage.py dumpdata --indent 2 core.Review > fixtures/reviews.json

start_me_up:
	find . -name '*.pyc' -delete
	rm -vf travelNetwork/db.sqlite3
	$(PIP) install -r requirements.txt -U
	$(PYTHON) manage.py makemigrations corsheaders
	$(PYTHON) manage.py makemigrations
	$(PYTHON) manage.py migrate --run-syncdb --noinput

	$(PYTHON) manage.py loaddata fixtures/locations.json
	$(PYTHON) manage.py loaddata fixtures/users.json
	$(PYTHON) manage.py loaddata fixtures/friends.json
	$(PYTHON) manage.py loaddata fixtures/reviews.json

server:
	$(PYTHON) manage.py runserver
