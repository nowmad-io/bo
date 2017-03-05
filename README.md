# TravelNetwork

## Start developping:
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

## Setting up fixtures

```
> make export_fixtures
```
Once you created a test database with a set of objects, you can export it as fixtures so it can be loaded during the next ```make start_me_up```.


## End point url

* ```GET api/friends/``` = return the list of the logged user friends (as user objects)
* ```GET api/friendships/``` = get the list of friendship request
* ```POST api/friendships/``` = create a friendship request
* TODO: ```GET api/friendships/(?P<pk>[0-9]+)/``` = information about a friendship request
* ```DEL api/friendships/(?P<pk>[0-9]+)/``` = cancel a friendship request
* TODO: ```PUT api/friendships/(?P<pk>[0-9]+)/``` = update a friendship request. Usefull if we want to change the text of the request or when we decide to switch off notification system.
`IMPORTANT` : work on the notification system. Need to add a notification_enabled in json.

* ```GET api/friendships/incoming/``` = return the list of request pending to this user
* ```GET api/friendships/outgoing/``` = return the list of request pending form this user



* ```GET api/friendships/accept/(?P<pk>[0-9]+)/``` = accept the friendship request
* ```GET api/friendships/reject/(?P<pk>[0-9]+)/``` = accept the friendship request
* TODO/USEFULL ?: ```GET api/friendships/accepts/``` = lsit of accepted friendship request
* TODO/USEFULL ?:```GET api/friendships/rejects/``` = list of rejected friendship request


## Miscellaneous

Error Dynos
```
> heroku ps --app travelnetwork
> heroku ps:stop run.6004 --app travelnetwork
> heroku login
> heroku run bash --app travelnetwork
```
