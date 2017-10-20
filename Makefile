ifdef SYSTEMROOT
	PYTHON = DEBUG=True ./venv/Scripts/python
	PIP = ./venv/Scripts/pip
else
	PYTHON = DEBUG=True ./venv/bin/python
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

migrate:
	$(PYTHON) manage.py migrate --run-syncdb --noinput

makemigrations:
	$(PYTHON) manage.py makemigrations

loaddata:
	$(PYTHON) manage.py loaddata fixtures/$(MODEL).json

start_me_up:
	find . -name '*.pyc' -delete
	rm -vf nowmad/db.sqlite3
	$(PIP) install -r requirements.txt -U
	$(PYTHON) manage.py makemigrations
	$(PYTHON) manage.py migrate --run-syncdb --noinput

	make loaddata MODEL="places"
	make loaddata MODEL="users"
	make loaddata MODEL="friends"
	make loaddata MODEL="categories"
	make loaddata MODEL="reviews"

server:
	DEFAULT_PORT=8080 $(PYTHON) manage.py runserver

build_client:
	cd ../webapp/ && git fetch && git checkout master
	cd ../webapp && latesttag=$(git describe --tags)
	echo checking out ${latesttag}
	cd ../webapp/ && git checkout ${latesttag}
	cd ../webapp/ && npm run build:clean && npm run build && npm run build:copy

test:
	echo  $(PYTHON)
