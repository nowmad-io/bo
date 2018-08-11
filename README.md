# Nowmad Backend
> Python/Django backend of nowmad.io

This server set up the REST API for the React Native app [Nowmad](https://github.com/nowmad-io/hybridapp). It offers Authentication, Friendship relations, and handles the CRUD actions for Reviews and Places objects.

## Installation

* Set up the virtual env:
  ```
  > make init
  ```
  This will set up a virtual env in the venv directory.

  In case you need to use ```pip``` or ```python``` command, use the executable of the virtual env.

  E.g:
  ```
  > ./venv/bin/python manage.py makemigrations
  ```
* Install dependicies and init data base:
  ```
  > make start_me_up
  ```
* Start dev server:
  ```
  > make server
  ```

## Miscellaneous

Setting up fixtures
```
> make export_fixtures
```
Once you created a test database with a set of objects, you can export it as fixtures so it can be loaded during the next ```make start_me_up```.

Login
```
$ heroku login
```

First launch
* Create new app in heroku
* Set up django en var SECRET_KEY from heroku dahsboard or using `heroku config:set SECRET_KEY=secret --app api-nowmad`
* Deploy connecting to github repo
* Check if migrations has been ran
* create super user `heroku run python manage.py createsuperuser --app api-nowmad`
* Set up custom domains if necessary [gandi-net-and-heroku-domain-routing](https://stackoverflow.com/questions/22854091/gandi-net-and-heroku-domain-routing)

```
$ heroku run bash --app api-nowmad
```

Clean Dynos
```
$ heroku ps --app api-nowmad
$ heroku ps:stop run.6004 --app api-nowmad
```

Run command
```
$ heroku run command
```
eg:
```
$ heroku run python manage.py migrate --app api-nowmad
```

Open bash
```
$ heroku run bash --app api-nowmad
```

Reset database
```
$ heroku pg:reset DATABASE --app api-nowmad
```

Create superuser
```
$ heroku run python manage.py createsuperuser --app api-nowmad
```

Set up SSL
* https://vimeo.com/209534466

## Meta

Julien Rougeron – [Portfolio](https://julienr2.github.io) – julien.rougeron@gmail.com

Distributed under the MIT license. See ``LICENSE`` for more information.

[https://github.com/julienr2/](https://github.com/dbader/)
