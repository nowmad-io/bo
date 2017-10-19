ifdef SYSTEMROOT
	PYTHON = ./venv/Scripts/python
	PIP = ./venv/Scripts/pip
else
	PYTHON = ./venv/bin/python
	PIP = ./venv/bin/pip
endif

init:
	rm -rf venv
	find . -name '*.pyc' -delete
	@echo Creating venv with python `which python`
	virtualenv venv --verbose

fixtures_users:
	$(PYTHON) manage.py dumpdata authentication.traveluser --indent 2 > fixtures/users.json

fixtures_friends:
	$(PYTHON) manage.py dumpdata friends.friend --indent 2 > fixtures/friends.json

fixtures_places:
	$(PYTHON) manage.py dumpdata core.place --indent 2 > fixtures/places.json

fixtures_reviews:
	$(PYTHON) manage.py dumpdata core.review --indent 2 > fixtures/reviews.json

fixtures_categories:
	$(PYTHON) manage.py dumpdata core.category --indent 2 > fixtures/categories.json

start_me_up:
	find . -name '*.pyc' -delete
	rm -vf nowmad/db.sqlite3
	$(PIP) install -r requirements.txt -U
	$(PYTHON) manage.py makemigrations
	$(PYTHON) manage.py migrate --run-syncdb --noinput

	$(PYTHON) manage.py loaddata fixtures/places.json
	$(PYTHON) manage.py loaddata fixtures/users.json
	$(PYTHON) manage.py loaddata fixtures/friends.json
	$(PYTHON) manage.py loaddata fixtures/categories.json
	$(PYTHON) manage.py loaddata fixtures/reviews.json

server:
	DEBUG=True DEFAULT_PORT=8080 $(PYTHON) manage.py runserver

build_client:
	cd ../webapp/ && git fetch && git checkout master
	cd ../webapp && latesttag=$(git describe --tags)
	echo checking out ${latesttag}
	cd ../webapp/ && git checkout ${latesttag}
	cd ../webapp/ && npm run build:clean && npm run build && npm run build:copy

test:
	echo  $(PYTHON)
