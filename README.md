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
